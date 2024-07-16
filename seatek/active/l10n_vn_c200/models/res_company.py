from odoo import models, api
import logging
_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def fix_account_internal_type(self):
        """
        Previous changes in user type did not change the account internal_type.
        This is for fixing
        """
        self.env.cr.execute("""
        UPDATE account_account AS a
        SET internal_type = (SELECT type FROM account_account_type WHERE id = a.user_type_id LIMIT 1)        
        WHERE internal_type != (SELECT type FROM account_account_type WHERE id = a.user_type_id LIMIT 1)
        """)

    @api.model
    def enable_tax_analytic(self):
        Tax = self.env['account.tax']
        vn_chart_id = self.env.ref('l10n_vn.vn_template').id
        vn_companies = self.search([('chart_template_id', '=', vn_chart_id)])
        existing_taxes = Tax.with_context(active_test=False).search([('company_id', 'in', vn_companies.ids), ('analytic', '=', False)])
        existing_taxes.write({'analytic': True})

    @api.model
    def fix_vietnam_coa(self):
        """
        This method is safe for calling multiple times.
        It may take long time for the first run, depending on how large the number of affected journal items is.
        The second time and on may cost a few seconds only.
        """
        vn_chart_id = self.env.ref('l10n_vn.vn_template').id
        Account = self.env['account.account']
        Tax = self.env['account.tax']
        template_taxes = self.env['account.tax.template'].search([('chart_template_id', '=', vn_chart_id)])
        # prefetching
        template_taxes.read(['id', 'name', 'type_tax_use', 'amount_type', 'amount', 'description', 'account_id', 'refund_account_id', 'tag_ids', 'tax_group_id'])

        template_accounts = self.env['account.account.template'].search([('chart_template_id', '=', vn_chart_id)])
        template_accounts.read(['code'])

        for company in self.search([('chart_template_id', '=', vn_chart_id)]):
            # FIX ACCOUNTS
            accounts = Account.search([('company_id', '=', company.id)])
            accounts.read(['code'])
            accounts_codes = accounts.mapped('code')

            for account in accounts:
                # sync accounts with their templates
                for template_account in template_accounts:
                    if account.code == template_account.code:
                        account._sync_account_from_template(template_account)
                if not account.group_id and account.code[0] == '1' or account.code[0] == '9':
                    account.write({
                        'group_id': self.env.ref('l10n_vn_c200.acc_group_%s' % account.code[0]).id
                        })

            for template_account in template_accounts:
                if template_account.code not in accounts_codes:
                    vals = {
                         'name': template_account.name,
                         'code': template_account.code,
                         'user_type_id': template_account.user_type_id.id,
                         'company_id': company.id,
                         'reconcile': template_account.reconcile,
                         }
                    if template_account.tag_ids.ids:
                        vals['tag_ids'] = [(6, 0, template_account.tag_ids.ids)]
                    if template_account.group_id:
                        vals['group_id'] = template_account.group_id.id

                    Account.create(vals)

            # FIX TAXES
            existing_taxes = Tax.with_context(active_test=False).search([('company_id', '=', company.id)])
            # prefetching
            existing_taxes.read(['name'])

            excl_template_tax_ids = []
            for template_tax in template_taxes:
                for existing_tax in existing_taxes:
                    if existing_tax.name == template_tax.name:
                        excl_template_tax_ids.append(template_tax.id)

            for template_tax in template_taxes:
                if template_tax.id not in excl_template_tax_ids:
                    data = {
                        'name': template_tax.name,
                        'type_tax_use': template_tax.type_tax_use,
                        'amount_type': template_tax.amount_type,
                        'amount': template_tax.amount,
                        'description': template_tax.description,
                        'account_id': Account.search([('code', '=', template_tax.account_id.code)], limit=1).id,
                        'refund_account_id': Account.search([('code', '=', template_tax.refund_account_id.code)], limit=1).id,
                        'tag_ids': [(6, 0, template_tax.tag_ids.ids)],
                        'company_id': company.id,
                        }
                    if template_tax.tax_group_id:
                        data['tax_group_id'] = template_tax.tax_group_id.id
                    Tax.create(data)

