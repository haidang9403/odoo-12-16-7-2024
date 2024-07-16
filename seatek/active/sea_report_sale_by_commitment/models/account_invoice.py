from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sea_invoice_finished = fields.Boolean('Invoice Finished')
