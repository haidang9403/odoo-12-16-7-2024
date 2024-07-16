from odoo import models, fields, _
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    legal_number = fields.Char(string='Legal Number', oldname='x_invoice_number', track_visibility='onchange', copy=False,
                               help="The number for legal identification purpose")
    old_number = fields.Char(string='Old Number', readonly=True,
                             help="This field is to store the old number of the invoice after it was changed")

    def action_synch_legal_number(self):
        if not self.env.user.has_group('account.group_account_manager'):
            manager_group = self.env.ref('account.group_account_manager')
            raise UserError(_("Only the users in the group %s can carry out this action. Please ask them for help if you still need to get this done.")
                               % manager_group.display_name)
        for r in self.filtered(lambda inv: inv.legal_number != inv.number):
            r.write({
                'old_number': r.number,
                'number': r.legal_number,
                })
            r.message_post(body=_("The number of invoice %s has been changed to %s due to Legal Number Synchorization action!") % (r.old_number, r.number))
