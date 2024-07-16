import pytz

from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from odoo.tools import float_is_zero
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


def getYear():
    year = []
    for i in range(2000, 2050):
        year.append((i, str(i)))
    return year


class InventoryPeriod(models.Model):
    _name = "inventory.period"
    _description = "Period Management"
    _order = "date_to desc"

    name = fields.Char(string="Name", compute='_compute_name', store=True)
    month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                              (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                              (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], string="Month",
                             required=True)
    year = fields.Selection(getYear(), string="Year", required=True)
    date_from = fields.Datetime(string="From date", compute='_compute_date', store=True)
    date_to = fields.Datetime(string="To the date", compute='_compute_date', store=True)
    close_period = fields.Boolean(string="Close period")
    inventory_management_id = fields.Many2one('inventory.period.management', string="Inventory Management",
                                              ondelete='cascade')
    stock_closing_ids = fields.One2many('stock.closing.month', 'period_id', string="Stock closing")

    compute_company_id_view = fields.Many2one('res.company', string='Company', readonly=True,
                                              compute='_compute_company_id')
    company_id = fields.Many2one('res.company', string='Company')

    def _compute_company_id(self):
        self.compute_company_id_view = self.env.user.company_id.id

    @api.model
    def create(self, vals_list):
        # tu tao period
        if vals_list.get('inventory_management_id') is None:
            search_ipm = self.env['inventory.period.management'].sudo().search(
                [('company_id', '=', self.env.user.company_id.id)], limit=1)
            if search_ipm:
                vals_list.update({'inventory_management_id': search_ipm.id})
            else:
                self.env['inventory.period.management'].sudo().create({
                    'period': False,
                    'company_id': self.env.user.company_id.id
                })
                search_ipm1 = self.env['inventory.period.management'].sudo().search(
                    [('company_id', '=', self.env.user.company_id.id)], limit=1)
                vals_list.update({'inventory_management_id': search_ipm1.id})
        # tao bang inventory management
        if vals_list.get('company_id') is None:
            vals_list.update({'company_id': self.env.user.company_id.id})
        else:
            vals_list.update({'company_id': vals_list.get('company_id')})
        return super(InventoryPeriod, self).create(vals_list)

    @api.depends('month', 'year')
    def _compute_name(self):
        for r in self:
            date_month = r.month
            date_year = r.year
            if date_month and date_year:
                r.name = 'Tháng %s năm %s' % (date_month, date_year)

    @api.depends('month', 'year')
    def _compute_date(self):
        tz_info = pytz.timezone(self._context.get('tz', 'utc') or 'utc')

        for r in self:
            date_month = r.month
            date_year = r.year
            if date_month and date_year:
                date_calc_from = "%s-%s-%s" % (date_year, date_month, 1)
                date_from = tz_info.localize(fields.Datetime.from_string(str(date_calc_from))).astimezone(pytz.UTC)

                if date_month == 12:
                    date_calc_to = "%s-%s-%s" % (date_year + 1, 1, 1)
                else:
                    date_calc_to = "%s-%s-%s" % (date_year, date_month + 1, 1)
                date_to = tz_info.localize(fields.Datetime.from_string(str(date_calc_to))).astimezone(pytz.UTC)
                date_to += relativedelta(seconds=-1)
                print(date_from, date_to)
                r.date_from = str(date_from)
                r.date_to = str(date_to)

    def action_open_period(self):
        if self.close_period:
            self.write({'close_period': False})

    def action_close_period(self):
        if not self.close_period:
            self.write({'close_period': True})

    def calc_stock_closing(self, date_from, date_to):
        productObject = self.env['product.product']
        inventoryPeriod = self.env['inventory.period']
        stockMoveLineObject = self.env['stock.move.line']
        stockClosingObject = self.env['stock.closing.month']

        date_pre = date_from
        date_pre += relativedelta(seconds=-1)
        search_pre_period = inventoryPeriod.sudo().search([('date_to', '=', date_pre)], limit=1)
        print("thang truoc", search_pre_period, search_pre_period.name, date_from, date_to)
        if search_pre_period:
            if not search_pre_period.close_period:
                raise ValidationError(_('Unclosed period \"%s\"' % search_pre_period.name))

        def write_stock_closing(location_ids, product_id):
            for i in location_ids:
                # if i != 65:
                #     continue
                line_val = {
                    'product_id': product_id,
                    'location_id': i,
                    'period_id': self.id,
                    'have_data': True,
                    'uom_id': productObject.sudo().browse(product_id).uom_id.id,
                    'date_from': date_from,
                    'date_to': date_to,
                    'stock_opening': 0,
                    'stock_adj_in': 0,
                    'stock_in_internal': 0,
                    'stock_purchase': 0,
                    'stock_refund': 0,
                    'stock_mo': 0,
                    'stock_in_other': 0,
                    'stock_sale': 0,
                    'stock_adj_out': 0,
                    'stock_out_internal': 0,
                    'stock_refund_supplier': 0,
                    'stock_to_mo': 0,
                    'stock_out_other': 0,
                    'stock_closing': 0
                }
                search_location = stockMoveLineObject.sudo().search(
                    [('state', '=', 'done'), ('product_id', '=', product_id), ('date', '>=', date_from),
                     ('date', '<=', date_to), '|', ('location_id', '=', i), ('location_dest_id', '=', i)])

                line = stockClosingObject.sudo().search(
                    [('date_from', '=', date_from), ('date_to', '=', date_to), ('product_id', '=', product_id),
                     ('location_id', '=', i)], limit=1)

                search_pre_period_stock_closing = stockClosingObject.sudo().search(
                    [('date_to', '<', date_from), ('location_id', '=', i), ('product_id', '=', product_id)],
                    order='date_to desc')

                for i1 in search_pre_period_stock_closing:
                    line_val['stock_opening'] = i1.stock_closing
                    break

                stock_out = 0
                stock_in = 0
                for i1 in search_location:
                    if i1.location_id.id == i:
                        # xuat ra
                        stock_out += i1.qty_done
                        if i1.location_dest_id.usage == 'inventory':
                            line_val['stock_adj_out'] += i1.qty_done
                        elif i1.location_dest_id.usage in ('internal', 'transit'):
                            line_val['stock_out_internal'] += i1.qty_done
                        elif i1.location_dest_id.usage == 'supplier':
                            line_val['stock_refund_supplier'] += i1.qty_done
                        elif i1.location_dest_id.usage == 'customer':
                            line_val['stock_sale'] += i1.qty_done
                        elif i1.location_dest_id.usage == 'production':
                            line_val['stock_to_mo'] += i1.qty_done
                        else:
                            line_val['stock_out_other'] += i1.qty_done

                    if i1.location_dest_id.id == i:
                        # nhap vao
                        stock_in += i1.qty_done
                        if i1.location_id.usage == 'inventory':
                            line_val['stock_adj_in'] += i1.qty_done
                        elif i1.location_id.usage in ('internal', 'transit'):
                            line_val['stock_in_internal'] += i1.qty_done
                        elif i1.location_id.usage == 'supplier':
                            line_val['stock_purchase'] += i1.qty_done
                        elif i1.location_id.usage == 'customer':
                            line_val['stock_refund'] += i1.qty_done
                        elif i1.location_id.usage == 'production':
                            line_val['stock_mo'] += i1.qty_done
                        else:
                            line_val['stock_in_other'] += i1.qty_done

                line_val['stock_closing'] = (float(line_val['stock_opening']) + float(stock_in)) - float(stock_out)

                print(productObject.sudo().browse(product_id).name, line_val)

                if not line:
                    line.create(line_val)
                else:
                    line.write(line_val)

        result = stockMoveLineObject.sudo().read_group(
            [('state', '=', 'done'), ('date', '>=', date_from), ('date', '<=', date_to)],
            fields=['product_id', 'location_id', 'location_dest_id'], groupby=['product_id'])
        products = [i['product_id'][0] for i in result if
                    productObject.sudo().browse(i['product_id'][0]).type in ['product']]  # type in ['product', 'consu']

        for i in products:
            search_sml = stockMoveLineObject.sudo().search(
                [('product_id', '=', i), ('date', '>=', date_from), ('date', '<=', date_to)])

            locationIDs = []
            for data in search_sml:
                if data.location_id.id not in locationIDs:
                    locationIDs.append(data.location_id.id)
                if data.location_dest_id.id not in locationIDs:
                    locationIDs.append(data.location_dest_id.id)

            # if i != 58:
            #     continue
            write_stock_closing(location_ids=locationIDs, product_id=i)

    def action_calc_stock(self):
        if not self.close_period:
            raise UserError(_('Please close period!'))

        search_period = self.env['inventory.period'].sudo().search([('date_to', '>=', self.date_to)],
                                                                   order='date_to asc')
        for i in search_period:
            if i.close_period:
                self.calc_stock_closing(i.date_from, i.date_to)


