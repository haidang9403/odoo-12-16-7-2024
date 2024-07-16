# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    sea_invoice_finished = fields.Boolean('Invoice Finished')
