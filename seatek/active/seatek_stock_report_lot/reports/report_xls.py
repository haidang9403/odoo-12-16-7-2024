import base64
import io

from odoo import models


class ReportExcel(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.seatek_stock_report_lot.inventory_report_lot_excel'

    def generate_xlsx_report(self, workbook, data, lines):

        if lines.date_from and lines.date_to:
            date_from_ = lines.date_from.strftime('%d-%m-%Y')
            date_to_ = lines.date_to.strftime('%d-%m-%Y')
        else:
            date_from_ = lines.date_from
            date_to_ = lines.date_to

        f1 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 12})
        f1_title = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 12, 'fg_color': '#8db4e2',
             'border': 1, 'valign': 'vcenter'})
        f2 = workbook.add_format({'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 18})
        f2_title = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_color': 'black', 'font_size': 18, 'border': 1})
        f3 = workbook.add_format({'font_size': 12, 'border': 1})
        f4 = workbook.add_format({'font_size': 12, 'align': 'center', 'border': 1})

        format_number = workbook.add_format(dict(num_format='#,##0.00', border=1))
        format_number1 = workbook.add_format(
            dict(num_format='#,##0.00', bold=True, align='center', valign='vcenter', border=1))

        # for location in lines.location_ids:

        location = lines.location_id
        worksheet = workbook.add_worksheet("%s" % location.name)
        image_company = io.BytesIO(base64.b64decode(location.company_id.logo_web))
        worksheet.insert_image('B2', "logo_company.png",
                               {'image_data': image_company, 'x_scale': 0.8, 'y_scale': 0.8})
        company_name = location.company_id.name
        street = ""
        street2 = ""
        city = ""
        state = ""
        country = ""
        if location.company_id.partner_id.street is not None:
            street = "%s, " % location.company_id.partner_id.street
        if location.company_id.partner_id.street2 is not None:
            street2 = "%s, " % location.company_id.partner_id.street2
        if location.company_id.partner_id.state_id.name is not None:
            state = "%s, " % location.company_id.partner_id.state_id.name
        if location.company_id.partner_id.country_id.name is not None:
            country = "%s" % location.company_id.partner_id.country_id.name

        user_id = lines.user_id.id
        employee_name = ""
        department = ""
        s_employee = self.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)
        if s_employee:
            employee_name = s_employee.name
            department = s_employee.department_id.name

        address = "%s%s%s%s%s" % (street, street2, city, state, country)
        vat = location.company_id.partner_id.vat

        worksheet.merge_range('C1:M1', company_name, f1)
        worksheet.merge_range('C2:M2', address, f1)
        worksheet.merge_range('C3:M3', "MST: %s" % vat, f1)

        worksheet.merge_range('C5:M5', "BÁO CÁO XUẤT NHẬP TỒN", f2)
        worksheet.merge_range('C6:M6', "Ngày %s - %s" % (date_from_, date_to_), f1)

        worksheet.set_row(7, 30)
        worksheet.set_column('C:C', 14)
        worksheet.set_column('D:D', 40)
        worksheet.set_column('F:G', 14)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:N', 13)
        worksheet.freeze_panes(8, 0)

        worksheet.merge_range('D7:F7', "Nhân viên: %s" % employee_name, f1)
        worksheet.merge_range('H7:J7', department, f1)

        # title
        worksheet.write('A8', 'STT', f1_title)
        worksheet.write('B8', 'Mã', f1_title)
        worksheet.write('C8', 'Mã kế toán', f1_title)
        worksheet.write('D8', 'Tên', f1_title)
        worksheet.write('E8', 'ĐVT', f1_title)
        worksheet.write('F8', 'Lô', f1_title)
        worksheet.write('G8', 'Tồn đầu kỳ', f1_title)
        worksheet.write('H8', 'Giá trị kho đầu kỳ', f1_title)
        worksheet.write('I8', 'Nhập trong kỳ', f1_title)
        worksheet.write('J8', 'Giá trị nhập trong kỳ', f1_title)
        worksheet.write('K8', 'Xuất trong kỳ', f1_title)
        worksheet.write('L8', 'Giá trị xuất trong kỳ', f1_title)
        worksheet.write('M8', 'Tồn cuối kỳ', f1_title)
        worksheet.write('N8', 'Giá trị tồn cuối kỳ', f1_title)

        index = 0
        total_stock_opening = 0
        total_value_opening = 0
        total_stock_in = 0
        total_value_in = 0
        total_stock_out = 0
        total_value_out = 0
        total_value_closing = 0

        for data in lines.inventory_report_line_ids_hide_display_product:
            if data.location_id.id == location.id:
                total_stock_opening += data.stock_opening
                total_value_opening += data.value_stock_opening
                total_stock_in += data.stock_in
                total_value_in += data.value_stock_in
                total_stock_out += data.stock_out
                total_value_out += data.value_stock_out
                total_value_closing += data.value_stock_closing
                index += 1
                worksheet.write('A%s' % (index + 8), index, f4)
                code = ""
                if data.default_code:
                    code = data.default_code
                worksheet.write('B%s' % (index + 8), code, f3)
                ac_code = ""
                if data.accounting_code:
                    ac_code = data.accounting_code
                worksheet.write('C%s' % (index + 8), ac_code, f3)
                worksheet.write('D%s' % (index + 8), data.product_id.name, f3)
                worksheet.write('E%s' % (index + 8), data.uom_id.name, f3)
                worksheet.write('F%s' % (index + 8), data.name_lot, f4)
                worksheet.write('G%s' % (index + 8), data.stock_opening, format_number)
                worksheet.write('H%s' % (index + 8), data.value_stock_opening, format_number)
                worksheet.write('I%s' % (index + 8), data.stock_in, format_number)
                worksheet.write('J%s' % (index + 8), data.value_stock_in, format_number)
                worksheet.write('K%s' % (index + 8), data.stock_out, format_number)
                worksheet.write('L%s' % (index + 8), data.value_stock_out, format_number)
                worksheet.write('M%s' % (index + 8), data.stock_closing, format_number)
                worksheet.write('N%s' % (index + 8), data.value_stock_closing, format_number)

        worksheet.merge_range('A%s:F%s' % (index + 9, index + 9), "Tổng", f2_title)
        worksheet.write_formula('G%s' % (index + 9), '=SUM(G9:G%s)' % (index + 8), format_number1)
        worksheet.write_formula('H%s' % (index + 9), '=SUM(H9:H%s)' % (index + 8), format_number1)
        worksheet.write_formula('I%s' % (index + 9), '=SUM(I9:I%s)' % (index + 8), format_number1)
        worksheet.write_formula('J%s' % (index + 9), '=SUM(J9:J%s)' % (index + 8), format_number1)
        worksheet.write_formula('K%s' % (index + 9), '=SUM(K9:K%s)' % (index + 8), format_number1)
        worksheet.write_formula('L%s' % (index + 9), '=SUM(L9:L%s)' % (index + 8), format_number1)
        worksheet.write_formula('M%s' % (index + 9), '=SUM(M9:M%s)' % (index + 8), format_number1)
        worksheet.write_formula('N%s' % (index + 9), '=SUM(N9:N%s)' % (index + 8), format_number1)
