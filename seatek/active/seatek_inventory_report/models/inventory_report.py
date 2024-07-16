import datetime
from datetime import timedelta

import pytz

from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp
from odoo.addons.mail.models.mail_template import format_tz
from odoo.fields import Datetime


class InventoryReport(models.Model):
    _name = "inventory.report"
    _description = "Báo cáo xuất nhập tồn tổng quát"

    name = fields.Char(string="Tên", default="Báo cáo xuất nhập tồn")
    type_location = fields.Boolean('Xuất theo một địa điểm kho', default=True)
    # type_get_value = fields.Selection([
    #     ('product', 'Giá trên sản phẩm'),
    #     ('stock', 'Quy trình kho'),
    #     ('account', 'Bút toán')], 'Lấy giá trị theo', default='product')
    report_with_lot = fields.Boolean(string="Xuất theo lô")
    date_from = fields.Datetime('Từ ngày', default=fields.Datetime.today(), required=True)
    date_to = fields.Datetime('Đến ngày', default=fields.Datetime.today(), required=True)
    location_id = fields.Many2one('stock.location', 'Địa điểm kho', domain=[('usage', 'in', ('internal', 'transit'))],
                                  required=True)
    location_ids = fields.Many2many('stock.location',
                                    'inventory_report_location_rel', 'report_id', 'location_id', 'Địa điểm kho',
                                    domain=[('usage', 'in', ('internal', 'transit'))], required=True)
    category_ids = fields.Many2many('product.category', 'inventory_report_category_rel', 'report_id', 'category_id',
                                    'Nhóm sản phẩm', required=True)
    product_ids = fields.Many2many('product.product', 'inventory_report_product_rel', 'report_id', 'product_id',
                                   'Sản phẩm')
    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Công ty', default=lambda self: self.env.user.company_id)
    display_product = fields.Boolean("Ẩn sản phẩm bằng 0", default=False)
    inventory_report_line_ids = fields.One2many('inventory.report.line', 'inventory_report_id', 'Chi tiết')
    inventory_report_line_ids_hide_display_product = fields.One2many('inventory.report.line', 'inventory_report_id',
                                                                     'Chi tiết',
                                                                     domain=['|', '|', '|', ('stock_out', '!=', 0),
                                                                             ('stock_opening', '!=', 0),
                                                                             ('stock_closing', '!=', 0),
                                                                             ('stock_in', '!=', 0)])
    value = fields.Float('Giá trị kho', digits=dp.get_precision('Product Price'), readonly=True)
    inventory_report_line_lot_ids = fields.One2many('inventory.report.line.lot', 'inventory_report_id', 'Chi tiết')
    inventory_report_line_lot_ids_hide_display_product = fields.One2many('inventory.report.line.lot',
                                                                         'inventory_report_id',
                                                                         'Chi tiết',
                                                                         domain=['|', '|', '|', ('stock_out', '!=', 0),
                                                                                 ('stock_opening', '!=', 0),
                                                                                 ('stock_closing', '!=', 0),
                                                                                 ('stock_in', '!=', 0)])

    @api.onchange('category_ids')
    def _category_onchange(self):
        res = {}
        list_category_ids = []
        category = self.category_ids
        if len(category) > 1:
            for c in category:
                list_category_ids.append(c.id)
            res['domain'] = {'product_ids': [('categ_id', 'in', list_category_ids)]}
        else:
            res['domain'] = {'product_ids': [('categ_id', '=', category.id)]}
        return res

    def action_remove_data_inventory_report_line(self):
        return self.inventory_report_line_ids.unlink()

    def action_remove_data_inventory_report_line_lot(self):
        return self.inventory_report_line_lot_ids.unlink()

    @api.model
    def action_open_form(self):
        action_values = self.env.ref('seatek_inventory_report.action_inventory_report_view').read()[0]
        res_id = self.env['inventory.report'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not res_id:
            res_id = self.env['inventory.report'].create({'user_id': self.env.user.id})
        res_id.write({'date_from': datetime.datetime.now(), 'date_to': datetime.datetime.now()})
        res_id.action_remove_data_inventory_report_line()
        action_values.update({'res_id': res_id.id})
        action = action_values
        return action

    def action_get_report_excel(self):
        return self.env.ref('seatek_inventory_report.inventory_report_excel').report_action(self)

    def _write_data(self, code_product, product, location, qty_opening, value_stock_opening, nhap_trong_ki,
                    value_stock_in, xuat_trong_ki, value_stock_out, qty_closing, value_stock_closing):
        lineObject = self.env['inventory.report.line']
        line = lineObject.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id),
                                  ('location_id', '=', location)], limit=1)
        if not line:
            lineObject.create({
                'inventory_report_id': self.id,
                'default_code': code_product,
                'product_id': product.id,
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
                'default_code': code_product,
                'stock_in': nhap_trong_ki,
                'stock_out': xuat_trong_ki,
                'value_stock_in': value_stock_in,
                'value_stock_out': value_stock_out,
                'stock_opening': qty_opening,
                'stock_closing': qty_closing,
            })

    def _write_data_lot(self, code_product, product, location, name_lot, qty_opening, value_stock_opening,
                        nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out, qty_closing,
                        value_stock_closing):
        lineLotObject = self.env['inventory.report.line.lot']
        line = lineLotObject.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id),
                                     ('location_id', '=', location), ('name_lot', '=', name_lot)], limit=1)
        if not line:
            lineLotObject.create({
                'inventory_report_id': self.id,
                'default_code': code_product,
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
                'stock_in': nhap_trong_ki,
                'stock_out': xuat_trong_ki,
                'value_stock_in': value_stock_in,
                'value_stock_out': value_stock_out,
                'stock_opening': qty_opening,
                'stock_closing': qty_closing,
            })

    def _cal_report(self, location_ids, products, date_from, date_to):
        for location in location_ids:
            for product in products:
                # ====> tính không theo lô
                stock_opening_not_lot = 0
                stock_in_not_lot = 0
                stock_out_not_lot = 0
                stock_closing_not_lot = 0

                # ====> tính theo lô
                sml = self.env['stock.move.line'].sudo().search(
                    [('state', '=', 'done'), ('product_id', '=', product.id), '|', ('location_id', '=', location),
                     ('location_dest_id', '=', location)])

                # có lot_id
                sml_lot_ids = [i.lot_id.id for i in sml if i.lot_id]
                lot_id_group_by_name = self.env['stock.production.lot'].read_group([('id', 'in', sml_lot_ids)],
                                                                                   fields=['lot_id', 'name'],
                                                                                   groupby=['name'])
                # tính có lot_id
                for i in lot_id_group_by_name:
                    spl_with_name = self.env['stock.production.lot'].sudo().search([
                        ('product_id', '=', product.id), ('name', '=', i['name'])], limit=1)

                    #   lot id của từng lô
                    #   spl_with_name.id -> là id của lô
                    #   tính cuối kì theo lot_id
                    search_sml = self.env['stock.move.line'].sudo().search(
                        [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(date_to)),
                         ('lot_id', '=', spl_with_name.id), '|', ('location_id', '=', location),
                         ('location_dest_id', '=', location)])
                    nhap = 0
                    xuat = 0
                    for search in search_sml:
                        if search.location_id.id == location:
                            xuat += search.qty_done
                        if search.location_dest_id.id == location:
                            nhap += search.qty_done
                    qty_closing = nhap - xuat

                    #   tính nhập xuất trong kì
                    search_sml_in_period = self.env['stock.move.line'].sudo().search(
                        [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(date_to)),
                         ('date', '>=', str(date_from)), ('lot_id', '=', spl_with_name.id), '|',
                         ('location_id', '=', location), ('location_dest_id', '=', location)])
                    nhap_trong_ki = 0
                    xuat_trong_ki = 0
                    for search in search_sml_in_period:
                        if search.location_id.id == location:
                            xuat_trong_ki += search.qty_done
                        if search.location_dest_id.id == location:
                            nhap_trong_ki += search.qty_done

                    #   tính đầu kì
                    qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
                    value_stock_opening = product.standard_price * qty_opening
                    value_stock_closing = product.standard_price * qty_closing
                    value_stock_in = product.standard_price * nhap_trong_ki
                    value_stock_out = product.standard_price * xuat_trong_ki

                    self._write_data_lot(product.product_tmpl_id.default_code, product, location, i['name'],
                                         qty_opening, value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki,
                                         value_stock_out, qty_closing, value_stock_closing)

                    stock_opening_not_lot += qty_opening
                    stock_in_not_lot += nhap_trong_ki
                    stock_out_not_lot += xuat_trong_ki
                    stock_closing_not_lot += qty_closing

                #   tính cuối kì không có lot_id ('lot_id', '=', None)
                search_sml = self.env['stock.move.line'].sudo().search(
                    [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(date_to)),
                     ('lot_id', '=', None), '|', ('location_id', '=', location),
                     ('location_dest_id', '=', location)])

                nhap = 0
                xuat = 0
                for search in search_sml:
                    if search.location_id.id == location:
                        xuat += search.qty_done
                    if search.location_dest_id.id == location:
                        nhap += search.qty_done
                qty_closing = nhap - xuat

                #   tính nhập xuất trong kì
                search_sml_in_period = self.env['stock.move.line'].sudo().search(
                    [('product_id', '=', product.id), ('state', '=', 'done'), ('date', '<=', str(date_to)),
                     ('date', '>=', str(date_from)), ('lot_id', '=', None), '|',
                     ('location_id', '=', location), ('location_dest_id', '=', location)])
                nhap_trong_ki = 0
                xuat_trong_ki = 0
                for search in search_sml_in_period:
                    if search.location_id.id == location:
                        xuat_trong_ki += search.qty_done
                    if search.location_dest_id.id == location:
                        nhap_trong_ki += search.qty_done

                #   tính đầu kì
                qty_opening = qty_closing + xuat_trong_ki - nhap_trong_ki
                value_stock_opening = product.standard_price * qty_opening
                value_stock_closing = product.standard_price * qty_closing
                value_stock_in = product.standard_price * nhap_trong_ki
                value_stock_out = product.standard_price * xuat_trong_ki

                self._write_data_lot(product.product_tmpl_id.default_code, product, location, "", qty_opening,
                                     value_stock_opening, nhap_trong_ki, value_stock_in, xuat_trong_ki, value_stock_out,
                                     qty_closing, value_stock_closing)

                stock_opening_not_lot += qty_opening
                value_stock_opening_not_lot = product.standard_price * stock_opening_not_lot
                stock_in_not_lot += nhap_trong_ki
                value_stock_in_not_lot = product.standard_price * stock_in_not_lot
                stock_out_not_lot += xuat_trong_ki
                value_stock_out_not_lot = product.standard_price * stock_out_not_lot
                stock_closing_not_lot += qty_closing
                value_stock_closing_not_lot = product.standard_price * stock_closing_not_lot

                self._write_data(product.product_tmpl_id.default_code, product, location, stock_opening_not_lot,
                                 value_stock_opening_not_lot, stock_in_not_lot, value_stock_in_not_lot,
                                 stock_out_not_lot, value_stock_out_not_lot, stock_closing_not_lot,
                                 value_stock_closing_not_lot)

    def action_get_report(self):
        global dt_from, dt_to
        self.inventory_report_line_ids.unlink()
        self.inventory_report_line_lot_ids.unlink()

        productObject = self.env['product.product']

        domain_product = []
        if self.category_ids:
            print(self.category_ids)
            domain_product.append(('categ_id', 'in', self.category_ids.ids))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        products = productObject.search([('type', 'in', ['product'])] + domain_product)

        domain_date = []

        if self.date_from:
            dt_from = Datetime.context_timestamp(self, self.date_from).replace(hour=0, minute=0, second=0)
            self.date_from = dt_from.replace(tzinfo=None)
            domain_date.append(('date', '>=', dt_from))
        if self.date_to:
            dt_to = Datetime.context_timestamp(self, self.date_to).replace(minute=59, hour=23, second=59)
            dt_to = dt_to.astimezone(pytz.utc)
            self.date_to = dt_to.replace(tzinfo=None)
            domain_date.append(('date', '<=', dt_to))

        if self.type_location:
            self._cal_report(location_ids=self.location_id.ids,
                             products=products,
                             date_from=dt_from,
                             date_to=dt_to)
        else:
            print("tính và gửi mail")


