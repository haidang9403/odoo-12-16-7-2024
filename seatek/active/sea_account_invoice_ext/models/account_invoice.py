# -*- coding: utf-8 -*-
from odoo import models, fields, api


class StockMoveLine(models.Model):
    _inherit = "account.invoice"

    def _commit_date(self):
        for invoice in self:
            if invoice.origin:
                sale_objs = self.env['sale.order'].search([('name', '=', invoice.origin)])
                invoice.commitment_date = sale_objs.commitment_date

    commitment_date = fields.Datetime(string='Commitment Date', store=False, compute=_commit_date)
    sea_payment_method = fields.Selection(
        selection=[('cash', 'Tiền Mặt'), ('bank', 'Ngân Hàng'), ('debt', 'Công Nợ'), ],
        string='Payment Method')
