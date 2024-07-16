from odoo import models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, float_round


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    def _is_sinvoice_deduction_line(self):
        prec = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        return (float_compare(self.quantity, 0.0, precision_digits=prec) == -1 or self.invoice_id.type == 'out_refund')

    def _prepare_sinvoice_line_uom_name(self):
        """
        Prepare name of UoM in both Vietnamese and English when needed
        """
        if not self.uom_id:
            return ''
        vietnam_lang = self.env.ref('base.lang_vi_VN')
        uom_name = self.uom_id.with_context(lang=vietnam_lang.code).name
        # add English subtitle for foreign customers
        if self.invoice_id._sinvoice_need_english():
            us_lang = self.env.ref('base.lang_en')
            uom_name += "\n(%s)" % self.uom_id.with_context(lang=us_lang.code).name
        return uom_name

    def _get_invoice_uom(self):
        if self.product_id.sea_unit_of_measure:
            return self.product_id.sea_unit_of_measure
        else:
            raise UserError(_('%s, has not set units yet.!') % (self.product_id.display_name))

    def standardize_sinvoice_item_name(self, item_name):
        journal = self.invoice_id.journal_id
        if journal.sinvoice_item_name_new_line_replacement:
            item_name = item_name.replace("\n", journal.sinvoice_item_name_new_line_replacement)
            if item_name.find(']'):
                index = item_name.index(']') + 2
                item_name = item_name[index:]
        return item_name
    
    def _get_invoice_line_name_from_product(self):
        res = super(AccountInvoiceLine, self)._get_invoice_line_name_from_product()
        invoice_type = self.invoice_id.type
        if invoice_type == 'out_invoice':
            product = self.product_id
            if product:
                if product.description_sale:
                    is_deduction_line = self._is_sinvoice_deduction_line()
                    res = product.with_context(lang=self.env.ref('base.lang_vi_VN').code).description_sale
                    if is_deduction_line:
                        res = '[Điều chỉnh giảm] ' + res
                    res = self.standardize_sinvoice_item_name(res)
                    if self.invoice_id._sinvoice_need_english():
                        res += ' '
                        if is_deduction_line:
                            res += '[Deduction Adjustment] '
                        res += '(%s)' % self.standardize_sinvoice_item_name((product.with_context(lang=self.env.ref('base.lang_en').code).description_sale))
        return res
    
    def _prepare_sinvoice_line_name(self):
        """
        Prepare a string type data for S-Invoice itemName in both Vietnamese and English when needed
        """

        def get_item_name_by_lang(sinvoice_item_name, lang):
            if sinvoice_item_name == 'invoice_line_product' and self.product_id:
                item_name = self.product_id.with_context(lang=lang).name
            else:
                item_name = self.with_context(lang=lang).name
            return item_name

        is_deduction_line = self._is_sinvoice_deduction_line()
        item_name = ''
        # get product description for itemname
        if self.invoice_id.journal_id.sinvoice_item_name == 'invoice_line_name':
            return self.standardize_sinvoice_item_name(self.name)
        
        # Vietnamese is required by the state so we take the Vietnamese language here for using in context
        vietnam_lang = self.env.ref('base.lang_vi_VN')
        item_name = get_item_name_by_lang(self.invoice_id.journal_id.sinvoice_item_name, vietnam_lang.code)
        if is_deduction_line:
            item_name = '[Điều chỉnh giảm] ' + item_name

        # add English subtitle for foreign customers
        if self.invoice_id._sinvoice_need_english() and self.product_id:
            us_lang = self.env.ref('base.lang_en')
            item_name += ' '
            if is_deduction_line:
                item_name += ' [Deduction Adjustment] '
            item_name += '(%s)' % get_item_name_by_lang(self.invoice_id.journal_id.sinvoice_item_name, us_lang.code)
        item_name = self.standardize_sinvoice_item_name(item_name)
        return item_name

    def _prepare_sinvoice_line_data(self, sequence=None):
        """
        Hook method for potential inheritance
        """
        self.ensure_one()
        prec = self.env['decimal.precision'].precision_get('Product Price')
        data = {
            # 'lineNumber': sequence or self.sequence
            "soThuTu": round(sequence) or round(self.sequence)
            }
        if self.display_type:
            data.update({
                'selection': 2,
                # 'itemName': self.name
                'tenHang': self.name

            })
        else:
            #check item name limit
            if len(self._prepare_sinvoice_line_name().encode('utf8')) > self.invoice_id.journal_id.sinvoice_item_name_limit:
                raise UserError(_("It seems that your product name/description in invoice lines was too long for SInvoice. You should shorten your product name/description to less than %s characters") % self.invoice_id.journal_id.sinvoice_item_name_limit)
                
            # calculate tax
            taxes_count = len(self.invoice_line_tax_ids)
            if taxes_count > 1:
                raise UserError(_("""The line containing the product %s comes with more than one tax which is not supported by S-Invoice.
                You may set some taxes to get their value included in the price to ensure that there is no more than one tax on a single line.""")
                % self.product_id.display_name)
            elif taxes_count == 0:
                raise UserError(_("""The line containing the product %s comes with no tax.""") % self.product_id.display_name)

            if float_is_zero(self.price_subtotal, precision_digits=prec):
                taxPercentage = 0.0
            else:
                taxPercentage = (self.price_total - self.price_subtotal) / self.price_subtotal * 100

            if taxes_count == 1:
                if self.invoice_line_tax_ids.amount_type == 'percent':
                    taxPercentage = self.invoice_line_tax_ids.amount
                exemption_group = self.env.ref('l10n_vn_c200.tax_group_exemption').id
                if self.invoice_line_tax_ids.tax_group_id.id == exemption_group:
                    taxPercentage = -2

            if self._is_sinvoice_deduction_line():
                data['isIncreaseItem'] = False

            # Check TAX
            tax_type = self.invoice_line_tax_ids.name
            if tax_type == 'KCT':
                tax = 'KCT'
            elif tax_type == 'KKKNT':
                tax = 'KKKNT'
            else:
                tax = round(self.invoice_line_tax_ids.amount)

            data.update({
                # 'itemName': self._prepare_sinvoice_line_name(),
                'tenHang': self._prepare_sinvoice_line_name(),

                # 'unitName': self._prepare_sinvoice_line_uom_name()
                'donViTinh': self._get_invoice_uom().name

            })

            if self.invoice_line_tax_ids.price_include:
                price_unit = round(self.price_unit / (1+taxPercentage/100))
            else:
                price_unit = self.price_unit
            # S-Invoice does not accept negative quantity while Odoo does
            quantity = abs(self.quantity)
            # S-Invoice does not accept negative Untaxed Subtotal while Odoo does
            price_subtotal = abs(self.quantity) * price_unit
            # S-Invoice does not accept negative Taxed Subtotal while Odoo does
            price_total = abs(self.price_total - self.price_tax)
            data.update({

                "idSTT": "",
                "maHang": self.product_id.default_code,
                # "tenHang": "self.invoice_line_ids._get_invoice_line_name_from_product()",
                # "donViTinh": "self.invoice_line_ids._prepare_sinvoice_line_uom_name()",
                "soLuong": quantity,
                # "donGia": float_round(price_unit * (1 - self.discount / 100), precision_digits=prec),
                "donGia": price_unit,
                "thanhTien": price_total,
                "tyLeCKGG": 0,
                "thanhTienCKGG": "",
                "thueSuat": tax,
                "tienThue": self.price_tax,
                "tongTien": price_total,
                "khuyenMai": "1",
                "thueTTDB": "",
                "khongHienThi": 0,
                "maSoLo": "",
                "ngayHetHan": "",
                "loaiDieuChinh": 0,
                "hoaDonMoRongCT": ""

                # 'itemCode': self.product_id.default_code,
                # 'unitPrice': float_round(price_unit * (1 - self.discount / 100), precision_digits=prec),
                # 'quantity': quantity,
                # 'itemTotalAmountWithoutTax': price_subtotal,
                # 'taxPercentage': taxPercentage,
                # 'taxAmount': price_total - price_subtotal,
                # 'discount': 0,
                # 'itemDiscount': 0,
                # 'itemTotalAmountWithTax': price_total
                })
        return data

    def _prepare_sinvoice_lines_data(self):
        invoice_ids = self.mapped('invoice_id')
        if len(invoice_ids) > 1:
            raise ValidationError(_("All the invoice lines must belong to the same invoice."))
        data = []
        sequence = 1
        for r in self:
            data.append(r._prepare_sinvoice_line_data(sequence))
            sequence += 1
        return data
