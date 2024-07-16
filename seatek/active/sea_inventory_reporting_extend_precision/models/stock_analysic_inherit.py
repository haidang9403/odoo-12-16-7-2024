from odoo import models, fields
from odoo.addons import decimal_precision as dp


class StockAnalysis(models.Model):
    _inherit = 'stock.analysis'

    quantity = fields.Float(string='Quantity', readonly=True, digits=dp.get_precision('Inventory Report'))
