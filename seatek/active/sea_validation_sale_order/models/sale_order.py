from odoo import models, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        setting_company = self.env['res.company'].search([('id', '=', values['company_id'])])
        if setting_company.sea_sale_order_take_invoice_enable:
            if not values['sea_check_customer_for_invoice']:
                customer = self.env['res.partner'].search([('id', '=', values['partner_vat_id'])])
                if customer and not customer.vat:
                    raise UserError(_("VAT Address does not have a Tax code..."))
        return res

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        if self.company_id.sea_sale_order_take_invoice_enable and not self.sea_check_customer_for_invoice:
            customer = self.env['res.partner'].search([('id', '=', self.partner_vat_id.id)])
            if customer and not customer.vat:
                raise UserError(_("VAT Address does not have a Tax code..."))
        return res
