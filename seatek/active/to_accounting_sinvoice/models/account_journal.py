from odoo import models, fields, api


class AccountJournal(models.Model):
    _inherit = 'account.journal'
    _description = 'Viettel S-Invoice Type'

    company_sinvoice_enabled = fields.Boolean(related='company_id.sinvoice_enabled',
                                              help="UI technical field to indicate if the journal's company has S-Invoice enabled.")
    sinvoice_disabled = fields.Boolean(string='S-Invoice Disabled',
                                      help="If checked, S-Invoice integration will be disabled for all the invoices"
                                      " of this journal no matter it is enabled at company level or not.")
    sinvoice_enabled = fields.Boolean(string='S-Invoice Enabled', compute='_compute_sinvoice_enabled', store=True,
                                      help="Technical field to indicate if S-Invoice is enabled for invoices of this journal")
    # account_sinvoice_serial_id = fields.Many2one('account.sinvoice.serial', string='S-Invoice Serial',
    #                                              help="The prefix (e.g. AA/16E, AA/17E, etc) of the invoice number that must be registered with"
    #                                              " S-Invoice priorily. See the Circular No. 39/2014/TT-BTC dated March 31, 2014 by The Ministry"
    #                                              " of Finance of Vietnam.\n"
    #                                              "Note: If this is not set, Odoo will use the one specified in the global Settings")
    # account_sinvoice_template_id = fields.Many2one('account.sinvoice.template', string='S-Invoice Template', help="The template that you have registered with"
    #                                                " S-Invoice for redering your invoices of this template.\n"
    #                                                "Note: If this is not set, Odoo will use the one specified in the global Settings")
    # account_sinvoice_type_id = fields.Many2one('account.sinvoice.type', string='S-Invoice Type', help="The invoice type provided by Viettel S-Invoice."
    #                                            " Leave it empty to use the one specified in the global Settings.\n"
    #                                            "Note: If this is not set, Odoo will use the one specified in the global Settings")
    send_mail_sinvoice_disabled = fields.Boolean(string='Disable Send S-Invoice PDF by email',
                                               help="By default, Odoo will replace it's standard invoice PDF with S-Invoice PDF"
                                               " when S-Invoice is enabled for the invoice. By checking this, you will be able to disable"
                                               " such behaviour for invoices of this journal to fallback to the standard behaviour")
    sinvoice_send_mail_option = fields.Selection([
        ('display', 'Display Version'),
        ('converted', 'Converted Version')
        ],
        default='display', required=True, string='S-Invoice Send Mail/Portal option', help="Choose which version of S-Invoice will be available"
        " for mail sending and download and print from customer portal.")
    sinvoice_item_name = fields.Selection([
        ('invoice_line_name', 'Invoice Line Description'),
        ('invoice_line_product', 'Product Name')],
        default='invoice_line_name', string='S-Invoice Item', required=True, help="This option allows you to choose between product name and invoice line description"
        " for issuing S-Invoice:\n"
        "- Invoice Line Description: the description of Odoo's invoice lines will be sent to S-Invoice system for items name;\n"
        "- Product Name: the name of Odoo's invoice line product will be sent to S-Invoice system for items name;\n")
    sinvoice_item_name_new_line_replacement = fields.Char(string='S-invoice item name new line replacement ', default='; ', trim=False, help="The character(s) with "
                                                          "which the new line character(s) in the S-Invoice item name will be replaced.")   
    sinvoice_item_name_limit = fields.Integer(string='S-invoice item name limit', require=True, default=300, help="Maximum number of characters for S-Invoice item name.")
    
    @api.depends('sinvoice_disabled', 'company_id.sinvoice_enabled')
    def _compute_sinvoice_enabled(self):
        for r in self:
            r.sinvoice_enabled = not r.sinvoice_disabled and r.company_id.sinvoice_enabled

    # def get_sinvoice_template(self):
    #     return self.account_sinvoice_template_id or self.company_id.account_sinvoice_template_id
    #
    # def get_account_sinvoice_type(self):
    #     return self.account_sinvoice_type_id or self.company_id.account_sinvoice_type_id
    #
    # def get_account_sinvoice_serial(self):
    #     return self.account_sinvoice_serial_id or self.company_id.account_sinvoice_serial_id

    # @api.onchange('account_sinvoice_serial_id')
    # def _onchange_account_sinvoice_serial(self):
    #     if self.account_sinvoice_serial_id:
    #         if self.account_sinvoice_serial_id.template_id:
    #             self.account_sinvoice_template_id = self.account_sinvoice_serial_id.template_id
    #
    # @api.onchange('account_sinvoice_template_id')
    # def _onchange_account_sinvoice_template(self):
    #     if self.account_sinvoice_template_id:
    #         if self.account_sinvoice_template_id.type_id:
    #             self.account_sinvoice_type_id = self.account_sinvoice_template_id.type_id
