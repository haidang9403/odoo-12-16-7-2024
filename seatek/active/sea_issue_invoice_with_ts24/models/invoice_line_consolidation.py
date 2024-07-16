from odoo import models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, float_round
import datetime


class InvoiceLineConsolidation(models.Model):
    _name = 'invoice.line.consolidation'
    _inherit = 'invoice.line.consolidation'

    def _get_invoice_uom(self):
        if self.product_id.sea_unit_of_measure:
            return self.product_id.sea_unit_of_measure
        else:
            raise UserError(_('%s, has not set units yet.!') % (self.product_id.display_name))

    # def _clear_unit_for_drink(self):
    #     if self.product_id.name == 'Thức uống':
    #         return ''
    #     else:
    #         return self._get_invoice_uom().name
    #
    # def _clear_qty_for_drink(self):
    #     if self.product_id.name == 'Thức uống':
    #         return ''
    #     else:
    #         return self.quantity
    #
    # def _clear_price_unit_for_drink(self):
    #     if self.product_id.name == 'Thức uống':
    #         return ''
    #     else:
    #         return self.price_unit

    def _get_product_name(self):
        if self.quantity:
            if self.quantity < 0:
                if self.product_id.name == 'Chiết khấu thương mại':
                    return self.description
                else:
                    obj = self.env['invoice.consolidation'].search([])
                    re = []
                    for rec in obj:
                        if rec.origin:
                            if ''.join(self.invoice_id.original) in ''.join(rec.origin):
                                re.append(rec)
                            if len(rec.origin) > 20 and ''.join(sorted(self.invoice_id.original)) == ''.join(
                                    sorted(rec.origin)):
                                re.append(rec)
                        if rec.original:
                            if ''.join(self.invoice_id.original) in ''.join(rec.original):
                                re.append(rec)
                            if len(rec.original) > 20 and ''.join(sorted(self.invoice_id.original)) == ''.join(
                                    sorted(rec.original)):
                                re.append(rec)
                    for rec in re:
                        item_name = ''
                        if self.description:
                            item_name += self.description
                        if rec.legal_number:
                            item_name += (' của hóa đơn số ' + rec.legal_number)
                        if rec.symbol_code:
                            item_name += (', ký hiệu ' + rec.symbol_code)
                        if rec.invoice_issued_date:
                            dt = datetime.datetime.strptime(rec.invoice_date_from_ts24, '%m/%d/%Y').date()
                            dt_str = datetime.datetime.strftime(dt, '%d/%m/%Y')
                            item_name += (', ngày ' + dt_str)
                        return item_name
            else:
                return self.description
        else:
            obj = self.env['invoice.consolidation'].search([])
            re = []
            for rec in obj:
                if rec.origin:
                    if ''.join(self.invoice_id.original) in ''.join(rec.origin):
                        re.append(rec)
                    if len(rec.origin) > 20 and ''.join(sorted(self.invoice_id.original)) == ''.join(
                            sorted(rec.origin)):
                        re.append(rec)
                if rec.original:
                    if ''.join(self.invoice_id.original) in ''.join(rec.original):
                        re.append(rec)
                    if len(rec.original) > 20 and ''.join(sorted(self.invoice_id.original)) == ''.join(
                            sorted(rec.original)):
                        re.append(rec)
            for rec in re:
                item_name = ''
                if self.description:
                    item_name += self.description
                if rec.legal_number:
                    item_name += (' của hóa đơn số ' + rec.legal_number)
                if rec.symbol_code:
                    item_name += (', ký hiệu ' + rec.symbol_code)
                if rec.invoice_issued_date:
                    dt = datetime.datetime.strptime(rec.invoice_date_from_ts24, '%m/%d/%Y').date()
                    dt_str = datetime.datetime.strftime(dt, '%d/%m/%Y')
                    item_name += (', ngày ' + dt_str)
                return item_name

    def _prepare_sinvoice_line_data(self, sequence=None):
        """
        Hook method for potential inheritance
        """
        self.ensure_one()
        prec = self.env['decimal.precision'].precision_get('Product Price')
        data = {
            "soThuTu": round(sequence) or round(self.sequence)
        }
        # if self.display_type:
        #     data.update({
        #         'selection': 2,
        #         # 'itemName': self.name
        #         'tenHang': self.name
        #
        #     })
        # else:
        # check item name limit
        # if len(self._prepare_sinvoice_line_name().encode(
        #         'utf8')) > self.invoice_id.journal_id.sinvoice_item_name_limit:
        #     raise UserError(_(
        #         "It seems that your product name/description in invoice lines was too long for SInvoice. You should shorten your product name/description to less than %s characters") % self.invoice_id.journal_id.sinvoice_item_name_limit)

        # calculate tax
        taxes_count = len(self.tax_id)
        if taxes_count > 1:
            raise UserError(_("""The line containing the product %s comes with more than one tax which is not supported by S-Invoice.
                You may set some taxes to get their value included in the price to ensure that there is no more than one tax on a single line.""")
                            % self.product_id.display_name)
        elif taxes_count == 0:
            raise UserError(
                _("""The line containing the product %s comes with no tax.""") % self.product_id.display_name)

        if float_is_zero(self.price_total, precision_digits=prec):
            taxPercentage = 0.0
        else:
            taxPercentage = (self.price_total - self.price_total) / self.price_total * 100

        if taxes_count == 1:
            if self.tax_id.amount_type == 'percent':
                taxPercentage = self.tax_id.amount
            exemption_group = self.env.ref('l10n_vn_c200.tax_group_exemption').id
            if self.tax_id.tax_group_id.id == exemption_group:
                taxPercentage = -2

        # Check TAX
        tax_type = self.tax_id.name
        if tax_type == 'KCT':
            tax = 'KCT'
        elif tax_type == 'KKKNT':
            tax = 'KKKNT'
        else:
            tax = round(self.tax_id.amount)

        # if self.tax_id.price_include:
        #     price_unit = round(self.price_unit / (1 + taxPercentage / 100))
        # else:
        #     price_unit = self.price_unit
        #
        # # Clear Unit, Quantity, Price Unit for Item is Drink or adjustment info
        # if self.product_id.name == 'Thức uống' or self.product_id.name == 'Điều chỉnh thông tin' or\
        #     self.product_id.name == 'Phí Vận Chuyển' or self.product_id.name == 'Phí Dịch Vụ':
        #     unit_value = ''
        #     quantity_value = '0'
        #     price_unit_value = '0'
        # else:
        #     unit_value = str(self._get_invoice_uom().name)
        #     quantity_value = str(self.quantity)
        #     price_unit_value = str(price_unit)
        #
        # price_tax = self.price_total - self.price_subtotal

        price_tax = self.price_total - self.price_subtotal

        if self.tax_id.price_include:
            price_unit = round((self.price_subtotal / self.quantity), 2)
        else:
            price_unit = round(self.price_unit, 2)

        # Clear Unit, Quantity, Price Unit for Item is Drink or adjustment info
        if self.product_id.name == 'Thức uống' or self.product_id.name == 'Điều chỉnh thông tin' or \
                self.product_id.name == 'Phí Vận Chuyển' or self.product_id.name == 'Phí Dịch Vụ' or \
                self.product_id.name == 'Chiết khấu thương mại':
            unit_value = ''
            quantity_value = '0'
            price_unit_value = '0'
        else:
            unit_value = str(self._get_invoice_uom().name)
            quantity_value = str(self.quantity)
            price_unit_value = str(price_unit)

        # Check field KhuyenMai
        khuyen_mai = '1'
        if self.product_id.name == 'Chiết khấu thương mại':
            khuyen_mai = '3'

        data.update({
            "idSTT": "",
            "maHang": self.product_id.default_code,
            "tenHang": self._get_product_name(),
            "donViTinh": unit_value,
            "soLuong": quantity_value,
            "donGia": price_unit_value,
            "thanhTien": self.price_subtotal,
            "tyLeCKGG": 0,
            "thanhTienCKGG": "",
            "thueSuat": tax,
            "tienThue": price_tax,
            "tongTien": abs(self.price_total),
            "khuyenMai": khuyen_mai,
            "thueTTDB": "",
            "khongHienThi": 0,
            "maSoLo": "",
            "ngayHetHan": "",
            "loaiDieuChinh": 0,
            "hoaDonMoRongCT": ""
        })
        return data

    def _prepare_sinvoice_lines_data(self):
        invoice_ids = self.mapped('invoice_id')
        if len(invoice_ids) > 1:
            raise ValidationError(_("All the invoice lines must belong to the same invoice."))
        data = []
        sequence = 1
        tax_id_KKKNT = []
        for r in self:
            if r.product_id.name == 'Điều chỉnh thông tin':
                data.append(r._prepare_sinvoice_line_data(sequence))
            # Do not issue invoice line with price_total = 0
            # Add condition price_unit = 0 but exist check_push_ts24 continue push TS24
            if r.price_total != 0 or r.price_total == 0 and r.check_push_ts24:
                # No invoice with Tax line == 'KKKNT' for SEAFARM
                if r.invoice_id.company_id.sea_no_issue_invoice_line_tax_kkknt:
                    if r.tax_id.name != 'KKKNT':
                        tax_id_KKKNT.append(r.tax_id.name)
                        data.append(r._prepare_sinvoice_line_data(sequence))
                        sequence += 1
                    else:
                        tax_id_KKKNT.append(r.tax_id.name)
                else:
                    data.append(r._prepare_sinvoice_line_data(sequence))
                    sequence += 1
        if list(set(tax_id_KKKNT)) == ['KKKNT']:
            raise UserError(_('Do not issue invoices with products with tax KKKNT.'))
        else:
            return data
