from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    customer_tax_enabled = fields.Boolean(string="Customer Tax Enabled", default=False,
                                          help="Uncheck this to disable Customer TAX for the current company.")

    # def get_status_customer_tax(self):
    #     self.ensure_one()
    #     return self.customer_tax_enabled
