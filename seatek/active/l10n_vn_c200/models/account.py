from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)


class account_account(models.Model):
    _inherit = 'account.account'

    @api.model
    def remove_acc_999999(self):
        vn_chart_id = self.env.ref('l10n_vn.vn_template').id
        Account = self.env['account.account']
        for company in self.env['res.company'].search([('chart_template_id', '=', vn_chart_id)]):
            acc_999999_id = Account.search([('code', '=', '999999'), ('company_id', '=', company.id)])
            if acc_999999_id:
                acc_999999_id.unlink()

    @api.model
    def _change_user_type(self, new_user_type):
        """
        This method is bypass the Odoo API which is very slow for the case of changing account's account typo
        Change only of difference found.
        """
        if self.user_type_id.id == new_user_type.id:
            return True
        self.env.cr.execute("""
            UPDATE account_move_line SET user_type_id = %s WHERE account_id = %s AND user_type_id != %s;
            UPDATE account_account SET user_type_id = %s, internal_type = %s WHERE id = %s AND user_type_id != %s;
        """, (self.user_type_id.id, self.id, new_user_type.id, new_user_type.id, new_user_type.type, self.id, new_user_type.id))

    def _change_reconcile(self, reconcile):
        """
        @param reconcile: (bool)         
        """
        if self.reconcile == reconcile:
            return True
        self.env.cr.execute("""
            UPDATE account_account SET reconcile = %s WHERE id = %s;
        """, (reconcile, self.id))
        # clear cache
        self.invalidate_cache()
        # recompute corresponding journal items' reconciled and amount_residual and amount_residual_currency
        aml_ids = self.env['account.move.line'].search([('account_id', '=', self.id)])
        _logger.info(_("The Allow Reconcile of the Account %s has been changed from %s to %s. There are %s"
                       " journal items to recompute for `reconciled` and `amount_residual` and `amount_residual_currency`"
                       " to reflex that change") % (self.code, not reconcile, reconcile, len(aml_ids)))
        aml_ids._amount_residual()

    def _sync_account_from_template(self, template_account):
        # synch account user type
        self._change_user_type(template_account.user_type_id)
        # synch reconcile
        self._change_reconcile(template_account.reconcile)

        vals = {}
        if self.name != template_account.name:
            vals['name'] = template_account.name
        if self.code != template_account.code:
            vals['code'] = template_account.code

        tag_ids = self.tag_ids.ids + template_account.tag_ids.ids
        tag_ids = list(set(tag_ids))
        tag_ids.sort()
        if tag_ids and tag_ids != self.tag_ids.ids:
            vals['tag_ids'] = [(6, 0, tag_ids)]
        if self.group_id != template_account.group_id:
            vals['group_id'] = template_account.group_id.id or False
        if not bool(vals):
            return

        # this will be reused in except block to avoid ParseError: "current transaction is aborted, commands ignored until end of transaction block.."
        # if we do query self.code after exception is catched. This is due to the fact that PostgreSQL has started the rollback while we query the data in the same time
        code = self.code
        template_account_code = template_account.code
        try:
            self.write(vals)
            _logger.info(_("Account %s has been synchronized with the template account %s.")
                         % (code, template_account_code))

        except Exception as e:
            _logger.error(_("Could not sync account %s with the template %s. Please try to upgrade this module again.\n%s")
                         % (code, template_account_code, e))

