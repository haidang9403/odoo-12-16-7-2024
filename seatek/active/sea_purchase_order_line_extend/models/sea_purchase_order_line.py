from odoo import models, fields, api, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero
import json


class SeaPuchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sea_hscode = fields.Text(string='HS Code', store=True, default="")

    # ThaiPham - 06/Dec/3023
    transaction_id = fields.Many2one('transaction.type', 'Transaction', domain=[('type', '=', 'incoming')])
    '''dkh add'''
    asset_code = fields.Many2one('account.asset.asset', string='Asset Code',
                                 domain=lambda self: [('company_id', '=', self.env.user.company_id.id)])
    advance_file_id = fields.Many2one('account.payment.res.file', domain="[('company_id', '=', company_id)]",
                                      string="Document Code")
    '''dkh end'''

    @api.onchange('product_id')
    def _onchange_default_transaction_purchase_line(self):
        self.ensure_one()
        if self.product_id:
            self.transaction_id = self.order_id.transaction_id.id
        self.advance_file_id = self.order_id.advance_file_id.id

    @api.multi
    def _prepare_stock_moves(self, picking):
        res = super(SeaPuchaseOrderLine, self)._prepare_stock_moves(picking)
        for re in res:
            if self.transaction_id.id:
                re['sea_transaction_id'] = self.transaction_id.id
                if self.transaction_id.dest_location_id:
                    re['location_dest_id'] = self.transaction_id.dest_location_id.id
            if self.asset_code:
                re['asset_code_id'] = self.asset_code.id
        return res


class SeaPuchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sea_vessel_name = fields.Many2one('res.partner', string='Vessel Name', readonly=True,
                                      states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                              'sale': [('readonly', False)]}, help="Vessel Name",
                                      domain="[('type','=','ship')]")
    '''dkh Add'''
    payment_vendor = fields.Many2one('res.partner', string="Payment Vendor")
    advance_file_id = fields.Many2one('account.payment.res.file', domain="[('company_id', '=', company_id)]",
                                      string="Document Code")

    @api.onchange('partner_id')
    def onchange_partner_id_warning(self):
        self.payment_vendor = self.partner_id
        res = super(SeaPuchaseOrder, self).onchange_partner_id_warning()
        return res

    # ThaiPham - 06/Dec/3023
    transaction_id = fields.Many2one('transaction.type', 'Transaction Type', domain=[('type', '=', 'incoming')])

    @api.onchange('transaction_id')
    def _onchange_update_transaction_purchase_line(self):
        if self.transaction_id:
            if self.order_line:
                for p in self.order_line:
                    p.update({
                        'transaction_id': self.transaction_id
                    })
        if self.advance_file_id:
            if self.order_line:
                for p in self.order_line:
                    p.update({
                        'advance_file_id': self.advance_file_id
                    })

    @api.onchange('picking_type_id')
    def _add_domain_transaction_purchase(self):
        if self.picking_type_id:
            return {'domain': {'transaction_id': [('type', '=', self.picking_type_id.code)]}}

    @api.multi
    def action_view_invoice(self):
        res=super(SeaPuchaseOrder,self).action_view_invoice()
        res.update({'advance_file_id':self.advance_file_id.id})
        return res
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    payment_vendor_id = fields.Many2one('res.partner')
    account_payment_vendor = fields.Many2one('account.account')
    advance_file_id = fields.Many2one('account.payment.res.file', domain="[('company_id', '=', company_id)]",
                                      string="Document Code")
    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.purchase_id.partner_id.id
        '''dkh'''
        if self.purchase_id.payment_vendor:
            self.payment_vendor_id = self.purchase_id.payment_vendor.id
        vendor_ref = self.purchase_id.partner_ref
        if vendor_ref and (not self.reference or (
                vendor_ref + ", " not in self.reference and not self.reference.endswith(vendor_ref))):
            self.reference = ", ".join([self.reference, vendor_ref]) if self.reference else vendor_ref

        if not self.invoice_line_ids:
            # as there's no invoice line yet, we keep the currency of the PO
            self.currency_id = self.purchase_id.currency_id

        new_lines = self.env['account.invoice.line']
        for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
            data = self._prepare_invoice_line_from_po_line(line)
            new_line = new_lines.new(data)
            new_line._set_additional_fields(self)
            new_lines += new_line

        self.invoice_line_ids += new_lines
        self.payment_term_id = self.purchase_id.payment_term_id
        self.env.context = dict(self.env.context, from_purchase_order_change=True)
        self.purchase_id = False
        return {}

    def _prepare_invoice_line_from_po_line(self, line):
        res = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        if line.transaction_id:
            res.update({
                'transaction_id': line.transaction_id.id
            })
        if line.asset_code and line.asset_code.category_id:
            res.update({
                'asset_code': line.asset_code.id
            })
        if line.advance_file_id:
            res.update({
                'advance_file_id': line.advance_file_id.id
            })
        return res

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        account_id = False
        payment_term_id = False
        fiscal_position = False
        bank_id = False
        warning = {}
        domain = {}
        company_id = self.company_id.id
        p = self.partner_id if not company_id else self.partner_id.with_context(force_company=company_id)
        type = self.type or self.env.context.get('type', 'out_invoice')
        if p:
            rec_account = p.property_account_receivable_id
            if self.payment_vendor_id:
                payment_vendor_id = self.payment_vendor_id if not company_id else self.payment_vendor_id.with_context(
                    force_company=company_id)

                pay_account = payment_vendor_id.property_account_payable_id
                '''dkh'''
                if pay_account:
                    self.account_payment_vendor = payment_vendor_id.property_account_payable_id.id
            else:
                pay_account = p.property_account_payable_id

            if not rec_account and not pay_account:
                action = self.env.ref('account.action_account_config')
                msg = _(
                    'Cannot find a chart of accounts for this company, You should configure it. \nPlease go to Account Configuration.')
                raise RedirectWarning(msg, action.id, _('Go to the configuration panel'))

            if type in ('in_invoice', 'in_refund'):
                account_id = pay_account.id
                payment_term_id = p.property_supplier_payment_term_id.id
            else:
                account_id = rec_account.id
                payment_term_id = p.property_payment_term_id.id

            delivery_partner_id = self.get_delivery_partner_id()
            fiscal_position = p.env['account.fiscal.position'].get_fiscal_position(self.partner_id.id,
                                                                                   delivery_id=delivery_partner_id)

            # If partner has no warning, check its company
            if p.invoice_warn == 'no-message' and p.parent_id:
                p = p.parent_id
            if p.invoice_warn and p.invoice_warn != 'no-message':
                # Block if partner only has warning but parent company is blocked
                if p.invoice_warn != 'block' and p.parent_id and p.parent_id.invoice_warn == 'block':
                    p = p.parent_id
                warning = {
                    'title': _("Warning for %s") % p.name,
                    'message': p.invoice_warn_msg
                }
                if p.invoice_warn == 'block':
                    self.partner_id = False

        self.account_id = account_id
        if payment_term_id:
            self.payment_term_id = payment_term_id
        self.date_due = False
        self.fiscal_position_id = fiscal_position

        if type in ('in_invoice', 'out_refund'):
            bank_ids = p.commercial_partner_id.bank_ids
            bank_id = bank_ids[0].id if bank_ids else False
            self.partner_bank_id = bank_id
            domain = {'partner_bank_id': [('id', 'in', bank_ids.ids)]}
        elif type == 'out_invoice':
            domain = {'partner_bank_id': [('partner_id.ref_company_ids', 'in', [self.company_id.id])]}

        res = {}
        if warning:
            res['warning'] = warning
        if domain:
            res['domain'] = domain
        return res

    @api.one
    def _get_outstanding_info_JSON(self):
        self.outstanding_credits_debits_widget = json.dumps(False)
        if self.state == 'open':
            '''dkh'''
            if self.payment_vendor_id:
                partner_id = self.payment_vendor_id
            else:
                partner_id = self.partner_id
            domain = [('account_id', '=', self.account_id.id),
                      ('partner_id', '=', self.env['res.partner']._find_accounting_partner(partner_id).id),
                      ('reconciled', '=', False),
                      ('move_id.state', '=', 'posted'),
                      '|',
                      '&', ('amount_residual_currency', '!=', 0.0), ('currency_id', '!=', None),
                      '&', ('amount_residual_currency', '=', 0.0), '&', ('currency_id', '=', None),
                      ('amount_residual', '!=', 0.0)]
            if self.type in ('out_invoice', 'in_refund'):
                domain.extend([('credit', '>', 0), ('debit', '=', 0)])
                type_payment = _('Outstanding credits')
            else:
                domain.extend([('credit', '=', 0), ('debit', '>', 0)])
                type_payment = _('Outstanding debits')
            info = {'title': '', 'outstanding': True, 'content': [], 'invoice_id': self.id}
            lines = self.env['account.move.line'].search(domain)
            currency_id = self.currency_id
            if len(lines) != 0:
                for line in lines:
                    # get the outstanding residual value in invoice currency
                    if line.currency_id and line.currency_id == self.currency_id:
                        amount_to_show = abs(line.amount_residual_currency)
                    else:
                        currency = line.company_id.currency_id
                        amount_to_show = currency._convert(abs(line.amount_residual), self.currency_id, self.company_id,
                                                           line.date or fields.Date.today())
                    if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
                        continue
                    if line.ref:
                        title = '%s : %s' % (line.move_id.name, line.ref)
                    else:
                        title = line.move_id.name
                    info['content'].append({
                        'journal_name': line.ref or line.move_id.name,
                        'title': title,
                        'amount': amount_to_show,
                        'currency': currency_id.symbol,
                        'id': line.id,
                        'position': currency_id.position,
                        'digits': [69, self.currency_id.decimal_places],
                    })
                info['title'] = type_payment
                self.outstanding_credits_debits_widget = json.dumps(info)
                self.has_outstanding = True


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    @api.depends('line_ids.partner_id')
    def _compute_partner_id(self):
        have_payment_vendor = False
        for move in self:
            partner = move.line_ids.mapped('partner_id')
            move.partner_id = partner.id if len(partner) == 1 else False
            for line in move.line_ids:
                if line.invoice_id.payment_vendor_id and line.invoice_id.partner_id:
                    move.partner_id = line.invoice_id.partner_id.id
                    break


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model_create_multi
    def create(self, vals_list):
        """ :context's key `check_move_validity`: check data consistency after move line creation. Eg. set to false to disable verification that the move
                debit-credit == 0 while creating the move lines composing the move.
        """
        for vals in vals_list:
            if 'invoice_id' in vals:
                account = self.env['account.account'].browse(vals['account_id'])
                invoice_id = self.env['account.invoice'].search([('id', '=', vals['invoice_id'])])
                if account and invoice_id.account_payment_vendor:
                    if account.id == invoice_id.account_payment_vendor.id:
                        if invoice_id.payment_vendor_id:
                            vals.update({'partner_id': invoice_id.payment_vendor_id.id})
        return super(AccountMoveLine, self).create(vals_list)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def create(self, vals):
        res = super(AccountPayment, self).create(vals)
        return res

    @api.model
    def default_get(self, fields):
        rec = super(AccountPayment, self).default_get(fields)
        invoice_defaults = self.resolve_2many_commands('invoice_ids', rec.get('invoice_ids'))
        if invoice_defaults and len(invoice_defaults) == 1:
            invoice = invoice_defaults[0]
            if 'payment_vendor_id' in invoice:
                if invoice.get('payment_vendor_id'):
                    rec['partner_id'] = invoice['payment_vendor_id'][0]
        return rec

