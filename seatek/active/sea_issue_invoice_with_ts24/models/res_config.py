from odoo import models, fields, api


class SinvoiceConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    sinvoice_enabled = fields.Boolean(related='company_id.sinvoice_enabled', readonly=False)
    sinvoice_mode = fields.Selection(related='company_id.sinvoice_mode', readonly=False)
    sinvoice_start = fields.Date(related='company_id.sinvoice_start', readonly=False)
    sinvoice_api_url = fields.Char(related='company_id.sinvoice_api_url', readonly=False)
    sandbox_sinvoice_api_url = fields.Char(related='company_id.sandbox_sinvoice_api_url', readonly=False)

    sinvoice_guild_issue = fields.Char(related='company_id.sinvoice_guild_issue', readonly=False)

    sinvoice_tenDN = fields.Char(related='company_id.tenDN', readonly=False)
    sinvoice_MatKhau = fields.Char(related='company_id.MatKhau', readonly=False)
    sinvoice_Program = fields.Char(related='company_id.Program', readonly=False)
    sinvoice_serviceID = fields.Char(related='company_id.serviceID', readonly=False)
    sinvoice_MST = fields.Char(related='company_id.MST', readonly=False)
    sinvoice_sKey = fields.Char(related='company_id.sKey', readonly=False)
    sinvoice_userConnect = fields.Char(related='company_id.userConnect', readonly=False)

    sinvoice_api_username = fields.Char(related='company_id.sinvoice_api_username', readonly=False)
    sinvoice_api_password = fields.Char(related='company_id.sinvoice_api_password', readonly=False)
    sinvoice_issue_earliest_invoice_first = fields.Boolean(related='company_id.sinvoice_issue_earliest_invoice_first', readonly=False)
    sinvoice_lock_legal_number = fields.Boolean(related='company_id.sinvoice_lock_legal_number', readonly=False)
    sinvoice_exchange_file_as_attachment = fields.Boolean(related='company_id.sinvoice_exchange_file_as_attachment', readonly=False)
    sinvoice_representation_file_as_attachment = fields.Boolean(related='company_id.sinvoice_representation_file_as_attachment', readonly=False)
    sinvoice_synch_payment_status = fields.Boolean(related='company_id.sinvoice_synch_payment_status', readonly=False)
    sinvoice_conversion_user_id = fields.Many2one(related='company_id.sinvoice_conversion_user_id', readonly=False)

    def button_show_sinvoice_disabled_journals(self):
        self.ensure_one()
        journals = self.env['account.journal'].search([('company_id', '=', self.company_id.id), ('sinvoice_disabled', '=', True)])
        action = self.env.ref('account.action_account_journal_form')
        result = action.read()[0]

        # reset context
        result['context'] = {}
        # choose the view_mode accordingly
        journals_count = len(journals)
        if journals_count != 1:
            result['domain'] = "[('id', 'in', %s)]" % str(journals.ids)
        elif journals_count == 1:
            res = self.env.ref('account.view_account_journal_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = journals.id
        return result

