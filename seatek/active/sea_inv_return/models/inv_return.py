# -*- coding: utf-8 -*-
from odoo import models, fields


class SeaStockMove1(models.Model):
    _inherit = "stock.move"

    to_refund = fields.Boolean(string="To Refund (update SO/PO)", default=True, copy=False,
                               help='Trigger a decrease of the delivered/received quantity in the associated Sale Order/Purchase Order')


class SeaStockReturnPicking1(models.TransientModel):
    _inherit = "stock.return.picking.line"

    to_refund = fields.Boolean(string="To Refund (update SO/PO)", default=True,
                               help='Trigger a decrease of the delivered/received quantity in the associated Sale Order/Purchase Order')
