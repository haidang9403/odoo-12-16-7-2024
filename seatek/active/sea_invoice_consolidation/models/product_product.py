from odoo import models, fields


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sea_pos_check_drinks = fields.Boolean('Is Drinks')
