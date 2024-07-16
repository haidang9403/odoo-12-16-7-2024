import requests, json
# from pylint.checkers.typecheck import _
from requests.auth import HTTPBasicAuth

from odoo import models, fields, api
from odoo.exceptions import ValidationError

SANDBOX_SINVOICE_API_URL = 'https://www.ts24.com.vn/xhdapi/XHD'
SINVOICE_API_URL = 'https://www.ts24.com.vn/xhdapi/XHD'
SINVOICE_STATUS_PATH = '/InvoiceAPI/InvoiceUtilsWS/getProvidesStatusUsingInvoice'

# SINVOICE_CREATE_PATH = '/CreateInvoice_01GTKT_TT78?'
SINVOICE_CREATE_PATH = '/CreateInvoice_01GTKT_TT78_V2?'
# SINVOICE_EDIT_PATH = '/EditInvoice_01GTKT_TT78?'
SINVOICE_EDIT_PATH = '/EditInvoice_01GTKT_TT78_V2?'
SINVOICE_ADJUSTMENT_PATH = '/AdjustedInvoice_01GTKT_TT78?'
SINVOICE_REPLACEMENT_PATH = '/ReplaceInvoice_01GTKT_TT78?'
SINVOICE_CANCEL_PATH = 'DeleteInvoice_01GTKT_TT78?'
SINVOICE_PRESENTATION_FILE_PATH = '/GetFilesInvoice?'
# SINVOICE_SIGN_INVOICE_PATH = '/SignInvoice_01GTKT_TT78?'
SINVOICE_SIGN_INVOICE_PATH = '/SignInvoice_01GTKT_TT78_V2?'
SINVOICE_SEARCH_INVOICE_PATH = '/searchInvoice?'
SINVOICE_LOOK_UP_INVOICE_PATH = '/traCuuKetQuaHoaDon_01GTKT_TT78?'
SINVOICE_SEND_EMAIL_INVOICE_PATH = '/SendMailInvoice_01GTKT_TT78?'

SINVOICE_UPDATE_PAYMENT_STATUS_PATH = '/InvoiceAPI/InvoiceWS/updatePaymentStatus'
SINVOICE_CANCEL_PAYMENT_STATUS_PATH = '/InvoiceAPI/InvoiceWS/cancelPaymentStatus'
SINVOICE_EXCHANGE_FILE_PATH = '/InvoiceAPI/InvoiceWS/createExchangeInvoiceFile'
# SINVOICE_CANCEL_PATH = '/InvoiceAPI/InvoiceWS/cancelTransactionInvoice'


