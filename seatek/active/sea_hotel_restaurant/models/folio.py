from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Folio(models.Model):
    _name = "sea.folio"
    _description = "Hotel and Restaurant Folio"
    _order = "id"

    @api.model
    def _get_current_datetime(self):
        if "checkin" in self._context:
            return self._context["checkin"]
        else:
            now = datetime.now()
            return now.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    active = fields.Boolean(string='Active', default=True)
    folio_sequence = fields.Char("Folio sequence", readonly=True, default=lambda self: _('New'), index=True)
    folio_name = fields.Char("Folio Name")
    order_date = fields.Datetime(string="Create Date", required=True, default=_get_current_datetime, readonly=True)
    order_ids = fields.One2many("sale.order", "folio_id")
    customer_id = fields.Many2one("res.partner", string='Customer', required=True,
                                  domain="[('property_account_receivable_id', 'not in', [None, False])]")
    state = fields.Selection([
        ('inprogress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Status', default='inprogress', readonly=True)
    sale_person_id = fields.Many2one("res.partner", string='Sale Person', required=True,
                                     default=lambda self: self.env.user.partner_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    branch_id = fields.Many2one('sea.hotel.restaurant.branch', string="Branch",
                                domain=lambda self: self.domain_branch_by_user(), require=True)
    invoice_id = fields.Many2one("account.invoice", "Invoice", copy=False)

    amount_untaxed = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', store=True, readonly=True,
                                     compute='compute_total_price', track_visibility='onchange', track_sequence=5)
    amount_tax = fields.Monetary(string='Taxes', currency_field='currency_id', store=True, readonly=True,
                                 compute='compute_total_price')
    amount_total = fields.Monetary(string='Total', currency_field='currency_id', store=True,
                                   readonly=True, compute='compute_total_price',
                                   track_visibility='always', track_sequence=6)
    total_global_discount = fields.Monetary(string='Discount', currency_field='currency_id',
                                            store=True, readonly=True, compute='compute_total_price',
                                            track_visibility='always')
    global_discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
    ], string="Discount Type",
        default="percent",
        help="If global discount type 'Fixed' has been applied then no partial invoice will be generated for this order.")
    global_folio_discount = fields.Float(
        string='Global Discount', store=True, track_visibility='always')
    note = fields.Char("Terms and conditions")
    ''''''

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)
    order_current = fields.Many2many("sale.order", string="Order Current")

    @api.multi
    def create_invoice_compute(self):
        for rec in self:
            rec.create_invoice = True
            if rec.order_ids:
                for order in rec.order_ids.sudo():
                    if order.invoice_status != 'to invoice':
                        rec.create_invoice = False
                        break

    create_invoice = fields.Boolean("Create invoice", compute='create_invoice_compute')

    '''tính tiền folio lại'''

    @api.multi
    def write(self, vals):
        for folio in self:
            if 'global_discount_type' in vals or 'global_folio_discount' in vals:
                for order in folio.order_ids.sudo():
                    order.global_discount_type = False
                    order.global_order_discount = 0.0
                '''update discount'''
                if folio.global_discount_type or vals.get(
                        'global_discount_type') and folio.global_folio_discount or vals.get('global_folio_discount'):
                    global_folio_discount = folio.global_folio_discount
                    global_discount_type = folio.global_discount_type
                    if 'global_folio_discount' in vals:
                        global_folio_discount = vals.get('global_folio_discount')
                    if 'global_discount_type' in vals:
                        global_discount_type = vals.get('global_discount_type')
                    if global_folio_discount > 0 and global_discount_type == 'percent':
                        for order in folio.order_ids.sudo():
                            if order.global_discount_type != global_discount_type:
                                order.global_discount_type = global_discount_type
                            order.global_order_discount = global_folio_discount

        return super(Folio, self).write(vals)

    @api.multi
    @api.depends('order_ids', 'order_ids.amount_total', 'global_folio_discount', 'global_discount_type')
    def compute_total_price(self):
        for folio in self:
            amount_untaxed = amount_tax = total_global_discount = amount_total = 0.0
            for order in folio.order_ids:
                amount_untaxed += order.amount_untaxed
                amount_tax += order.amount_tax
                total_global_discount += order.total_discount
                amount_total += order.amount_total

            folio.update({
                "amount_untaxed": amount_untaxed,
                "amount_tax": amount_tax,
                "total_global_discount": folio.global_folio_discount + total_global_discount if folio.global_discount_type == 'fixed' else total_global_discount,
                "amount_total": amount_total - folio.global_folio_discount
            })

    @api.model
    def domain_branch_by_user(self):
        user_branch = []
        branches = self.env["sea.hotel.restaurant.branch"].sudo().search([])
        for branch in branches:
            if self.env.user.partner_id.id in [user.partner_id.id for user in branch.user_ids]:
                user_branch.append(branch.id)
        domain = [("id", "in", user_branch)]
        return domain

    @api.model
    def create(self, vals):
        if vals.get('folio_sequence', _('New')) == _('New'):
            # print('test vals company', vals)
            if 'company_id' in vals:
                vals['folio_sequence'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'seatek.folio') or _('New')
            else:
                vals['folio_sequence'] = self.env['ir.sequence'].next_by_code('seatek.folio') or _('New')

        customer_id = self.env["res.partner"].sudo().search([("id", "=", vals["customer_id"])])
        vals["folio_name"] = customer_id.display_name
        if customer_id.phone:
            vals["folio_name"] += " | " + customer_id.phone

        # if "hotel_order_ids" in vals:
        #     for order in vals["hotel_order_ids"]:
        #         order[2]["order_type"] = 'hotel_order'
        #         for order_line in order[2]["order_line"]:
        #             order_line_data = order_line[2]
        #             room = self.env['sea.hotel.room'].sudo().search([("id", "=", order_line_data["room_id"])])
        #             room.write({"status": "occupied", "available": False})
        #
        # if "restaurant_order_ids" in vals:
        #     for order in vals["restaurant_order_ids"]:
        #         order[2]["order_type"] = 'restaurant_order'
        return super(Folio, self).create(vals)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            if self.env.context.get("folio_display_name"):
                folio_name = '[' + rec.folio_sequence + ']  ' + rec.folio_name
            else:
                folio_name = rec.folio_sequence
            result.append((rec.id, folio_name))
        return result

    @api.model
    def _name_search(self, folio_name="folio_sequence", args=None, operator="ilike", limit=100):
        if args is None:
            args = []
        domain = args + ["|", ("folio_sequence", operator, folio_name), ("folio_name", operator, folio_name)]
        return super(Folio, self).search(domain, limit=limit).name_get()

    @api.multi
    def lock_folio(self):
        if not self.order_ids or not self.order_ids.filtered(
                lambda record: record.state not in ['cancel']):
            self.state = "cancel"
            raise ValidationError(_("Can't create invoice when hotel order or restaurant order is empty or cancel"))
            return
        # sale_order_current = self.env['sale.order'].search(
        #     [("id", "in", self.order_ids.ids), ('state', 'not in', ['done', 'cancel'])])
        sale_order_current = self.order_ids.sudo().filtered(
            lambda record: record.state not in ['done', 'cancel'])
        self.order_current = [(6, 0, sale_order_current.ids)]
        for order in sale_order_current:
            if order.order_type and order.state not in ['done', 'cancel']:
                if order.order_type == 'hotel_order':
                    order.lock_hotel_order({'state_folio': True})
                elif order.order_type == 'restaurant_order':
                    order.lock_restaurant_order({'state_folio': True})
        self.state = "done"

    @api.multi
    def unlock_folio(self):
        for order in self.order_current:
            order.write({'state': 'sale'})
        self.state = "inprogress"

    @api.multi
    def view_invoice(self):
        sale_orders = self.env["sale.order"].search(
            [("id", "in", self.order_ids.ids)])
        return sale_orders.action_view_invoice()

    @api.multi
    def invoice_create_and_validate_folio(self, payment_id=False):
        '''tạo invoices'''
        '''phải browse để lấy user đang đăng nhập nếu không sẽ là seaerp(ODOO)'''
        if len(self.order_ids) > 1:
            list_invoice = self.env['sale.order'].browse(self.order_ids.ids).action_invoice_create(final=True)
        else:
            list_invoice = self.env['sale.order'].browse(self.order_ids.ids).action_invoice_create()

        '''Thay đổi:
            + journal_id lấy invoice_journal_id trong POS, branch(branch giành cho folio hoặc khi POS không có)
            
            nếu đúng thì , origin, partner_id, partner_shipping_id,user_id đều không cần đổi
            + account_id lấy trong res_partner (property_account_recievable_id) (không lấy partner có trường này null)
            + origin lấy từ SO (lấy tất cả các tên của SO. Cách nhau bằng ",")
            + partner_id và partner_shipping_id (lấy từ SO đẩy qua invoice)
            + user_id (từ salesperson trong SO, và salesperson trong folio)
        '''
        for rec in self:
            '''lấy journal_id'''
            journal_ids = []
            if payment_id:
                if 'account_payment_id' in payment_id:
                    # journal_id = self.env['account.journal'].sudo().search(
                    #     [('id', '=', payment_id.get('account_payment_id'))], limit=1)
                    journals = payment_id.get('account_payment_id').split(',')
                    for j in journals:
                        value = j.split(':')
                        if value and len(value) == 2:
                            journal_ids.append({'id': value[0], 'value': value[1]})

            '''nếu không có thì chỉ validate => phương thức Ghi Nợ'''
            # if len(journal_ids) == 0:
            #     for i in rec.branch_id.sudo().payment_journal_ids:
            #         journal_ids.append({'id': i.id, 'value': False})
            #         break
            '''thay đổi Discount Type và Global Discount'''
            global_order_discount = 0.0
            global_discount_type = 'fixed'
            if len(rec.order_ids) > 1:
                check = False
                if rec.global_folio_discount and rec.global_discount_type:
                    if rec.global_folio_discount > 0:
                        check = True
                '''tính toán và write và account.invoice'''
                if not check:
                    for order in rec.order_ids:
                        amount_untaxed = amount_tax = 0.0
                        for line in order.order_line:
                            amount_untaxed += line.price_subtotal
                            if order.company_id.tax_calculation_rounding_method == 'round_globally':
                                quantity = 1.0
                                if line.discount_type == 'fixed':
                                    price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
                                else:
                                    quantity = line.product_uom_qty
                                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                                taxes = line.tax_id.compute_all(price, line.order_id.currency_id,
                                                                quantity, product=line.product_id,
                                                                partner=line.order_id.partner_id)
                                amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                            else:
                                amount_tax += line.price_tax

                        IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
                        discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
                        total_amount = amount_untaxed
                        if discTax == 'taxed':
                            total_amount = amount_untaxed + amount_tax
                        if order.global_discount_type == 'fixed':
                            global_discount = order.global_order_discount or 0.0
                        else:
                            global_discount = total_amount * (order.global_order_discount or 0.0) / 100
                        print("global_discount ", order, " : ", global_discount)
                        global_order_discount += global_discount
                else:
                    global_order_discount = rec.global_folio_discount
                    global_discount_type = rec.global_discount_type

                print("discount: ", global_order_discount, "-", global_discount_type)
            for invoice in self.env['account.invoice'].sudo().browse(list_invoice):
                if len(rec.order_ids) > 1:
                    note = rec.note
                    for notes in rec.order_ids:
                        if notes.note:
                            if not note:
                                note = notes.note
                            else:
                                note = note + ', ' + notes.note
                    self.env['account.invoice'].sudo().browse([invoice.id]).comment = note
                    self.env['account.invoice'].sudo().browse(
                        [invoice.id]).global_order_discount = global_order_discount
                    self.env['account.invoice'].sudo().browse([invoice.id]).global_discount_type = global_discount_type

                if rec.branch_id.sudo().invoice_journal_id.id != invoice.journal_id.id:
                    self.env['account.invoice'].sudo().browse(
                        [invoice.id]).journal_id = rec.branch_id.sudo().invoice_journal_id.id
                '''validate'''
                '''phải browse để lấy user đang đăng nhập nếu không sẽ là seaerp(ODOO)'''
                self.env['account.invoice'].browse([invoice.id]).action_invoice_open()

                '''Register Payment'''
                '''account.payment
                create: {
                    'partner_id': 8912, 'amount': 1100000, 'journal_id': 34,
                    data default
                    'currency_id': 23, 'payment_date': '2023-07-22', 'communication': 'INV/2023/230949/89',
                    'payment_type': 'inbound', 'partner_type': 'customer',
                    'payment_difference_handling': 'open', 'writeoff_label': 'Write-Off',
                    'payment_method_id': 1}'''
                if journal_ids and len(journal_ids) > 0:
                    for journal in journal_ids:
                        account_payment = {
                            'invoice_ids': [[6, False, [invoice.id]]],
                            'journal_id': journal['id'],
                            'amount': journal['value'] if journal['value'] else invoice.amount_total,
                            'currency_id': invoice.currency_id.id,
                            'partner_id': invoice.partner_id.id,
                            'payment_date': datetime.now().strftime("%Y-%m-%d"),
                            'communication': invoice.reference,
                            'payment_type': 'inbound',
                            'partner_type': 'customer',
                            'payment_difference_handling': 'open',
                            'writeoff_label': 'Write-Off',
                            'payment_method_id': 1
                        }
                        res = self.env['account.payment'].sudo().create(account_payment)
                        self.env['account.payment'].browse([res.id]).action_validate_invoice_payment()
