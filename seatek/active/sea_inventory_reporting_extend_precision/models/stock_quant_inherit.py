from odoo import fields, models
from odoo.addons import decimal_precision as dp


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    quantity = fields.Float(
        'Quantity',
        digits=dp.get_precision('Inventory Report'),
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True, required=True, oldname='qty')
    reserved_quantity = fields.Float(
        'Reserved Quantity',
        default=0.0,
        digits=dp.get_precision('Inventory Report'),
        help='Quantity of reserved products in this quant, in the default unit of measure of the product',
        readonly=True, required=True)
