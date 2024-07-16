from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sea_is_asset = fields.Boolean('Is Asset')
