from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sea_check_customer_for_invoice = fields.Boolean(string='Customer Don\'t Take Invoice')
