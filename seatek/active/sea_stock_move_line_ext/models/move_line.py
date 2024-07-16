# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    origin = fields.Char(related='move_id.origin', string='Source', store=False)
    receipt_pos = fields.Char(string='Pos Receipt', compute='_get_pos_receipt')

    @api.multi
    @api.depends()
    def _get_pos_receipt(self):
        for move in self:
            if move.move_id.picking_id.pos_order_id and move.move_id.picking_id.pos_order_id.pos_reference:
                move.receipt_pos = move.move_id.picking_id.pos_order_id.pos_reference
