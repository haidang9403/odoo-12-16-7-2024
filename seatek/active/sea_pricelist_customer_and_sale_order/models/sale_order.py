from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_pricelist_customer_sale(self):
        if self.partner_id:
            self.pricelist_id = self.partner_id.property_product_pricelist

    @api.onchange('pricelist_id')
    def _onchange_pricelist_to_customer(self):
        if self.pricelist_id and self.partner_id:
            partner = self.env['res.partner'].browse(self.partner_id.id)
            partner.write({
                'pricelist_id': self.pricelist_id.id
            })
