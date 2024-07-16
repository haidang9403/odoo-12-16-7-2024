from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    print_product_label = fields.Boolean(related="product_tmpl_id.print_product_label", readonly=False)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    print_product_label = fields.Boolean(string="Print Product Label")
