from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def _get_sinvoices_to_issue_domain(self):
        domain = [
            ('state', '!=', 'cancel'),
            ('type', 'in', ['out_invoice', 'out_refund']),
            ('sinvoice_state', '=', 'not_issued'),
            ('date_invoice', '<=', fields.Date.today()),
            ('journal_id', '=', self.id), ]
        if self.company_id.sinvoice_start:
            domain.append(('date_invoice', '>', self.company_id.sinvoice_start))
        return domain

    def _get_sinvoices_to_issue(self):
        return self.env['account.invoice'].search(self._get_sinvoices_to_issue_domain())

    def get_journal_dashboard_datas(self):
        action = super(AccountJournal, self).get_journal_dashboard_datas()
        sinvoice_to_issue = self._get_sinvoices_to_issue()
        action.update({
            'sinvoice_to_issue_count': len(sinvoice_to_issue),
            'sinvoice_enabled': self.sinvoice_enabled
            })
        return action

    def action_open_sinvoice_to_issue_action(self):
        self.ensure_one()
        action = self.env.ref('account.action_invoice_tree1')
        result = action.read()[0]

        # reset context
        result['context'] = {}
        # choose the view_mode accordingly
        sinvoice_to_issue = self._get_sinvoices_to_issue()
        sinvoice_to_issue_count = len(sinvoice_to_issue)
        if sinvoice_to_issue_count != 1:
            result['domain'] = self._get_sinvoices_to_issue_domain()
        elif sinvoice_to_issue_count == 1:
            res = self.env.ref('account.invoice_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = sinvoice_to_issue.id
        return result

