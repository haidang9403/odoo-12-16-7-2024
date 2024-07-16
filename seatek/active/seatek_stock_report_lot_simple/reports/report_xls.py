import base64
import io

from odoo import models


class ReportExcel(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.seatek_stock_report_lot_simple.report_excel'

    def generate_xlsx_report(self, workbook, data, lines):

        if lines.date:
            date_ = lines.date.strftime('%d-%m-%Y')
        else:
            date_ = lines.date

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
        # cqminh 25.5.23
        company_id = location.company_id
        street = ""
        street2 = ""
        city = ""
        state = ""
        country = ""
        if company_id.partner_id.street is not None:
            street = "%s, " % company_id.partner_id.street
        if company_id.partner_id.street2 is not None:
            street2 = "%s, " % company_id.partner_id.street2
        if company_id.partner_id.state_id.name is not None:
            state = "%s, " % company_id.partner_id.state_id.name
        if company_id.partner_id.country_id.name is not None:
            country = "%s" % company_id.partner_id.country_id.name

        user_id = lines.user_id.id
        employee_name = ""
        department = ""
        # s_employee = self.env['hr.employee.multi.company'].sudo().search([('user_id', '=', user_id)], limit=1)
        # if s_employee:
        #     employee_name = s_employee.name.name
        #     department = s_employee.department_id.name

        address = "%s%s%s%s%s" % (street, street2, city, state, country)
        vat = lines.company_id.partner_id.vat

        worksheet.merge_range('A1:G1', company_id.name, f1)
        worksheet.merge_range('A2:G2', address, f1)
        worksheet.merge_range('A3:G3', "MST: %s" % vat, f1)

        worksheet.merge_range('A5:G5', "BÁO CÁO TỒN KHO", f2)
        worksheet.merge_range('A6:G6', "Ngày %s" % date_, f1)

        worksheet.set_row(7, 30)
        worksheet.set_column('C:C', 14)
        worksheet.set_column('D:D', 40)
        worksheet.set_column('F:G', 14)
        worksheet.set_column('H:H', 20)
        worksheet.set_column('I:N', 13)
        worksheet.freeze_panes(8, 0)

        worksheet.merge_range('A7:C7', "Nhân viên: %s" % employee_name, f1)
        worksheet.merge_range('D7:F7', department, f1)

        # title
        worksheet.write('A8', 'STT', f1_title)
        worksheet.write('B8', 'Mã', f1_title)
        worksheet.write('C8', 'Mã kế toán', f1_title)
        worksheet.write('D8', 'Tên', f1_title)
        worksheet.write('E8', 'ĐVT', f1_title)
        worksheet.write('F8', 'Lô', f1_title)
        worksheet.write('G8', 'Tồn kho', f1_title)

        index = 0
        total_value_closing = 0

        for data in lines.inventory_report_line_ids_hide_display_product:
            if data.location_id.id == location.id:
                total_value_closing += data.stock_closing
                index += 1
                worksheet.write('A%s' % (index + 8), index, f4)
                code = ""
                if data.default_code:
                    code = data.default_code
                lot = ""
                if data.name_lot:
                    lot = data.name_lot
                ac_code = ""
                if data.accounting_code:
                    ac_code = data.accounting_code
                worksheet.write('B%s' % (index + 8), code, f3)
                worksheet.write('C%s' % (index + 8), ac_code, f3)
                worksheet.write('D%s' % (index + 8), data.product_id.name, f3)
                worksheet.write('E%s' % (index + 8), data.uom_id.name, f3)
                worksheet.write('F%s' % (index + 8), lot, f4)
                worksheet.write('G%s' % (index + 8), data.stock_closing, format_number)

        worksheet.merge_range('A%s:F%s' % (index + 9, index + 9), "Tổng", f2_title)
        worksheet.write_formula('G%s' % (index + 9), '=SUM(G9:G%s)' % (index + 8), format_number1)
