from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pricelist_id = fields.Many2one('product.pricelist', 'Price List',
                                   default=lambda self: self.env['product.pricelist'].search(
                                       [('is_default', '=', True)], limit=1))

    @api.onchange('property_product_pricelist')
    def _onchange_product_pricelist(self):
        self.pricelist_id = self.property_product_pricelist

    def _compute_product_pricelist(self):
        for p in self:
            p.property_product_pricelist = p.pricelist_id

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if 'property_product_pricelist' in vals:
            partner.property_product_pricelist = vals['property_product_pricelist']
            partner.pricelist_id = vals['property_product_pricelist']
        return partner

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if 'property_product_pricelist' in vals and 'name' in vals:
            for partner in self:
                partner.property_product_pricelist = vals['property_product_pricelist']
                partner.pricelist_id = vals['property_product_pricelist']
        return res
