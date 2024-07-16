from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sea_customer_get_invoice = fields.Boolean('Customer Get Invoice')
    sea_pos_auto_push_invoice_to_issue = fields.Boolean('Auto Push Invoice')
    sea_pos_auto_issue_invoice = fields.Boolean('Auto Issue Invoice')
