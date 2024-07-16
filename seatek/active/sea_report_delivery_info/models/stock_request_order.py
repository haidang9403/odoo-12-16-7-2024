from odoo import models, fields


class StockRequestOrder(models.Model):
    _inherit = 'stock.request.order'

    note = fields.Char('Note')
