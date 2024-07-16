from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    categ_id = fields.Many2one('product.category', 'Product Category', domain="[('company_id','=',company_id)]")
