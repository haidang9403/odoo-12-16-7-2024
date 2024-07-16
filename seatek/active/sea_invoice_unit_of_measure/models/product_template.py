from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.template'

    # sea_unit_of_measure = fields.Many2one('invoice.unit.of.measure', 'Invoice Unit of Measure')
