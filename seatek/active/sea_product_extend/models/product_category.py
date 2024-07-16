from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company', string='Company')
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env['res.company']._company_default_get())
