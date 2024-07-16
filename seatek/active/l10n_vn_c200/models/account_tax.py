from odoo import models, fields


class AccountTax(models.Model):
    _inherit = 'account.tax'

    analytic = fields.Boolean(default=True)
