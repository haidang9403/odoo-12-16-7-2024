from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sea_pos_check_drinks = fields.Boolean('Is Drinks')
