from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    sea_user_department_ids = fields.Many2many(
        'sales.department',
        'sea_user_sales_department',
        'user_id',
        'sales_department_id',
        'Allow Sales Department'
    )
