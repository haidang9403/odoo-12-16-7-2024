import base64
import logging
import requests, json
import datetime, time

from odoo import models, api, fields, registry, _
from odoo.exceptions import UserError, ValidationError, MissingError
from odoo.tools import format_date

_logger = logging.getLogger(__name__)

# Viettel S-Invoice' representation file types
SINVOICE_REPRESENTATION_FILETYPE = ['PDF', 'HTML']
# Viettel implements asynch mechanism
SINVOICE_TIMEOUT = 20000


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'to.vietnamese.number2words']

    # This field is deprecated
    # TODO: remove in Odoo 13
    electric_invoice_created = fields.Boolean("Electric Invoice Created?", readonly=True, default=False, copy=False,
                                              help="Technical field to indicate if an e-invoice has been generated corresponding to this invoice")
    sinvoice_enabled = fields.Boolean(related='journal_id.sinvoice_enabled',
                                      help="This technical field is to indicate if S-Invoice service is available for this invoice")
    sinvoice_state = fields.Selection([
        ('not_issued', 'Not Issued'),
        ('issued', 'Issued and not Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Issued but Cancelled')
    ], string='S-Invoice Status', copy=False, index=True, required=True, default='not_issued', readonly=True,
        track_visibility='onchange')
    sinvoice_invoice_date = fields.Datetime(string='S-Invoice Issued Date', copy=False, readonly=True,
                                            track_visibility='onchange',
                                            help="The date and time at which the S-Invoice was issued.")
    sinvoice_cancellation_date = fields.Datetime(string='S-Invoice Cancellation Date', copy=False, readonly=True,
                                                 track_visibility='onchange',
                                                 help="The cancellation date of the S-Invoice which may differ from the date on which the cancel request was sent to S-Invoice.")
    sinvoice_issue_user_id = fields.Many2one('res.users', string='S-Invoice Issue User', copy=False, readonly=True,
                                             track_visibility='onchange',
                                             help="The user who issued the Sinvoice for this invoice")
    sinvoice_reservation_code = fields.Char('S-Invoice Secret Code', copy=False, readonly=True)
    sinvoice_representation_pdf = fields.Binary(string='S-Invoice Representation File (PDF)', attachment=True,
                                                readonly=True, copy=False, oldname='sinvoice_representation_file',
                                                help="The display version of the S-Invoice in PDF format")
    sinvoice_representation_filename_pdf = fields.Char(string='S-Invoice Representation Filename (PDF)', readonly=True,
                                                       copy=False, oldname='sinvoice_representation_filename')

    sinvoice_representation_html = fields.Binary(string='S-Invoice Representation File (HTML)', attachment=True,
                                                 readonly=True, copy=False, oldname='sinvoice_representation_file',
                                                 help="The display version of the S-Invoice in HTML format")
    sinvoice_representation_filename_html = fields.Char(string='S-Invoice Representation Filename (HTML)',
                                                        readonly=True,
                                                        copy=False, oldname='sinvoice_representation_filename')
    sinvoice_converted_file = fields.Binary(string='S-Invoice Converted File', attachment=True, readonly=True,
                                            copy=False)
    sinvoice_converted_filename = fields.Char(string='S-Invoice Converted Filename', readonly=True, copy=False)
    sinvoice_representation_file_created = fields.Boolean("Electric Representation Invoice Downloaded?", copy=False,
                                                          readonly=True, default=False)
    sinvoice_exchange_file_created = fields.Boolean("Electric Exchange Invoice Downloaded?", copy=False, readonly=True,
                                                    default=False)
    sinvoice_transactionid = fields.Char(string='S-Invoice Transaction ID', copy=False, readonly=True,
                                         help="Technical field to store transaction ID that was returned by S-Invoice after invoice creation.")
    # account_sinvoice_serial_id = fields.Many2one('account.sinvoice.serial', string='S-Invoice Serial', copy=False,
    #                                              readonly=True, ondelete='restrict')
    # account_sinvoice_template_id = fields.Many2one('account.sinvoice.template', string='S-Invoice Template', copy=False,
    #                                               readonly=True, ondelete='restrict')
    # account_sinvoice_type_id = fields.Many2one('account.sinvoice.type', string='S-Invoice Type', copy=False,
    #                                            readonly=True, ondelete='restrict')
    sinvoice_receive_code = fields.Char(string='Invoice receive code')
    lock_legal_number = fields.Boolean(string='Lock Legal Number', compute='_compute_lock_legal_number',
                                       help="If checked, invoice's legal number will be locked after S-Invoice will be issued.")
    total_in_word = fields.Char(string='In words', compute='_compute_num2words')
    sea_invoice_note = fields.Char(string="Invoice Note")

    # sea_check_customer_for_invoice = fields.Boolean(string='Customers Don\'t Take Invoice')

    def _compute_lock_legal_number(self):
        for r in self:
            if r.sinvoice_enabled and r.company_id.sinvoice_lock_legal_number and r.sinvoice_state != 'not_issued':
                r.lock_legal_number = True
            else:
                r.lock_legal_number = False

    @api.multi
    def _compute_num2words(self):
        for r in self:
            r.total_in_word = r.num2words(r.amount_total, precision_rounding=r.currency_id.rounding)

    def _get_sinvvoice_date(self):
        return self.env['to.base'].convert_time_to_utc(datetime.datetime.combine(self.date_invoice, datetime.time.min),
                                                       'UTC') - datetime.timedelta(hours=7)

    # def _get_account_sinvoice_serial_name(self):
    #     """
    #     Return the name of the sinvoice serial. For example, 'AA/18E', 'AA/19E'
    #     :rtype: string
    #     """
    #     if self.account_sinvoice_serial_id:
    #         return self.account_sinvoice_serial_id.name
    #     else:
    #         return self.journal_id.get_account_sinvoice_serial().name

    # def _get_sinvoice_template_name(self):
    #     """
    #     Return the name of the sinvoice template. For example, '01GTKT0/001', '01GTKT0/002'
    #     :rtype: string
    #     """
    #     if self.account_sinvoice_template_id:
    #         return self.account_sinvoice_template_id.name
    #     else:
    #         return self.journal_id.get_sinvoice_template().name

    # def _get_account_sinvoice_type_name(self):
    #     """
    #     Return the code of the sinvoice type. For example, '01GTKT', '02GTTT'
    #     :rtype: string
    #     """
    #     if self.account_sinvoice_type_id:
    #         return self.account_sinvoice_type_id.name
    #     else:
    #         return self.journal_id.get_account_sinvoice_type().name

    def _prepare_sinvoice_strIssueDate(self):
        """
        S-Invoice requires invoice date in the format of '%Y%m%d%H%M%S' (e.g. 20191202201243)
        """
        return self.date_invoice.strftime('%Y%m%d%H%M%S')

    def _get_sinvoice_presentation_data(self, file_type):
        """
        This method will connect S-Invoice and request for representated data that could be used for displaying purpose
        
        @param file_type: the file type to get which is either 'ZIP' or 'PDF'
        :return: dictionary of return data
            {
                'errorCode': None, if no error,
                'description': error discription or None if no error,
                'fileName': 'the name of the file returned',
                'fileToBytes': file content in bytes which is ready for storing in Odoo's Binary fields
            }
        :rtype: dict
        :raise requests.HTTPError: 
        """
        self.ensure_one()
        if file_type not in SINVOICE_REPRESENTATION_FILETYPE:
            types_msg = "\n* %s;".join(SINVOICE_REPRESENTATION_FILETYPE)
            raise ValidationError(
                _("The filetype for S-Invoice representation file %s is not supported. It should be either:\n%s")
                % (file_type, types_msg))

        if self.type not in ['out_invoice', 'out_refund']:
            raise UserError(_(
                "Could not get S-Invoice display file as the invoice %s is neither a customer invoice nor customer credit note.")
                            % (self.number or self.legal_number,))
        if self.sinvoice_state == 'not_issued':
            raise UserError(
                _("S-Invoice has not been issued for this invoice %s") % (self.number or self.legal_number,))
        if not self.legal_number:
            raise UserError(_(
                "The invoice %s has no legal number. This could be a data inconsitant problem. Please contact your service provider for help")
                            % self.legal_number)
        request_data = {
            'maNhanHoaDon': self.sinvoice_reservation_code,
            'fileType': file_type

            # 'supplierTaxCode': self.company_id.vat,
            # 'invoiceNo': self.legal_number,
            # 'templateCode': self._get_sinvoice_template_name(),
            # 'fileType': file_type

        }
        auth = self.company_id.get_sinvoice_auth_str()
        API_INVOICE_RECEIVE_CODE = str(self.company_id.get_sinvoice_presentation_file_url()) + '&maNhanHoaDon=' + str(
            self.sinvoice_reservation_code)
        req = requests.post(
            API_INVOICE_RECEIVE_CODE,
            data=json.dumps(request_data),
            headers={"Content-type": "application/json; charset=utf-8"},
            timeout=SINVOICE_TIMEOUT,
            auth=auth
        )
        # Raises :class:`HTTPError`, if one occurred.
        req.raise_for_status()
        data = req.json()
        print(data)
        return data

    def get_sinvoice_representation_files(self):
        self.ensure_one()
        update_vals = {}
        attachments = []
        generate_attachment = self.company_id.sinvoice_representation_file_as_attachment or self._context.get(
            'force_sinvoice_representation_file_as_attachment', False)
        try:
            for file_type in SINVOICE_REPRESENTATION_FILETYPE:
                data = self._get_sinvoice_presentation_data(file_type)
                file_type = file_type.lower()
                filename = '%s.%s' % (data['hoaDonObjectReturn']['maNhanHoaDon'], file_type)
                if file_type == 'pdf':
                    file_content_pdf = data['hoaDonObjectReturn']['contentHoaDonPDF']
                    update_vals.update({
                        'sinvoice_representation_%s' % file_type: file_content_pdf,
                        'sinvoice_representation_filename_%s' % file_type: filename
                    })
                if file_type == 'html':
                    file_name_html = filename + '.zip'
                    print(file_name_html)
                    file_content_html = data['hoaDonObjectReturn']['contentHoaDonHTML']
                    update_vals.update({
                        'sinvoice_representation_%s' % file_type: file_content_html,
                        'sinvoice_representation_filename_%s' % file_type: file_name_html
                    })

                # data = self._get_sinvoice_presentation_data(file_type)
                # file_type = file_type.lower()
                # filename = '%s.%s' % (data['hoaDonObjectReturn']['maNhanHoaDon'], file_type)
                # file_content = data['hoaDonObjectReturn']['contentHoaDonPDF']
                # update_vals.update({
                #     'sinvoice_representation_%s' % file_type: file_content,
                #     'sinvoice_representation_filename_%s' % file_type: filename
                # })

                # if the company wants attachment
                # if generate_attachment:
                #     req_content = base64.decodebytes(file_content_html.encode())
                #     attachment = (file_name_html, req_content)
                #     attachments.append(attachment)

            message = _("Successfully downloaded representation versions of the S-Invoice from the S-Invoice system.")
            if not generate_attachment:
                message += _("\nYou will be able to find the in the tab S-Invoice of the invoice form view above.")

        except requests.HTTPError as e:
            message = _(
                "Something went wrong while downloading the Representation version of the S-Invoice. Here is the debugging information:\n%s") % str(
                e)

        if bool(update_vals):
            self.write(update_vals)
        if self._context.get('log_sinvoice_message', False):
            self.message_post(body=message, attachments=attachments or None)
        return update_vals

    def _ensure_sinvoice_representation_files(self, retries=0, sleep=3):
        """
        This method is to ensure representation files available

        :param retries: number of times to retry. SInvoice may not have these information right after issueing invoice
        :param sleep: number of second to wait before retrying

        :return: dictionary of representation files in pdf and zip formats
        :rtype: dict
        
        :raise MissingError: when no file available in S-Invoice system to get
        """
        self.ensure_one()
        if not self.sinvoice_representation_pdf or not self.sinvoice_representation_html or self._context.get(
                'refresh_sinvoice_representation_file', False):
            self.get_sinvoice_representation_files()
        data = {
            'pdf': self.sinvoice_representation_pdf,
            'html': self.sinvoice_representation_html
        }
        if not data['pdf'] or not data['html']:
            if retries > 0:
                retries -= 1
                time.sleep(sleep)
                return self._ensure_sinvoice_representation_files(retries)
            else:
                raise MissingError(
                    _("No representation files avaiable yet. Please wait for a few minutes before trying again!"))
        else:
            return data

    def _get_exchange_user(self):
        return self.company_id.sinvoice_conversion_user_id or self.env.user

    def _get_sinvoice_exchange_data(self):
        """
        This method will connect S-Invoice and request for exchange data that could be used for conversion purpose
        
        :return: dictionary of return data
            {
                'errorCode': None, if no error,
                'description': error discription or None if no error,
                'fileName': 'the name of the file returned',
                'fileToBytes': file content in bytes which is ready for storing in Odoo's Binary fields
            }
            error code
            ----------
            200 OK, Success
            201 Created, Success of a resource creation when using the POST method
            400 Bad Request, The request parameters are incomplete or missing
            403 Forbidden, The action or the request URI is not allowed by the system
            404 Not Found, The resource referenced by the URI was not found
            422 Unprocessable Entity, One of the requested action has generated an error
            429 Too Many Requests, Your application is making too many requests and is being rate limited
            500 Internal Server Error, Used in case of time out or when the request, otherwise correct, was not able to complete.

        :rtype: dict
        :raise requests.HTTPError: 
        """
        self.ensure_one()
        if self.type not in ['out_invoice', 'out_refund']:
            raise UserError(_(
                "Could not get S-Invoice exchange file as the invoice %s is neither a customer invoice nor customer credit note.")
                            % (self.number or self.legal_number,))
        if self.sinvoice_state == 'not_issued':
            raise UserError(
                _("S-Invoice has not been issued for this invoice %s") % (self.number or self.legal_number,))
        if not self.legal_number:
            raise UserError(_(
                "The invoice %s has no legal number. This could be a data inconsitant problem. Please contact your service provider for help")
                            % self.legal_number)
        req_path = self.company_id.get_sinvoice_exchange_file_url()
        auth = self.company_id.get_sinvoice_auth_str()
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        request_data = {
            'supplierTaxCode': self.company_id.vat,
            # 'templateCode': self._get_sinvoice_template_name(),
            'invoiceNo': self.legal_number,
            'strIssueDate': self._prepare_sinvoice_strIssueDate(),
            'exchangeUser': self._get_exchange_user().name,
        }
        req = requests.post(
            req_path,
            data=request_data,
            headers=headers,
            timeout=SINVOICE_TIMEOUT,
            auth=auth
        )
        req.raise_for_status()
        data = req.json()
        return data

    def get_sinvoice_exchange_files(self):
        self.ensure_one()
        update_vals = {}
        attachments = []
        try:
            data = self._get_sinvoice_exchange_data()
            if data['errorCode']:
                if data['errorCode'] == 'INVOICE_NOT_FOUND':
                    message = _(
                        "The Invoice %s was not found for conversion. If the invoice has just been issued, you may need to wait"
                        " for a few minutes for the S-Invoice system to get it available for your query.") % self.legal_number
                else:
                    message = _(
                        "Could not download S-Invoice Converted file.\nError Code: %s\nError Description: %s") % (
                                  data['errorCode'],
                                  data['description']
                              )
            else:
                filename = '%s.pdf' % data['fileName']
                file_content = data['fileToBytes']
                update_vals.update({
                    'sinvoice_converted_file': file_content,
                    'sinvoice_converted_filename': filename
                })
                message = _("Successfully downloaded the converted version of the S-Invoice from the S-Invoice system.")

                # if the company wants attachment
                if self.company_id.sinvoice_exchange_file_as_attachment or self._context.get(
                        'force_sinvoice_exchange_file_as_attachment', False):
                    req_content = base64.decodebytes(file_content.encode())
                    attachment = (filename, req_content)
                    attachments.append(attachment)
                else:
                    message += _("\nYou will be able to find it in the tab S-Invoice of the invoice form view above.")

        except requests.HTTPError as e:
            message = _(
                "Something went wrong while downloading S-Invoice Exchange/Converted invoice. Here is debugging information:\n%s") % str(
                e)

        if bool(update_vals):
            self.write(update_vals)
        if self._context.get('log_sinvoice_message', False):
            self.message_post(body=message, attachments=attachments or None)
        return update_vals

    def _ensure_sinvoice_converted_file(self, retries=0, sleep=3):
        """
        This method is to ensure converted file available

        :param retries: number of times to retry. SInvoice may not have these information right after issueing invoice
        :param sleep: number of second to wait before retrying

        :return: converted file in binary
        :rtype: bytes
        
        :raise MissingError: when no file available in S-Invoice system to get
        """
        self.ensure_one()
        if not self.sinvoice_converted_file or self._context.get('refresh_sinvoice_converted_file', False):
            self.get_sinvoice_exchange_files()

        if not self.sinvoice_converted_file:
            if retries > 0:
                retries -= 1
                time.sleep(sleep)
                return self._ensure_sinvoice_converted_file(retries)
            else:
                raise MissingError(
                    _("No converted file avaiable yet. Please wait for a few minutes before trying again!"))
        else:
            return self.sinvoice_converted_file

    def _get_sinvoice_taxpercentage(self):
        self.ensure_one()
        notax_line_ids = self.invoice_line_ids.filtered(
            lambda r: r.display_type == False and not r.invoice_line_tax_ids)
        invoice_tax_ids = self.invoice_line_ids.mapped('invoice_line_tax_ids')
        if not notax_line_ids and len(invoice_tax_ids) == 1:
            if invoice_tax_ids.amount_type == 'percent':
                return invoice_tax_ids[0].amount
        return (self.amount_tax / self.amount_untaxed) * 100

    def _prepare_sinvoice_payments_data(self):
        # TODO: find all related payments and there methods to fill here
        return [
            {
                # Tên phương thức thanh toán. Có thể nhập giá trị tùy ý.
                'paymentMethodName': 'CK',
            }
        ]

    def _prepare_tax_breakdowns(self):
        tax_groups = []
        exemption_group = self.env.ref('l10n_vn_c200.tax_group_exemption').id
        exemption_tax_lines = self.tax_line_ids.filtered(lambda r: r.tax_id.tax_group_id.id == exemption_group)
        taxableAmount = sum(exemption_tax_lines.mapped('base'))
        if taxableAmount:
            tax_groups.append({
                'taxPercentage': -2,
                'taxableAmount': taxableAmount,
                'taxAmount': 0
            })

        percent_tax_lines = self.tax_line_ids.filtered(lambda r: r.tax_id.amount_type == 'percent'
                                                                 and r.tax_id.tax_group_id.id != exemption_group)
        for tax_line in percent_tax_lines:
            tax_groups.append({
                'taxPercentage': tax_line.tax_id.amount,
                'taxableAmount': tax_line.base,
                'taxAmount': tax_line.amount_total
            })

        remain_tax_lines = self.tax_line_ids.filtered(lambda r: r.tax_id.amount_type != 'percent'
                                                                and r.tax_id.tax_group_id.id != exemption_group)
        if remain_tax_lines:
            tax_groups.append({
                'taxableAmount': sum(remain_tax_lines.mapped('base')),
                'taxAmount': sum(remain_tax_lines.mapped('amount_total'))
            })
        return tax_groups

    def _sinvoice_need_english(self):
        """
        This method is to check if this invoice does need subtitle in English during issuing S-Invoice
        """
        if self.commercial_partner_id.country_id and self.commercial_partner_id.country_id != self.env.ref('base.vn'):
            return True
        else:
            return False

    def _prepare_sinvoice_seller_legal_name(self):
        ctx = dict(self._context).copy()
        ctx['lang'] = self.env.ref('base.lang_vi_VN').code
        name = self.with_context(ctx).company_id.partner_id.name
        ctx['lang'] = 'en'
        en_name = self.with_context(ctx).company_id.partner_id.name
        if en_name != name and self._sinvoice_need_english():
            name += " (%s)" % self.with_context(ctx).company_id.partner_id.name
        return name

    def _get_cusomter_invoice_address(self):
        if self.sea_check_customer_for_invoice:
            for obj in self.env['res.partner'].search([('id', '=', 6538)]):
                return obj
        else:
            return self.partner_id if self.partner_id.type == 'invoice' else self.commercial_partner_id

    def _get_issuing_user(self):
        return self.user_id or self.env.user

    def _prepare_sinvoice_data(self):
        """
        Hook method that prepare data to send to S-Invoice for issuing new invoice there

        :return: the data to post to S-Invoice for invoice issuing according to the
            instructions here: https://sinvoice.viettel.vn/download/soft/tl_mo_ta_webservice_hoadondientu_doitac.doc
        :rtype: dict
        """

        def phone_format(phone_number):
            # Sinvoice does not accept blank, minus and plus in customer phone number
            phone_number = phone_number.replace(' ', '').replace('-', '').replace('+', '00')
            return phone_number

        date = self._get_sinvvoice_date()
        # there could be a reason that cause the access_token is empty. E.g. due to wrong migration
        self._portal_ensure_token()

        # Trạng thái điều chỉnh hóa đơn:
        # '1': Hóa đơn gốc
        # '3': Hóa đơn thay thế
        # '5': Hóa đơn điều chỉnh (dự kiến sẽ bỏ theo NĐ119)
        adjustment_type = '1'
        if self.type == 'out_refund':
            adjustment_type = '5'

        total_in_word = self.total_in_word
        if self.commercial_partner_id.country_id and self.commercial_partner_id.country_id != self.env.ref('base.vn'):
            total_in_word += " (%s)" % self.currency_id.with_context(lang='en_US').amount_to_text(self.amount_total)

        # return {
        #     'generalInvoiceInfo': {
        #         # ID để kiểm trùng giao dịch lập hóa đơn, là duy nhất với mỗi hóa đơn.
        #         # Với mỗi transactionUuid, khi đã gửi một transactionUuid với một hóa
        #         # đơn A thì mọi request lập hóa đơn với cùng transactionUuid sẽ trả về
        #         # hóa đơn A chứ không lập hóa đơn khác. Thời gian hiệu lực của
        #         # transactionUuid là 3 ngày.
        #         'transactionUuid': self.access_token,
        #         # Tên người lập hóa đơn. Nếu không truyền sang, hệ thống sẽ tự động lấy user được dùng để xác thực để lưu vào.
        #         'userName': self._get_issuing_user().name,
        #         'currencyCode': self.currency_id.name,
        #         # 'currencyRate': 1 / self.currency_id.with_context(date=date).rate,
        #         'invoiceSeries': self._get_account_sinvoice_serial_name(),
        #         'templateCode': self._get_sinvoice_template_name(),
        #         'invoiceType': self._get_account_sinvoice_type_name(),
        #         # ngày phát hành hoá đơn không được phép lớn hơn ngày hiện tại và nhỏ hơn ngày của hoá đơn đã phát hành trước đó.
        #         'invoiceIssuedDate': int(datetime.datetime.timestamp(date) * 1000),
        #         'adjustmentType': adjustment_type,
        #         # Trạng thái thanh toán của hóa đơn
        #         # True: Đã thanh toán
        #         # False: Chưa thanh toán
        #         'paymentStatus': True if self.state == 'paid' else False,
        #         'paymentType': 'CK',
        #         'paymentTypeName': 'CK',
        #         # Cho khách hàng xem hóa đơn trong Quản lý hóa đơn
        #         'cusGetInvoiceRight': True,
        #     },
        #     'payments': self._prepare_sinvoice_payments_data(),
        #     'buyerInfo': {
        #         'buyerName': self.partner_id.name if self.partner_id.name and self.partner_id.name != self.partner_id.commercial_company_name else '',
        #         'buyerLegalName': self.commercial_partner_id.name,
        #         'buyerTaxCode': self.commercial_partner_id.vat or '',
        #         'buyerAddressLine': self._get_cusomter_invoice_address()._sinvoice_display_address(),
        #         'buyerCityName': self.commercial_partner_id.city or self.commercial_partner_id.state_id.name or '',
        #         'buyerCountryCode': self.commercial_partner_id.country_id and self.commercial_partner_id.country_id.code or '',
        #         'buyerPhoneNumber': self.commercial_partner_id.phone and phone_format(
        #             self.commercial_partner_id.phone) or '',
        #         'buyerEmail': self.commercial_partner_id.email or '',
        #         'buyerIdNo': "",
        #         'buyerIdType': "1"
        #     },
        #     'sellerInfo': {
        #         'sellerLegalName': self._prepare_sinvoice_seller_legal_name(),
        #         'sellerTaxCode': self.company_id.vat or '',
        #         'sellerAddressLine': self.company_id.partner_id._sinvoice_display_address(),
        #         'sellerPhoneNumber': self.company_id.phone or '',
        #         'sellerEmail': self.company_id.email and self.company_id.email.strip() or '',
        #         'sellerBankName': "",
        #         'sellerBankAccount': ""
        #     },
        #     'itemInfo': self.invoice_line_ids._prepare_sinvoice_lines_data(),
        #     'summarizeInfo': {
        #         'sumOfTotalLineAmountWithoutTax': self.amount_untaxed,
        #         'totalAmountWithoutTax': self.amount_untaxed,
        #         'totalTaxAmount': self.amount_tax,
        #         'totalAmountWithTax': self.amount_total,
        #         'totalAmountWithTaxInWords': total_in_word,
        #         'discountAmount': 0,
        #         'taxPercentage': self._get_sinvoice_taxpercentage()
        #     },
        #     'taxBreakdowns': self._prepare_tax_breakdowns()
        # }

        item_invoice = self.invoice_line_ids._prepare_sinvoice_lines_data()
        total_amount_no_tax = 0
        total_amount_tax_0 = 0
        total_amount_without_tax_5 = 0
        total_amount_tax_5 = 0
        total_amount_without_tax_10 = 0
        total_amount_tax_10 = 0
        for line in item_invoice:
            if line['thueSuat'] == 5:
                total_amount_without_tax_5 += line['tongTien']
                total_amount_tax_5 += line['tienThue']
            if line['thueSuat'] == 10:
                total_amount_without_tax_10 += line['tongTien']
                total_amount_tax_10 += line['tienThue']
        if self.sea_check_customer_for_invoice:
            return {
                "id_master": self.access_token,
                # "id_master": '32485435-6608-4aa4-b638-f8caefd9d022',
                "guid_PhatHanh": self.company_id.get_sinvoice_guild_issue_str(),
                "soDonHang": "",
                "ngayDonHang": str(self.date_invoice),
                "maKhachHang": "",
                "tenKhachHang": 'Khách hàng không lấy hóa đơn',
                "tenDonVi": '',
                "maSoThue": '',
                "maSoThueNN": "",
                "diaChi": self._get_cusomter_invoice_address()._sinvoice_display_address() or '',
                "faxNguoiMua": "",
                "emailNguoiMua": self._get_cusomter_invoice_address().email or '',
                "soTaiKhoan": "",
                "noiMoTaiKhoan": "",
                "hinhThucThanhToan": "TM/CK",
                "tongTienKCT": "",
                "tongTien0": "",
                "tongTienChuaVat5": total_amount_without_tax_5,
                "tongTienVat5": total_amount_tax_5,
                "tongTienChuaVat10": total_amount_without_tax_10,
                "tongTienVat10": total_amount_tax_10,
                "tongTienHang": self.amount_untaxed,
                "tongTienThue": self.amount_tax,
                "tongTienCKGG": "",
                "tienChiPhiKhac": "",
                "tongTienTT": self.amount_total,
                "soTienBangChu": total_in_word + ' đồng.',
                "ngayHoaDon": "",
                "tinhTrangHoaDon": 0,
                "loaiTienTe": self.currency_id.name,
                "tyGia": "1",
                "tinhTrangKyNguoiBan": 0,
                "tinhLaiSoTien": "0",
                "loiKhongTaoHoaDon": "0",
                "hienThiNgoaiTe": "0",
                "dongbohoadon": "0",
                "listMasterCT": self.invoice_line_ids._prepare_sinvoice_lines_data(),
            }
        else:
            return {
                "id_master": self.access_token,
                # "id_master": '32485435-6608-4aa4-b638-f8caefd9d022',
                "guid_PhatHanh": self.company_id.get_sinvoice_guild_issue_str(),
                "soDonHang": "",
                "ngayDonHang": str(self.date_invoice),
                "maKhachHang": "",
                "tenKhachHang": self.partner_id.name if self.partner_id.name and self.partner_id.name != self.partner_id.commercial_company_name else '',
                "tenDonVi": self.commercial_partner_id.name,
                "maSoThue": self.commercial_partner_id.vat or '',
                "maSoThueNN": "",
                "diaChi": self._get_cusomter_invoice_address()._sinvoice_display_address(),
                "dienThoaiNguoiMua": self.commercial_partner_id.phone and phone_format(
                    self.commercial_partner_id.phone) or '',
                "faxNguoiMua": "",
                "emailNguoiMua": self.commercial_partner_id.email or '',
                "soTaiKhoan": "",
                "noiMoTaiKhoan": "",
                "hinhThucThanhToan": "TM/CK",
                "tongTienKCT": "",
                "tongTien0": "",
                "tongTienChuaVat5": total_amount_without_tax_5,
                "tongTienVat5": total_amount_tax_5,
                "tongTienChuaVat10": total_amount_without_tax_10,
                "tongTienVat10": total_amount_tax_10,
                "tongTienHang": self.amount_untaxed,
                "tongTienThue": self.amount_tax,
                "tongTienCKGG": "",
                "tienChiPhiKhac": "",
                "tongTienTT": self.amount_total,
                "soTienBangChu": total_in_word + ' đồng.',
                "ngayHoaDon": "",
                "tinhTrangHoaDon": 0,
                "loaiTienTe": self.currency_id.name,
                "tyGia": "1",
                "tinhTrangKyNguoiBan": 0,
                "tinhLaiSoTien": "0",
                "loiKhongTaoHoaDon": "0",
                "hienThiNgoaiTe": "0",
                "dongbohoadon": "0",
                "listMasterCT": self.invoice_line_ids._prepare_sinvoice_lines_data(),
            }

    def _find_earliest_unissued_customer_invoice(self):
        """
        This method finds the earliest unissued customer invoice / credit note
        """
        self.ensure_one()
        domain = [
            ('state', '!=', 'cancel'),
            ('type', 'in', ['out_invoice', 'out_refund']),
            ('sinvoice_state', '=', 'not_issued'),
            ('date_invoice', '<', self.date_invoice),
            ('journal_id.sinvoice_enabled', '=', True)
        ]
        if self.company_id.sinvoice_start:
            domain.append(('date_invoice', '>', self.company_id.sinvoice_start))
        return self.env['account.invoice'].search(domain, order='date_invoice asc, id asc', limit=1)

    def _prepare_update_vals_after_issuing(self, returned_vals):
        """
        This method is called by the method `_issue_sinvoice`. This prepares data to write back to the current invoice after issuing on S-Invoice system

        @param returned_vals: the result that returned by S-Invoice system after issuing the invoice
        @return: dictionary of values to update the current invoice after issuing
        @rtype: dict
        """
        return {
            'sinvoice_transactionid': returned_vals['hoaDonObjectReturn']['guid_PX'],
            'sinvoice_invoice_date': fields.Datetime.now(),
            'legal_number': returned_vals['hoaDonObjectReturn']['so'],
            'sinvoice_reservation_code': returned_vals['hoaDonObjectReturn']['maNhanHoaDon'],
            'sinvoice_state': 'paid' if self.state == 'paid' else 'issued',
            # 'account_sinvoice_serial_id': self.journal_id.get_account_sinvoice_serial().id,
            # 'account_sinvoice_template_id': self.journal_id.get_sinvoice_template().id,
            # 'account_sinvoice_type_id': self.journal_id.get_account_sinvoice_type().id,
            'sinvoice_issue_user_id': self.env.user.id,
        }

    def _issue_sinvoice(self, raise_error=True):
        self.ensure_one()

        # check invoice
        if self.type not in ['out_invoice', 'out_refund']:
            raise UserError(_("Only customer invoices or customer credit notes can generate S-Invoice!"))
        if self.state not in ('open', 'paid'):
            raise ValidationError(_(
                "You cannot generate S-Invoice from the Odoo invoice %s while the Odoo invoice status is neither Open nor Paid")
                                  % (self.number or self.legal_number,))
        if self.sinvoice_state != 'not_issued':
            raise UserError(
                _("S-Invoice for the invoice %s has been issued already!") % (self.number or self.legal_number,))

        # check customer
        if not self.sea_check_customer_for_invoice:
            customer = self._get_cusomter_invoice_address()
            if not customer.street:
                raise ValidationError(_("Please specify address for the customer %s.") % customer.name)
            if not customer.country_id:
                raise ValidationError(_("Please specify a country for the customer %s.") % customer.name)
            # VAT number is required for enterprise customers in Vietnam
            if customer.country_id == self.env.ref(
                    'base.vn') and self.commercial_partner_id.is_company and not self.commercial_partner_id.vat:
                raise ValidationError(
                    _("You must provide Tax Identication Number of the customer %s.") % self.commercial_partner_id.name)

        # Check company
        if not self.company_id.street:
            raise ValidationError(_("Please specify your company address before you can issue an S-Invoice"))
        if not self.company_id.vat:
            raise ValidationError(
                _("You have not configured Tax Identication Number for your company %s.") % self.company_id.name)
        if self.company_id.sinvoice_start and self.date_invoice and self.date_invoice < self.company_id.sinvoice_start:
            raise UserError(
                _("You cannot issue S-Invoice for the invoices %s that has invoice date earlier than the company's"
                  " S-Invoice Start Date (%s). If you still want to do it, you could either:\n"
                  "* Change the date of the invoice to a date that is later than or equal to %s;\n"
                  "* Or, go to Accounting > Configuration > Settings and change S-Invoice Start Date to"
                  " a date that is earlier than or equal to %s.")
                % (
                    self.number,
                    format_date(self.env, self.company_id.sinvoice_start),
                    format_date(self.env, self.company_id.sinvoice_start),
                    format_date(self.env, self.date_invoice)
                )
            )

        if self.company_id.sinvoice_issue_earliest_invoice_first and self.company_id.sinvoice_start:
            earlier_invoice = self._find_earliest_unissued_customer_invoice()
            if earlier_invoice:
                raise UserError(_(
                    "You should issue S-Invoice for the invoice %s dated %s before issueing S-Invoice for the current one %s dated %s."
                    " Or, you could go to Accounting > Configuration > Settings to disable this verification although you are not"
                    " recommended to do that unless you know what you do.")
                                % (
                                    earlier_invoice.number or earlier_invoice.legal_number,
                                    format_date(self.env, earlier_invoice.date_invoice),
                                    self.number or self.legal_number,
                                    format_date(self.env, self.date_invoice)
                                ),
                                )
        # use new cursor to handle each invoice issuing
        # this could help commit a success issue before an error occurs that may roll back
        # the data in Odoo while the invoice is already available in S-Invoice database
        cr = registry(self._cr.dbname).cursor()
        self = self.with_env(self.env(cr=cr))

        auth_str = self.company_id.get_sinvoice_auth_str()
        error = False
        try:
            req = requests.post(
                self.company_id.get_sinvoice_create_url(),
                data=json.dumps(self._prepare_sinvoice_data()),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            print(req.headers.get('Content-type'))
            print(req)
            print(returned_vals)
            json_object = self._prepare_sinvoice_data()
            print("__Data__", json_object)


            if not returned_vals['hoaDonObjectReturn']:
                error = True
                message = _("Could not issue S-Invoice from the invoice %s due to the error code `%s`.\n") % (
                    self.number or self.legal_number, returned_vals['errorCode'])
                if returned_vals['errorCode'] == 'DONOT_HAVE_PERMISSION':
                    message += _(
                        "Your S-Invoice account has been disabled or you don't have enough permission. Please contact your Viettel"
                        " S-Invoice agent for help.")
                elif returned_vals['errorCode'] == 'TEMPLATE_NOT_FOUND':
                    message += _(
                        "The template is invalid. Please specify a right S-Invoice template for the journal %s or the company %s."
                        " You may need to register a template in S-Invoice system priorily.") % (
                                   self.journal_id.name, self.company_id.name)
                elif returned_vals['errorCode'] == 'INVOICE_ISSUED_DATE_INVALID':
                    message += _(
                        "The invoice date %s is invalid. Probably this date is earlier than the issue date of a previously issued invoice."
                        " You may fix this by modifying the invoice date to a later one.") % format_date(self.env,
                                                                                                         self.date_invoice)
                elif returned_vals['errorCode'] == 'INVOICE_ISSUED_DATE_OVER_CURRENT_TIME':
                    message += _(
                        "The invoice date must not be in the future. If you find it as the current date, this could be a problem"
                        " in your timezone settings. You may fix this by modifying the invoice date to a date that is less than"
                        " or equal to %s, or fixing your timezone.") % format_date(self.env, self.date_invoice)
                elif returned_vals['errorCode'] == 'OUT_OF_INVOICE_NO':
                    message += _("The possibility could be either:\n"
                                 "1. The S-Invoice template is not relevant to the S-Invoice Serial\n"
                                 "2. You have run out of your registered range of invoice numbers."
                                 " You may need to contact your Viettel S-Invoice agent for help.")
                elif returned_vals['errorCode'] == 'BUYER_PHONE_NUMBER_INVALID':
                    message += _("Invalid customer phone number %s") % self.commercial_partner_id.phone
                elif returned_vals['errorCode'] == 'ITEM_NAME_INVALID':
                    message += _(
                        "It seems that your product name/description was too long for SInvoice. If you were sending product description to SInvoice, you "
                        "may either reconfigure your corresponding journal to use product name instead, or shorten your product description to less than %s characters. ") % (
                                   self.journal_id.sinvoice_item_name_limit)
                elif returned_vals['errorCode'] == 'ITEM_NAME_NULL':
                    message += _(
                        "An invoice line has no name / description. If you were sending product description to SInvoice, you may either reconfigure your "
                        "corresponding journal to use product name instead, or enter a description for this product.")
                else:
                    message += _(" Error: %s") % returned_vals['description']
            else:
                message = _("E-Invoice created on S-Invoice: Invoice No: %s") % (returned_vals['hoaDonObjectReturn']['so'])
                self.write(self._prepare_update_vals_after_issuing(returned_vals))
        except requests.HTTPError as e:
            print(self._prepare_sinvoice_data())
            error = True
            message = _("Something went wrong when issuing E-Invoice. Here is the debugging information:\n%s") % str(e)
        except Exception as e:
            error = True
            print(self._prepare_sinvoice_data())
            # message = _("Something went wrong when issuing the E-Invoice: %s") % str(e)
            message = _("Something went wrong when issuing the E-Invoice: %s") % returned_vals['objKetQua']['moTaKetQua']
        if error and raise_error:
            cr.rollback()
            cr.close()
            raise ValidationError(message)
        self.message_post(body=message)
        cr.commit()
        cr.close()
        return error

    def _edit_sinvoices(self, raise_error=True):
        self.ensure_one()
        cr = registry(self._cr.dbname).cursor()
        self = self.with_env(self.env(cr=cr))

        auth_str = self.company_id.get_sinvoice_auth_str()
        error = False
        json_object = self._prepare_sinvoice_data()
        json_object['id_master'] = 'Edit_Invoice_' + str(self.legal_number) + '_' + str(datetime.datetime.now())
        json_object['maNhanHoaDon'] = self.sinvoice_reservation_code
        try:
            req = requests.post(
                self.company_id.get_sinvoice_edit_url(),
                data=json.dumps(json_object),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            print(req.headers.get('Content-type'))
            print(req)
            print(returned_vals)
            json_object = self._prepare_sinvoice_data()
            print("__Data__", json_object)

            if not returned_vals['hoaDonObjectReturn']:
                error = True
                message = _("Could not issue S-Invoice from the invoice %s due to the error code `%s`.\n") % (
                    self.number or self.legal_number, returned_vals['errorCode'])
            else:
                message = _("E-Invoice edit on S-Invoice: Invoice No: %s") % (returned_vals['hoaDonObjectReturn']['so'])
                self.write(self._prepare_update_vals_after_issuing(returned_vals))
        except Exception as e:
            error = True
            json_object = self._prepare_sinvoice_data()
            print("__Data__", json_object)
            message = _("Something went wrong when issuing the E-Invoice: %s") % str(e)
            # message = _("Something went wrong when issuing the E-Invoice: %s") % returned_vals['objKetQua'][
            #     'moTaKetQua']
        if error and raise_error:
            cr.rollback()
            cr.close()
            raise ValidationError(message)
        self.message_post(body=message)
        cr.commit()
        cr.close()
        return error

    def issue_sinvoices(self, raise_error=True):
        # we sort the invoices to ensure the earliest invoice should be at the first position
        # otherwise, we will get error during invoice generation
        self = self.sorted('date_invoice')
        error_invoices = self.env['account.invoice']
        for r in self:
            res = r._issue_sinvoice(raise_error)
            if res:
                error_invoices |= r
        return error_invoices, self - error_invoices

    def edit_sinvoices(self, raise_error=True):
        # we sort the invoices to ensure the earliest invoice should be at the first position
        # otherwise, we will get error during invoice generation
        self = self.sorted('date_invoice')
        error_invoices = self.env['account.invoice']
        for r in self:
            res = r._edit_sinvoices(raise_error)
            if res:
                error_invoices |= r
        return error_invoices, self - error_invoices

    def _sinvoice_unpaid(self, raise_error=True):
        """
        This method will connect the S-Invoice system and set the status of the corresponding S-Invoice to Paid
        """
        self.ensure_one()
        auth_str = self.company_id.get_sinvoice_auth_str()
        req_data = {
            'supplierTaxCode': self.company_id.vat,
            'invoiceNo': self.legal_number,
            'strIssueDate': self._prepare_sinvoice_strIssueDate(),
        }
        error = False
        update_vals = {}
        try:
            req = requests.post(
                self.company_id.get_sinvoice_cancel_payment_status_url(),
                data=req_data,
                headers={"Content-type": "application/x-www-form-urlencoded; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            content = req.json()
            if content['errorCode'] and content['errorCode'] != 'NO_RECORD_UPDATED':
                message = _(
                    "Could not set the corresponding S-Invoice as Issued and not Paid. Error Code: %s.\nError Description: %s") % (
                              content['errorCode'], content['description'])
                error = True
            elif content['errorCode'] == 'NO_RECORD_UPDATED':
                message = _(
                    "The S-Invoice seemed to be turned into the status Issued and not Paid previously. Error Code: %s.\nError Description: %s") % (
                              content['errorCode'], content['description'])
                if self.sinvoice_state != 'issued':
                    update_vals.update({
                        'sinvoice_state': 'issued',
                    })
            else:
                message = _(
                    "The corresponding S-Invoice %s has been set as Unpaid in S-Invoice system.") % self.legal_number
                update_vals.update({
                    'sinvoice_state': 'issued',
                })
        except requests.HTTPError as e:
            error = True
            message = _("Could not set the S-Invoice %s as Issued and not Paid.") % self.legal_number
            if e.response.status_code == 500:
                message += _(
                    " You might have not configured allowed IPs in your S-Invoice portal to grant access from your Odoo instance's IP."
                    " Or there could be something wrong with your S-Invoice's username and/or password.")
            else:
                message += _(" Here is the debugging information:\n%s") % str(e)
        except Exception as e:
            error = True
            message = _(
                "Something went wrong when set the E-Invoice %s as Unpaid. Here is the debugging information:\n%s") % (
                          self.legal_number, str(e))
        if error and raise_error:
            raise ValidationError(message)
        if bool(update_vals):
            self.write(update_vals)
        self.message_post(body=message)

    def action_sinvoice_unpaid(self):
        for r in self:
            r._sinvoice_unpaid()

    def action_invoice_re_open(self):
        res = super(AccountInvoice, self).action_invoice_re_open()
        for r in self.filtered(
                lambda inv: inv.sinvoice_state == 'paid' and inv.company_id.sinvoice_synch_payment_status):
            r._sinvoice_unpaid()
        return res

    def _sinvoice_paid(self, raise_error=True):
        """
        This method will connect the S-Invoice system and set the status of the corresponding S-Invoice to Paid
        """
        self.ensure_one()
        auth_str = self.company_id.get_sinvoice_auth_str()
        req_data = {
            'supplierTaxCode': self.company_id.vat,
            'invoiceNo': self.legal_number,
            'strIssueDate': self._prepare_sinvoice_strIssueDate(),
            # mặc dùng trong tài liệu có nói paymentType không còn sử dụng và thay bằng paymentMethodName như thực tế không phải vậy
            'paymentType': 'CK',
            # mặc dùng trong tài liệu có nói paymentTypeName không còn sử dụng và thay bằng paymentMethodName như thực tế không phải vậy
            'paymentTypeName': 'CK',
            'paymentMethodName': 'CK',
            'cusGetInvoiceRight': True,
            # mặc dùng trong tài liệu không nói là phải truyền templateCode nhưng ko truyền thì lỗi
            # 'templateCode': self._get_sinvoice_template_name(),
        }
        error = False
        update_vals = {}
        try:
            req = requests.post(
                self.company_id.get_sinvoice_update_payment_status_url(),
                data=req_data,
                headers={"Content-type": "application/x-www-form-urlencoded; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            content = req.json()
            if content['errorCode'] and content['errorCode'] != 'INVOICE_PAID':
                message = _(
                    "Could not set the corresponding S-Invoice as Paid. Error Code: %s.\nError Description: %s") % (
                              content['errorCode'], content['description'])
                error = True
            elif content['errorCode'] == 'INVOICE_PAID':
                message = _("The S-Invoice %s has been set as Paid in S-Invoice system already.") % self.legal_number
                if self.sinvoice_state != 'paid':
                    update_vals.update({
                        'sinvoice_state': 'paid',
                    })
            else:
                message = _(
                    "The corresponding S-Invoice %s has been set as Paid in S-Invoice system.") % self.legal_number
                update_vals.update({
                    'sinvoice_state': 'paid',
                })
        except requests.HTTPError as e:
            error = True
            message = _("Could not set the S-Invoice %s as Paid.") % self.legal_number
            if e.response.status_code == 500:
                message += _(
                    " You might have not configured allowed IPs in your S-Invoice portal to grant access from your Odoo instance's IP."
                    " Or there could be something wrong with your S-Invoice's username and/or password.")
            else:
                message += _(" Here is the debugging information:\n%s") % str(e)
        except Exception as e:
            error = True
            message = _(
                "Something went wrong when set the E-Invoice %s as Paid. Here is the debugging information:\n%s") % (
                          self.legal_number, str(e))
        if error and raise_error:
            raise ValidationError(message)
        if bool(update_vals):
            self.write(update_vals)
        self.message_post(body=message)

    def action_sinvoice_paid(self):
        for r in self:
            r._sinvoice_paid()

    def action_invoice_paid(self):
        super(AccountInvoice, self).action_invoice_paid()
        for r in self.filtered(lambda
                                       inv: inv.state == 'paid' and inv.sinvoice_state == 'issued' and inv.company_id.sinvoice_synch_payment_status):
            r._sinvoice_paid()

    def _cancel_sinvoice(self, raise_error=True):
        if self.sinvoice_state != 'issued':
            raise UserError(_("The S-Invoice corresponding to the invoice %s could not be cancelled because"
                              " it has not been issued or cancelled aready.")
                            % self._name)
        auth_str = self.company_id.get_sinvoice_auth_str()
        additional_ref_date = self._context.get('additionalReferenceDate', fields.Datetime.now())
        # S-Invoice uses UTC+7
        additional_ref_date_utc7 = self.env['to.base'].convert_utc_time_to_tz(additional_ref_date,
                                                                              tz_name='Asia/Ho_Chi_Minh')

        req_data = {
            'supplierTaxCode': self.company_id.vat,
            # 'templateCode': self._get_sinvoice_template_name(),
            'invoiceNo': self.legal_number,
            'strIssueDate': self._prepare_sinvoice_strIssueDate(),
            # Tên văn bản thỏa thuận hủy hóa đơn
            'additionalReferenceDesc': self._context.get('additionalReferenceDesc'),
            # Ngày thỏa thuận huỷ hoá đơn, không vượt quá ngày hiện tại
            'additionalReferenceDate': additional_ref_date_utc7.strftime('%Y%m%d%H%M%S'),
        }
        error = False
        # use new cursor to handle each invoice cancel
        # this could help commit a success cancel action before an error occurs that may roll back
        # the data in Odoo while the invoice is already cancel in S-Invoice database
        cr = registry(self._cr.dbname).cursor()
        self = self.with_env(self.env(cr=cr))
        try:
            req = requests.post(
                self.company_id.get_sinvoice_cancel_url(),
                data=req_data,
                headers={"Content-type": "application/x-www-form-urlencoded; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            content = req.json()
            if content['errorCode']:
                message = _("Could not cancel the E-invoice %s in S-Invoice system. Error: %s") % (
                    self.legal_number or self.number, content['description'])
                error = True
            else:
                message = _("The legal E-Invoice %s has been cancelled on S-Invoice.") % self.legal_number
                self.write({
                    'sinvoice_state': 'cancelled',
                    'sinvoice_cancellation_date': additional_ref_date
                })
        except requests.HTTPError as e:
            error = True
            message = _("Could not cancel the S-Invoice %s.") % self.legal_number
            if e.response.status_code == 500:
                message += _(
                    " You might have not configured allowed IPs in your S-Invoice portal to grant access from your Odoo instance's IP."
                    " Or there could be something wrong with your S-Invoice's username and/or password.")
        except Exception as e:
            error = True
            message = _(
                "Something went wrong when cancelling the E-Invoice %s. Here is the debugging information:\n%s") % (
                          self.legal_number, str(e))
        if error and raise_error:
            cr.rollback()
            cr.close()
            raise ValidationError(message)
        self.message_post(body=message)
        cr.commit()
        cr.close()

    def action_cancel_sinvoice(self):
        for r in self:
            r._cancel_sinvoice()

    def action_issue_sinvoices(self):
        self.issue_sinvoices(raise_error=True)

    def action_edit_sinvoices(self):
        self.edit_sinvoices(raise_error=True)

    @api.multi
    def _get_report_base_filename(self):
        self.ensure_one()
        if self.journal_id.sinvoice_send_mail_option == 'converted':
            name = self.sinvoice_converted_filename
        else:
            name = self.sinvoice_representation_filename_pdf
        if self.type in ('out_invoice', 'out_refund') and self.sinvoice_state != 'not_issued' and name:
            name = '.'.join(name.split('.')[:-1])
            return _("Invoice - %s") % name
        else:
            return super(AccountInvoice, self)._get_report_base_filename()

    @api.model
    def cron_issue_sinvoices(self):
        for journal in self.env['account.journal'].with_context(active_test=False).search(
                [('sinvoice_enabled', '>=', True)]):
            domain = [
                ('state', 'in', ('open', 'paid')),
                ('sinvoice_state', '=', 'not_issued'),
                ('journal_id', '=', journal.id),
            ]
            if journal.company_id.sinvoice_start:
                domain += [('date_invoice', '=', journal.company_id.sinvoice_start)]
            invoices = self.env['account.invoice'].search(domain)

            error_invoices, success_invoices = invoices.issue_sinvoices(raise_error=False)
            if error_invoices:
                _logger.error("Could not issue S-Invoice for the following invoices: %s",
                              ', '.join(error_invoices.mapped('name')))
            if success_invoices:
                _logger.info("Successfully issued S-Invoice for the following invoices: %s",
                             ', '.join(success_invoices.mapped('name')))

    @api.model
    def _cron_ensure_sinvoice_download_file(self):
        invoices = self.env['account.invoice'].search([('sinvoice_state', '!=', 'not_issued')])
        for invoice in invoices:
            # invoice._ensure_sinvoice_converted_file()
            invoice._ensure_sinvoice_representation_files()
