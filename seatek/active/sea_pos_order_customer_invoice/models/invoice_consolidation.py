from odoo import fields, models
from datetime import date


class InvoiceConsolidation(models.Model):
    _inherit = 'invoice.consolidation'

    pos_auto_issue_invoice_customer = fields.Boolean('POS Auto Invoice Customer')
    pos_auto_issue_invoice_not_customer = fields.Boolean('POS Auto Invoice Not Customer')
    invoice_pos_branch_id = fields.Many2one('pos.branch', 'Branch')

    def cron_pos_issue_invoice_customer(self):
        domain = [('date_invoice', '=', date.today()), ('pos_auto_issue_invoice_customer', '!=', False),
                  ('state', '=', 'open')]
        for invoice in self.env['invoice.consolidation'].search(domain):
            if invoice:
                invoice._issue_invoice()

    def cron_pos_issue_invoice_not_customer(self):
        domain = [('date_invoice', '=', date.today()), ('pos_auto_issue_invoice_not_customer', '!=', False),
                  ('state', '=', 'open')]
        for invoice in self.env['invoice.consolidation'].search(domain):
            if invoice:
                invoice._issue_invoice()
