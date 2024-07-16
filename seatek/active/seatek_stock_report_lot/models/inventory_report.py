# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import pytz

from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp
from odoo.addons.mail.models.mail_template import format_tz
from odoo.fields import Datetime


class InventoryReportLot(models.Model):
    _name = 'seatek.inventory.report.lot'
    _description = 'Báo cáo xuất nhập tồn theo lô'

    name = fields.Char('Tên', default='Báo cáo xuất nhập tồn theo lô')

    date_from = fields.Datetime('Từ ngày', default=fields.Datetime.today())
    date_to = fields.Datetime('Đến ngày', default=fields.Datetime.today())
    type_get_value = fields.Selection([
        ('product', 'Giá trên sản phẩm'),
        ('stock', 'Quy trình kho'),
        ('account', 'Bút toán')], 'Lấy giá trị theo', default='product')
    value = fields.Float('Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)

    @api.model
    def get_location_default(self):
        return self.env['stock.location'].search([('id', '=', 21)]).ids

    @api.model
    def get_product_default(self):
        return self.env['product.product'].search([('id', '=', 25)]).ids

    location_ids = fields.Many2many('stock.location',
                                    'seatek_inventory_report_lot_location_rel',
                                    'report_id',
                                    'location_id',
                                    'Địa điểm kho',
                                    domain=[('usage', 'in', ('internal', 'transit'))],
                                    default=get_location_default)

    location_id = fields.Many2one('stock.location', "Địa điểm kho", domain=[('usage', 'in', ('internal', 'transit'))])

    categ_ids = fields.Many2many('product.category', 'vio_inventory_report_lot_pc_rel', 'report_id', 'categ_id',
                                 'Nhóm sản phẩm', required=True)
    product_ids = fields.Many2many('product.product', 'vio_inventory_report_lot_product_rel', 'report_id', 'product',
                                   'Sản phẩm')

    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    display_product = fields.Boolean("Ẩn sản phẩm bằng 0", default=False)
    inventory_report_line_ids = fields.One2many('seatek.inventory.report.lot.line', 'inventory_report_id', 'Chi tiết')
    inventory_report_line_ids_hide_display_product = fields.One2many('seatek.inventory.report.lot.line',
                                                                     'inventory_report_id', 'Chi tiết',
                                                                     domain=['|', '|', '|',
                                                                             ('stock_out', '!=', 0),
                                                                             ('stock_opening', '!=', 0),
                                                                             ('stock_closing', '!=', 0),
                                                                             ('stock_in', '!=', 0)])

    # đệ quy tìm child của category
    def _get_category(self, categories, list_category):
        for cate in categories:
            child = cate.child_id
            if not child:
                if cate.id not in list_category:
                    list_category.append(cate.id)
            else:
                for i in child.ids:
                    if i not in list_category:
                        list_category.append(i)
                self._get_category(child, list_category)

    @api.onchange('categ_ids')
    def _categ_onchange(self):
        res = {}
        list_categ_ids = []
        categories = self.categ_ids
        list_categ_ids += categories.ids
        if len(categories) > 0:
            self._get_category(categories, list_categ_ids)
            res['domain'] = {'product_ids': [('categ_id', 'in', list_categ_ids)]}
        else:
            res['domain'] = {'product_ids': [('categ_id', 'in', [])]}
        return res

    @api.model
    def action_open_report(self):
        action_values = self.env.ref('seatek_stock_report_lot.action_inventory_report_lot_view').read()[0]
        res_id = self.env['seatek.inventory.report.lot'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not res_id:
            res_id = self.env['seatek.inventory.report.lot'].create({'user_id': self.env.user.id})
        res_id.write({'date_from': datetime.datetime.now(), 'date_to': datetime.datetime.now()})
        res_id.action_remove_data_inventory_report_line()
        action_values.update({'res_id': res_id.id})
        action = action_values
        return action

    def action_remove_data_inventory_report_line(self):
        return self.inventory_report_line_ids.unlink()

    def action_get_data_inventory_report_line(self):
        self.inventory_report_line_ids.unlink()

        LineObj = self.env['seatek.inventory.report.lot.line']
        #Lọc sản phẩm product.product theo company_id
        productTemplateId = self.env['product.template'].search([
            ('company_id', '=', self.env.user.company_id.id)
        ]).mapped('id')
        ProductObj = self.env['product.product'].search([
            ('product_tmpl_id', 'in', productTemplateId)
        ])
        # ProductObj = self.env['product.product']

        domain_product = []
        list_category = []
        # Tìm danh sách child của các catogory
        self._get_category(self.categ_ids, list_category)
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', list_category))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        #chỉ lấy sản phẩm loại product (xóa loại consu)
        products = ProductObj.search([('type', '=', ('product'))] + domain_product)

        # """đầu kỳ và tồn của tất cả các loại sản phẩm consu bằng 0"""
        # products_consu = ProductObj.search([('type', '=', 'consu')])

        location = self.location_id.id
        # if not location_id:
        #     location_ids = self.env['stock.location'].search([('usage', 'in', ('internal', 'transit'))]).ids

        domain_date = []

        if self.date_to:
            dt_to = Datetime.context_timestamp(self, self.date_to).replace(minute=59, hour=23, second=59)
            dt_to = dt_to.astimezone(pytz.utc)
            self.date_to = dt_to.replace(tzinfo=None)
            domain_date.append(('date', '<=', dt_to))
        if self.date_from:
            dt_from = Datetime.context_timestamp(self, self.date_from).replace(hour=0, minute=0, second=0)
            self.date_from = dt_from.replace(tzinfo=None)
            domain_date.append(('date', '>=', dt_from))

        def write_data(code_product, product, location, name_lot, qty_opening, value_stock_opening, nhap_trong_ki,
                       value_stock_in,
                       xuat_trong_ki, value_stock_out, qty_closing, value_stock_closing):
            line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id),
                                   ('location_id', '=', location), ('name_lot', '=', name_lot)], limit=1)
            if not line:
                LineObj.create({
                    'inventory_report_id': self.id,
                    'default_code': code_product,
                    'accounting_code': product.product_tmpl_id.accounting_code,
                    'product_id': product.id,
                    'name_lot': name_lot,
                    'uom_id': product.uom_id.id,
                    'stock_opening': qty_opening,
                    'stock_in': nhap_trong_ki,
                    'stock_out': xuat_trong_ki,
                    'value_stock_in': value_stock_in,
                    'value_stock_out': value_stock_out,
                    'stock_closing': qty_closing,
                    'location_id': location,
                    'value_stock_opening': value_stock_opening,
                    'value_stock_closing': value_stock_closing
                })
            else:
                line.write({
                    'name_lot': name_lot,
                    'default_code': code_product,
                    'accounting_code': product.product_tmpl_id.accounting_code,
                    'stock_in': nhap_trong_ki,
                    'stock_out': xuat_trong_ki,
                    'value_stock_in': value_stock_in,
                    'value_stock_out': value_stock_out,
                    'stock_opening': qty_opening,
                    'stock_closing': qty_closing,
                })

        value = 0

        # # Code cũ
        # # for location in location_ids:
        # for product in products:
        #     sml = self.env['stock.move.line'].sudo().search(
        #         [('state', '=', 'done'), ('product_id', '=', product.id), '|', ('location_id', '=', location),
        #          ('location_dest_id', '=', location)])
        #
        #     # có lot_id
        #     sml_lot_ids = [i.lot_id.id for i in sml if i.lot_id]
        #     lot_id_group_by_name = self.env['stock.production.lot'].read_group([('id', 'in', sml_lot_ids)],
        #                                                                        fields=['lot_id', 'name'],
        #                                                                        groupby=['name'])
        #     # tính có lot_id
        #     for i in lot_id_group_by_name:
        #         spl_with_name = self.env['stock.production.lot'].sudo().search([
        #             ('product_id', '=', product.id), ('name', '=', i['name'])], limit=1)
        #
        #         #   lot id của từng lô
        #         #   spl_with_name.id -> là id của lô
        #         #   tính cuối kì theo lot_id
        #         search_sml = self.env['stock.move.line'].sudo().search(
        #             [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
        #              ('lot_id', '=', spl_with_name.id), '|', ('location_id', '=', location),
        #              ('location_dest_id', '=', location)])
        #         nhap = 0
        #         xuat = 0
        #         for search in search_sml:
        #             if search.location_id.id == location:
        #                 xuat += search.qty_done
        #             if search.location_dest_id.id == location:
        #                 nhap += search.qty_done
        #         qty_closing = nhap - xuat
        #
        #         #   tính nhập xuất trong kì
        #         search_sml_in_period = self.env['stock.move.line'].sudo().search(
        #             [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
        #              ('date', '>=', str(dt_from)), ('lot_id', '=', spl_with_name.id), '|',
        #              ('location_id', '=', location), ('location_dest_id', '=', location)])
        #         nhap_trong_ki = 0
        #         xuat_trong_ki = 0
        #         for search in search_sml_in_period:
        #             if search.location_id.id == location:
        #                 xuat_trong_ki += search.qty_done
        #             if search.location_dest_id.id == location:
        #                 nhap_trong_ki += search.qty_done
        #
        #         #   tính đầu kì
        #         qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
        #         value_stock_opening = product.standard_price * qty_opening
        #         value_stock_closing = product.standard_price * qty_closing
        #         value_stock_in = product.standard_price * nhap_trong_ki
        #         value_stock_out = product.standard_price * xuat_trong_ki
        #
        #         write_data(product.product_tmpl_id.default_code, product, location, i['name'], qty_opening,
        #                    value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out,
        #                    qty_closing, value_stock_closing)
        #         value += value_stock_closing
        #
        #     #   tính cuối kì không có lot_id ('lot_id', '=', None)
        #     search_sml = self.env['stock.move.line'].sudo().search(
        #         [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
        #          ('lot_id', '=', None), '|', ('location_id', '=', location),
        #          ('location_dest_id', '=', location)])
        #
        #     if not search_sml:
        #         # những sản phẩm không có lô sẽ tiếp tục tính sang sản phẩm khác
        #         continue
        #     nhap = 0
        #     xuat = 0
        #     for search in search_sml:
        #         if search.location_id.id == location:
        #             xuat += search.qty_done
        #         if search.location_dest_id.id == location:
        #             nhap += search.qty_done
        #     qty_closing = nhap - xuat
        #
        #     #   tính nhập xuất trong kì
        #     search_sml_in_period = self.env['stock.move.line'].sudo().search(
        #         [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
        #          ('date', '>=', str(dt_from)), ('lot_id', '=', None), '|',
        #          ('location_id', '=', location), ('location_dest_id', '=', location)])
        #     nhap_trong_ki = 0
        #     xuat_trong_ki = 0
        #     for search in search_sml_in_period:
        #         if search.location_id.id == location:
        #             xuat_trong_ki += search.qty_done
        #         if search.location_dest_id.id == location:
        #             nhap_trong_ki += search.qty_done
        #
        #     #   tính đầu kì
        #     qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
        #     value_stock_opening = product.standard_price * qty_opening
        #     value_stock_closing = product.standard_price * qty_closing
        #     value_stock_in = product.standard_price * nhap_trong_ki
        #     value_stock_out = product.standard_price * xuat_trong_ki
        #
        #     write_data(product.product_tmpl_id.default_code, product, location, "", qty_opening,
        #                value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out,
        #                qty_closing, value_stock_closing)
        #     value += value_stock_closing

        # Code mới
        # Tìm các product_id của các stock_move_line thỏa yêu cầu
        sml_product_ids = self.env['stock.move.line'].sudo().search(
            [('state', '=', 'done'), ('date', '<=', str(dt_to)),
             '|', ('location_id', '=', location), ('location_dest_id', '=', location)
             ]).mapped('product_id.id')

        for product in products:
            # F
            if product.id not in sml_product_ids:
                continue

            # Có lot_id
            # Tìm các lot_id của các sml thỏa đk và date <= date_to
            sml_lot_ids = self.env['stock.move.line'].sudo().search([
                ('state', '=', 'done'), ('product_id', '=', product.id), ('date', '<=', str(dt_to)),
                '|', ('location_id', '=', location), ('location_dest_id', '=', location)
            ]).mapped('lot_id')

            # Tính mỗi lô
            for sml_lot_id in sml_lot_ids:
                # Tìm sml thỏa đk và lot_id = sml_lot_id
                search_sml = self.env['stock.move.line'].sudo().search([
                    ('state', '=', 'done'), ('product_id', '=', product.id), ('date', '<=', str(dt_to)),
                    ('lot_id', '=', sml_lot_id.id),
                    '|', ('location_id', '=', location), ('location_dest_id', '=', location)
                ])

                nhap = 0
                xuat = 0
                for search in search_sml:
                    if search.location_id.id == location:
                        xuat += search.qty_done
                    if search.location_dest_id.id == location:
                        nhap += search.qty_done

                # Tính cuối kỳ
                qty_closing = nhap - xuat

                # Tìm sml trong kỳ
                search_sml_in_period = self.env['stock.move.line'].sudo().search([
                    ('state', '=', 'done'), ('product_id', '=', product.id), ('date', '<=', str(dt_to)),
                    ('date', '>=', str(dt_from)), ('lot_id', '=', sml_lot_id.id),
                    '|', ('location_id', '=', location), ('location_dest_id', '=', location)
                ])

                nhap_trong_ki = 0
                xuat_trong_ki = 0
                for search in search_sml_in_period:
                    if search.location_id.id == location:
                        xuat_trong_ki += search.qty_done
                    if search.location_dest_id.id == location:
                        nhap_trong_ki += search.qty_done

                # Tính đầu kỳ
                qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
                value_stock_opening = product.standard_price * qty_opening
                value_stock_closing = product.standard_price * qty_closing
                value_stock_in = product.standard_price * nhap_trong_ki
                value_stock_out = product.standard_price * xuat_trong_ki

                write_data(product.product_tmpl_id.default_code, product, location, sml_lot_id.name, qty_opening,
                        value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out,
                        qty_closing, value_stock_closing)
                value += value_stock_closing

            # Không có lot_id
            search_sml = self.env['stock.move.line'].sudo().search(
                [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
                 ('lot_id', '=', None),
                 '|', ('location_id', '=', location), ('location_dest_id', '=', location)])

            if not search_sml:
                # những sản phẩm không có lô sẽ tiếp tục tính sang sản phẩm khác
                continue

            nhap = 0
            xuat = 0
            for search in search_sml:
                if search.location_id.id == location:
                    xuat += search.qty_done
                if search.location_dest_id.id == location:
                    nhap += search.qty_done
            # Tính cuối kỳ
            qty_closing = nhap - xuat

            #   tính nhập xuất trong kì
            search_sml_in_period = self.env['stock.move.line'].sudo().search(
                [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
                 ('date', '>=', str(dt_from)), ('lot_id', '=', None), '|',
                 ('location_id', '=', location), ('location_dest_id', '=', location)])
            nhap_trong_ki = 0
            xuat_trong_ki = 0
            for search in search_sml_in_period:
                if search.location_id.id == location:
                    xuat_trong_ki += search.qty_done
                if search.location_dest_id.id == location:
                    nhap_trong_ki += search.qty_done

            #   tính đầu kỳ
            qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
            value_stock_opening = product.standard_price * qty_opening
            value_stock_closing = product.standard_price * qty_closing
            value_stock_in = product.standard_price * nhap_trong_ki
            value_stock_out = product.standard_price * xuat_trong_ki

            write_data(product.product_tmpl_id.default_code, product, location, "", qty_opening,
                       value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out,
                       qty_closing, value_stock_closing)
            value += value_stock_closing

        self.value = value

    def action_report_excel(self):
        return self.env.ref('seatek_stock_report_lot.inventory_report_lot_excel').report_action(self)


class InventoryReportLine(models.Model):
    _name = 'seatek.inventory.report.lot.line'
    _description = 'Chi tiết xuất nhập tồn tổng quát'
    _order = 'location_id, default_code, name_lot asc'

    default_code = fields.Char(string="Mã")
    accounting_code = fields.Char(string="Mã kế toán")
    name_lot = fields.Char(string="Lô")
    inventory_report_id = fields.Many2one('seatek.inventory.report.lot', 'Inventory report id', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_in = fields.Float('Nhập trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_out = fields.Float('Xuất trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))
    location_id = fields.Many2one('stock.location', 'Địa điểm kho',
                                  domain=[('usage', 'in', ('internal', 'transit'))])

    value_stock_opening = fields.Float('Giá trị kho đầu kì', digits=(16, 0))
    value_stock_in = fields.Float('Giá trị nhập', digits=(16, 0))
    value_stock_out = fields.Float('Giá trị xuất', digits=(16, 0))
    value_stock_closing = fields.Float('Giá trị kho cuối kì', digits=(16, 0))
