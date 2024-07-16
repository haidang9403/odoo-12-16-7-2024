import base64
import io

from odoo import models


class ReportExcel(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.seatek_inventory_report.inventory_report_excel'

    def get_lot(self, workbook, lines, data_line):
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

        if lines.type_location:
            locations = lines.location_id
        else:
            locations = lines.location_ids

        for location in locations:
            worksheet = workbook.add_worksheet("%s" % location.name)
            image_company = io.BytesIO(base64.b64decode(location.company_id.logo_web))
            worksheet.insert_image('B2', "logo_company.png",
                                   {'image_data': image_company, 'x_scale': 0.8, 'y_scale': 0.8})
            company_name = lines.company_id.name
            street = ""
            street2 = ""
            city = ""
            state = ""
            country = ""
            if lines.company_id.partner_id.street is not None:
                street = "%s, " % lines.company_id.partner_id.street
            if lines.company_id.partner_id.street2 is not None:
                street2 = "%s, " % lines.company_id.partner_id.street2
            if lines.company_id.partner_id.state_id.name is not None:
                state = "%s, " % lines.company_id.partner_id.state_id.name
            if lines.company_id.partner_id.country_id.name is not None:
                country = "%s" % lines.company_id.partner_id.country_id.name

            user_id = lines.user_id.id
            employee_name = ""
            department = ""
            s_employee = self.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)
            if s_employee:
                employee_name = s_employee.name
                department = s_employee.department_id.name

            address = "%s%s%s%s%s" % (street, street2, city, state, country)
            vat = lines.company_id.partner_id.vat

            worksheet.merge_range('C1:L1', company_name, f1)
            worksheet.merge_range('C2:L2', address, f1)
            worksheet.merge_range('C3:L3', "MST: %s" % vat, f1)

            worksheet.merge_range('C5:L5', "BÁO CÁO XUẤT NHẬP TỒN", f2)
            worksheet.merge_range('C6:L6', "Ngày %s - %s" % (date_from_, date_to_), f1)

            worksheet.set_row(7, 30)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('E:F', 14)
            worksheet.set_column('G:G', 20)
            worksheet.set_column('H:M', 13)
            worksheet.freeze_panes(8, 0)

            worksheet.merge_range('D7:F7', "Nhân viên: %s" % employee_name, f1)
            worksheet.merge_range('H7:J7', department, f1)

            # title
            worksheet.write('A8', 'STT', f1_title)
            worksheet.write('B8', 'Mã', f1_title)
            worksheet.write('C8', 'Tên', f1_title)
            worksheet.write('D8', 'ĐVT', f1_title)
            worksheet.write('E8', 'Lô', f1_title)
            worksheet.write('F8', 'Tồn đầu kỳ', f1_title)
            worksheet.write('G8', 'Giá trị kho đầu kỳ', f1_title)
            worksheet.write('H8', 'Nhập trong kỳ', f1_title)
            worksheet.write('I8', 'Giá trị nhập trong kỳ', f1_title)
            worksheet.write('J8', 'Xuất trong kỳ', f1_title)
            worksheet.write('K8', 'Giá trị xuất trong kỳ', f1_title)
            worksheet.write('L8', 'Tồn cuối kỳ', f1_title)
            worksheet.write('M8', 'Giá trị tồn cuối kỳ', f1_title)

            index = 0
            for data in data_line:
                if data.location_id.id == location.id:
                    index += 1
                    worksheet.write('A%s' % (index + 8), index, f4)
                    code = ""
                    if data.default_code:
                        code = data.default_code
                    worksheet.write('B%s' % (index + 8), code, f3)
                    worksheet.write('C%s' % (index + 8), data.product_id.name, f3)
                    worksheet.write('D%s' % (index + 8), data.uom_id.name, f3)
                    worksheet.write('E%s' % (index + 8), data.name_lot, f4)
                    worksheet.write('F%s' % (index + 8), data.stock_opening, format_number)
                    worksheet.write('G%s' % (index + 8), data.value_stock_opening, format_number)
                    worksheet.write('H%s' % (index + 8), data.stock_in, format_number)
                    worksheet.write('I%s' % (index + 8), data.value_stock_in, format_number)
                    worksheet.write('J%s' % (index + 8), data.stock_out, format_number)
                    worksheet.write('K%s' % (index + 8), data.value_stock_out, format_number)
                    worksheet.write('L%s' % (index + 8), data.stock_closing, format_number)
                    worksheet.write('M%s' % (index + 8), data.value_stock_closing, format_number)

            worksheet.merge_range('A%s:E%s' % (index + 9, index + 9), "Tổng", f2_title)
            worksheet.write_formula('F%s' % (index + 9), '=SUM(F9:F%s)' % (index + 8), format_number1)
            worksheet.write_formula('G%s' % (index + 9), '=SUM(G9:G%s)' % (index + 8), format_number1)
            worksheet.write_formula('H%s' % (index + 9), '=SUM(H9:H%s)' % (index + 8), format_number1)
            worksheet.write_formula('I%s' % (index + 9), '=SUM(I9:I%s)' % (index + 8), format_number1)
            worksheet.write_formula('J%s' % (index + 9), '=SUM(J9:J%s)' % (index + 8), format_number1)
            worksheet.write_formula('K%s' % (index + 9), '=SUM(K9:K%s)' % (index + 8), format_number1)
            worksheet.write_formula('L%s' % (index + 9), '=SUM(L9:L%s)' % (index + 8), format_number1)
            worksheet.write_formula('M%s' % (index + 9), '=SUM(M9:M%s)' % (index + 8), format_number1)

    def get_not_lot(self, workbook, lines, data_line):
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
        if lines.type_location:
            locations = lines.location_id
        else:
            locations = lines.location_ids

        for location in locations:
            worksheet = workbook.add_worksheet("%s" % location.name)
            image_company = io.BytesIO(base64.b64decode(location.company_id.logo_web))
            worksheet.insert_image('B2', "logo_company.png",
                                   {'image_data': image_company, 'x_scale': 0.8, 'y_scale': 0.8})
            company_name = lines.company_id.name
            street = ""
            street2 = ""
            city = ""
            state = ""
            country = ""
            if lines.company_id.partner_id.street is not None:
                street = "%s, " % lines.company_id.partner_id.street
            if lines.company_id.partner_id.street2 is not None:
                street2 = "%s, " % lines.company_id.partner_id.street2
            if lines.company_id.partner_id.state_id.name is not None:
                state = "%s, " % lines.company_id.partner_id.state_id.name
            if lines.company_id.partner_id.country_id.name is not None:
                country = "%s" % lines.company_id.partner_id.country_id.name

            user_id = lines.user_id.id
            employee_name = ""
            department = ""
            s_employee = self.env['hr.employee'].sudo().search([('user_id', '=', user_id)], limit=1)
            if s_employee:
                employee_name = s_employee.name
                department = s_employee.department_id.name

            address = "%s%s%s%s%s" % (street, street2, city, state, country)
            vat = lines.company_id.partner_id.vat

            worksheet.merge_range('C1:L1', company_name, f1)
            worksheet.merge_range('C2:L2', address, f1)
            worksheet.merge_range('C3:L3', "MST: %s" % vat, f1)

            worksheet.merge_range('C5:L5', "BÁO CÁO XUẤT NHẬP TỒN", f2)
            worksheet.merge_range('C6:L6', "Ngày %s - %s" % (date_from_, date_to_), f1)

            worksheet.set_row(7, 30)
            worksheet.set_column('C:C', 40)
            worksheet.set_column('E:F', 14)
            worksheet.set_column('G:G', 20)
            worksheet.set_column('H:L', 13)
            worksheet.freeze_panes(8, 0)

            worksheet.merge_range('D7:F7', "Nhân viên: %s" % employee_name, f1)
            worksheet.merge_range('H7:J7', department, f1)

            # title
            worksheet.write('A8', 'STT', f1_title)
            worksheet.write('B8', 'Mã', f1_title)
            worksheet.write('C8', 'Tên', f1_title)
            worksheet.write('D8', 'ĐVT', f1_title)
            worksheet.write('E8', 'Tồn đầu kỳ', f1_title)
            worksheet.write('F8', 'Giá trị kho đầu kỳ', f1_title)
            worksheet.write('G8', 'Nhập trong kỳ', f1_title)
            worksheet.write('H8', 'Giá trị nhập trong kỳ', f1_title)
            worksheet.write('I8', 'Xuất trong kỳ', f1_title)
            worksheet.write('J8', 'Giá trị xuất trong kỳ', f1_title)
            worksheet.write('K8', 'Tồn cuối kỳ', f1_title)
            worksheet.write('L8', 'Giá trị tồn cuối kỳ', f1_title)

            index = 0
            for data in data_line:
                if data.location_id.id == location.id:
                    index += 1
                    worksheet.write('A%s' % (index + 8), index, f4)
                    code = ""
                    if data.default_code:
                        code = data.default_code
                    worksheet.write('B%s' % (index + 8), code, f3)
                    worksheet.write('C%s' % (index + 8), data.product_id.name, f3)
                    worksheet.write('D%s' % (index + 8), data.uom_id.name, f3)
                    worksheet.write('E%s' % (index + 8), data.stock_opening, format_number)
                    worksheet.write('F%s' % (index + 8), data.value_stock_opening, format_number)
                    worksheet.write('G%s' % (index + 8), data.stock_in, format_number)
                    worksheet.write('H%s' % (index + 8), data.value_stock_in, format_number)
                    worksheet.write('I%s' % (index + 8), data.stock_out, format_number)
                    worksheet.write('J%s' % (index + 8), data.value_stock_out, format_number)
                    worksheet.write('K%s' % (index + 8), data.stock_closing, format_number)
                    worksheet.write('L%s' % (index + 8), data.value_stock_closing, format_number)

            worksheet.merge_range('A%s:D%s' % (index + 9, index + 9), "Tổng", f2_title)
            worksheet.write_formula('E%s' % (index + 9), '=SUM(E9:E%s)' % (index + 8), format_number1)
            worksheet.write_formula('F%s' % (index + 9), '=SUM(F9:F%s)' % (index + 8), format_number1)
            worksheet.write_formula('G%s' % (index + 9), '=SUM(G9:G%s)' % (index + 8), format_number1)
            worksheet.write_formula('H%s' % (index + 9), '=SUM(H9:H%s)' % (index + 8), format_number1)
            worksheet.write_formula('I%s' % (index + 9), '=SUM(I9:I%s)' % (index + 8), format_number1)
            worksheet.write_formula('J%s' % (index + 9), '=SUM(J9:J%s)' % (index + 8), format_number1)
            worksheet.write_formula('K%s' % (index + 9), '=SUM(K9:K%s)' % (index + 8), format_number1)
            worksheet.write_formula('L%s' % (index + 9), '=SUM(L9:L%s)' % (index + 8), format_number1)

    def generate_xlsx_report(self, workbook, data, lines):
        lot = lines.report_with_lot
        display_product = lines.display_product
        if lot:
            # xuất theo lô
            if display_product:
                # ẩn sp = 0
                data_line = lines.inventory_report_line_lot_ids_hide_display_product
                print(data_line)
                self.get_lot(workbook, lines, data_line)
            else:
                # không ẩn sp = 0
                data_line = lines.inventory_report_line_lot_ids
                self.get_lot(workbook, lines, data_line)
        else:
            # xuất không theo lô
            if display_product:
                # ẩn sp = 0
                data_line = lines.inventory_report_line_ids_hide_display_product
                self.get_not_lot(workbook, lines, data_line)
            else:
                # không ẩn sp = 0
                data_line = lines.inventory_report_line_ids
                self.get_not_lot(workbook, lines, data_line)
