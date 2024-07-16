# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta

import pytz

from odoo import fields, models, tools, api
import odoo.addons.decimal_precision as dp
from odoo.addons.mail.models.mail_template import format_tz
from odoo.fields import Datetime

class AssignOrder(models.TransientModel):
    _name = 'seatek.assign.order'
    _description = 'Danh sách những đơn đang giữ hàng nhưng chưa gửi'

    name = fields.Char('Name', default='Danh sách những đơn đang giữ hàng nhưng chưa gửi')
    user_id = fields.Many2one('res.users')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id)

    assign_order_line_ids = fields.One2many('seatek.assign.order.line', 'assign_oder_id', "Details")

    @api.model
    def action_open_report(self):
        action_values = self.env.ref('seatek_assign_order_report.action_assign_order_report_view').read()[0]
        res_id = self.env['seatek.assign.order'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not res_id:
            res_id = self.env['seatek.assign.order'].create({'user_id': self.env.user.id})
        res_id.action_remove_data_assign_order_report_line()
        res_id.action_get_assign_order_report_data()
        action_values.update({'res_id': res_id.id})
        action = action_values
        return action

    def action_remove_data_assign_order_report_line(self):
        return self.assign_order_line_ids.unlink()

    def action_get_assign_order_report_data(self):
        self.action_remove_data_assign_order_report_line()
        # Case 1: stock move line from stock picking
        stock_picking_ids = self.env['stock.picking'].sudo().search([
            ('company_id', '=', self.env.user.company_id.id),
            ('state', '=', 'assigned')
        ]).mapped('id')
        stock_move_line_searchs = self.env['stock.move.line'].sudo().search([
            ('company_id', '=', self.env.user.company_id.id),
            ('product_uom_qty', '>', 0),
            ('picking_id', 'in', stock_picking_ids)
        ])
        if len(stock_move_line_searchs) > 0:
            for stock_move_line in stock_move_line_searchs:
                val = {
                    'assign_oder_id': self.id,
                    'date': stock_move_line.date,
                    'ref': stock_move_line.reference,
                    'product_id': stock_move_line.product_id.id,
                    'location_from': stock_move_line.location_id.id,
                    'location_to': stock_move_line.location_dest_id.id,
                    'reserve_qty': stock_move_line.product_uom_qty,
                }
                if stock_move_line.picking_id.sale_id:
                    val['sale_id'] = stock_move_line.picking_id.origin
                self.env['seatek.assign.order.line'].create(val)

class AssignOrderLine(models.TransientModel):
    _name = 'seatek.assign.order.line'
    _description = 'Chi tiết danh sách những đơn đang giữ hàng nhưng chưa gửi'

    assign_oder_id = fields.Many2one('seatek.assign.order', "Assign Order Report ID")
    date = fields.Datetime('Date')
    ref = fields.Char('Reference')
    product_id = fields.Many2one('product.product', 'Product')
    sale_id = fields.Char('Sale Order')
    location_from = fields.Many2one('stock.location', 'From')
    location_to = fields.Many2one('stock.location', 'To')
    reserve_qty = fields.Float('Reserve Qty', digits=(16, 3))
    # inti_qty = fields.Float('Initial Qty')
    # Sale_Order
    # Pos_Order
    # Manufacturing_Order

    @api.model
    def action_open_report(self):
        assign_order_report = self.env['seatek.assign.order'].search([('user_id', '=', self.env.user.id)], limit=1)
        if not assign_order_report:
            assign_order_report = self.env['seatek.assign.order'].create({'user_id': self.env.user.id})
        self.delete_all_data()
        assign_order_report.action_get_assign_order_report_data()
        action_values = self.env.ref('seatek_assign_order_report.action_assign_oder_report_line_view_tree').read()[0]
        return action_values

    def delete_all_data(self):
        all_records = self.env['seatek.assign.order.line'].search([])
        for record in all_records:
            record.unlink()