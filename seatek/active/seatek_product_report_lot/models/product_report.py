from odoo.tools import  pycompat
from odoo.tools.safe_eval import safe_eval
import pytz

from odoo import models, fields, api
from odoo.fields import Datetime


class ProductReport(models.Model):
    _name = 'product.report.lot'
    _description = 'Xuất báo cáo tình trạng sản phẩm theo lô'

    name = fields.Char(string='Tên', default='Báo cáo tình trạng tồn kho lô')
    user_id = fields.Many2one('res.users')
    location_ids = fields.Many2many(comodel_name='stock.location', string='Địa điểm kho', required=True,
                                    domain=[('usage', 'in', ('internal', 'transit'))])
    date_from = fields.Datetime(string="Từ ngày")
    date_to = fields.Datetime(string="Đến ngày")
    hide_stock_closing_zero = fields.Boolean(string="Còn tồn kho", default=True)

    product_ids = fields.Many2many('product.product', string='Sản phẩm', domain=[('type', 'in', ['product'])])

    product_report_line_ids = fields.One2many('product.report.lot.line', 'product_report_id', 'Chi tiết')
    product_report_line_ids_hide_stock_closing_zero = fields.One2many('product.report.lot.line', 'product_report_id', 'Chi tiết', domain=[('product_qty', '<', 0)])

    @api.model
    def action_open_report(self):
        action_values = self.env.ref('seatek_product_report_lot.action_product_report_lot_view').read()[0]
        res_id = self.env['product.report.lot'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not res_id:
            res_id = self.env['product.report.lot'].create({'user_id': self.env.user.id})
        res_id.action_remove_data_report_line()
        action_values.update({'res_id': res_id.id})
        action = action_values
        return action

    def action_remove_data_report_line(self):
        return self.product_report_line_ids.unlink()

    def action_report_data(self):
        self.product_report_line_ids.unlink()

        lineObject = self.env['product.report.lot.line']

        product_ids = self.product_ids.ids
        domain_product = []
        if self.product_ids:
            domain_product.append(('product_id', 'in', product_ids))
        location_ids = self.location_ids

        domain_date = []
        if self.date_from:
            dt_from = Datetime.context_timestamp(self, self.date_from).replace(hour=0, minute=0, second=0)
            self.date_from = dt_from.replace(tzinfo=None)
            domain_date.append(('create_date', '>=', dt_from))
        if self.date_to:
            dt_to = Datetime.context_timestamp(self, self.date_to).replace(hour=23, minute=59, second=59)
            dt_to = dt_to.astimezone(pytz.utc)
            self.date_to = dt_to.replace(tzinfo=None)
            domain_date.append(('create_date', '<=', dt_to))

        production_lot = self.env['stock.production.lot'].sudo().search([] + domain_product + domain_date)
        for location in location_ids:
            for lot in production_lot:
                # tính tồn kho
                sml = self.env['stock.move.line'].sudo().search(
                    [('product_id', '=', lot.product_id.id), ('lot_id', '=', lot.id), '|',
                     ('location_id', '=', location.id), ('location_dest_id', '=', location.id)])

                nhap = 0
                xuat = 0
                for search in sml:
                    if search.location_id.id == location.id:
                        xuat += search.qty_done
                    if search.location_dest_id.id == location.id:
                        nhap += search.qty_done
                qty = nhap - xuat

                if self.hide_stock_closing_zero:
                    if qty <= 0.01:
                        continue

                # lấy log gần nhất
                mail_message = self.env['mail.message'].sudo().search(
                    [('model', '=', 'stock.production.lot'), ('res_id', '=', lot.id)])

                logs = [i.id for i in mail_message]
                logs.sort(reverse=True)
                id_log = logs[0]
                s_log = self.env['mail.message'].sudo().search(
                    [('id', '=', id_log)], limit=1)
                data_log = s_log.body.replace("<p>", "").replace("</p>", "")

                line = lineObject.search(
                    [('product_report_id', '=', self.id), ('lot_id', '=', lot.id),
                     ('product_id', '=', lot.product_id.id),
                     ('location_id', '=', location.id)], limit=1)

                product_name = lot.product_id.name

                if not line:
                    lineObject.create({
                        "product_report_id": self.id,
                        "location_id": location.id,
                        "lot_id": lot.id,
                        "lot_name": lot.name,
                        "default_code": lot.product_id.product_tmpl_id.default_code,
                        "product_name": product_name,
                        "product_id": lot.product_id.id,
                        "product_qty": qty,
                        "lot_create_date": lot.create_date,
                        "life_date": lot.life_date,
                        "use_date": lot.use_date,
                        "removal_date": lot.removal_date,
                        "alert_date": lot.alert_date,
                        "log_end": data_log,
                    })
                else:
                    line.write({
                        "product_qty": qty,
                        "default_code": lot.product_id.product_tmpl_id.default_code,
                        "log_end": data_log,
                    })

    def action_report_excel(self):
        print("")

    def action_open_detail(self):
        action = self.env.ref('seatek_product_report_lot.action_product_report_line_view').read()[0]
        action['domain'] = [('product_report_id', 'in', self.ids)]
        return action


class ProductReportLine(models.Model):
    _name = 'product.report.lot.line'
    _order = 'location_id, default_code, lot_create_date asc'
    _description = 'Chi tiết báo cáo sản phẩm theo lô'

    name = fields.Char(string="Thông tin chi tiết", default="Thông tin chi tiết")

    product_report_id = fields.Many2one('product.report.lot', string='Report ID', ondelete='cascade')
    location_id = fields.Many2one('stock.location', string="Địa điểm kho")

    lot_name = fields.Char(string="Lô")
    lot_id = fields.Many2one('stock.production.lot', string="Lot ID")
    default_code = fields.Char('Mã sản phẩm')
    product_id = fields.Many2one('product.product', 'Sản phẩm')
    product_name = fields.Char(string="Sản phẩm")
    product_qty = fields.Float(string="Tồn kho")
    lot_create_date = fields.Datetime(string="Ngày tạo")
    life_date = fields.Datetime(string='Ngày hết hạn',
                                help='This is the date on which the goods with this Serial Number may become dangerous and must not be consumed.')
    use_date = fields.Datetime(string='Sử dụng trước ngày',
                               help='This is the date on which the goods with this Serial Number start deteriorating, without being dangerous yet.')
    removal_date = fields.Datetime(string='Ngày loại bỏ',
                                   help='This is the date on which the goods with this Serial Number should be removed from the stock.')
    alert_date = fields.Datetime(string='Ngày cảnh báo',
                                 help='Date to determine the expired lots and serial numbers using the filter "Expiration Alerts".')
    log_end = fields.Char(string="Ghi chú gần nhất")

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_sale_total=fields.Monetary(string="Sale Total")
    product_output_qty=fields.Float(string="Sale Quantity")
    product_sale_target_price=fields.Monetary(string="Target Price")
    product_sale_target_total=fields.Monetary(string="Sale Target Total",compute='_product_sale_target_total')
    differential_value=fields.Monetary(string="Differential Value",compute='_differential_value')

    @api.depends('product_output_qty')
    def _compute_product_output_qty(self):
        self.product_sale_target_total=self.product_sale_target_price*self.product_output_qty
    @api.one
    def _differential_value(self):
        self.differential_value=self.product_sale_target_total- self.product_sale_total
    @api.one
    def _product_sale_target_total(self):
        self.product_sale_target_total=self.product_output_qty*self.product_sale_target_price
    product_cost=fields.Float(string="Cost")
    currency_id = fields.Many2one('res.currency', string='Currency',default=lambda self: self.env.user.company_id.currency_id)

class ReportProductCostWizard(models.TransientModel):
    _name="report.product.cost.lot.wizard"

    company_id=fields.Many2one('res.company',default=lambda self: self.env.user.company_id)
    product_id=fields.Many2many('product.product')
    lot_id=fields.Many2many('stock.production.lot')
    date_to=fields.Datetime()
    calculate_product_cost=fields.Boolean(default=False)
    hide_display_zero=fields.Boolean(default=False)

    @api.model
    def action_open_report(self):
        action_values = self.env.ref('seatek_product_report_lot.action_report_product_cost_lot_wizard_view').read()[0]
        action = action_values
        return action

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        action = self.env.ref('seatek_product_report_lot.action_report_product_cost_lot_view')
        action_data = action.read()[0]
        context1 = action_data.get('context', {})
        if isinstance(context1, pycompat.string_types):
            context1 = safe_eval(context1)
        report = self._prepare_report_product_cost()
        report.compute_data_for_report(limit=True)
        context1.update({'active_id':report.id})
        context1.update({'company_id':report.company_id})
        action_data['context'] = context1
        action_data['company_id'] = report.company_id
        #
        return action_data
    def _prepare_report_product_cost(self):
        self.ensure_one()
        if self.calculate_product_cost:
            date_to=fields.Datetime.now()
        else:
            date_to=False
        values= {
            'date_to': self.date_to,
            'company_id': self.company_id.id,
            'lot_id': [[6,False,self.lot_id.ids]],
            'product_id': [[6,False,self.product_id.ids]],
            'current_page': 1,
            'date_to':date_to,
            'hide_display_zero':self.hide_display_zero,

        }

        res=self.env['report.product.cost.lot'].create(values)
        return res

    def get_html(self):
        result = {}
        rcontext = {}
        context = dict(self.env.context)
        report = self.browse(context.get('active_id'))
        if report:
            rcontext['docs'] = report
            result['html'] = self.env.ref(
                'seatek_product_report_lot.report_product_cost_lot').render(
                rcontext)
        return result

    @api.model
    def create(self, vals):
        res = super(ReportProductCostWizard, self).create(vals)
        return res
class ReportProductCostLotLine(models.TransientModel):
    _name = "report.product.cost.lot.line"

    product_cost_lot_id=fields.Many2one('report.product.cost.lot')
    product_id=fields.Many2one('product.product')
    lot_id=fields.Many2many('stock.production.lot')
    lot_detail=fields.One2many('report.product.cost.lot.line.detail','product_cost_lot_line')
    show_detail =fields.Boolean(default=True)
    hide_display_zero = fields.Boolean(default=False, string="Ẩn dòng không phát sinh")
    @api.model
    def create(self, vals):
        res = super(ReportProductCostLotLine, self).create(vals)
        return res
class ReportProductCostLotLineDetail(models.TransientModel):
    _name = "report.product.cost.lot.line.detail"

    product_cost_lot_line=fields.Many2one('report.product.cost.lot.line')
    lot_id=fields.Many2one('stock.production.lot')
    product_cost=fields.Monetary(string="Product Cost",precision_digits=2)
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)
    product_sale_total = fields.Monetary(string="Sale Total")
    product_output_qty = fields.Float(string="Sale Quantity")
    product_sale_target_price = fields.Monetary(string="Target Price")
    product_sale_target_total = fields.Monetary(string="Sale Target Total", compute='_product_sale_target_total')
    differential_value = fields.Monetary(string="Differential Value", compute='_differential_value')

    @api.model
    def create(self, vals):
        res = super(ReportProductCostLotLineDetail, self).create(vals)
        return res

    @api.depends('product_output_qty')
    def _compute_product_output_qty(self):
        self.product_sale_target_total = self.product_sale_target_price * self.product_output_qty

    @api.one
    def _differential_value(self):
        self.differential_value = self.product_sale_target_total - self.product_sale_total

    @api.one
    def _product_sale_target_total(self):
        self.product_sale_target_total = self.product_output_qty * self.product_sale_target_price

