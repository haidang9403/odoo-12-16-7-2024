# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    symbol_invoice = fields.Char('Invoice Symbol')
    supplier_invoice_number = fields.Char('Invoice Number')
    supplier_invoice_date = fields.Date('Invoice Date')
    supplier_vat = fields.Char('VAT')
