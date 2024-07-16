# -*- coding: utf-8 -*-
import datetime
import pytz
from odoo import fields, models, api
import odoo.addons.decimal_precision as dp
from odoo.fields import Datetime


class InventoryReportLot(models.Model):
    _name = 'seatek.inventory.report.lot.simple'
    _description = 'Báo cáo tồn kho tức thời'

    name = fields.Char('Tên', default='Báo cáo tồn kho tức thời')

    date = fields.Datetime('Ngày', default=fields.Datetime.today())
    type_get_value = fields.Selection([
        ('product', 'Giá trên sản phẩm'),
        ('stock', 'Quy trình kho'),
        ('account', 'Bút toán')], 'Lấy giá trị theo', default='product')
    value = fields.Float('Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)

    @api.model
    def get_location_default(self):
        return self.env['stock.location'].search([('id', '=', 288)])

    location_id = fields.Many2one('stock.location', "Địa điểm kho", domain=[('usage', 'in', ('internal', 'transit'))], default=get_location_default)

    @api.model
    def get_category_default(self):
        return self.env['product.category'].search([('id', 'in', [22, 21])])
    categ_ids = fields.Many2many('product.category', 'vio_inventory_report_lot_simple_pc_rel', 'report_id', 'categ_id',
                                 'Nhóm sản phẩm', required=True, default=get_category_default)

    # @api.onchange('categ_ids')
    # def _onchange_cate(self):
    #     print(self.categ_ids)

    product_ids = fields.Many2many('product.product', 'vio_inventory_report_lot_simple_product_rel', 'report_id', 'product',
                                   'Sản phẩm')

    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    display_product = fields.Boolean("Hiển thị lô sản phẩm lớn hơn 0", default=True)
    inventory_report_line_ids = fields.One2many('seatek.inventory.report.lot.line.simple', 'inventory_report_id', 'Chi tiết')
    inventory_report_line_ids_hide_display_product = fields.One2many('seatek.inventory.report.lot.line.simple',
                                                                     'inventory_report_id', 'Chi tiết',
                                                                     domain=[('stock_closing', '>', 0)])

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
        action_values = self.env.ref('seatek_stock_report_lot_simple.action_inventory_report_lot_simple_view').read()[0]
        res_id = self.env['seatek.inventory.report.lot.simple'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not res_id:
            res_id = self.env['seatek.inventory.report.lot.simple'].create({'user_id': self.env.user.id})
        res_id.write({'date': datetime.datetime.now()})
        res_id.action_remove_data_inventory_report_line()
        action_values.update({'res_id': res_id.id})
        action = action_values
        return action

    def action_remove_data_inventory_report_line(self):
        return self.inventory_report_line_ids.unlink()

    # def action_get_data_inventory_report_line(self):
    #     self.inventory_report_line_ids.unlink()
    #
    #     LineObj = self.env['seatek.inventory.report.lot.line.simple']
    #     ProductObj = self.env['product.product']
    #
    #     domain_product = []
    #     list_category = []
    #     # Tìm danh sách child của các catogory
    #     self._get_category(self.categ_ids, list_category)
    #     if self.categ_ids:
    #         domain_product.append(('categ_id', 'in', list_category))
    #     if self.product_ids:
    #         domain_product.append(('id', 'in', self.product_ids.ids))
    #     products = ProductObj.search([('type', 'in', ('product', 'consu'))] + domain_product)
    #
    #     # """đầu kỳ và tồn của tất cả các loại sản phẩm consu bằng 0"""
    #     products_consu = ProductObj.search([('type', '=', 'consu')])
    #
    #     location = self.location_id.id
    #     # if not location_id:
    #     #     location_ids = self.env['stock.location'].search([('usage', 'in', ('internal', 'transit'))]).ids
    #
    #     domain_date = []
    #     if self.date:
    #         dt_to = Datetime.context_timestamp(self, self.date).replace(minute=59, hour=23, second=59)
    #         dt_to = dt_to.astimezone(pytz.utc)
    #         self.date = dt_to.replace(tzinfo=None)
    #         domain_date.append(('date', '<=', dt_to))
    #
    #     def write_data(code_product, product, location, name_lot, qty_closing):
    #         line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id),
    #                                ('location_id', '=', location), ('name_lot', '=', name_lot)], limit=1)
    #
    #         if not line:
    #             LineObj.create({
    #                 'inventory_report_id': self.id,
    #                 'product_category': product.categ_id.id,
    #                 'default_code': code_product,
    #                 'product_id': product.id,
    #                 'name_lot': name_lot,
    #                 'uom_id': product.uom_id.id,
    #                 'location_id': location,
    #                 'stock_closing': qty_closing,
    #             })
    #         else:
    #             line.write({
    #                 'name_lot': name_lot,
    #                 'product_category': product.categ_id.id,
    #                 'default_code': code_product,
    #                 'location_id': location,
    #                 'stock_closing': qty_closing,
    #             })
    #
    #     value = 0
    #     # for location in location_ids:
    #     for product in products:
    #         sml = self.env['stock.move.line'].sudo().search(
    #             [('state', '=', 'done'), ('product_id', '=', product.id), '|', ('location_id', '=', location),
    #              ('location_dest_id', '=', location)])
    #
    #         # có lot_id
    #         sml_lot_ids = [i.lot_id.id for i in sml if i.lot_id]
    #         lot_id_group_by_name = self.env['stock.production.lot'].read_group([('id', 'in', sml_lot_ids)],
    #                                                                            fields=['lot_id', 'name'],
    #                                                                            groupby=['name'])
    #         # tính có lot_id
    #         for i in lot_id_group_by_name:
    #             spl_with_name = self.env['stock.production.lot'].sudo().search([
    #                 ('product_id', '=', product.id), ('name', '=', i['name'])], limit=1)
    #
    #             #   lot id của từng lô
    #             #   spl_with_name.id -> là id của lô
    #             #   tính cuối kì theo lot_id
    #             search_sml = self.env['stock.move.line'].sudo().search(
    #                 [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
    #                  ('lot_id', '=', spl_with_name.id), '|', ('location_id', '=', location),
    #                  ('location_dest_id', '=', location)])
    #             nhap = 0
    #             xuat = 0
    #             for search in search_sml:
    #                 if search.location_id.id == location:
    #                     xuat += search.qty_done
    #                 if search.location_dest_id.id == location:
    #                     nhap += search.qty_done
    #             qty_closing = nhap - xuat
    #
    #             write_data(product.product_tmpl_id.default_code, product, location, i['name'], qty_closing)
    #
    #         #   tính cuối kì không có lot_id ('lot_id', '=', None)
    #         search_sml = self.env['stock.move.line'].sudo().search(
    #             [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(dt_to)),
    #              ('lot_id', '=', None), '|', ('location_id', '=', location),
    #              ('location_dest_id', '=', location)])
    #
    #         if not search_sml:
    #             # những sản phẩm không có lô sẽ tiếp tục tính sang sản phẩm khác
    #             continue
    #         nhap = 0
    #         xuat = 0
    #         for search in search_sml:
    #             if search.location_id.id == location:
    #                 xuat += search.qty_done
    #             if search.location_dest_id.id == location:
    #                 nhap += search.qty_done
    #         qty_closing = nhap - xuat
    #
    #         write_data(product.product_tmpl_id.default_code, product, location, "", qty_closing)
    #
    #     self.value = value

    # cqminh 25.5.23
    def action_get_data_inventory_report_line(self):
        self.inventory_report_line_ids.unlink()
        lineObj = self.env['seatek.inventory.report.lot.line.simple']
        # productObj = self.env['product.product']
        # Lọc sản phẩm theo company
        productTemplateId = self.env['product.template'].search([
            ('company_id', '=', self.env.user.company_id.id)
        ]).mapped('id')
        productObj = self.env['product.product'].search([
            ('product_tmpl_id', 'in', productTemplateId)
        ])

        domain_product = []
        list_category = []
        # Tìm danh sách child của các catogory
        self._get_category(self.categ_ids, list_category)
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', list_category))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        # products = productObj.search([('type', 'in', ('product', 'consu'))] + domain_product)
        # Bỏ sản phẩm loại consu
        products = productObj.search([('type', '=', ('product'))] + domain_product)

        # # """đầu kỳ và tồn của tất cả các loại sản phẩm consu bằng 0"""
        # products_consu = productObj.search([('type', '=', 'consu')])

        location = self.location_id.id
        domain_date = []
        if self.date:
            dt_to = Datetime.context_timestamp(self, self.date).replace(hour=23, minute=59, second=59)
            dt_to = dt_to.astimezone(pytz.utc)
            self.date = dt_to.replace(tzinfo=None)

            domain_date.append(('in_date', '<=', dt_to))
            print(domain_date)
        search_stock_quant = self.env['stock.quant'].sudo().search([('location_id', '=', location), ('product_id', 'in', products.ids)] + domain_date)

        for sq in search_stock_quant:
            line = lineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', sq.product_id.id),
                                   ('location_id', '=', location), ('name_lot', '=', sq.lot_id.name)], limit=1)

            if not line:
                lineObj.create({
                    'inventory_report_id': self.id,
                    'product_category': sq.product_id.categ_id.id,
                    'default_code': sq.product_id.product_tmpl_id.default_code,
                    'accounting_code': sq.product_id.product_tmpl_id.accounting_code,
                    'product_id': sq.product_id.id,
                    'name_lot': sq.lot_id.name,
                    'uom_id': sq.product_id.uom_id.id,
                    'location_id': location,
                    'stock_closing': sq.quantity,
                })
            else:
                line.write({
                    'name_lot': sq.lot_id.name,
                    'product_category': sq.product_id.categ_id.id,
                    'default_code': sq.product_id.product_tmpl_id.default_code,
                    'location_id': location,
                    'stock_closing': sq.quantity,
                })

    def action_report_excel(self):
        return self.env.ref('seatek_stock_report_lot_simple.inventory_report_lot_simple_excel').report_action(self)


class InventoryReportLine(models.Model):
    _name = 'seatek.inventory.report.lot.line.simple'
    _description = 'Chi tiết xuất nhập tồn tổng quát'
    _order = 'product_category, default_code, name_lot asc'

    product_category = fields.Many2one("product.category", "Nhóm sản phẩm")
    default_code = fields.Char(string="Mã")
    accounting_code = fields.Char(string="Mã kế toán")
    name_lot = fields.Char(string="Lô")
    inventory_report_id = fields.Many2one('seatek.inventory.report.lot.simple', 'Inventory report id', ondelete='cascade')
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    stock_closing = fields.Float('Tồn kho', digits=dp.get_precision('Product Unit of Measure'))
    location_id = fields.Many2one('stock.location', 'Kho',
                                  domain=[('usage', 'in', ('internal', 'transit'))])