class ReportProductCost(models.TransientModel):
    _name="report.product.cost.lot"

    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    product_id = fields.Many2many('product.product','product_cost_lot_rel')
    lot_id = fields.Many2many('stock.production.lot')
    date_to = fields.Datetime()
    product_cost_lot_detail=fields.One2many('report.product.cost.lot.line','product_cost_lot_id')
    product_offset=fields.Float()
    offset = fields.Integer(default=0)
    page_limit = fields.Integer(default=3)
    pages = fields.Integer(default=1)
    current_page = fields.Integer(default=1)
    hide_display_zero = fields.Boolean(default=False,string="Ẩn dòng không phát sinh")

    def get_html(self):
        result = {}
        rcontext = {}
        context = dict(self.env.context)
        report = self.browse(context.get('active_id'))
        if report:
            rcontext['docs'] = report
            result['html'] = self.env.ref(
                'seatek_product_report_lot.report_product_cost_lot').render(
                rcontext)
        return result

    @api.multi
    def compute_data_for_report(self,limit=False):
        list_product=[]
        self.product_cost_lot_detail.unlink()
        if self.product_id:
            list_product=self.product_id.ids
        else:

            products=self.env['product.product'].sudo().search([('company_id','=',self.env.user.company_id.id)])
            list_product=products.ids
        domain=[('product_id','in',list_product)]
        domain=[]
        if self.lot_id:
            domain.append(('id', 'in', self.lot_id.ids))
        if self.hide_display_zero:
            domain.append(('product_cost','>',0))
            domain.append(('product_cost','!=',False))
        if self.hide_display_zero or self.lot_id:
            # lot_ids = self.env['stock.production.lot'].sudo().search(domain,order='create_date DESC')
            lot_ids = self.env['stock.production.lot'].sudo().read_group(domain, fields=['product_id'], groupby=['product_id'],
                                                                         orderby='create_date DESC')
            list_product=[]
            for lot_id in lot_ids:
                if lot_id['product_id']:
                    if lot_id['product_id'][0] not in list_product:
                        list_product.append(lot_id['product_id'][0])
        self.pages=len(list_product)/self.page_limit
        if limit:
            products=self.env['product.product'].sudo().search([('id','in',list_product)],limit=self.page_limit,offset=self.offset)
        else:
            products = self.env['product.product'].sudo().search([('id', 'in', list_product)])
        for product_id in products:
            domain=[('product_id','=',product_id.id)]


            # lot_ids = self.env['stock.move.line'].sudo().read_group(domain, fields=['lot_id','create_date'], groupby=['lot_id','create_date'], orderby='create_date DESC',
            #                                                     limit=160)
            if self.lot_id:
                domain.append(('id', 'in', self.lot_id.ids))
            lot_ids = self.env['stock.production.lot'].sudo().search(domain, order='create_date DESC')
            vals = {}
            vals.update({'product_cost_lot_id': self.id, 'product_id': product_id.id})
            if len(lot_ids)>0:
                lots=[]
                for lot_id in lot_ids:
                    lots.append(lot_id.id)
                vals.update({'lot_id':[(6,False,lots)]})
            self.product_cost_lot_detail.create(vals)
        for detail in self.product_cost_lot_detail:
            vals={}
            hide_display_zero=True
            for lot in detail.lot_id:
                if self.date_to:
                    stock_move_lines=self.env['stock.move.line'].sudo().search([('lot_id','=',lot.id),('state','=','done'),('date','<=',self.date_to)],
                                                                               order='date desc')
                    cost_total=0
                    quantity_total=0
                    product_cost=0
                    for stock_move_line in stock_move_lines:
                        if stock_move_line.qty_done>0:
                            if stock_move_line.move_id and not stock_move_line.move_id.origin_returned_move_id:
                                if stock_move_line.picking_id.picking_type_id.code=='incoming':
                                    cost=stock_move_line.qty_done*stock_move_line.move_id.price_unit
                                    quantity_total += stock_move_line.qty_done
                                    if cost>0:
                                        cost_total+=cost
                                    if quantity_total > 0:
                                        product_cost = cost_total / quantity_total
                                elif stock_move_line.picking_id.picking_type_id.code=='outgoing' and stock_move_line.move_id.sale_line_id:
                                    quantity_total -= stock_move_line.qty_done

                    vals.update({'product_cost': product_cost})
                else:
                    product_cost=lot.product_cost
                    product_sale_total=lot.product_sale_total
                    product_output_qty=lot.product_output_qty
                    product_sale_target_price=lot.product_sale_target_price
                    product_sale_target_total=lot.product_sale_target_total
                    differential_value=lot.differential_value
                    vals.update({'product_cost': product_cost})
                    vals.update({'product_output_qty': product_output_qty})
                    vals.update({'product_sale_target_price': product_sale_target_price})
                    vals.update({'product_sale_target_total': product_sale_target_total})
                    vals.update({'product_sale_total': product_sale_total})
                    vals.update({'differential_value': differential_value})
                if self.hide_display_zero:
                    if product_cost>0:
                        vals.update({'product_cost_lot_line':detail.id,'lot_id':lot.id})
                        hide_display_zero=False
                else:
                    hide_display_zero=False
                    vals.update({'product_cost_lot_line': detail.id, 'lot_id': lot.id})

                detail.lot_detail.create(vals)
            detail.write({'hide_display_zero': hide_display_zero})
        return {'current_page':self.current_page,
                'pages':self.pages,
            'docs': self
        }

    @api.multi
    def action_next(self):
        self.ensure_one()
        self.product_cost_lot_detail.unlink()
        if self.current_page >= self.pages:
            result = self.get_page_data()
            return result
        else:
            self.write({'offset': self.offset + self.page_limit})
            self.write({'current_page': self.current_page + 1})
            result = self.get_page_data()
            return result

    @api.multi
    def action_prev(self):

        self.ensure_one()
        self.product_cost_lot_detail.unlink()
        if self.current_page <= 1:
            result = self.get_page_data()
            return result
        else:
            self.write({'offset': self.offset - self.page_limit})
            self.write({'current_page': self.current_page - 1})
            result = self.get_page_data()
            return result

    def get_page_data(self):
        self.self_action = action = self.env.ref(
            'seatek_product_report_lot.action_report_product_cost_lot_view_qweb')
        action_data = action.read()[0]
        context1 = action_data.get('context', {})
        if isinstance(context1, pycompat.string_types):
            context1 = safe_eval(context1)
        self.compute_data_for_report(limit=True)
        context1['active_id'] = self.id
        action_data['context'] = context1
        result = {}
        rcontext = {}
        context = dict(self.env.context)
        report = self.browse(context.get('active_id'))
        if report:
            rcontext['docs'] = report
            result['html'] = self.env.ref(
                'seatek_product_report_lot.report_product_cost_lot').render(
                rcontext)
        return result
    @api.multi
    def action_show_detail(self,values):
        print("action_show_detail",values)

    @api.multi
    def print_report(self, report_type):
        self.ensure_one()
        self.compute_data_for_report()
        if report_type == 'xlsx':
            report_name = 'a_f_r.report_product_cost_lot_xlsx'
        else:
            report_name = 'seatek_product_report_lot.report_product_cost_lot'
        res =self.env['ir.actions.report'].search(
            [('report_name', '=', report_name),
             ('report_type', '=', report_type)],
            limit=1).report_action(self, config=False)
        return res