class InventoryPeriodManagement(models.Model):
    _name = "inventory.period.management"
    _description = "Inventory period management"

    name = fields.Char(string="Name", default="Inventory period management")
    month_from = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                                   (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                                   (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],
                                  string="From month", default="1", required=True)
    year_from = fields.Selection(getYear(), string="From year", default="2000", required=True)
    month_to = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
                                 (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
                                 (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],
                                string="To the month", default="1", required=True)
    year_to = fields.Selection(getYear(), string="To the year", default="2000", required=True)
    period = fields.Boolean(string="Close Period")
    period_ids = fields.One2many('inventory.period', 'inventory_management_id', string="Inventory Period Management",
                                 domain=lambda self: [('company_id', '=', self.env.user.company_id.id)])
    compute_company_id_view = fields.Many2one('res.company', string='Company', readonly=True,
                                              compute='_compute_company_id')
    company_id = fields.Many2one('res.company', string='Company')

    def _compute_company_id(self):
        self.compute_company_id_view = self.env.user.company_id.id

    @api.model
    def action_calc_period(self):
        action_values = self.env.ref('seatek_inventory_period.action_inventory_period_management').read()[0]
        search = self.env['inventory.period.management'].sudo().search(
            [('company_id', '=', self.env.user.company_id.id)], limit=1)
        if not search:
            search = self.env['inventory.period.management'].create(
                {'period': False, 'company_id': self.env.user.company_id.id})
        action_values.update({'period': search.period, 'res_id': search.id})
        action = action_values
        return action

    def auto_upgrade_period(self):
        if self.compute_company_id_view.id != self.company_id.id:
            raise UserError(_("You just changed company, need to reload the menu to reload the data!"))

        inventoryPeriodObj = self.env['inventory.period']

        if self.month_from and self.year_from and self.month_to and self.year_to:
            month_from = self.month_from
            year_from = self.year_from
            month_to = self.month_to
            year_to = self.year_to

            for year in range(year_from, year_to + 1):
                for month in range(1, 13):
                    if year == year_from:
                        if month < month_from:
                            continue
                    if year == year_to:
                        if month > month_to:
                            continue

                    search = inventoryPeriodObj.sudo().search(
                        [('year', '=', year), ('month', '=', month), ('inventory_management_id', '=', self.id),
                         ('company_id', '=', self.compute_company_id_view.id)])
                    if not search:
                        inventoryPeriodObj.sudo().create({
                            'year': year, 'month': month, 'inventory_management_id': self.id,
                            'close_period': self.period, 'company_id': self.env.user.company_id.id
                        })
                    else:
                        search.sudo().write({
                            'close_period': self.period
                        })
        else:
            raise ValidationError(_('Please select month and year!'))

    def action_calculation_all_period(self):
        search_period_ids = self.env['inventory.period'].sudo().search([('inventory_management_id', '=', self.id)],
                                                                       order='date_to asc')
        for i in search_period_ids:
            if not i.close_period:
                break
            self.env['inventory.period'].calc_stock_closing(date_from=i.date_from, date_to=i.date_to)


