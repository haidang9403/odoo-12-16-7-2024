from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_payment_method_with_contact(self):
        if self.partner_id and self.partner_id.sea_payment_method:
            self.sea_payment_method = self.partner_id.sea_payment_method
        else:
            self.sea_payment_method = ""
