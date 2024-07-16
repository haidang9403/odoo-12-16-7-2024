from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
import datetime
import pytz
import locale
from pytz import timezone
from datetime import timedelta
import base64
import io

class Report_Excel(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.seatek_stock_report_xnt._report_excel'

    # Code báo cáo cũ
    # def generate_xlsx_report(self, workbook, data, lines):
    #
    #     if lines.date_from and lines.date_to:
    #         date_from_ = lines.date_from.strftime('%d-%m-%Y')
    #         date_to_ = lines.date_to.strftime('%d-%m-%Y')
    #     else:
    #         date_from_ = lines.date_from
    #         date_to_ = lines.date_to
    #
    #     worksheet = workbook.add_worksheet("Chi tiết xuất nhập tồn")
    #
    #     f1 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black'})
    #     f2 = workbook.add_format({'align': 'center'})
    #     f3 = workbook.add_format({'bold': True, 'font_size': 18, 'align': 'center'})
    #     format_number = workbook.add_format(dict(num_format='#,##0.00'))
    #
    #     # ---------------------------------------------- #
    #     row_date_from = 0
    #     row_date_to = 1
    #     worksheet.write(row_date_from, 0, "Từ Ngày")
    #     worksheet.write(row_date_to, 0, "Đến Ngày")
    #
    #     worksheet.write(row_date_from, 1, date_from_)
    #     worksheet.write(row_date_to, 1, date_to_)
    #
    #     # ---------------------------------------------- #
    #     worksheet.write(0, 4, "Địa điểm kho")
    #     worksheet.write(1, 4, "Lấy giá trị theo")
    #     worksheet.write(2, 4, "Giá trị kho")
    #
    #     location_col = 5
    #     for line_location in lines.location_ids:
    #         worksheet.write(0, location_col, line_location.name)
    #         location_col += 1
    #
    #     worksheet.write(1, 5, dict(lines._fields['type_get_value'].selection).get(lines.type_get_value))
    #     worksheet.write(2, 5, lines.value, format_number)
    #
    #     # ---------------------------------------------- #
    #     no1_row = 5
    #     no1_col = 0
    #
    #     worksheet.merge_range('A5:G5', 'CHI TIẾT XUẤT NHẬP TỒN - ' + data.get('company_id'), f3)
    #     worksheet.write(no1_row, no1_col, "STT", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Mã sản phẩm", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Mã kế toán", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Tên Sản Phẩm", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Đơn Vị", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Kho", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Đầu Kỳ", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Giá trị kho đầu kì", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Nhập Trong Kỳ", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Giá trị nhập", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Xuất Trong Kỳ", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Giá trị xuất", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Cuối Kỳ", f1)
    #     no1_col += 1
    #     worksheet.write(no1_row, no1_col, "Giá trị kho cuối kì", f1)
    #
    #     # ---------------------------------------------- #
    #     sheet_row = 5
    #     number = 0
    #     total_stock_opening = 0
    #     total_stock_in = 0
    #     total_stock_out = 0
    #     total_stock_closing = 0
    #
    #     total_value_opening = 0
    #     total_value_in = 0
    #     total_value_out = 0
    #     total_value_closing = 0
    #
    #     for line in lines.inventory_report_line_ids_hide_display_product:
    #         sheet_row += 1
    #         number += 1
    #         sheet_col = 0
    #
    #         worksheet.write(sheet_row, sheet_col, number, f2)
    #         sheet_col += 1
    #         # if line.product_template_id.default_code:
    #         #     worksheet.write(sheet_row, sheet_col, line.product_template_id.default_code, format_number)
    #         worksheet.write(sheet_row, sheet_col, line.product_template_id.default_code, format_number)
    #         sheet_col += 1
    #         if line.product_template_id.accounting_code:
    #             worksheet.write(sheet_row, sheet_col, line.product_template_id.accounting_code, format_number)
    #         sheet_col += 1
    #         worksheet.write(sheet_row, sheet_col, line.product_id.name, format_number)
    #         sheet_col += 1
    #         worksheet.write(sheet_row, sheet_col, line.uom_id.name, f2)
    #         sheet_col += 1
    #         worksheet.write(sheet_row, sheet_col, line.location_id.name, f2)
    #         sheet_col += 1
    #         worksheet.write(sheet_row, sheet_col, line.stock_opening, format_number)
    #         sheet_col += 1
    #         total_stock_opening += line.stock_opening
    #         worksheet.write(sheet_row, sheet_col, line.value_stock_opening, format_number)
    #         sheet_col += 1
    #         total_value_opening += line.value_stock_opening
    #         worksheet.write(sheet_row, sheet_col, line.stock_in, format_number)
    #         sheet_col += 1
    #         total_stock_in += line.stock_in
    #         worksheet.write(sheet_row, sheet_col, line.value_stock_in, format_number)
    #         sheet_col += 1
    #         total_value_in += line.value_stock_in
    #         worksheet.write(sheet_row, sheet_col, line.stock_out, format_number)
    #         sheet_col += 1
    #         total_stock_out += line.stock_out
    #         worksheet.write(sheet_row, sheet_col, line.value_stock_out, format_number)
    #         sheet_col += 1
    #         total_value_out += line.value_stock_out
    #         worksheet.write(sheet_row, sheet_col, line.stock_closing, format_number)
    #         sheet_col += 1
    #         total_stock_closing += line.stock_closing
    #         worksheet.write(sheet_row, sheet_col, line.value_stock_closing, format_number)
    #         sheet_col += 1
    #         total_value_closing += line.value_stock_closing
    #
    #
    #     # custom total
    #     total_row = sheet_row + 2
    #     total_col = 5
    #     merge_range_A_E = 'A' + str(total_row + 1) + ':F' + str(total_row + 1)
    #     worksheet.merge_range(merge_range_A_E, '#TỔNG', f3)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_stock_opening, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_value_opening, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_stock_in, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_value_in, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_stock_out, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_value_out, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_stock_closing, format_number)
    #     total_col += 1
    #     worksheet.write(total_row, total_col, total_value_closing, format_number)

    # cqminh 25.5.23
    def generate_xlsx_report(self, workbook, data, lines):

        if lines.date_from and lines.date_to:
            date_from_ = lines.date_from.strftime('%d-%m-%Y')
            date_to_ = lines.date_to.strftime('%d-%m-%Y')
        else:
            date_from_ = lines.date_from
            date_to_ = lines.date_to

        worksheet = workbook.add_worksheet("Chi tiết xuất nhập tồn")

        f1 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black'})
        f2 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 18})
        f3 = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 12, 'fg_color': '#8db4e2',
             'border': 1, 'valign': 'vcenter'})
        f4 = workbook.add_format({'border': 1})
        f5 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 18, 'border': 1})

        format_number = workbook.add_format(dict(num_format='#,##0.00', border=1))
        format_number1 = workbook.add_format(dict(num_format='#,##0.00'))
        format_number_sum = workbook.add_format(
            dict(num_format='#,##0.00', bold=True, align='center', valign='vcenter', border=1))

        worksheet.set_column('A:A', 5)
        worksheet.set_column('B:C', 13)
        worksheet.set_column('D:D', 40)
        worksheet.set_column('F:G', 13)
        worksheet.set_column('H:H', 18)
        worksheet.set_column('I:J', 16)
        worksheet.set_column('K:K', 14)
        worksheet.set_column('L:N', 13)

        worksheet.set_row(6, 30)

        worksheet.freeze_panes(7, 0)

        # ---------------------------------------------- #
        for location in lines.location_ids:
            continue
        company_id = location.company_id

        # Hình ảnh của công ty
        image_company = io.BytesIO(base64.b64decode(company_id.logo_web))
        worksheet.insert_image('C2', "logo_company.png",
                               {'image_data': image_company, 'x_scale': 0.8, 'y_scale': 0.8})

        worksheet.merge_range('E1:K1', company_id.name, f1)

        # ---------------------------------------------- #
        row_date_from = 1
        row_date_to = 2
        worksheet.write(row_date_from, 4, "Từ Ngày", f1)
        worksheet.write(row_date_to, 4, "Đến Ngày", f1)

        worksheet.write(row_date_from, 5, date_from_)
        worksheet.write(row_date_to, 5, date_to_)

        # ---------------------------------------------- #
        worksheet.write(1, 8, "Địa điểm kho", f1)
        worksheet.write(2, 8, "Lấy giá trị theo", f1)
        worksheet.write(3, 8, "Giá trị kho", f1)

        location_col = 9
        for line_location in lines.location_ids:
            worksheet.write(1, location_col, line_location.name)
            location_col += 1

        worksheet.write(2, 9, dict(lines._fields['type_get_value'].selection).get(lines.type_get_value))
        worksheet.write(3, 9, lines.value, format_number1)

        # ---------------------------------------------- #
        no1_row = 6
        no_col = 0

        worksheet.merge_range('B6:K6', 'CHI TIẾT XUẤT NHẬP TỒN', f2)
        worksheet.write(no1_row, no_col, "STT", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Mã sản phẩm", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Mã kế toán", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Tên Sản Phẩm", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Đơn Vị", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Kho", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Đầu Kỳ", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Giá trị kho đầu kì", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Nhập Trong Kỳ", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Giá trị nhập", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Xuất Trong Kỳ", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Giá trị xuất", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Cuối Kỳ", f3)
        no_col += 1
        worksheet.write(no1_row, no_col, "Giá trị kho cuối kì", f3)

        # ---------------------------------------------- #
        sheet_row = 6
        number = 0
        total_stock_opening = 0
        total_stock_in = 0
        total_stock_out = 0
        total_stock_closing = 0

        total_value_opening = 0
        total_value_in = 0
        total_value_out = 0
        total_value_closing = 0

        for line in lines.inventory_report_line_ids_hide_display_product:
            sheet_row += 1
            number += 1
            sheet_col = 0

            worksheet.write(sheet_row, sheet_col, number, f4)
            sheet_col += 1
            if line.product_template_id.default_code:
                worksheet.write(sheet_row, sheet_col, line.product_template_id.default_code, format_number)
            else:
                worksheet.write(sheet_row, sheet_col, "", format_number)
            sheet_col += 1
            if line.product_template_id.accounting_code:
                worksheet.write(sheet_row, sheet_col, line.product_template_id.accounting_code, format_number)
            else:
                worksheet.write(sheet_row, sheet_col, "", format_number)
            sheet_col += 1
            worksheet.write(sheet_row, sheet_col, line.product_id.name, format_number)
            sheet_col += 1
            worksheet.write(sheet_row, sheet_col, line.uom_id.name, f4)
            sheet_col += 1
            worksheet.write(sheet_row, sheet_col, line.location_id.name, f4)
            sheet_col += 1
            worksheet.write(sheet_row, sheet_col, line.stock_opening, format_number)
            sheet_col += 1
            total_stock_opening += line.stock_opening
            worksheet.write(sheet_row, sheet_col, line.value_stock_opening, format_number)
            sheet_col += 1
            total_value_opening += line.value_stock_opening
            worksheet.write(sheet_row, sheet_col, line.stock_in, format_number)
            sheet_col += 1
            total_stock_in += line.stock_in
            worksheet.write(sheet_row, sheet_col, line.value_stock_in, format_number)
            sheet_col += 1
            total_value_in += line.value_stock_in
            worksheet.write(sheet_row, sheet_col, line.stock_out, format_number)
            sheet_col += 1
            total_stock_out += line.stock_out
            worksheet.write(sheet_row, sheet_col, line.value_stock_out, format_number)
            sheet_col += 1
            total_value_out += line.value_stock_out
            worksheet.write(sheet_row, sheet_col, line.stock_closing, format_number)
            sheet_col += 1
            total_stock_closing += line.stock_closing
            worksheet.write(sheet_row, sheet_col, line.value_stock_closing, format_number)
            sheet_col += 1
            total_value_closing += line.value_stock_closing


        # custom total
        total_row = sheet_row + 1
        total_col = 5
        merge_range_A_F = 'A' + str(total_row + 1) + ':F' + str(total_row + 1)
        worksheet.merge_range(merge_range_A_F, 'TỔNG', f5)
        total_col += 1
        worksheet.write(total_row, total_col, total_stock_opening, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_value_opening, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_stock_in, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_value_in, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_stock_out, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_value_out, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_stock_closing, format_number_sum)
        total_col += 1
        worksheet.write(total_row, total_col, total_value_closing, format_number_sum)
