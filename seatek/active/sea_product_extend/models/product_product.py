from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    categ_id = fields.Many2one('product.category', 'Product Category', domain="[('company_id','=',company_id)]")
