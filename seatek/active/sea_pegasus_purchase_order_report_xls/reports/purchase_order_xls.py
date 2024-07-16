import base64
import pytz, io, base64, datetime
from pytz import timezone
from datetime import timedelta
import logging
from odoo import models, api
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class PurchaseOrderXLS(models.AbstractModel):
    _name = 'report.sea_pegasus_purchase_order_report_xls.purchase_order_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_address_format(self, company):
        address = ""
        if company.street:
            address += company.street + ", "
        if company.street2:
            address += company.street2 + ", "
        if company.city:
            address += company.city + ", "
        if company.country_id:
            address += company.country_id.name
        return address

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet1 = workbook.add_worksheet('Purchase Order')
        company_name = self.env.user.company_id.display_name
        company_phone = self.env.user.company_id.phone
        company_mail = self.env.user.company_id.email
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        f1 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Times New Roman', 'font_size': 10})
        f2 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 18,
             'font_color': '#00008B', 'font_name': 'Times New Roman'})
        f3 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Times New Roman', 'font_size': 12})
        f3_1 = workbook.add_format(
            {'bold': 1, 'bottom': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Times New Roman', 'font_size': 12})
        f4 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Times New Roman', 'font_size': 12})
        f5 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Times New Roman', 'font_size': 12})
        f6 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_color': '#0000FF',
             'font_name': 'Times New Roman', 'font_size': 12})
        f6_4 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Times New Roman', 'font_size': 12})
        f6_3 = workbook.add_format(
            {'bold': 1, 'bottom': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_color': '#FF0000',
             'font_name': 'Times New Roman', 'font_size': 12})
        f6_1 = workbook.add_format(
            {'bottom': 1, 'right': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Times New Roman', 'font_size': 12})
        f6_2 = workbook.add_format(
            {'bold': 1, 'bottom': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_color': '#0000FF',
             'font_name': 'Times New Roman', 'font_size': 12})
        f6_5 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_color': '#FF0000',
             'font_name': 'Times New Roman', 'font_size': 12})
        f7 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'left': 1, 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f7_1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_color': '#FF0000', 'font_name': 'Times New Roman'})
        f7_2 = workbook.add_format(
            {'bold': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_color': '#FF0000', 'font_name': 'Times New Roman'})
        f8 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12, 'underline': True,
             'font_name': 'Times New Roman'})
        f8_1 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'underline': True, 'font_name': 'Times New Roman'})
        f9 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f10 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        f11 = workbook.add_format(
            {'align': 'center', 'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f11_1 = workbook.add_format(
            {'align': 'left', 'border': 1, 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f12 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000',
             'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'})
        f13 = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#CCFFFF',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f14 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'bg_color': '#ADD8E6'})
        f15 = workbook.add_format(
            {'valign': 'vcenter', 'text_wrap': True, 'font_size': 12, 'font_name': 'Times New Roman'})
        f16 = workbook.add_format(
            {'italic': 1, 'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '#,##0',
             'font_size': 12, 'font_name': 'Times New Roman'})
        f17 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'})
        short_date = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd-mmm-yy',
             'font_name': 'Times New Roman', 'font_size': 12})
        border_short_date = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mmm'})
        money_bold_usd = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0.00', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_light_usd = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0.00', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_light_vnd = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        money_bold_vnd = workbook.add_format(
            {'border': 1, 'bold': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0', 'font_size': 12,
             'font_name': 'Times New Roman'})
        row_no = 0

        # Report Header
        worksheet1.set_column(0, 0, 9.29)
        worksheet1.set_column(1, 1, 16.14)
        worksheet1.set_column(2, 2, 37)
        worksheet1.set_column(3, 3, 8)
        worksheet1.set_column(4, 4, 8)
        worksheet1.set_column(5, 5, 17.14)
        worksheet1.set_column(6, 6, 11)
        worksheet1.set_column(7, 7, 10.57)

        worksheet1.insert_image(0, 0, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.25, 'y_scale': 0.2})
        worksheet1.merge_range(row_no, 5, row_no, 7, _('PM-QT-11.01 (05-01/06/2022)'), f1)
        row_no += 1
        worksheet1.merge_range(row_no, 5, row_no, 7, _('PURCHASE ORDER'), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 4, _('PO Number: '), f4)

        # Edit Purchase number (13/Jan/2023)
        purchase_number = objects.name.split('/')[0]

        if objects.partner_id.sea_business_code:
            worksheet1.write(row_no, 5, str(purchase_number) + '.' + str(objects.partner_id.sea_business_code) or '', f5)
        else:
            worksheet1.write(row_no, 5, str(purchase_number), f5)
        worksheet1.write(row_no, 6, _('Date: '), f4)
        worksheet1.write(row_no, 7, objects.date_order, short_date)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 4, _('Ref. Order: '), f4)
        worksheet1.write(row_no, 5, objects.origin or '', f4)
        worksheet1.write(row_no, 6, _('Date: '), f4)
        for obj in self.env['sale.order'].search([('name', '=', objects.origin)]):
            worksheet1.write(row_no, 7, obj.date_order, short_date)
        row_no += 1
        worksheet1.merge_range(row_no, 3, row_no, 4, _('Total of pages: '), f4)
        row_no += 2

        # TO
        worksheet1.write(row_no, 0, _('TO:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.partner_id.display_name, f6)
        row_no += 1
        worksheet1.write(row_no, 0, _('Address:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, self.get_address_format(objects.partner_id), f6)
        row_no += 1
        worksheet1.write(row_no, 0, _('Tel:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.partner_id.parent_id.phone or '', f6_2)
        worksheet1.write(row_no, 4, _('Fax:'), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, '', f6_1)
        row_no += 1
        worksheet1.write(row_no, 0, _('Email:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 7, objects.partner_id.email or '', f6)
        row_no += 1
        worksheet1.write(row_no, 0, _('Attn:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.partner_id.parent_id.name or '', f6_2)
        worksheet1.write(row_no, 4, _('Tel:'), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, '', f6_1)
        row_no += 2

        # FROM
        worksheet1.write(row_no, 0, _('FROM:'), f3)
        if objects.currency_id.name == 'VND':
            worksheet1.merge_range(row_no, 1, row_no, 7, company_name, f6_5)
        else:
            worksheet1.merge_range(row_no, 1, row_no, 7, objects.company_id.sea_company_foreign, f6_5)
        row_no += 1
        worksheet1.write(row_no, 0, _('Address:'), f3)
        for obj in self.env['res.partner'].search([('parent_id', '=', objects.company_id.partner_id.id)]):
            if obj.type == 'invoice':
                if objects.currency_id.name == 'VND':
                    if obj.name == 'VN':
                        worksheet1.merge_range(row_no, 1, row_no, 7, obj.street + ', ' + obj.city + '.', f3)
                else:
                    if obj.name == 'EN':
                        worksheet1.merge_range(row_no, 1, row_no, 7,
                                               obj.street + ', ' + obj.city + ', ' + obj.country_id.name + '.', f3)
        row_no += 1
        worksheet1.write(row_no, 0, _('Tel:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, company_phone or '', f6_4)
        worksheet1.write(row_no, 4, _('Fax:'), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, '', f6_1)
        row_no += 1
        worksheet1.write(row_no, 0, _('Email:'), f3)

        for obj in self.env['crm.team'].search([('member_ids', '=', objects.user_id.id)]):
            if obj.alias_name:
                worksheet1.merge_range(row_no, 1, row_no, 7, obj.alias_name + '@pegasuscorp.com.vn' or '', f12)
            else:
                worksheet1.merge_range(row_no, 1, row_no, 7, _('') or '', f12)

        row_no += 1
        worksheet1.write(row_no, 0, _('P.I.C:'), f3)
        worksheet1.merge_range(row_no, 1, row_no, 3, objects.user_id.partner_id.name or '', f6_3)
        worksheet1.write(row_no, 4, _('Tel:'), f3_1)
        worksheet1.merge_range(row_no, 5, row_no, 7, objects.user_id.partner_id.mobile or '', f6_1)
        row_no += 2

        worksheet1.merge_range(row_no, 0, row_no, 1, _('Dear Sir/Madam,'), f15)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 2,
                               _('As per our mutual agreement, please process our order as below'), f15)
        row_no += 2

        # Product
        worksheet1.merge_range(row_no, 0, row_no + 1, 0, _("Line's No."), f13)
        worksheet1.merge_range(row_no, 1, row_no, 2, _('Items'), f13)
        unit = ''
        for line in objects.order_line:
            if line.product_type == 'service':
                unit += 'Months '
            else:
                unit += 'Unit '
        worksheet1.merge_range(row_no, 3, row_no + 1, 3, unit.split(' ')[0], f13)
        worksheet1.merge_range(row_no, 4, row_no + 1, 4, _("Qty"), f13)
        worksheet1.merge_range(row_no, 5, row_no + 1, 5, _("Unit Price"), f13)
        worksheet1.merge_range(row_no, 6, row_no + 1, 6, _("Line's Value"), f13)
        worksheet1.merge_range(row_no, 7, row_no + 1, 7, _("Remark"), f13)
        row_no += 1
        worksheet1.write(row_no, 1, _('Code'), f13)
        worksheet1.write(row_no, 2, _('Description'), f13)
        row_no += 1
        if objects.sea_vessel_name:
            worksheet1.merge_range(row_no, 0, row_no, 1, _("Vessel Name"), f7)
            worksheet1.write(row_no, 2, (str(objects.sea_vessel_name.name).upper()), f7_1)
            worksheet1.write(row_no, 7, _(''), f7_2)
            row_no += 1

        def get_code(default_code):
            code_len = len(default_code)
            result = default_code[0: code_len - 4]
            check_months = default_code[code_len - 4: code_len]
            if check_months == check_months == '_03M' or check_months == '_06M' or check_months == '_09M' or check_months == '_12M' or check_months == '_18M' or check_months == '_24M':
                return result
            else:
                return default_code.split('_')[0]

        def get_unit_or_months(default_code):
            code_len = len(default_code)
            check_months = default_code[code_len - 4: code_len]
            result = default_code[code_len - 3: code_len - 1]
            if check_months == check_months == '_03M' or check_months == '_06M' or check_months == '_09M' or check_months == '_12M' or check_months == '_18M' or check_months == '_24M':
                return result
            else:
                return 'Pc'

        total_no_tax = 0
        subtotal_no_tax = 0
        seq_no_tax = 1
        check_type_tax_no = ''
        for line in objects.order_line:
            if line.taxes_id.name == 'Thuế GTGT-Không chịu thuế (PM)':
                check_type_tax_no = line.taxes_id.name
                worksheet1.write(row_no, 0, seq_no_tax, f11)
                seq_no_tax += 1
                worksheet1.write(row_no, 1, line.product_id.default_code.split('_')[0] or '', f11)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                    worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11_1)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11_1)
                worksheet1.write(row_no, 3, get_unit_or_months(line.product_id.default_code), f17)
                worksheet1.write(row_no, 4, line.product_qty, f11)
                if objects.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)

                total_no_tax += line.price_total
                subtotal_no_tax += line.price_subtotal
                row_no += 1
        if check_type_tax_no == 'Thuế GTGT-Không chịu thuế (PM)':
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Sub Total Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_no_tax, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_no_tax, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('X%'), f16)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, '', money_light_vnd)
            else:
                worksheet1.write(row_no, 6, '', money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            if objects.amount_untaxed == subtotal_no_tax:
                worksheet1.write(row_no, 5, _(''), f9)
            else:
                worksheet1.write(row_no, 5, _('1'), f9)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_no_tax, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_no_tax, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        subtotal_0 = 0
        total_tax_0 = 0
        total_0 = 0
        seq_0 = seq_no_tax
        total_tax = -1
        check_type_tax_0 = ''
        for line in objects.order_line:
            if line.taxes_id.amount == 0 and line.taxes_id.name == 'Thuế GTGT được khấu trừ 0%':
                check_type_tax_0 = 'Thuế GTGT được khấu trừ 0%'
                if total_tax == -1:
                    total_tax = line.taxes_id.amount
                worksheet1.write(row_no, 0, seq_0, f11)
                seq_0 += 1
                worksheet1.write(row_no, 1, get_code(line.product_id.default_code) or '', f11)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                    worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11_1)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11_1)
                worksheet1.write(row_no, 3, get_unit_or_months(line.product_id.default_code), f17)
                worksheet1.write(row_no, 4, line.product_qty, f11)
                if objects.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_0 += line.price_subtotal
                total_tax_0 += line.price_tax
                total_0 += line.price_total
                row_no += 1
        if check_type_tax_0 == 'Thuế GTGT được khấu trừ 0%':
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Sub Total Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_0, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_0, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('0%'), f16)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_0, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_0, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)

            if objects.amount_untaxed == subtotal_0:
                worksheet1.write(row_no, 5, _(''), f9)
            else:
                if subtotal_no_tax:
                    worksheet1.write(row_no, 5, _('2'), f9)
                else:
                    worksheet1.write(row_no, 5, _('1'), f9)

            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_0, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_0, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        subtotal_05 = 0
        total_tax_05 = 0
        total_05 = 0
        seq_5 = seq_0
        total_tax = -1
        for line in objects.order_line:
            if line.taxes_id.amount == 5:
                if total_tax == -1:
                    total_tax = line.taxes_id.amount
                worksheet1.write(row_no, 0, seq_5, f11)
                seq_5 += 1
                worksheet1.write(row_no, 1, get_code(line.product_id.default_code) or '', f11)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                    worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11_1)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11_1)
                worksheet1.write(row_no, 3, get_unit_or_months(line.product_id.default_code), f17)
                worksheet1.write(row_no, 4, line.product_qty, f11)
                if objects.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_05 += line.price_subtotal
                total_tax_05 += line.price_tax
                total_05 += line.price_total
                row_no += 1
        if total_tax == 5:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Sub Total Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_05, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_05, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('5%'), f16)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_05, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_05, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)

            if objects.amount_untaxed != subtotal_05:
                if not subtotal_no_tax or not subtotal_0:
                    worksheet1.write(row_no, 5, _('1'), f9)
                    if subtotal_no_tax or subtotal_0:
                        worksheet1.write(row_no, 5, _('2'), f9)
                else:
                    worksheet1.write(row_no, 5, _('3'), f9)
            else:
                worksheet1.write(row_no, 5, _(''), f9)

            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_05, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_05, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        subtotal_08 = 0
        total_tax_08 = 0
        total_08 = 0
        seq_08 = seq_5
        total_tax = -1
        for line in objects.order_line:
            if line.taxes_id.amount == 8:
                if total_tax == -1:
                    total_tax = line.taxes_id.amount
                worksheet1.write(row_no, 0, seq_08, f11)
                seq_08 += 1
                worksheet1.write(row_no, 1, get_code(line.product_id.default_code) or '', f11)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                    worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11_1)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11_1)
                worksheet1.write(row_no, 3, get_unit_or_months(line.product_id.default_code), f17)
                worksheet1.write(row_no, 4, line.product_qty, f11)
                if objects.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_08 += line.price_subtotal
                total_tax_08 += line.price_tax
                total_08 += line.price_total
                row_no += 1
        if total_tax == 8:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Sub Total Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_08, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_08, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('8%'), f16)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_08, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_08, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)

            if objects.amount_untaxed != subtotal_08:
                if subtotal_no_tax and subtotal_0 and subtotal_05:
                    worksheet1.write(row_no, 5, _('4'), f9)
                else:
                    if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or subtotal_0 and subtotal_05:
                        worksheet1.write(row_no, 5, _('3'), f9)
                    else:
                        if subtotal_no_tax or subtotal_0 or subtotal_05:
                            worksheet1.write(row_no, 5, _('2'), f9)
                        else:
                            worksheet1.write(row_no, 5, _('1'), f9)
            else:
                worksheet1.write(row_no, 5, _(''), f9)
            # if subtotal_no_tax and subtotal_0 and subtotal_05:
            #     worksheet1.write(row_no, 5, _('4'), f9)
            # else:
            #     if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or subtotal_0 and subtotal_05:
            #         worksheet1.write(row_no, 5, _('3'), f9)
            #     elif subtotal_no_tax or subtotal_0 or subtotal_05:
            #         worksheet1.write(row_no, 5, _('2'), f9)
            #     else:
            #         worksheet1.write(row_no, 5, _(''), f9)

            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_08, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_08, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        subtotal_10 = 0
        total_tax_10 = 0
        total_10 = 0
        seq_10 = seq_5
        total_tax = -1
        for line in objects.order_line:
            if line.taxes_id.amount == 10:
                if total_tax == -1:
                    total_tax = line.taxes_id.amount
                worksheet1.write(row_no, 0, seq_10, f11)
                seq_10 += 1
                worksheet1.write(row_no, 1, get_code(line.product_id.default_code) or '', f11)
                if line.product_id.type == 'service' and line.product_id.categ_id.name == 'Admiralty Vertor Chart Service':
                    worksheet1.write(row_no, 2, line.product_id.sea_product_variant_name, f11_1)
                else:
                    worksheet1.write(row_no, 2, line.product_id.name, f11_1)
                worksheet1.write(row_no, 3, get_unit_or_months(line.product_id.default_code), f17)
                worksheet1.write(row_no, 4, line.product_qty, f11)
                if objects.currency_id.name == 'VND':
                    worksheet1.write(row_no, 5, line.price_unit, money_light_vnd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_vnd)
                else:
                    worksheet1.write(row_no, 5, line.price_unit, money_light_usd)
                    worksheet1.write(row_no, 6, line.price_subtotal, money_light_usd)
                worksheet1.write(row_no, 7, line.remarks, f11)
                subtotal_10 += line.price_subtotal
                total_tax_10 += line.price_tax
                total_10 += line.price_total
                row_no += 1
        if total_tax == 10:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Sub Total Amount:'), f10)
            worksheet1.write(row_no, 5, _(''), f10)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, subtotal_10, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, subtotal_10, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f10)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Tax:'), f16)
            worksheet1.write(row_no, 5, _('10%'), f16)
            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_tax_10, money_light_vnd)
            else:
                worksheet1.write(row_no, 6, total_tax_10, money_light_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)

            if subtotal_no_tax and subtotal_0 and subtotal_05 and subtotal_08:
                worksheet1.write(row_no, 5, _('5'), f9)
            else:
                if subtotal_no_tax and subtotal_0 and subtotal_05 or \
                        subtotal_no_tax and subtotal_0 and subtotal_08 or \
                        subtotal_no_tax and subtotal_05 and subtotal_08 or \
                        subtotal_0 and subtotal_05 and subtotal_08:
                    worksheet1.write(row_no, 5, _('4'), f9)
                else:
                    if subtotal_no_tax and subtotal_0 or \
                            subtotal_no_tax and subtotal_05 or \
                            subtotal_no_tax and subtotal_08 or \
                            subtotal_0 and subtotal_05 or \
                            subtotal_0 and subtotal_08 or \
                            subtotal_05 and subtotal_08:
                        worksheet1.write(row_no, 5, _('3'), f9)
                    else:
                        if subtotal_no_tax or subtotal_0 or subtotal_05 or subtotal_08:
                            worksheet1.write(row_no, 5, _('2'), f9)
                        else:
                            worksheet1.write(row_no, 5, _(''), f9)
            # if subtotal_no_tax and subtotal_0 and subtotal_05:
            #     worksheet1.write(row_no, 5, _('4'), f9)
            # else:
            #     if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or subtotal_0 and subtotal_05:
            #         worksheet1.write(row_no, 5, _('3'), f9)
            #     elif subtotal_no_tax or subtotal_0 or subtotal_05:
            #         worksheet1.write(row_no, 5, _('2'), f9)
            #     else:
            #         worksheet1.write(row_no, 5, _(''), f9)

            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, total_10, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, total_10, money_bold_usd)
            worksheet1.write(row_no, 7, _(''), f9)
            row_no += 1

        if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or \
                subtotal_no_tax and subtotal_08 or subtotal_no_tax and subtotal_10 or \
                subtotal_0 and subtotal_05 or subtotal_0 and subtotal_08 or \
                subtotal_0 and subtotal_10 or subtotal_05 and subtotal_08 or \
                subtotal_05 and subtotal_10 or subtotal_08 and subtotal_10:
            worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount To be Paid:'), f9)

            if subtotal_no_tax and subtotal_0 and subtotal_05 and subtotal_08 and subtotal_10:
                worksheet1.write(row_no, 5, _('1 + 2 + 3 + 4 + 5'), f9)
            else:
                if subtotal_no_tax and subtotal_0 and subtotal_05 and subtotal_08 or \
                        subtotal_no_tax and subtotal_0 and subtotal_05 and subtotal_10 or \
                        subtotal_no_tax and subtotal_05 and subtotal_08 and subtotal_10 or \
                        subtotal_0 and subtotal_05 and subtotal_08 and subtotal_10:
                    worksheet1.write(row_no, 5, _('1 + 2 + 3 + 4'), f9)
                else:
                    if subtotal_no_tax and subtotal_0 and subtotal_05 or \
                            subtotal_no_tax and subtotal_0 and subtotal_08 or \
                            subtotal_no_tax and subtotal_0 and subtotal_10 or \
                            subtotal_no_tax and subtotal_05 and subtotal_08 or \
                            subtotal_no_tax and subtotal_05 and subtotal_10 or \
                            subtotal_no_tax and subtotal_08 and subtotal_10 or \
                            subtotal_0 and subtotal_05 and subtotal_08 or \
                            subtotal_0 and subtotal_05 and subtotal_10 or \
                            subtotal_0 and subtotal_08 and subtotal_10 or \
                            subtotal_05 and subtotal_08 and subtotal_10:
                        worksheet1.write(row_no, 5, _('1 + 2 + 3'), f9)
                    else:
                        worksheet1.write(row_no, 5, _('1 + 2'), f9)

            if objects.currency_id.name == 'VND':
                worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            else:
                worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            # if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or subtotal_no_tax and subtotal_10 or \
            #         subtotal_0 and subtotal_05 or subtotal_0 and subtotal_10 or subtotal_05 and subtotal_10:
            #     worksheet1.merge_range(row_no, 0, row_no, 4, _('Total Amount:'), f9)
            #     if subtotal_no_tax and subtotal_0 and subtotal_05 and subtotal_10:
            #         worksheet1.write(row_no, 5, _('1 + 2 + 3 + 4'), f9)
            #     else:
            #         if subtotal_no_tax and subtotal_0 and subtotal_05 or subtotal_no_tax and subtotal_0 and subtotal_10 or \
            #                 subtotal_no_tax and subtotal_05 and subtotal_10 or subtotal_0 and subtotal_05 and subtotal_10:
            #             worksheet1.write(row_no, 5, _('1 + 2 + 3'), f9)
            #         else:
            #             worksheet1.write(row_no, 5, _('1 + 2'), f9)
            #
            #     if subtotal_no_tax and subtotal_0 or subtotal_no_tax and subtotal_05 or subtotal_no_tax and subtotal_10 or \
            #             subtotal_0 and subtotal_05 or subtotal_0 and subtotal_10 or subtotal_05 and subtotal_10:
            #         if objects.currency_id.name == 'VND':
            #             worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            #         else:
            #             worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)

            # if subtotal_0 > 0 and subtotal_05 > 0 and subtotal_10 == 0:
            #     if objects.currency_id.name == 'VND':
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            #     else:
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            # elif subtotal_0 > 0 and subtotal_10 > 0 and subtotal_05 == 0:
            #     if objects.currency_id.name == 'VND':
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            #     else:
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            # elif subtotal_05 > 0 and subtotal_10 > 0 and subtotal_0 == 0:
            #     if objects.currency_id.name == 'VND':
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            #     else:
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
            # elif subtotal_0 > 0 and subtotal_05 > 0 and subtotal_10 > 0:
            #     if objects.currency_id.name == 'VND':
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_vnd)
            #     else:
            #         worksheet1.write(row_no, 6, objects.amount_total, money_bold_usd)
        worksheet1.write(row_no, 7, '', f9)
        row_no += 1

        worksheet1.merge_range(row_no, 0, row_no, 7, _('Delivery Information'), workbook.add_format(
            {'border': 1, 'bottom': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'}))
        row_no += 1
        if objects.notes:
            worksheet1.merge_range(row_no, 0, row_no, 1, "",
                                   workbook.add_format(
                                       {'border': 1, 'top': 0, 'right': 0, 'align': 'left', 'valign': 'vcenter',
                                        'text_wrap': True,
                                        'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
            worksheet1.merge_range(row_no, 2, row_no, 7, objects.notes,
                                   workbook.add_format(
                                       {'border': 1, 'top': 0, 'left': 0, 'align': 'left', 'valign': 'vcenter',
                                        'text_wrap': True,
                                        'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
        else:
            worksheet1.merge_range(row_no, 0, row_no, 1, "",
                                   workbook.add_format(
                                       {'border': 1, 'top': 0, 'right': 0, 'align': 'center', 'valign': 'vcenter',
                                        'text_wrap': True,
                                        'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
            worksheet1.merge_range(row_no, 2, row_no, 7, _('PEGASUS MARITIME & DEVELOPMENT CORPORATION'),
                                   workbook.add_format(
                                       {'border': 1, 'top': 0, 'left': 0, 'align': 'left', 'valign': 'vcenter',
                                        'text_wrap': True,
                                        'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
        row_no += 2
        worksheet1.merge_range(row_no, 0, row_no, 7, _('Invoice Information'), workbook.add_format(
            {'border': 1, 'bottom': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Times New Roman'}))
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 1, "",
                               workbook.add_format(
                                   {'border': 1, 'top': 0, 'right': 0, 'align': 'center', 'valign': 'vcenter',
                                    'text_wrap': True,
                                    'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
        worksheet1.merge_range(row_no, 2, row_no, 7, _('PEGASUS MARITIME & DEVELOPMENT CORPORATION'),
                               workbook.add_format(
                                   {'border': 1, 'top': 0, 'left': 0, 'align': 'left', 'valign': 'vcenter',
                                    'text_wrap': True,
                                    'font_color': '#0000FF', 'font_size': 12, 'font_name': 'Times New Roman'}))
        row_no += 2
        worksheet1.write(row_no, 0, _('With many thanks and best regards,'),
                         workbook.add_format({'font_size': 12, 'font_name': 'Times New Roman'}))
        row_no += 2
        worksheet1.merge_range(row_no, 0, row_no, 2, _('ORDERED BY:'), f8_1)
        worksheet1.merge_range(row_no, 3, row_no, 7, _('CHECKED BY:'), f8_1)
        row_no += 2

        worksheet1.insert_textbox(row_no, 0, ' ',
                                  {'border': {'color': 'black'}, 'x_offset': 30, 'width': 270, 'height': 140})
        worksheet1.insert_textbox(row_no, 3, ' ',
                                  {'border': {'color': 'black'}, 'x_offset': 40, 'width': 280, 'height': 140})
