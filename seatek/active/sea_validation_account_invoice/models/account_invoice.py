from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = ['account.invoice']

    @api.multi
    def write(self, vals):
        res = super(AccountInvoice, self).write(vals)
        if self.company_id.sea_sale_order_take_invoice_enable and not self.sea_check_customer_for_invoice:
            customer = self.env['res.partner'].search([('id', '=', self.partner_vat_id.id)])
            if customer and not customer.vat:
                raise UserError(_("VAT Address does not have a Tax code..."))
        return res
