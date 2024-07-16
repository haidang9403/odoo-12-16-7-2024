from odoo import fields, models, api


class ProductPriceList(models.Model):
    _inherit = 'product.pricelist'

    is_default = fields.Boolean('Default PriceList')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)

    @api.onchange('is_default')
    def _onchange_default_pricelist(self):
        if self.is_default:
            pricelists = self.env['product.pricelist'].search([('company_id', '=', self.company_id.id)])
            for pl in pricelists:
                pl.write({
                    'is_default': False
                })
            self.is_default = self.is_default
