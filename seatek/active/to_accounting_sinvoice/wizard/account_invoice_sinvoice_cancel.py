from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_date


class AccountInvoiceSInvoiceCancel(models.TransientModel):
    _name = 'account.invoice.sinvoice.cancel'
    _description = 'S-Invoice Cancellation Wizard'

    invoice_id = fields.Many2one('account.invoice', string='Invoice to Cancel', required=True)
    additional_reference_desc = fields.Char(string='Refenrence', required=True,
                                            help="The name/reference of the agreement between you and your customer for the invoice cancellation.")
    additional_reference_date = fields.Datetime(string='Cancellation Date', required=True,
                                            help="The date and time of the agreement between you and your customer for the invoice cancellation.")

    @api.depends('additional_reference_date', 'invoice_id')
    def _check_additional_reference_date(self):
        for r in self:
            if r.additional_reference_date > fields.Datetime.now():
                raise ValidationError(_("The Cancellation Date must not be in the future"))
            if r.additional_reference_date.date() <= r.invoice_id.sinvoice_invoice_date:
                raise ValidationError(_("The Cancellation Date must not be earlier than the issue date which is %s")
                                      % format_date(self.env, r.invoice_id.sinvoice_invoice_date))

    def action_cancel_sinvoice(self):
        for r in self:
            r.invoice_id.with_context(
                additionalReferenceDesc=r.additional_reference_desc,
                additionalReferenceDate=r.additional_reference_date
                )._cancel_sinvoice()