class InventoryReportPeriodMonth(models.Model):
    _name = "stock.closing.month"
    _description = "Stock closing month"

    @api.depends('stock_adj_in', 'stock_in_internal', 'stock_purchase', 'stock_refund', 'stock_mo', 'stock_in_other')
    def compute_stock_in(self):
        for record in self:
            record.stock_in = record.stock_adj_in + record.stock_in_internal + record.stock_purchase + record.stock_refund + record.stock_mo + record.stock_in_other

    @api.depends('stock_sale', 'stock_adj_out', 'stock_out_internal', 'stock_refund_supplier', 'stock_to_mo',
                 'stock_out_other')
    def compute_stock_out(self):
        for record in self:
            record.stock_out = record.stock_sale + record.stock_adj_out + record.stock_out_internal + record.stock_refund_supplier + record.stock_to_mo + record.stock_out_other

    location_id = fields.Many2one('stock.location', "Địa điểm kho")
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    date_from = fields.Datetime(string="Từ ngày")
    date_to = fields.Datetime(string="Đến ngày")
    period_id = fields.Many2one('inventory.period', string="Kỳ")
    have_data = fields.Boolean(string="Have data", default=False)
    uom_id = fields.Many2one('uom.uom', 'Đơn vị')

    stock_opening = fields.Float('Tồn đầu kỳ', digits=dp.get_precision('Product Unit of Measure'))
    stock_adj_in = fields.Float('Điều chỉnh tăng', digits=dp.get_precision('Product Unit of Measure'))
    stock_in_internal = fields.Float('Nhập nội bộ', digits=dp.get_precision('Product Unit of Measure'))
    stock_purchase = fields.Float('Mua', digits=dp.get_precision('Product Unit of Measure'))
    stock_refund = fields.Float('Khách trả hàng', digits=dp.get_precision('Product Unit of Measure'))
    stock_mo = fields.Float('Sản xuất', digits=dp.get_precision('Product Unit of Measure'))
    stock_in_other = fields.Float('Nhập khác', digits=dp.get_precision('Product Unit of Measure'))
    stock_in = fields.Float('Tổng nhập', compute='compute_stock_in', store=True,
                            digits=dp.get_precision('Product Unit of Measure'))
    stock_sale = fields.Float('Bán', digits=dp.get_precision('Product Unit of Measure'))
    stock_adj_out = fields.Float('Điều chỉnh giảm', digits=dp.get_precision('Product Unit of Measure'))
    stock_out_internal = fields.Float('Xuất nội bộ', digits=dp.get_precision('Product Unit of Measure'))
    stock_refund_supplier = fields.Float('Trả hàng NCC', digits=dp.get_precision('Product Unit of Measure'))
    stock_to_mo = fields.Float('NVL SX', digits=dp.get_precision('Product Unit of Measure'))
    stock_out_other = fields.Float('Xuất khác', digits=dp.get_precision('Product Unit of Measure'))
    stock_out = fields.Float('Tổng xuất', compute='compute_stock_out', store=True,
                             digits=dp.get_precision('Product Unit of Measure'))
    stock_closing = fields.Float('Tồn cuối kỳ', digits=dp.get_precision('Product Unit of Measure'))

    # @staticmethod     # run every day
    # def get_inventory_report():
    #     date_today = datetime.datetime.today()
    #     # self.env['inventory.report.calculator.log'].sudo().create({"date": date_today, "state": "done"})


