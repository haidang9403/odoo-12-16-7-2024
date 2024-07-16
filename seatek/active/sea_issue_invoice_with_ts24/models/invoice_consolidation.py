import base64
import logging
import requests, json
from odoo.addons.global_seatek import Seatek
from datetime import date
# from odoo.addons.to_vietnam_number2words import Seatek
# from odoo.addons.portal import PortalMixin
from odoo.http import request

import datetime, time
from odoo.tools import float_is_zero, float_compare, float_round
from odoo import models, api, fields, registry, _
from odoo.exceptions import UserError, ValidationError, MissingError
from odoo.tools import format_date

_logger = logging.getLogger(__name__)

SINVOICE_REPRESENTATION_FILETYPE = ['PDF', 'HTML']
SINVOICE_TIMEOUT = 20000


class InvoiceConsolidation(models.Model, Seatek):
    _name = 'invoice.consolidation'
    _inherit = ['invoice.consolidation', 'portal.mixin', 'to.vietnamese.number2words']

    access_token = fields.Char('Token')
    symbol_code = fields.Char('Symbol code')
    invoice_date_from_ts24 = fields.Char('Invoice date from TS24')
    invoice_transaction_id = fields.Char(string='Transaction ID', copy=False, readonly=True)
    invoice_sign_status = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes'),
    ], string='Invoice sign status', index=True, readonly=True, default='no', copy=False)
    cqt_code_status = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes'),
    ], string='QCT Code Status', index=True, readonly=True, default='no', copy=False)
    email_send_status = fields.Selection([
        ('no', 'No'),
        ('yes', 'Yes'),
    ], string='Email Send Status', index=True, readonly=True, default='no', copy=False)
    invoice_issued_date = fields.Datetime(string='Invoice issued date', copy=False, readonly=True)
    invoice_receive_code = fields.Char('Invoice receive code', copy=False, readonly=True)
    invoice_issue_user_id = fields.Many2one('res.users', string='User issue invoice', copy=False, readonly=True,
                                            help="The user who issued the TS24 invoice for this invoice")

    total_in_word = fields.Char(string='In words', compute='_compute_num2words')

    @api.multi
    def _compute_num2words(self):
        for r in self:
            r.total_in_word = r.num2words(r.amount_total, precision_rounding=r.currency_id.rounding)

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

        # if self.type not in ['out_invoice', 'out_refund']:
        #     raise UserError(_(
        #         "Could not get S-Invoice display file as the invoice %s is neither a customer invoice nor customer credit note.")
        #                     % (self.number or self.legal_number,))
        # if self.sinvoice_state == 'not_issued':
        #     raise UserError(
        #         _("S-Invoice has not been issued for this invoice %s") % (self.number or self.legal_number,))
        if not self.legal_number:
            raise UserError(_(
                "The invoice %s has no legal number. This could be a data inconsitant problem. Please contact your service provider for help")
                            % self.legal_number)
        request_data = {
            'maNhanHoaDon': self.invoice_receive_code,
            'fileType': file_type

            # 'supplierTaxCode': self.company_id.vat,
            # 'invoiceNo': self.legal_number,
            # 'templateCode': self._get_sinvoice_template_name(),
            # 'fileType': file_type

        }
        auth = self.company_id.get_sinvoice_auth_str()
        API_INVOICE_RECEIVE_CODE = str(self.company_id.get_sinvoice_presentation_file_url()) + '&maNhanHoaDon=' + str(
            self.invoice_receive_code)
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

    def _prepare_sinvoice_data(self):

        def phone_format(phone_number):
            # Sinvoice does not accept blank, minus and plus in customer phone number
            phone_number = phone_number.replace(' ', '').replace('-', '').replace('+', '00')
            return phone_number

        self._portal_ensure_token()

        # calculate total taxes
        item_invoice = self.invoice_line_ids._prepare_sinvoice_lines_data()
        total_amount_no_tax = 0
        total_amount_tax_0 = 0
        total_amount_without_tax_5 = 0
        total_amount_tax_5 = 0
        total_amount_without_tax_10 = 0
        total_amount_tax_10 = 0
        total_amount_without_tax_other = 0
        total_amount_tax_other = 0
        for line in item_invoice:
            if line['thueSuat'] == 5:
                total_amount_without_tax_5 += line['thanhTien']
                total_amount_tax_5 += line['tienThue']
            if line['thueSuat'] == 10:
                total_amount_without_tax_10 += line['thanhTien']
                total_amount_tax_10 += line['tienThue']
            if line['thueSuat'] == 8:
                total_amount_without_tax_other += line['thanhTien']
                total_amount_tax_other += line['tienThue']

        # Check customer name, company name
        customer_name = ''
        company_name = ''
        if self.partner_id.name:
            if self.partner_id.name == 'Khách lẻ (Người mua không lấy hóa đơn)':
                customer_name = 'Khách lẻ (Người mua không lấy hóa đơn)'
                company_name = ''
            elif self.team_id and self.team_id.name == 'TMĐT' and self.sale_channel_id and self.sale_channel_id.parent_id.name == 'TMĐT':
                customer_name = 'Khách lẻ (Người mua không lấy hóa đơn) - ' + str(self.sale_channel_id.name)
                company_name = ''
            # if self.partner_id.name == 'Khách lẻ (Người mua không lấy hóa đơn)' or self.partner_id.sea_partner_sale_channel_id.complete_name == 'TMĐT':
            #     customer_name = self.partner_id.name
            #     company_name = ''
            else:
                if self.customer_po_name and self.customer_po_code:
                    customer_name = self.customer_po_name + ' - ' + self.customer_po_code
                elif self.customer_po_name:
                    customer_name = self.customer_po_name
                elif self.customer_po_code:
                    customer_name = self.customer_po_code
                company_name = self.partner_id.name
        # Read numbers into words
        total_in_word = self.total_in_word
        if self.state == 'adjustment' and self.amount_total != 0:
            total_in_word = self.total_in_word.lower()

        # Check tinhTrangKyNguoiBan
        tinhTrangKyNguoiBan = 0
        if self.allow_sign_now:
            tinhTrangKyNguoiBan = 1

        # Check hinhThucThanhToan
        hinhThucThanhToan = 'TM/CK'
        if self.payment_term:
            hinhThucThanhToan = dict(self._fields['payment_term'].selection).get(self.payment_term)

        # Data push TS24
        return {
            "id_master": self.access_token,
            "guid_PhatHanh": self.company_id.get_sinvoice_guild_issue_str(),
            "soDonHang": self.number,
            "ngayDonHang": str(self.date_invoice),
            "maKhachHang": "",
            "tenKhachHang": customer_name,
            "tenDonVi": company_name,
            "maSoThue": self.vat_number or '',
            "maSoThueNN": "",
            "diaChi": self.address,
            "dienThoaiNguoiMua": '',
            "faxNguoiMua": "",
            "emailNguoiMua": self.email or '',
            "soTaiKhoan": "",
            "noiMoTaiKhoan": "",
            "hinhThucThanhToan": hinhThucThanhToan,
            "tongTienKCT": "",
            "tongTien0": "",
            "tongTienChuaVat5": str(total_amount_without_tax_5),
            "tongTienVat5": str(total_amount_tax_5),
            "tongTienChuaVat10": str(total_amount_without_tax_10),
            "tongTienVat10": str(total_amount_tax_10),
            "tongTienChuaVatKhac": str(total_amount_without_tax_other),
            "tongTienVatKhac": str(total_amount_tax_other),
            "tongTienHang": str(self.amount_untaxed),
            "tongTienThue": str(self.amount_tax),
            "tongTienCKGG": "",
            "tienChiPhiKhac": "",
            "tongTienTT": str(self.amount_total),
            "soTienBangChu": total_in_word + ' đồng.',
            "ngayHoaDon": '',
            "tinhTrangHoaDon": 0,
            "loaiTienTe": 'VND',
            "tyGia": "1",
            "tinhTrangKyNguoiBan": tinhTrangKyNguoiBan,
            "tinhLaiSoTien": "0",
            "loiKhongTaoHoaDon": "0",
            "hienThiNgoaiTe": "0",
            "dongbohoadon": "1",
            "listMasterCT": self.invoice_line_ids._prepare_sinvoice_lines_data(),
        }

    def _prepare_update_vals_after_issuing(self, returned_vals):
        return {
            'invoice_transaction_id': returned_vals['hoaDonObjectReturn']['guid_PX'],
            'invoice_issued_date': fields.Datetime.now(),
            'legal_number': returned_vals['hoaDonObjectReturn']['so'],
            'invoice_receive_code': returned_vals['hoaDonObjectReturn']['maNhanHoaDon'],
            'invoice_issue_user_id': self.env.user.id,
            'state': 'issued',
            'symbol_code': returned_vals['hoaDonObjectReturn']['kyHieu'],
            'invoice_date_from_ts24': returned_vals['hoaDonObjectReturn']['ngay'],
        }

    def _issue_invoice(self):
        self.ensure_one()
        # Check Invoice
        if self.state != 'open':
            raise UserError(_('You cannot issue Invoice'))

        # Check API info settings for companies
        if not self.company_id.sinvoice_enabled:
            raise UserError(_('You cannot issue Invoice while not setting info API\n'
                              'Go to Accounting > Configuration > Settings and check S-Invoice Enable, '
                              'enter the provided API info'))

        auth_str = self.company_id.get_sinvoice_auth_str()
        error_url = False
        error_url_value = ''
        error = False
        error_message = []
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
            json_object = self._prepare_sinvoice_data()
            url = self.company_id.get_sinvoice_create_url()
            url_log = json.dumps(url)
            print('URL', url)
            print('Data', json_object)
            _logger.info("URL: %s", url_log)
            log_file = json.dumps(json_object)
            _logger.info("Issue Push Data: %s", log_file)
            if returned_vals['hoaDonObjectReturn']:
                self.write(self._prepare_update_vals_after_issuing(returned_vals))
            else:
                error = True
                error_message = returned_vals
        except Exception as e:
            error_url = True
            error_url_value += str(e)
        if error_url:
            raise UserError(_("Something went wrong when issuing the E-Invoice: %s") % str(error_url_value))
        if error:
            raise UserError(_("%s") % error_message['objKetQua']['moTaKetQua'])

    def _edit_invoice(self):
        self.ensure_one()

        auth_str = self.company_id.get_sinvoice_auth_str()
        json_object = self._prepare_sinvoice_data()
        json_object['id_master'] = 'Edit_Invoice_' + str(self.legal_number)
        json_object['maNhanHoaDon'] = self.invoice_receive_code

        error_url = False
        error_url_value = ''
        error = False
        error_message = []
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
            print('data', json_object)
            log_file = json.dumps(json_object)
            _logger.info("EDIT TS24 INVOICE: %s", log_file)
            if returned_vals['hoaDonObjectReturn']:
                self.write(self._prepare_update_vals_after_issuing(returned_vals))
            else:
                error = True
                error_message = returned_vals
            # if returned_vals['hoaDonObjectReturn']:
            #     self.write(self._prepare_update_vals_after_issuing(returned_vals))
        # except Exception as e:
        #     print(e)
        except Exception as e:
            error_url = True
            error_url_value += str(e)
        if error_url:
            raise UserError(_("Something went wrong when issuing the E-Invoice: %s") % str(error_url_value))
        if error:
            raise UserError(_("%s") % error_message['objKetQua']['moTaKetQua'])

    def _get_original_invoice_adjustment(self):
        obj = self.env['invoice.consolidation'].search([])
        if self.invoice_link:
            for item in self.env['invoice.consolidation'].search([('id', '!=', self.id)]):
                if item.invoice_link:
                    if self.invoice_link == item.invoice_link:
                        return item
        else:
            for rec in obj:
                if rec.origin:
                    if ''.join(self.original) in ''.join(rec.origin):
                        return rec
                    if len(rec.origin) > 20 and ''.join(sorted(self.original)) == ''.join(sorted(rec.origin)):
                        return rec
                if rec.original:
                    if ''.join(self.original) in ''.join(rec.original):
                        print(rec.name)
                        return rec
                    if len(rec.original) > 20 and ''.join(sorted(self.original)) == ''.join(sorted(rec.original)):
                        return rec

    def _get_original_invoice_replacement(self):
        obj = self.env['invoice.consolidation'].search([])
        if self.invoice_link:
            for item in self.env['invoice.consolidation'].search([('id', '!=', self.id)]):
                if item.invoice_link:
                    if self.invoice_link == item.invoice_link:
                        return item
        else:
            for rec in obj:
                if rec.origin:
                    if ''.join(self.original) in ''.join(rec.origin):
                        return rec
                    if len(rec.origin) > 20 and ''.join(sorted(self.original)) == ''.join(sorted(rec.origin)):
                        return rec
                if rec.original:
                    if ''.join(self.original) in ''.join(rec.original):
                        return rec
                    if len(rec.original) > 20 and ''.join(sorted(self.original)) == ''.join(sorted(rec.original)):
                        return rec

    def _get_original_invoice_cancel(self):
        obj = self.env['invoice.consolidation'].search([])
        if self.invoice_link:
            for item in self.env['invoice.consolidation'].search([('id', '!=', self.id)]):
                if item.invoice_link:
                    if self.invoice_link == item.invoice_link:
                        return item
        else:
            for rec in obj:
                if rec.origin:
                    if len(rec.origin) > 20:
                        if ''.join(sorted(self.original)) == ''.join(sorted(rec.origin)):
                            return rec
                    else:
                        if ''.join(self.original) in ''.join(rec.origin):
                            return rec
                if rec.original:
                    if len(rec.original) > 20:
                        if ''.join(sorted(self.original)) == ''.join(sorted(rec.original)):
                            return rec
                    else:
                        if ''.join(self.original) in ''.join(rec.original):
                            return rec
            # for rec in obj:
            #     if rec.origin:
            #         if ''.join(self.original) in ''.join(rec.origin) \
            #                 or ''.join(sorted(self.original)) == ''.join(sorted(rec.origin)):
            #             return rec
            #     if rec.original:
            #         if ''.join(self.original) in ''.join(rec.original) \
            #                 or ''.join(sorted(self.original)) == ''.join(sorted(rec.original)):
            #             return rec

    def _prepare_update_vals_after_adjustment(self, returned_vals):
        return {
            'invoice_transaction_id': returned_vals['hoaDonObjectReturn']['guid_PX'],
            'invoice_issued_date': fields.Datetime.now(),
            'legal_number': returned_vals['hoaDonObjectReturn'][
                                'so'] + ' Adjustment for Invoice ' + self._get_original_invoice_adjustment().legal_number,
            'invoice_receive_code': returned_vals['hoaDonObjectReturn']['maNhanHoaDon'],
            'invoice_issue_user_id': self.env.user.id,
            'state': 'adjusted',
            'symbol_code': returned_vals['hoaDonObjectReturn']['kyHieu'],
            'invoice_date_from_ts24': returned_vals['hoaDonObjectReturn']['ngay'],
        }

    def _prepare_update_vals_after_replacement(self, returned_vals):
        origin = self._get_original_invoice_replacement()
        origin.update({
            'state': 'cancelled'
        })
        return {
            'invoice_transaction_id': returned_vals['hoaDonObjectReturn']['guid_PX'],
            'invoice_issued_date': fields.Datetime.now(),
            'legal_number': returned_vals['hoaDonObjectReturn'][
                                'so'] + ' Replace for Invoice ' + self._get_original_invoice_replacement().legal_number,
            'invoice_receive_code': returned_vals['hoaDonObjectReturn']['maNhanHoaDon'],
            'invoice_issue_user_id': self.env.user.id,
            'state': 'replaced',
            'symbol_code': returned_vals['hoaDonObjectReturn']['kyHieu'],
            'invoice_date_from_ts24': returned_vals['hoaDonObjectReturn']['ngay'],
        }

    def _prepare_update_vals_after_cancel(self):
        origin = self._get_original_invoice_cancel()
        origin.update({
            'state': 'cancelled'
        })
        return {
            'invoice_issued_date': fields.Datetime.now(),
            'legal_number': 'Cancel for Invoice ' + self._get_original_invoice_cancel().legal_number,
            'invoice_issue_user_id': self.env.user.id,
            'state': 'cancelled',
        }

    def _adjustment_invoice(self):
        data_adjustment = {
            'objInvoceMasterOld': {
                "manhanHoaDon_Ref": self._get_original_invoice_adjustment().invoice_receive_code
            },
            'objMasterReplace': self._prepare_sinvoice_data()
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        error = False
        error_message = []
        try:
            req = requests.post(
                self.company_id.get_sinvoice_adjustment_url(),
                data=json.dumps(data_adjustment),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            log_file = json.dumps(data_adjustment)
            _logger.info("Issue Adjustmemnt Data: %s", log_file)
            if returned_vals['hoaDonObjectReturn']:
                self.write(self._prepare_update_vals_after_adjustment(returned_vals))
            else:
                error = True
                error_message = returned_vals
        except Exception as e:
            print(e)
        if error:
            raise UserError(_("%s") % error_message['objKetQua']['moTaKetQua'])

    def _replacement_invoice(self):
        data_replacement = {
            'objInvoceMasterOld': {
                "manhanHoaDon_Ref": self._get_original_invoice_replacement().invoice_receive_code
            },
            'objMasterReplace': self._prepare_sinvoice_data()
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        error = False
        error_message = []
        try:
            req = requests.post(
                self.company_id.get_sinvoice_replacement_url(),
                data=json.dumps(data_replacement),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            log_file = json.dumps(data_replacement)
            _logger.info("Issue Replacement Data: %s", log_file)
            if returned_vals['hoaDonObjectReturn']:
                self.write(self._prepare_update_vals_after_replacement(returned_vals))
            else:
                error = True
                error_message = returned_vals
        except Exception as e:
            print(e)
        if error:
            raise UserError(_("%s") % error_message['objKetQua']['moTaKetQua'])

    def _cancel_invoice(self):
        _logger.info("Invoice Cancel : %s", self._get_original_invoice_cancel())
        data_cancel = {
            "manhanHoaDon_Ref": self._get_original_invoice_cancel().invoice_receive_code
        }

        auth_str = self.company_id.get_sinvoice_auth_str()
        error = False
        error_message = []
        try:
            req = requests.post(
                self.company_id.get_sinvoice_cancel_url(),
                data=json.dumps(data_cancel),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            log_file = json.dumps(data_cancel)
            _logger.info("Issue Canncel Data: %s", log_file)
            if returned_vals['objKetQua']['moTaKetQua'] == 'Xóa hóa đơn thành công':
                self.write(self._prepare_update_vals_after_cancel())
            else:
                error = True
                error_message = returned_vals
        except Exception as e:
            print(e)
        if error:
            raise UserError(_("%s") % error_message['objKetQua']['moTaKetQua'])

    def issue_invoices(self):
        self = self.sorted('date_invoice')
        for r in reversed(self):
            r._issue_invoice()

    def edit_invoices(self):
        self.ensure_one()
        self = self.sorted('date_invoice')
        for r in reversed(self):
            r._edit_invoice()

    def action_issue_invoices(self):
        self.issue_invoices()

    def action_edit_invoices(self):
        self.edit_invoices()

    def action_adjustment_invoice(self):
        self._adjustment_invoice()

    def action_replacement_invoice(self):
        self._replacement_invoice()

    def action_cancel_invoice(self):
        self._cancel_invoice()

    # Auto sign TS24 invoices at a preset time
    def auto_sign_invoice(self):
        auth_str = self.company_id.get_sinvoice_auth_str()
        url_sign = self.company_id.get_sinvoice_sign_url() + '&maNhanHoaDon=' + self.invoice_receive_code
        try:
            req = requests.post(
                url_sign,
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            log_url = json.dumps(url_sign)
            log_file = json.dumps(returned_vals)
            _logger.info("URL Sign: %s", log_url)
            _logger.info("Auto Sign: %s", log_file)
            if returned_vals['hoaDonObjectReturn']:
                self.update({
                    'invoice_sign_status': 'yes',
                })
        except Exception as e:
            print(e)

    def search_invoice_ts24(self):
        search_param = {
            "tuNgayXHD": "",
            "denNgayXHD": "",
            "maSoThue": "",
            "idPhatHanh": "",
            "maNhanHoaDon": self.invoice_receive_code,
            "id_Master": "",
            "keySearch": ""
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        try:
            req = requests.post(
                self.company_id.get_sinvoice_search_url(),
                data=json.dumps(search_param),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            print(returned_vals)
            invoice_sign_status = returned_vals['listHoaDonObjectSearch'][0]['tinhTrangKyNguoiBan']
            if invoice_sign_status == "":
                self.auto_sign_invoice()
            else:
                self.update({
                    'invoice_sign_status': 'yes',
                })
        except Exception as e:
            print(e)

    def search_invoice(self):
        search_param = {
            "tuNgayXHD": "",
            "denNgayXHD": "",
            "maSoThue": "",
            "idPhatHanh": "",
            "maNhanHoaDon": self.invoice_receive_code,
            "id_Master": "",
            "keySearch": ""
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        try:
            req = requests.post(
                self.company_id.get_sinvoice_search_url(),
                data=json.dumps(search_param),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            print(returned_vals)
        except Exception as e:
            print(e)

    # LOOKUP INVOICE HAVE TAX AUTHORITY CODE
    def lookup_invoice(self):
        lookup_param = {
            "tuNgay": "",
            "denNgay": "",
            "maSoThue": "",
            "idPhatHanh": "",
            "maNhanHoaDon": self.invoice_receive_code,
            "id_Master": ""
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        try:
            req = requests.post(
                self.company_id.get_sinvoice_look_up_url(),
                data=json.dumps(lookup_param),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            if returned_vals['listHoaDonObjectSearch']:
                if returned_vals['listHoaDonObjectSearch'][0]['mccqt']:
                    self.update({'cqt_code_status': 'yes'})
                    self.send_email_invoice()
        except Exception as e:
            print(e)

    # SEND EMAIL INVOICE
    def send_email_invoice(self):
        listEmail = []
        if self.email:
            listEmail = self.email.split(';')

        email_param = {
            "id_Master": "",
            "manhanHoaDon": self.invoice_receive_code,
            "listEmail": listEmail
        }
        auth_str = self.company_id.get_sinvoice_auth_str()
        try:
            req = requests.post(
                self.company_id.get_sinvoice_send_email_url(),
                data=json.dumps(email_param),
                headers={"Content-type": "application/json; charset=utf-8"},
                timeout=SINVOICE_TIMEOUT,
                auth=auth_str
            )
            req.raise_for_status()
            returned_vals = req.json()
            # if returned_vals['objKetQua']['maKetQua'] == 'XHD_1111':
            self.update({'email_send_status': 'yes'})
        except Exception as e:
            print(e)

    def action_search_invoice_issue(self):
        domain = [('date_invoice', '=', date.today()),
                  ('state', 'in', ['issued', 'adjusted', 'replaced', 'cancelled']),
                  ('company_id.auto_sign_invoice', '!=', False),
                  ('invoice_sign_status', '!=', 'yes')]
        for invoice in self.env['invoice.consolidation'].search(domain):
            if invoice:
                invoice.search_invoice_ts24()

    def action_cron_sign_invoice(self):
        self.action_search_invoice_issue()

    # Auto sign TS24 invoice now if allow_sign_now is enabled
    def action_search_invoice_sign_now(self):
        domain = [('date_invoice', '=', date.today()),
                  ('state', 'in', ['issued', 'adjusted', 'replaced', 'cancelled']),
                  ('allow_sign_now', '!=', False),
                  ('invoice_sign_status', '!=', 'yes')]
        for invoice in self.env['invoice.consolidation'].search(domain):
            if invoice:
                invoice.search_invoice_ts24()

    def action_cron_sign_invoice_now(self):
        self.action_search_invoice_sign_now()

    # ACTION AUTO SEND EMAIL
    def action_search_invoice_send_email(self):
        domain = [('date_invoice', '=', date.today()),
                  ('state', 'in', ['issued', 'adjusted', 'replaced', 'cancelled']),
                  ('invoice_sign_status', '=', 'yes'),
                  ('email_send_status', '!=', 'yes')]
        for invoice in self.env['invoice.consolidation'].search(domain):
            if invoice:
                invoice.lookup_invoice()

    def action_cron_send_email(self):
        self.action_search_invoice_send_email()

    # Start Test
    # def action_reset_invoice(self):
    #     self.state = 'open'
    # def action_reset_adjusted(self):
    #     self.state = 'adjustment'
    # End Test