class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    @api.multi
    def write(self,values):
        result=super(StockMoveInherit,self).write(values)
        for res in self:
            if 'state' in values and values.get("state")=="done":
                if res.product_id and res.product_id.tracking=='lot':
                    stock_move_lines=self.env['stock.move.line'].sudo().search([('move_id','=',res.id)])
                    if not res.origin_returned_move_id:
                        if res.picking_id.picking_type_id.code == "incoming":
                            current_cost=0
                            current_qty=0
                            init_cost=0
                            lot_id=False
                            quantity_total=0
                            for stock_move_line in stock_move_lines:
                                if stock_move_line.lot_id:
                                    lot_id=stock_move_line.lot_id
                                    quantity_total = stock_move_line.lot_id.product_qty
                                    init_cost=stock_move_line.lot_id.product_cost
                                    current_qty+=stock_move_line.qty_done
                                    current_cost += stock_move_line.qty_done * res.price_unit
                            if quantity_total > 0 and lot_id:
                                init_qty=quantity_total-current_qty
                                product_cost_current =((init_cost*init_qty) + current_cost) / quantity_total
                                lot_id.write({'product_cost':product_cost_current})
                        elif res.picking_id.picking_type_id.code == "outgoing" and res.sale_line_id:
                            current_sale_qty = 0
                            product_output_qty=0
                            lot_id=False
                            current_sale_total=0
                            product_sale_total=0
                            for stock_move_line in stock_move_lines:
                                if stock_move_line.lot_id:
                                    lot_id = stock_move_line.lot_id
                                    product_output_qty=stock_move_line.lot_id.product_output_qty
                                    product_sale_total=stock_move_line.lot_id.product_sale_total
                                    current_sale_total += (res.sale_line_id.price_unit * stock_move_line.qty_done)
                                    if stock_move_line.qty_done>0:
                                        current_sale_qty+=stock_move_line.qty_done
                            if lot_id:
                                product_sale_total=product_sale_total+current_sale_total
                                product_output_qty=product_output_qty+current_sale_qty
                                lot_id.write({'product_output_qty': product_output_qty,'product_sale_total':product_sale_total})
                    elif res.picking_id.picking_type_id.code == "outgoing" and res.sale_line_id:
                        current_sale_qty = 0
                        product_output_qty = 0
                        lot_id = False
                        current_sale_total = 0
                        product_sale_total = 0
                        for stock_move_line in stock_move_lines:
                            if stock_move_line.lot_id:
                                lot_id = stock_move_line.lot_id
                                product_output_qty = stock_move_line.lot_id.product_output_qty
                                product_sale_total = stock_move_line.lot_id.product_sale_total
                                current_sale_total += (res.sale_line_id.price_unit * stock_move_line.qty_done)
                                if stock_move_line.qty_done > 0:
                                    current_sale_qty += stock_move_line.qty_done
                        if lot_id:
                            product_sale_total = product_sale_total - current_sale_total
                            product_output_qty = product_output_qty - current_sale_qty
                            lot_id.write({'product_output_qty': product_output_qty, 'product_sale_total': product_sale_total})
        return result