class StockMove(models.Model):
    _inherit = ['stock.move']

    def create(self, vals):
        inventoryPeriodObj = self.env['inventory.period']
        if vals.get('date_expected') is not None:
            date = vals.get('date_expected')
            search_in_inventory_period = inventoryPeriodObj.sudo().search(
                [('date_from', '<=', date), ('date_to', '>=', date), ('company_id', '=', self.env.user.company_id.id)])
            for i in search_in_inventory_period:
                if i.close_period:
                    raise UserError(_('Period closed please do not modify!'))
        res = super(StockMove, self).create(vals)
        return res

    def write(self, vals):
        inventoryPeriodObj = self.env['inventory.period']
        for r in self:
            date = r.date
            search_in_inventory_period = inventoryPeriodObj.sudo().search(
                [('date_from', '<=', date), ('date_to', '>=', date), ('company_id', '=', self.env.user.company_id.id)])
            for i in search_in_inventory_period:
                if i.close_period:
                    raise UserError(_('Period closed please do not modify!'))

        res = super(StockMove, self).write(vals)
        return res


class InventoryPeriodReport(models.Model):
    _name = "vio.inventory.report"
    _inherit = "vio.inventory.report"

    def action_inventor_period_report(self):
        self.inventory_report_line_ids.unlink()

        LineObj = self.env['vio.inventory.report.line']
        ProductObj = self.env['product.product']
        LocationObj = self.env['stock.location']

        domain_product = []
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', self.categ_ids.ids))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        products = ProductObj.search([('type', '=', 'product')] + domain_product)

        location_ids = self.location_ids.ids
        if not location_ids:
            location_ids = LocationObj.search([('usage', 'in', ('internal', 'transit'))]).ids
        value = 0

        tzinfo = pytz.timezone(self._context.get('tz', 'utc') or 'utc')

        domain_date = []

        date_to = tzinfo.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)
        date_from = tzinfo.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)

        if self.date_to:
            date_to = tzinfo.localize(fields.Datetime.from_string(str(self.date_to))).astimezone(pytz.UTC)
            date_to += relativedelta(days=1, seconds=-1)
            date_to = str(date_to)
            domain_date.append(('date', '<=', date_to))
        if self.date_from:
            date_from = tzinfo.localize(fields.Datetime.from_string(str(self.date_from))).astimezone(pytz.UTC)
            domain_date.append(('date', '>=', str(date_from)))
            date_from += relativedelta(seconds=-1)
            date_from = str(date_from)

        domain_in = [('location_id', 'not in', location_ids), ('location_dest_id', 'in', location_ids)]
        domain_out = [('location_id', 'in', location_ids), ('location_dest_id', 'not in', location_ids)]

        pro = self.env['stock.move.line'].read_group([('state', '=', 'done')] + domain_date,
                                                     ['product_id'], ['product_id'])
        pro_ids = [i['product_id'][0] for i in pro]
        for product in products:
            print(product.id, location_ids, domain_date)
            line = LineObj.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id)], limit=1)
            if product.id not in pro_ids:
                line_valx = {'inventory_report_id': self.id, 'product_id': product.id, 'uom_id': product.uom_id.id,
                             'stock_opening': 0.0, 'stock_closing': 0.0, 'stock_adj_in': 0, 'stock_in_internal': 0,
                             'stock_purchase': 0, 'stock_refund': 0, 'stock_adj_out': 0, 'stock_ount_internal': 0,
                             'stock_refund_supplier': 0, 'stock_sale': 0, 'stock_mo': 0, 'stock_to_mo': 0}
                if not self.hide_zero_line:
                    if not line:
                        LineObj.create(line_valx)
                    else:
                        line.write(line_valx)
                else:
                    if line:
                        line.unlink()
                continue

            qty_opening = product.with_context(location=location_ids, to_date=date_from).qty_available
            qty_closing = product.with_context(location=location_ids, to_date=date_to).qty_available

            line_val = {
                'inventory_report_id': self.id,
                'product_id': product.id,
                'uom_id': product.uom_id.id,
                'stock_opening': qty_opening,
                'stock_closing': qty_closing,
                'stock_adj_in': 0,
                'stock_in_internal': 0,
                'stock_purchase': 0,
                'stock_refund': 0,
                'stock_adj_out': 0,
                'stock_ount_internal': 0,
                'stock_refund_supplier': 0,
                'stock_sale': 0,
                'stock_mo': 0,
                'stock_to_mo': 0,
            }

            move_in_ids = self.env['stock.move.line'].read_group(
                [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_in + domain_date,
                ['qty_done'], ['location_id'])

            for move_val in move_in_ids:
                location = LocationObj.browse(move_val['location_id'][0])
                qty_done = move_val['qty_done']
                if location.usage == 'inventory':
                    line_val['stock_adj_in'] += qty_done
                elif location.usage in ('internal', 'transit'):
                    line_val['stock_in_internal'] += qty_done
                elif location.usage == 'supplier':
                    line_val['stock_purchase'] += qty_done
                elif location.usage == 'customer':
                    line_val['stock_refund'] += qty_done
                elif location.usage == 'production':
                    line_val['stock_mo'] += qty_done
                else:
                    line_val['stock_in_other'] += qty_done

            move_out_ids = self.env['stock.move.line'].read_group(
                [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_out + domain_date,
                ['qty_done'], ['location_dest_id'])

            for move_val in move_out_ids:
                location = LocationObj.browse(move_val['location_dest_id'][0])
                qty_done = move_val['qty_done']
                if location.usage == 'inventory':
                    line_val['stock_adj_out'] += qty_done
                elif location.usage in ('internal', 'transit'):
                    line_val['stock_ount_internal'] += qty_done
                elif location.usage == 'supplier':
                    line_val['stock_refund_supplier'] += qty_done
                elif location.usage == 'customer':
                    line_val['stock_sale'] += qty_done
                elif location.usage == 'production':
                    line_val['stock_to_mo'] += qty_done
                else:
                    line_val['stock_out_other'] += qty_done

            if not line:
                LineObj.create(line_val)
            else:
                line.write(line_val)

            if self.hide_zero_line:
                if not float_is_zero(line.stock_opening, precision_rounding=2):
                    continue
                if not float_is_zero(line.stock_in, precision_rounding=2):
                    continue
                if not float_is_zero(line.stock_out, precision_rounding=2):
                    continue
                if not float_is_zero(line.stock_closing, precision_rounding=2):
                    continue
                line.unlink()

            value += product.standard_price * qty_closing

    def action_inventor_period_report_with_date(self, date_from, date_to, product):
        locationObject = self.env['stock.location']

        location_ids = self.location_ids.ids
        if not location_ids:
            location_ids = locationObject.search([('usage', 'in', ('internal', 'transit'))]).ids
        value = 0
        tz_info = pytz.timezone(self._context.get('tz', 'utc') or 'utc')
        domain_date = [('date', '>=', date_from), ('date', '<=', date_to)]
        domain_in = [('location_id', 'not in', location_ids), ('location_dest_id', 'in', location_ids)]
        domain_out = [('location_id', 'in', location_ids), ('location_dest_id', 'not in', location_ids)]

        qty_opening = product.with_context(location=location_ids, to_date=date_from).qty_available
        qty_closing = product.with_context(location=location_ids, to_date=date_to).qty_available

        line_val = {
            'inventory_report_id': self.id,
            'product_id': product.id,
            'uom_id': product.uom_id.id,
            'stock_opening': qty_opening,
            'stock_closing': qty_closing,
            'stock_adj_in': 0,
            'stock_in_internal': 0,
            'stock_purchase': 0,
            'stock_refund': 0,
            'stock_adj_out': 0,
            'stock_ount_internal': 0,
            'stock_refund_supplier': 0,
            'stock_sale': 0,
            'stock_mo': 0,
            'stock_to_mo': 0,
        }

        move_in_ids = self.env['stock.move.line'].read_group(
            [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_in + domain_date,
            ['qty_done'], ['location_id'])

        for move_val in move_in_ids:
            location = locationObject.browse(move_val['location_id'][0])
            qty_done = move_val['qty_done']
            if location.usage == 'inventory':
                line_val['stock_adj_in'] += qty_done
            elif location.usage in ('internal', 'transit'):
                line_val['stock_in_internal'] += qty_done
            elif location.usage == 'supplier':
                line_val['stock_purchase'] += qty_done
            elif location.usage == 'customer':
                line_val['stock_refund'] += qty_done
            elif location.usage == 'production':
                line_val['stock_mo'] += qty_done
            else:
                line_val['stock_in_other'] += qty_done

        move_out_ids = self.env['stock.move.line'].read_group(
            [('state', '=', 'done'), ('product_id', '=', product.id)] + domain_out + domain_date,
            ['qty_done'], ['location_dest_id'])

        for move_val in move_out_ids:
            location = locationObject.browse(move_val['location_dest_id'][0])
            qty_done = move_val['qty_done']
            if location.usage == 'inventory':
                line_val['stock_adj_out'] += qty_done
            elif location.usage in ('internal', 'transit'):
                line_val['stock_ount_internal'] += qty_done
            elif location.usage == 'supplier':
                line_val['stock_refund_supplier'] += qty_done
            elif location.usage == 'customer':
                line_val['stock_sale'] += qty_done
            elif location.usage == 'production':
                line_val['stock_to_mo'] += qty_done
            else:
                line_val['stock_out_other'] += qty_done

        value += product.standard_price * qty_closing
        return line_val, value

    def action_inventor_period_report1(self):
        self.inventory_report_line_ids.unlink()

        inventoryLineObject = self.env['vio.inventory.report.line']
        productObject = self.env['product.product']
        locationObject = self.env['stock.location']
        stockClosingObject = self.env['stock.closing.month']
        inventoryPeriodObject = self.env['inventory.period']

        domain_product = []
        if self.categ_ids:
            domain_product.append(('categ_id', 'in', self.categ_ids.ids))
        if self.product_ids:
            domain_product.append(('id', 'in', self.product_ids.ids))
        products = productObject.search([('type', '=', 'product')] + domain_product)
        product_ids = [i.id for i in products]

        location_ids = self.location_ids.ids
        if not location_ids:
            location_ids = locationObject.search([('usage', 'in', ('internal', 'transit'))]).ids
        value = 0

        tz_info = pytz.timezone(self._context.get('tz', 'utc') or 'utc')

        domain_date = []

        date_to = tz_info.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)
        date_from = tz_info.localize(fields.Datetime.from_string(str(fields.Date.today()))).astimezone(pytz.UTC)

        if self.date_from:
            date_from = tz_info.localize(fields.Datetime.from_string(str(self.date_from))).astimezone(pytz.UTC)
            domain_date.append(('date_from', '>=', str(date_from)))

        if self.date_to:
            date_to = tz_info.localize(fields.Datetime.from_string(str(self.date_to))).astimezone(pytz.UTC)
            date_to += relativedelta(days=1, seconds=-1)
            domain_date.append(('date_to', '<=', str(date_to)))

        for product in products:
            if product.id != 73:
                continue
            line = inventoryLineObject.search([('inventory_report_id', '=', self.id), ('product_id', '=', product.id)],
                                              limit=1)
            search_with_date = stockClosingObject.sudo().search(
                [('location_id', 'in', location_ids), ('product_id', '=', product.id)] + domain_date)
            line_val = {
                'inventory_report_id': self.id,
                'product_id': product.id,
                'uom_id': product.uom_id.id,
                'stock_in': 0,
                'stock_opening': 0,
                'stock_adj_in': 0,
                'stock_in_internal': 0,
                'stock_purchase': 0,
                'stock_refund': 0,
                'stock_mo': 0,
                'stock_in_other': 0,
                'stock_out': 0,
                'stock_sale': 0,
                'stock_adj_out': 0,
                'stock_out_internal': 0,
                'stock_refund_supplier': 0,
                'stock_to_mo': 0,
                'stock_out_other': 0,
                'stock_closing': 0
            }
            for index, i in enumerate(search_with_date):
                line_val['stock_in'] += i.stock_in
                line_val['stock_adj_in'] += i.stock_adj_in
                line_val['stock_in_internal'] += i.stock_in_internal
                line_val['stock_purchase'] += i.stock_purchase
                line_val['stock_refund'] += i.stock_refund
                line_val['stock_mo'] += i.stock_mo
                line_val['stock_in_other'] += i.stock_in_other
                line_val['stock_out'] += i.stock_out
                line_val['stock_sale'] += i.stock_sale
                line_val['stock_adj_out'] += i.stock_adj_out
                line_val['stock_out_internal'] += i.stock_out_internal
                line_val['stock_refund_supplier'] += i.stock_refund_supplier
                line_val['stock_to_mo'] += i.stock_to_mo
                line_val['stock_out_other'] += i.stock_out_other

                if index == 0:
                    line_val['stock_opening'] = i.stock_opening
                if index == len(search_with_date) - 1:
                    line_val['stock_closing'] = i.stock_closing

            # tinh cac ngay con lai
            data = []
            custom_domain_date = []
            search_date = inventoryPeriodObject.sudo().search(domain_date)
            if len(search_date) == 0:
                custom_domain_date = [('date', '>=', str(date_from)), ('date', '<=', str(date_to))]
            else:
                if str(search_date[0].date_from) not in str(date_from):
                    line_value, value = self.action_inventor_period_report_with_date(str(date_from),
                                                                                     str(search_date[0].date_from),
                                                                                     product)
                    data.append([line_value, value])
                    # custom_domain_date.append(('date', '>=', str(date_from)))
                    # custom_domain_date.append(('date', '<=', str(search_date[0].date_from)))
                if str(search_date[len(search_date) - 1].date_to) not in str(date_to):
                    line_value, value = self.action_inventor_period_report_with_date(
                        str(search_date[len(search_date) - 1].date_to), str(date_to), product)
                    data.append([line_value, value])
                    # custom_domain_date.append(('date', '>=', str(search_date[len(search_date) - 1].date_to)))
                    # custom_domain_date.append(('date', '<=', str(date_to)))

            print(product.id, product.name, data[0][0], line_val)

            if not line:
                line.create(line_val)
            else:
                line.write(line_val)
            value += product.standard_price * line_val['stock_closing']

            # print(product.id, product.name, line_val)
            # print('\n\n')

        # custom_domain_date = []
        # search_date = stockClosingObject.sudo().search(
        #     [('product_id', '=', 73), ('location_id', '=', 65)] + domain_date)
        # if len(search_date) == 0:
        #     custom_domain_date = [('date', '>=', str(date_from)), ('date', '<=', str(date_to))]
        # else:
        #     if str(search_date[0].date_from) not in str(date_from):
        #         custom_domain_date.append(('date', '>=', str(date_from)))
        #         custom_domain_date.append(('date', '<=', str(search_date[0].date_from)))
        #     if str(search_date[len(search_date)-1].date_to) not in str(date_to):
        #         custom_domain_date.append(('date', '>=', str(search_date[len(search_date)-1].date_to)))
        #         custom_domain_date.append(('date', '<=', str(date_to)))
        #
        # print('custom', custom_domain_date)
