from datetime import date
from odoo.addons import decimal_precision as dp
from odoo import models, fields, _, api
from odoo.exceptions import UserError


class InvoiceConsolidation(models.Model):
    _name = 'invoice.consolidation'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Invoice consolidation'

    partner_id = fields.Many2one('res.partner', 'Customer')
    address = fields.Char('Address')
    vat_number = fields.Char('Vat Number', track_visibility='always')
    email = fields.Char('Email')
    date_invoice = fields.Date('Invoice Date', default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', 'Invoice Person', default=lambda self: self.env.user)
    customer_po_name = fields.Char('Customer Name', track_visibility='onchange')
    customer_po_code = fields.Char('PO Code', track_visibility='onchange')

    name = fields.Char(compute='_get_number_invoice')
    number = fields.Char('Number', related='name', store=True, readonly=True, copy=False)
    legal_number = fields.Char('Legal Number')
    # company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)
    company_id = fields.Many2one('res.company', string='Company', change_default=True, required=True, readonly=True,
                                 default=lambda self: self.env['res.company']._company_default_get(
                                     'invoice.consolidation'))
    origin = fields.Char(string='Source Document')
    amount_untaxed = fields.Float('Tax Excluded')
    amount_tax = fields.Float('Tax')
    amount_total = fields.Float('Total')
    currency_id = fields.Many2one('res.currency', 'Currency')
    state = fields.Selection([
        ('open', 'Open'),
        ('issued', 'Issued'),
        ('adjustment', 'Adjustment'),
        ('adjusted', 'Adjusted'),
        ('replacement', 'Replacement'),
        ('replaced', 'Replaced'),
        ('cancel', 'Cancel'),
        ('cancelled', 'Cancelled'),
    ], string='Status', index=True, readonly=True, default='open', copy=False)

    original = fields.Char('Original')
    bill_pos = fields.Char('Bill Pos')
    allow_sign_now = fields.Boolean('Allow signing TS24 Invoice now')
    payment_term = fields.Selection([
        ('tm/ck', 'TM/CK'),
        ('tm', 'Tiền Mặt'),
        ('ck', 'Chuyển Khoản'),
        ('ctcn', 'Cấn trừ công nợ'),
    ], string='Payment Term', index=True, default='tm/ck', copy=False)

    invoice_id = fields.Many2one('account.invoice', 'Invoice ID')
    invoice_link = fields.Char('Invoice Link')
    sinvoice_representation_pdf = fields.Binary(string='Invoice File (PDF)', attachment=True, readonly=True, copy=False,
                                               oldname='invoice_representation_file',
                                               help="The display version of the S-Invoice in PDF format")
    sinvoice_representation_filename_pdf = fields.Char(string='Invoice Filename (PDF)', readonly=True,
                                                      copy=False, oldname='invoice_representation_filename')

    invoice_line_ids = fields.One2many('invoice.line.consolidation', 'invoice_id', string='Invoice Lines')

    sequence_number_next = fields.Char(string='Next Number', compute="_get_sequence_number_next",
                                       inverse="_set_sequence_next")
    sequence_number_next_prefix = fields.Char(string='Next Number Prefix', compute="_get_sequence_prefix")

    team_id = fields.Many2one('crm.team', string='Sales Team', readonly=True)
    sale_channel_id = fields.Many2one('sale.channel', string='Sales Channel', readonly=True)
    email_split = fields.Text('Emails', compute='_compute_email_split', store=True)

    @api.depends('email')
    def _compute_email_split(self):
        for record in self:
            if record.email:
                emails = record.email.replace(';', '\n').split('\n')
                formatted_emails = '\n'.join(email.strip() for email in emails)
                record.email_split = formatted_emails
            else:
                record.email_split = False

    @api.depends('name')
    def _get_number_invoice(self):
        prefix = 'INV/'
        current_year = str(date.today().year)
        for rec in self:
            inv_id = rec.ids
            for o in inv_id:
                number = o
                rec.name = prefix + current_year + '/' + str(f'{number:05}')

    # @api.multi
    # def unlink(self):
    #     if self.state == 'open' and not self.legal_number:
    #         list_origin = []
    #         for rec in self:
    #             list_origin += (str(rec.origin).split())
    #         invoice_ids = self.env['account.invoice'].search([('number', '=', list_origin)])
    #         print(invoice_ids)
    #         if invoice_ids:
    #             for invoice in invoice_ids:
    #                 invoice.sea_consolidation_state = 'not'
    #         return models.Model.unlink(self)
    #     else:
    #         raise UserError(_('Issued invoice cannot be deleted.!'))

    @api.multi
    def unlink(self):
        list_origin = []
        for rec in self:
            if not rec.legal_number:
                list_origin += (str(rec.origin).split())
            else:
                raise UserError(_('Issued invoice cannot be deleted.!'))
        print(list_origin)
        for r in self:
            invoice_ids = r.env['account.invoice'].search([('number', '=', list_origin)])
            print(invoice_ids)
            if invoice_ids:
                for invoice in invoice_ids:
                    # Update merge status
                    if invoice.sea_consolidation_state != 'split':
                        invoice.sea_consolidation_state = 'not'
                    elif invoice.sea_consolidation_state == 'split':
                        quantity_list = []
                        for lines in invoice.invoice_line_ids:
                            for line in r.invoice_line_ids:
                                # Update quantity_split of invoice line
                                if lines.product_id.id == line.product_id.id and lines.price_unit == line.price_unit:
                                    qty_invoice_split_current = lines.quantity_split
                                    lines.quantity_split = qty_invoice_split_current - abs(line.quantity)
                            if lines.quantity_split != 0:
                                quantity_list.append(lines.quantity_split)
                        if not quantity_list:
                            invoice.sea_consolidation_state = 'not'
        return models.Model.unlink(self)


class InvoiceLineConsolidation(models.Model):
    _name = 'invoice.line.consolidation'
    _description = 'Invoice Line consolidation'

    invoice_id = fields.Many2one('invoice.consolidation', string='Invoice Reference')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Char('Description')
    quantity = fields.Float('Quantity', digits=dp.get_precision('Product Unit of Measure'))
    uom_id = fields.Many2one('invoice.unit.of.measure', 'Unit')
    price_unit = fields.Float('Price')
    tax_id = fields.Many2one('account.tax', 'Taxes')
    price_tax = fields.Float('Price Tax')
    price_subtotal = fields.Float('Amount without Tax')
    price_total = fields.Float('Total')
    check_push_ts24 = fields.Boolean('Push TS24')
