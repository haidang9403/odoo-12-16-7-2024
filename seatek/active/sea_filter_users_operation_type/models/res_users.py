from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    sea_user_operation_type_ids = fields.Many2many(
        'stock.picking.type',
        'sea_user_operation_type',
        'user_id',
        'picking_type_id',
        'Allow Operation Type'
    )

    sea_user_warehouse_ids = fields.Many2many(
        'stock.warehouse',
        'sea_user_warehouse',
        'user_id',
        'warehouse_id',
        'Allow Warehouse'
    )
