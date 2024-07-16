from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sea_customer_received = fields.Datetime('Customer Received', readonly=True)

    def _get_customer_receive(self):
        if self.sea_customer_received:
            return self.sea_customer_received
