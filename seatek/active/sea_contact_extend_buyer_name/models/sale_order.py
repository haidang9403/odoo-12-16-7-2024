from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_shipping_id')
    def _onchange_temp_contact(self):
        if self.partner_shipping_id and self.partner_shipping_id.sea_full_name:
            self.sea_temp_contact = self.partner_shipping_id.sea_full_name
        else:
            self.sea_temp_contact = ""