class InventoryReportLine(models.Model):
    _name = "inventory.report.line"
    _description = "Chi tiết xuất nhập tồn"
    _order = 'location_id, default_code asc'

    default_code = fields.Char(string="Mã sản phẩm")
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    inventory_report_id = fields.Many2one('inventory.report', 'Inventory Report', ondelete='cascade')

    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_opening = fields.Float('Giá trị tồn đầu kì', digits=(16, 0))

    stock_in = fields.Float('Nhập trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_in = fields.Float('Giá trị nhập trong kỳ', digits=(16, 0))

    stock_out = fields.Float('Xuất trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_out = fields.Float('Giá trị xuất trong kỳ', digits=(16, 0))

    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_closing = fields.Float('Giá trị tồn cuối kì', digits=(16, 0))

    location_id = fields.Many2one('stock.location', 'Địa điểm kho', domain=[('usage', 'in', ('internal', 'transit'))])


class InventoryReportLineLot(models.Model):
    _name = "inventory.report.line.lot"
    _description = "Chi tiết xuất nhập tồn"
    _order = 'location_id, default_code, name_lot asc'

    default_code = fields.Char(string="Mã sản phẩm")
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')
    name_lot = fields.Char(string="Lô sản phẩm")
    inventory_report_id = fields.Many2one('inventory.report', 'Inventory Report', ondelete='cascade')

    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_opening = fields.Float('Giá trị tồn đầu kì', digits=(16, 0))

    stock_in = fields.Float('Nhập trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_in = fields.Float('Giá trị nhập trong kỳ', digits=(16, 0))

    stock_out = fields.Float('Xuất trong kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_out = fields.Float('Giá trị xuất trong kỳ', digits=(16, 0))

    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))
    value_stock_closing = fields.Float('Giá trị tồn cuối kì', digits=(16, 0))

    location_id = fields.Many2one('stock.location', 'Địa điểm kho', domain=[('usage', 'in', ('internal', 'transit'))])
