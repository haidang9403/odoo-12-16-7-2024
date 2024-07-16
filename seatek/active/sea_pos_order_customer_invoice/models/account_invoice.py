from odoo import models
from datetime import date


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def cron_push_invoice_to_issue(self):
        domain = [('date_invoice', '=', date.today()), ('state', 'not in', ['draft', 'cancel']),
                  ('sea_consolidation_state', '=', 'not'), ('pos_config_id', '!=', False),
                  ('sea_check_customer_for_invoice', '!=', True)]
        for invoice in self.env['account.invoice'].search(domain):
            if invoice.pos_config_id.sea_pos_auto_push_invoice_to_issue:
                invoice.push_invoice_to_issue()
                invoice_issue = invoice.invoice_consolidation_id
                if invoice_issue.state == 'open':
                    invoice_issue.update({
                        'company_id': invoice.company_id,
                        'invoice_pos_branch_id': invoice.pos_order_id.pos_branch_id.id,
                        'pos_auto_issue_invoice_customer': True,
                    })
                else:
                    invoice_issue.update({
                        'company_id': invoice.company_id,
                        'invoice_pos_branch_id': invoice.pos_order_id.pos_branch_id.id,
                        'pos_auto_issue_invoice_customer': False,
                    })

    def cron_pos_consolidation_invoice(self):
        if self.get_invoice():
            invoices = self.get_invoice()
            branch_pos = []
            invoice_pos = []
            for pos in invoices:
                if pos.pos_config_id.sea_pos_auto_push_invoice_to_issue:
                    if pos.sea_check_customer_for_invoice:
                        if not pos.pos_order_id.is_return:
                            branch_pos.append(pos.pos_order_id.pos_branch_id)
                            invoice_pos.append(pos)
                        if pos.pos_order_id.is_return:
                            if pos.pos_order_id.return_order_id.date_order.strftime(
                                    "%d") == pos.pos_order_id.date_order.strftime("%d"):
                                invoice_pos.append(pos)
            if branch_pos:
                for branch in set(branch_pos):
                    invoice_branch_pos = []
                    for inv in invoice_pos:
                        if branch.id == inv.pos_order_id.pos_branch_id.id:
                            invoice_branch_pos.append(inv.id)
                    consolidation = self.env['account.invoice'].browse(invoice_branch_pos)
                    consolidation.invoice_consolidation()
                    get_invoice_issue = self.env['account.invoice'].search([('id', 'in', invoice_branch_pos)], limit=1)
                    invoice_issue = get_invoice_issue.invoice_consolidation_id
                    invoice_issue.update({
                        'company_id': get_invoice_issue.company_id,
                        'invoice_pos_branch_id': branch.id,
                        'pos_auto_issue_invoice_not_customer': True,
                    })

    def get_invoice(self):
        domain = [('date_invoice', '=', date.today()), ('state', 'not in', ['draft', 'cancel']),
                  ('sea_consolidation_state', '=', 'not')]
        return self.env['account.invoice'].search(domain)
