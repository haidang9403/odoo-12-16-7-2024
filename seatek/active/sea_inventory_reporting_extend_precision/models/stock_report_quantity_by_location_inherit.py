from odoo import fields, models
from odoo.addons import decimal_precision as dp


class StockReportQuantityByLocation(models.TransientModel):
    _inherit = ['stock.report.quantity.by.location']

    quantity = fields.Float(digits=dp.get_precision('Inventory Report'))