class ResCompany(models.Model):
    _inherit = 'res.company'

    sinvoice_enabled = fields.Boolean(string='S-Invoice Enabled', default=False,
                                      help="Uncheck this to disable S-Invoice for the current company.")
    sinvoice_mode = fields.Selection([
        ('sandbox', 'Sandbox'), ('production', 'Production')], default='sandbox', copy=False, required=True,
        string='S-Invoice Mode', help="Choose Sandbox mode for testing before switch it to Production")
    sinvoice_start = fields.Date(string='S-Invoice Start Date',
                                 help="The date from which your company announced the start of using S-Invoice.")
    sinvoice_api_url = fields.Char(string='API URL', compute='_compute_sinvoice_api_url',
                                   inverse='_set_sinvoice_api_url')
    sandbox_sinvoice_api_url = fields.Char(string='Sandbox API URL', compute='_compute_sandbox_sinvoice_api_url',
                                           inverse='_set_sandbox_sinvoice_api_url')
    sinvoice_issue_earliest_invoice_first = fields.Boolean(string='Issue Earlier Invoice First', default=True,
                                                           help="If checked, during issuing a new S-Invoice, Odoo will check to validate if there is an"
                                                                " existing invoice the invoice date of which is earlier than the current one's. If there is,"
                                                                " Odoo will stop you from issuing S-Invoice for the current one and ask you to do for the"
                                                                " earlier one priorily.")
    sinvoice_lock_legal_number = fields.Boolean(string='Lock Legal Number', default=True,
                                                help="If checked, invoice's legal number will be locked after S-Invoice will be issued.")
    sinvoice_exchange_file_as_attachment = fields.Boolean(string='Attach Invoice Converted Version', default=False,
                                                          help="If checked, when generating the converted version of the S-Invoice,"
                                                               " Odoo will also generate a corresponding attachment and attach it to the invoice.")
    sinvoice_representation_file_as_attachment = fields.Boolean(string='Attach Invoice Repensentation Version',
                                                                default=False,
                                                                help="If checked, when generating the representation version of the S-Invoice,"
                                                                     " Odoo will also generate a corresponding attachment and attach it to the invoice.")
    sinvoice_synch_payment_status = fields.Boolean(string='Payment Status Synchronization', default=True,
                                                   help="If checked, having invoice paid in Odoo will also get the sinvoice paid. Having a paid invoice"
                                                        " reopened in Odoo will also get the sinvoice reopened accordingly.")
    sinvoice_conversion_user_id = fields.Many2one('res.users', string='SInvoice Force Conversion User',
                                                  help="If specified, during conversion, Odoo will use this user as the conversion user"
                                                       " instead the one who actually converts the invoice.")

    # TODO: remove sinvoice_api_invoice_template in v13. It is here for backward
    # compatibility with existing databases before account_sinvoice_type_id was added
    sinvoice_api_invoice_template = fields.Char('S-Invoice Invoice Template Code', copy=False)
    # TODO: remove sinvoice_api_invoice_type in v13. It is here for backward
    # compatibility with existing databases before account_sinvoice_type_id was added
    sinvoice_api_invoice_type = fields.Char('S-Invoice Invoice Type', copy=False)

    # Start //---
    sinvoice_guild_issue = fields.Char('S-Invoice Guild Issue', copy=False)

    tenDN = fields.Char('tenDN', copy=False)
    MatKhau = fields.Char('MatKhau', copy=False)
    Program = fields.Char('Program', copy=False)
    serviceID = fields.Char('serviceID', copy=False)
    MST = fields.Char('MST', copy=False)
    sKey = fields.Char('sKey', copy=False)
    userConnect = fields.Char('userConnect', copy=False)
    # End //-->

    sinvoice_api_username = fields.Char('S-Invoice username', copy=False)
    sinvoice_api_password = fields.Char('S-Invoice password', copy=False)

    # Start //---
    def get_sinvoice_guild_issue_str(self):
        self.ensure_one()
        return self.sinvoice_guild_issue

    def get_sinvoice_api_params_str(self):
        self.ensure_one()
        return 'tenDN='+self.tenDN + '&MatKhau=' + self.MatKhau + '&Program=' + self.Program + '&serviceID='\
               + self.serviceID + '&MST=' + self.MST + '&sKey=' + self.sKey + '&userConnect=' + self.userConnect

    # End //--->

    def get_sinvoice_auth_str(self):
        self.ensure_one()
        return HTTPBasicAuth(self.sinvoice_api_username, self.sinvoice_api_password)

    def _get_sinvoice_api_url(self):
        """
        Return S-Invoice API URL according to the S-Invoice Mode which is either sandbox or production
        """
        self.ensure_one()
        return self.sinvoice_api_url if self.sinvoice_mode == 'production' else self.sandbox_sinvoice_api_url

    def get_sinvoice_create_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_CREATE_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_edit_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_EDIT_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_adjustment_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_ADJUSTMENT_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_replacement_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_REPLACEMENT_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_cancel_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_CANCEL_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_search_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_SEARCH_INVOICE_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_look_up_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_LOOK_UP_INVOICE_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_send_email_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_SEND_EMAIL_INVOICE_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_sign_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_SIGN_INVOICE_PATH, self.get_sinvoice_api_params_str())

    def get_sinvoice_update_payment_status_url(self):
        self.ensure_one()
        return '%s%s' % (self._get_sinvoice_api_url(), SINVOICE_UPDATE_PAYMENT_STATUS_PATH)

    def get_sinvoice_cancel_payment_status_url(self):
        self.ensure_one()
        return '%s%s' % (self._get_sinvoice_api_url(), SINVOICE_CANCEL_PAYMENT_STATUS_PATH)

    # def get_sinvoice_cancel_url(self):
    #     self.ensure_one()
    #     return '%s%s' % (self._get_sinvoice_api_url(), SINVOICE_CANCEL_PATH)

    def get_sinvoice_exchange_file_url(self):
        self.ensure_one()
        return '%s%s' % (self._get_sinvoice_api_url(), SINVOICE_EXCHANGE_FILE_PATH)

    def get_sinvoice_presentation_file_url(self):
        self.ensure_one()
        return '%s%s%s' % (self._get_sinvoice_api_url(), SINVOICE_PRESENTATION_FILE_PATH, self.get_sinvoice_api_params_str())

    # def get_sinvoice_status_url(self):
    #     self.ensure_one()
    #     return '%s%s' % (self._get_sinvoice_api_url(), SINVOICE_STATUS_PATH)

    # def get_sinvoice_status(self):
    #     api_url = self.get_sinvoice_status_url()
    #
    #     data = {
    #         'supplierTaxCode': self.vat,
    #         'templateCode': self.account_sinvoice_type_id.name,
    #         'serial': self.account_sinvoice_serial_id.name,
    #     }
    #     result = requests.post(
    #         api_url,
    #         json=data,
    #         headers={"Content-type": "application/json; charset=utf-8"},
    #         auth=(self.account_sinvoice_serial_id.name, self.sinvoice_api_password)
    #     )
    #
    #     if result.status_code == 200:
    #         output = json.loads(result.text)
    #         if not output['errorCode'] and not output['description']:
    #             raise ValidationError("Số hóa đơn đã sử dụng %s / %s" % (output['numOfpublishInv'], output['totalInv']))
    #         else:
    #             raise ValidationError("%s\n%s" % (output['errorCode'], output['description']))
    #     else:
    #         raise ValidationError("Lỗi Kết Nối: %s" % (result.status_code))

    @api.model
    def _generate_sinvoice_config_params(self):
        """
        To be called from post_init_hook
        """
        Config = self.env['ir.config_parameter']
        Config.set_param('sinvoice_api_url', SINVOICE_API_URL)
        Config.set_param('sandbox_sinvoice_api_url', SANDBOX_SINVOICE_API_URL)

    @api.model
    def _update_sinvoice_settings(self):
        """
        To be called from post_init_hook
        """
        # account_sinvoice_type_id = self.env.ref('to_accounting_sinvoice.sinvoice_type_01GTKT')
        # account_sinvoice_template_id = self.env.ref('to_accounting_sinvoice.sinvoice_template_01GTKT0_001')
        # self.search([]).write({
        #     'account_sinvoice_type_id': account_sinvoice_type_id.id,
        #     'account_sinvoice_template_id': account_sinvoice_template_id.id
        # })

    # ----------------
    # Production
    # ----------------
    def _compute_sinvoice_api_url(self):
        ConfigParameter = self.env['ir.config_parameter'].sudo()
        sinvoice_api_url = ConfigParameter.get_param('sinvoice_api_url')
        for r in self:
            r.sinvoice_api_url = sinvoice_api_url

    def _set_sinvoice_api_url(self):
        sinvoice_api_url = self and self[0].sinvoice_api_url or False
        self.env['ir.config_parameter'].sudo().set_param('sinvoice_api_url', sinvoice_api_url)

    # ----------------
    # Sandbox
    # ----------------
    def _compute_sandbox_sinvoice_api_url(self):
        ConfigParameter = self.env['ir.config_parameter'].sudo()
        sandbox_sinvoice_api_url = ConfigParameter.get_param('sandbox_sinvoice_api_url')
        for r in self:
            r.sandbox_sinvoice_api_url = sandbox_sinvoice_api_url

    def _set_sandbox_sinvoice_api_url(self):
        sandbox_sinvoice_api_url = self and self[0].sandbox_sinvoice_api_url or False
        self.env['ir.config_parameter'].sudo().set_param('sandbox_sinvoice_api_url', sandbox_sinvoice_api_url)
