# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import io
import logging
from datetime import date, timedelta

from odoo import fields
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DSBDNSMonth(models.AbstractModel):
    '''TKK'''
    _name = 'report.sea_employee_reports.report_biendong_nhansu_month_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def employee_list(self, stt, row, sheet, employee_id, workbook, objects):
        salary_style = workbook.add_format({'bold': False,
                                            'font_size': 9,
                                            'font_name': "Times New Roman",
                                            'font_color': '#000000',
                                            'align': 'center',
                                            'border': 1,
                                            'text_wrap': True,
                                            'num_format': '#,###',
                                            'valign': 'vcenter'})
        content_style = workbook.add_format({'bold': False,
                                             'font_size': 9,
                                             'font_name': "Times New Roman",
                                             'font_color': '#000000',
                                             'align': 'center',
                                             'border': 1,
                                             'text_wrap': True,
                                             'valign': 'vcenter'})
        sheet.write('A%s' % row, stt, content_style)
        if employee_id.sudo().name.s_identification_id:
            sheet.write('B%s' % row, employee_id.sudo().name.s_identification_id, content_style)
        else:
            sheet.write('B%s' % row, '', content_style)
        if employee_id.sudo().name.name:
            sheet.write('C%s' % row, employee_id.sudo().name.name, content_style)
        else:
            sheet.write('C%s' % row, '', content_style)
        if employee_id.sudo().name.gender == 'male':
            sheet.write('D%s' % row, 'Nam', content_style)
        else:
            sheet.write('D%s' % row, 'Nữ', content_style)
        if employee_id.sudo().name.birthday:
            sheet.write('E%s' % row, employee_id.sudo().name.birthday.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('E%s' % row, '', content_style)
        if employee_id.sudo().job_id:
            sheet.write('F%s' % row, employee_id.sudo().job_id.sudo().name, content_style)
        else:
            sheet.write('F%s' % row, '', content_style)
        if employee_id.sudo().job_title:
            sheet.write('G%s' % row, employee_id.sudo().job_title, content_style)
        else:
            sheet.write('G%s' % row, '', content_style)
        if employee_id.sudo().name.social_insurance_number:
            sheet.write('H%s' % row, employee_id.sudo().name.social_insurance_number, content_style)
        else:
            sheet.write('H%s' % row, '', content_style)
        if employee_id.sudo().name.health_insurance_number:
            sheet.write('I%s' % row, employee_id.sudo().name.health_insurance_number, content_style)
        else:
            sheet.write('I%s' % row, '', content_style)
        if employee_id.sudo().name.tax_tncn_code:
            sheet.write('J%s' % row, employee_id.sudo().name.tax_tncn_code, content_style)
        else:
            sheet.write('J%s' % row, '', content_style)

        family = self.env['hr.employee.family'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('member_independent', '=', 'Y')])
        if family:
            sheet.write('K%s' % row, len(family), content_style)
        else:
            sheet.write('K%s' % row, '', content_style)

        if employee_id.sudo().name.sudo().identification_id:
            sheet.write('L%s' % row, employee_id.sudo().name.sudo().identification_id, content_style)
        else:
            sheet.write('L%s' % row, '', content_style)
        if employee_id.sudo().name.sudo().sea_id_issue_date:
            sheet.write('M%s' % row, employee_id.sudo().name.sudo().sea_id_issue_date.strftime("%d/%m/%Y"),
                        content_style)
        if employee_id.sudo().name.sudo().id_issue_place.sudo().name:
            sheet.write('N%s' % row, employee_id.sudo().name.sudo().id_issue_place.sudo().name, content_style)
        else:
            sheet.write('N%s' % row, '', content_style)

        seagroup_tv = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 4), ('contract_category', '=', 'contract'), ('date_start', '<=', objects.update_date)],
            order='date_start asc', limit=1)
        seagroup_ct = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 1), ('contract_category', '=', 'contract'), ('date_start', '<=', objects.update_date)],
            order='date_start asc', limit=1)

        company_tv = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 4), ('contract_category', '=', 'contract'),
             ('company_id', '=', employee_id.sudo().company_id.id), ('date_start', '<=', objects.update_date)],
            order='date_start asc', limit=1)
        company_ct = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 1), ('contract_category', '=', 'contract'),
             ('company_id', '=', employee_id.sudo().company_id.id), ('date_start', '<=', objects.update_date)],
            order='date_start asc', limit=1)

        if seagroup_tv.sudo().date_start:
            sheet.write('O%s' % row, seagroup_tv.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('O%s' % row, '', content_style)
        if seagroup_ct.sudo().date_start:
            sheet.write('P%s' % row, seagroup_ct.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('P%s' % row, '', content_style)
        if company_tv.sudo().date_start:
            sheet.write('Q%s' % row, company_tv.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('Q%s' % row, '', content_style)
        if company_ct.sudo().date_start:
            sheet.write('R%s' % row, company_ct.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('R%s' % row, '', content_style)

        tham_nien = ''
        if employee_id.sudo().seagroup_join_date and objects.update_date:
            tham_nien = objects.update_date - employee_id.sudo().seagroup_join_date
            start = date(1, 1, 1)  # This is the "days since" part
            if tham_nien.days > 0:
                delta = timedelta(tham_nien.days - 1)  # Create a time delta object from the number of days
                tham_nien = start + delta
            else:
                tham_nien = date(1, 1, 1)

        if employee_id.sudo().seagroup_join_date and objects.update_date:
            sheet.write('S%s' % row, tham_nien.year - 1, content_style)
        else:
            sheet.write('S%s' % row, '', content_style)
        if employee_id.sudo().seagroup_join_date:
            sheet.write('T%s' % row, tham_nien.month - 1, content_style)
        else:
            sheet.write('T%s' % row, '', content_style)
        if employee_id.sudo().seagroup_join_date:
            sheet.write('U%s' % row, tham_nien.day - 1, content_style)
        else:
            sheet.write('U%s' % row, '', content_style)

        contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending', 'close']), ('type_id', '=', 4),
             ('date_start', '<=', objects.update_date)], order='wage desc', limit=1)
        if contract.sudo().wage:
            sheet.write('V%s' % row, float('%.2f' % float(contract.sudo().wage)), salary_style)
        else:
            sheet.write('V%s' % row, '', salary_style)

        salary_contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending', 'close']), ('type_id', '=', 1), ('wage', '>', 0),
             ('date_start', '<=', objects.update_date), '|', ('date_end', '>', objects.update_date),
             ('date_end', 'in', [None, False])], order='wage desc', limit=1)

        salary_extend = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending', 'close']), ('type_id', '=', 1), ('contract_extend_salary', '>', 0),
             ('contract_category', '=', 'addition'), ('date_start', '<=', objects.update_date), '|',
             ('date_end', '>', objects.update_date), ('date_end', 'in', [None, False])],
            order='contract_extend_salary desc', limit=1)
        tong = 0
        if salary_contract.sudo().wage:
            sheet.write('W%s' % row, float('%.2f' % float(salary_contract.sudo().wage)), salary_style)
            tong += float(salary_contract.sudo().wage)
        else:
            sheet.write('W%s' % row, '', salary_style)

        if salary_extend.sudo().contract_extend_salary:
            sheet.write('X%s' % row,
                        float('%.2f' % float(salary_extend.sudo().contract_extend_salary)), salary_style)
            tong += float(salary_extend.sudo().contract_extend_salary)
        else:
            sheet.write('X%s' % row, '', salary_style)

        if tong > 0:
            sheet.write('Y%s' % row, tong, salary_style)
        else:
            sheet.write('Y%s' % row, '', salary_style)

        contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending', 'close']), ('active', '=', True),
             ('contract_category', '=', 'contract'), ('date_start', '<=', objects.update_date), '|',
             ('date_end', '>', objects.update_date), ('date_end', 'in', [None, False])],
            order='date_start desc', limit=1)
        if contract.sudo():
            if contract.sudo().contract_period_id.sudo().name:
                sheet.write('Z%s' % row, contract.sudo().contract_period_id.sudo().name, content_style)
            else:
                sheet.write('Z%s' % row, '', content_style)

            sheet.write('AA%s' % row, contract.sudo().name, content_style)
            if contract.sudo().date_start:
                sheet.write('AB%s' % row, contract.sudo().date_start.strftime("%d/%m/%Y"), content_style)
            else:
                sheet.write('AB%s' % row, '', content_style)

            if contract.sudo().date_end:
                sheet.write('AC%s' % row, contract.sudo().date_end.strftime("%d/%m/%Y"), content_style)
            else:
                sheet.write('AC%s' % row, '', content_style)
        else:
            sheet.write('Z%s' % row, '', content_style)
            sheet.write('AA%s' % row, '', content_style)
            sheet.write('AB%s' % row, '', content_style)
            sheet.write('AC%s' % row, '', content_style)

        '''TKK'''
        employee_1 = self.env['sea.employee.history.current.status'].sudo().search(
            [('employee_multi_id', '=', employee_id.id), '|', ('leaving_to_date', '>=', objects.update_date),
             ('leaving_to_date', 'in', [None, False])])
        if employee_1:
            if len(employee_1) == 1:
                employee = employee_1
            elif len(employee_1) > 1:
                employee_2 = self.env['sea.employee.history.current.status'].sudo().search(
                    [('employee_multi_id', '=', employee_id.id), ('resignation_date', '<=', objects.update_date),
                     '|', ('leaving_to_date', '>=', objects.update_date), ('leaving_to_date', 'in', [None, False])],
                    order='id desc', limit=1)
                if employee_2:
                    employee = employee_2
                else:
                    employee_3 = self.env['sea.employee.history.current.status'].sudo().search(
                        [('employee_multi_id', '=', employee_id.id), ('resignation_date', 'in', [None, False]),
                         '|', ('leaving_to_date', '>=', objects.update_date), ('leaving_to_date', 'in', [None, False])],
                        order='id desc', limit=1)
                    employee = employee_3
        else:
            print("không có luôn nè")
            employee = employee_id
        print('chốt', employee)
        current_status = ''
        resignation_date = ''
        leaving_to_date = ''
        if employee:
            if employee.sudo().employee_current_status == 'working':
                current_status = 'Đang làm việc'
            elif employee.employee_current_status == 'resigned' and employee.resignation_date:
                if employee.resignation_date > objects.update_date:
                    current_status = 'Đang làm việc'
            elif employee.sudo().employee_current_status == 'leaving':
                current_status = 'Nghỉ không lương'
            elif employee.sudo().employee_current_status == 'maternity_leave':
                current_status = 'Nghỉ thai sản'
            elif employee.sudo().employee_current_status == 'sick_leave':
                current_status = 'Nghỉ đau ốm'

            if employee.sudo().employee_current_status not in ['working', 'resigned']:
                if employee.sudo().leaving_to_date:
                    leaving_to_date = employee.sudo().leaving_to_date.strftime("%d/%m/%Y")
                if employee.sudo().resignation_date:
                    resignation_date = employee.sudo().resignation_date.strftime("%d/%m/%Y")

        sheet.write('AD%s' % row, current_status or '', content_style)
        sheet.write('AE%s' % row, resignation_date or '', content_style)
        sheet.write('AF%s' % row, leaving_to_date or '', content_style)

        ''''''
        DC = ''
        DCTT = ''
        if employee_id.sudo().name.sea_permanent_addr:
            DC += employee_id.sudo().name.sea_permanent_addr + ', '
        if employee_id.sudo().name.sudo().permanent_district_id.id:
            DC += employee_id.sudo().name.sudo().permanent_district_id.name + ', '
        if employee_id.sudo().name.sudo().permanent_city_id.id:
            DC += employee_id.sudo().name.sudo().permanent_city_id.name + ', '
        if employee_id.sudo().name.sudo().permanent_country_id.id:
            DC += employee_id.sudo().name.sudo().permanent_country_id.name

        sheet.write('AG%s' % row, DC or '', content_style)

        if employee_id.sudo().name.sea_temp_addr:
            DCTT += employee_id.sudo().name.sea_temp_addr + ', '
        if employee_id.sudo().name.sudo().temporary_district_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_district_id.name + ', '
        if employee_id.sudo().name.sudo().temporary_city_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_city_id.name + ', '
        if employee_id.sudo().name.sudo().temporary_country_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_country_id.name

        sheet.write('AH%s' % row, DCTT or '', content_style)

        sheet.write('AI%s' % row, employee_id.sudo().name.main_phone_number or '', content_style)
        sheet.write('AJ%s' % row, employee_id.sudo().name.sea_personal_email or '', content_style)
        sheet.write('AK%s' % row, employee_id.sudo().work_email or '', content_style)
        sheet.write('AL%s' % row, '', content_style)

    def get_department_child(self, list_department, id_department, department, department_search, index=1):
        list_department.append([index, department])
        for i in department_search:
            if i.parent_id.id == id_department:
                self.get_department_child(list_department=list_department, id_department=i.id, department=i,
                                          department_search=department_search, index=index + 1)

    def get_job_position(self, employee_id):
        search = self.env['hr.employee'].sudo().search([('id', '=', employee_id)], limit=1)

        if search.job_id:
            if search.job_id.sequence == 0:
                return 99
            return search.job_id.sequence
        return 99

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})

        sheet = workbook.add_worksheet(_('TỔNG HỢP'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': False,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center'})
        sheet.write('A1', 'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ', tong_hop_title)

        sheet.merge_range('A1:I1',
                          'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ THÁNG ' + str(objects.month) + ' NĂM ' + str(objects.year),
                          tong_hop_title)
        date = ''
        if objects.update_date is not None:
            if objects.update_date:
                date = 'Từ ' + str(objects.update_date.replace(day=1).strftime("%d/%m/%Y")) + ' đến ' + str(
                    objects.update_date.strftime("%d/%m/%Y"))
        sheet.merge_range('A2:I2', date, tong_hop_date)
        '''STT'''
        tong_hop_stt = workbook.add_format({'bold': True,
                                            'font_size': 13,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_name': "Times New Roman"})
        sheet.merge_range('A3:A4', 'STT', tong_hop_stt)
        sheet.merge_range('B3:B4', 'ĐƠN VỊ', tong_hop_stt)
        tong_hop_tong_laodong_thang_truoc = workbook.add_format({'bold': True,
                                                                 'font_size': 11,
                                                                 'align': 'center',
                                                                 'valign': 'vcenter',
                                                                 'border': 1,
                                                                 'text_wrap': True,
                                                                 'font_color': '#c00000',
                                                                 'bg_color': '#f8cbad',
                                                                 'font_name': "Times New Roman"})
        sheet.merge_range('C3:C4', 'TỔNG LAO ĐỘNG THÁNG TRƯỚC', tong_hop_tong_laodong_thang_truoc)

        tong_hop_tang = workbook.add_format({'bold': True,
                                             'font_size': 11,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'border': 1,
                                             'text_wrap': True,
                                             'font_color': '#000000',
                                             'bg_color': '#bdd7ee',
                                             'font_name': "Times New Roman"})
        sheet.merge_range('D3:J3', 'TỔNG HỢP LAO ĐỘNG PHÁT SINH TRONG THÁNG', tong_hop_tang)
        sheet.write('D4', 'TĂNG', tong_hop_tang)
        sheet.write('E4', 'GIẢM', tong_hop_tang)
        sheet.write('F4', 'NGHỈ THAI SẢN', tong_hop_tang)
        sheet.write('G4', 'NGHỈ ỐM ĐAU', tong_hop_tang)
        sheet.write('H4', 'NGHỈ KHÔNG LƯƠNG', tong_hop_tang)
        sheet.write('I4', 'TỔNG LAO ĐỘNG LÀM VIỆC', tong_hop_tang)

        tong_hop_tong_lao_dong = workbook.add_format({'bold': True,
                                                      'font_size': 11,
                                                      'align': 'center',
                                                      'valign': 'vcenter',
                                                      'border': 1,
                                                      'text_wrap': True,
                                                      'font_color': '#ff0000',
                                                      'bg_color': '#ffff00',
                                                      'font_name': "Times New Roman"})
        sheet.write('J4', 'TỔNG LAO ĐỘNG', tong_hop_tong_lao_dong)
        sheet.set_row(0, 27)
        sheet.set_row(1, 15)
        sheet.set_row(2, 21)
        sheet.set_row(3, 43)
        sheet.set_column('A:A', 8)
        sheet.set_column('B:B', 70)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:E', 8)
        sheet.set_column('F:H', 17)
        sheet.set_column('I:I', 13)
        stt = 0
        tong_hop_stt = workbook.add_format({'bold': True,
                                            'font_size': 11,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_color': '#000000',
                                            'font_name': "Times New Roman"})
        tong_hop_company_name = workbook.add_format({'bold': True,
                                                     'font_size': 11,
                                                     'align': 'center',
                                                     'valign': 'vcenter',
                                                     'border': 1,
                                                     'text_wrap': True,
                                                     'font_color': '#3b63c1',
                                                     'font_name': "Times New Roman"})
        row = 4
        tong_ld_thang_truoc = 0
        tong_tang = 0
        tong_giam = 0
        tong_nghi_thai_san = 0
        tong_nghi_om_dau = 0
        tong_nghi_khong_luong = 0
        tong_current_ld = 0
        tong_ld = 0

        for i in objects.bdns_companies:
            stt += 1
            row += 1
            sheet.set_row(row, 23)
            sheet.write('A%s' % row, stt, tong_hop_stt)
            sheet.write('B%s' % row, i.company_name, tong_hop_company_name)
            sheet.write('C%s' % row, i.employee_previous_month_total, tong_hop_tong_laodong_thang_truoc)
            sheet.write('D%s' % row, i.employee_increase, tong_hop_tang)
            sheet.write('E%s' % row, i.employee_decrease, tong_hop_tang)
            sheet.write('F%s' % row, i.nghi_thai_san, tong_hop_tang)
            sheet.write('G%s' % row, i.nghi_om_dau, tong_hop_tang)
            sheet.write('H%s' % row, i.nghi_khong_luong, tong_hop_tang)
            sheet.write('I%s' % row, i.employee_current_working_total, tong_hop_tang)
            sheet.write('J%s' % row, i.employee_working_total, tong_hop_tong_lao_dong)
            tong_ld_thang_truoc += i.employee_previous_month_total
            tong_tang += i.employee_increase
            tong_giam += i.employee_decrease
            tong_nghi_thai_san += i.nghi_thai_san
            tong_nghi_om_dau += i.nghi_om_dau
            tong_nghi_khong_luong += i.nghi_khong_luong
            tong_current_ld += i.employee_current_working_total
            tong_ld += i.employee_working_total

        tong_cong_style = workbook.add_format({'bold': True,
                                               'font_size': 11,
                                               'align': 'center',
                                               'valign': 'vcenter',
                                               'border': 1,
                                               'text_wrap': True,
                                               'font_color': '#000000',
                                               'font_name': "Times New Roman"})
        row += 1

        sheet.merge_range('A%s:B%s' % (row, row), 'TỔNG CỘNG', tong_cong_style)
        sheet.write('C%s' % row, tong_ld_thang_truoc, tong_cong_style)
        sheet.write('D%s' % row, tong_tang, tong_cong_style)
        sheet.write('E%s' % row, tong_giam, tong_cong_style)
        sheet.write('F%s' % row, tong_nghi_thai_san, tong_cong_style)
        sheet.write('G%s' % row, tong_nghi_om_dau, tong_cong_style)
        sheet.write('H%s' % row, tong_nghi_khong_luong, tong_cong_style)
        sheet.write('I%s' % row, tong_current_ld, tong_cong_style)
        sheet.write('J%s' % row, tong_ld, tong_cong_style)
        sheet.freeze_panes(4, 2)

        '''Add Sheet Company'''
        for i in objects.bdns_companies:

            sheet = workbook.add_worksheet(_(i.sudo().company_id.short_name))
            sheet.set_column('D:E', 10)
            sheet.set_column('F:G', 30)
            sheet.set_column('H:J', 17)
            sheet.set_column('K:K', 12)
            sheet.set_column('L:R', 11)
            sheet.set_column('S:U', 4)
            sheet.set_column('S:U', 10)
            sheet.set_column('AB:AD', 17)
            sheet.set_column('AE:AF', 11)
            sheet.set_row(8, 20)
            sheet.set_row(9, 33)

            if i.sudo().company_id:
                if i.sudo().company_id.logo_web:
                    image_company = io.BytesIO(base64.b64decode(i.sudo().company_id.logo_web))
                    sheet.insert_image('C1', "logocompany.png",
                                       {'image_data': image_company, 'x_scale': 1, 'y_scale': 1})
                title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
                title_style_name_company = workbook.add_format({'bold': True,
                                                                'font_size': 20,
                                                                'font_name': "Times New Roman",
                                                                'align': 'left',
                                                                'valign': 'vcenter'})
                sheet.write('D1', i.sudo().company_name, title_style_name_company)
                sheet.write('D2', i.sudo().company_id.sea_company_foreign, title_style_name_company)
                title_style = workbook.add_format({'bold': True,
                                                   'font_size': 20,
                                                   'font_name': "Times New Roman",
                                                   'align': 'center',
                                                   'valign': 'vcenter'})
                sheet.merge_range('A6:AL6', 'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ', title_style)
                date = ''
                if objects.update_date is not None:
                    if objects.update_date:
                        date = 'Từ ' + str(objects.update_date.replace(day=1).strftime("%d/%m/%Y")) + ' đến ' + str(
                            objects.update_date.strftime("%d/%m/%Y"))

                sheet.merge_range('A7:AL7', date, tong_hop_date)
                if objects.update_date is not None:
                    update_date = 'Ngày Cập Nhật: ' + str(objects.update_date.strftime("%d/%m/%Y"))
                    update_date_style = workbook.add_format({'bold': True,
                                                             'font_size': 12,
                                                             'font_name': "Times New Roman",
                                                             'font_color': '#ff0000',
                                                             'valign': 'vcenter'})
                    sheet.write('AB8', update_date, update_date_style)
                address = ''
                if i.sudo().company_id.street:
                    address += i.sudo().company_id.street
                if i.sudo().company_id.street2:
                    address += i.sudo().company_id.street2
                if i.sudo().company_id.city:
                    address += i.sudo().company_id.city
                if i.sudo().company_id.state_id:
                    address += i.sudo().company_id.state_id.name
                if i.sudo().company_id.country_id:
                    address += ', ' + i.sudo().company_id.country_id.name
                sheet.write('D3', address, title_style_address_company)
                sheet.set_row(3, 28)
                header_style = workbook.add_format({'bold': True,
                                                    'font_size': 9,
                                                    'font_name': "Times New Roman",
                                                    'font_color': '#000000',
                                                    'bg_color': '#fce4d6',
                                                    'align': 'center',
                                                    'border': 1,
                                                    'text_wrap': True,
                                                    'valign': 'vcenter'})
                sheet.merge_range('A9:A10', 'STT', header_style)
                sheet.merge_range('B9:B10', 'MÃ NV', header_style)
                sheet.merge_range('C9:C10', 'HỌ TÊN', header_style)
                sheet.merge_range('D9:D10', 'GIỚI TÍNH', header_style)
                sheet.merge_range('E9:E10', 'NGÀY SINH', header_style)
                sheet.merge_range('F9:F10', 'CHỨC VỤ', header_style)
                sheet.merge_range('G9:G10', 'CÔNG VIỆC ĐẢM NHẬN', header_style)
                sheet.merge_range('H9:H10', 'SỐ SỔ BẢO HIỂM', header_style)
                sheet.merge_range('I9:I10', 'MÃ THẺ HIỂM Y TẾ', header_style)
                sheet.merge_range('J9:J10', 'MÃ SỐ THUẾ', header_style)
                sheet.merge_range('K9:K10', 'SỐ NGƯỜI PHỤ THUỘC', header_style)
                sheet.merge_range('L9:N9', 'CMND/THẺ CĂN CƯỢC', header_style)
                sheet.write('L10', 'SỐ', header_style)
                sheet.write('M10', 'NGÀY CẤP', header_style)
                sheet.write('N10', 'NƠI CẤP', header_style)
                sheet.merge_range('O9:P9', 'NGÀY VÀO SEAGROUP', header_style)
                sheet.write('O10', 'TV', header_style)
                sheet.write('P10', 'CHÍNH THỨC', header_style)
                sheet.merge_range('Q9:R9', 'NGÀY VÀO ' + str(i.sudo().company_id.short_name), header_style)
                sheet.write('Q10', 'TV', header_style)
                sheet.write('R10', 'CHÍNH THỨC', header_style)
                sheet.merge_range('S9:U9', 'THÂM NIÊN', header_style)
                sheet.write('S10', 'Y', header_style)
                sheet.write('T10', 'M', header_style)
                sheet.write('U10', 'D', header_style)
                sheet.write('V9', '', header_style)
                sheet.write('V10', 'LƯƠNG KHOÁN/THỬ VIỆC', header_style)
                sheet.merge_range('W9:Y9', 'THU NHẬP', header_style)
                sheet.write('W10', 'LƯƠNG CHÍNH', header_style)
                sheet.write('X10', 'LƯƠNG BỔ SUNG', header_style)
                sheet.write('Y10', 'TỔNG', header_style)
                sheet.merge_range('Z9:AC9', ' HỢP ĐỒNG LAO ĐỘNG(Hợp đồng gần nhất)', header_style)
                sheet.write('Z10', 'LOẠI HĐ', header_style)
                sheet.write('AA10', 'SỐ HĐ', header_style)
                sheet.write('AB10', 'NGÀY KÝ HỢP ĐỒNG (Ghi ngày ký HĐ)', header_style)
                sheet.write('AC10', 'NGÀY HẾT HẠN HỢP ĐỒNG', header_style)
                sheet.merge_range('AD9:AF9', 'TÌNH TRẠNG LAO ĐỘNG', header_style)
                sheet.write('AD10', 'LÀM VIỆC/ NGHỈ CHẾ ĐỘ/ THÔI VIỆC', header_style)
                sheet.write('AE10', 'NGHỈ TỪ NGÀY', header_style)
                sheet.write('AF10', 'ĐẾN NGÀY', header_style)
                sheet.merge_range('AG9:AG10', 'ĐỊA CHỈ THƯỜNG TRÚ', header_style)
                sheet.merge_range('AH9:AH10', 'ĐỊA CHỈ TẠM TRÚ', header_style)
                sheet.merge_range('AI9:AI10', 'ĐIỆN THOẠI DI ĐỘNG', header_style)
                sheet.merge_range('AJ9:AJ10', 'EMAIL CÁ NHÂN', header_style)
                sheet.merge_range('AK9:AK10', 'EMAIL CÔNG TY', header_style)
                sheet.merge_range('AL9:AL10', 'GHI CHÚ', header_style)

                sheet.write('AF10', 'ĐẾN NGÀY', header_style)

                department_style = workbook.add_format({'bold': True,
                                                        'font_size': 9,
                                                        'font_name': "Times New Roman",
                                                        'font_color': '#000000',
                                                        'bg_color': '#e2efda',
                                                        'align': 'left',
                                                        'border': 1,
                                                        'text_wrap': True,
                                                        'valign': 'vcenter'})

                row = 10
                stt = 0
                departments = self.env['hr.department'].sudo().search(
                    [('company_id', '=', i.sudo().company_id.id), ('active', '=', True)], order='sort_name asc')

                list_not_in = []
                list_in = []
                for department in departments:
                    row += 1
                    job_positions = self.env['hr.job'].sudo().search(
                        [('company_id', '=', i.sudo().company_id.id), ('department_id', '=', department.id)],
                        order='sequence asc')
                    sheet.set_row(row - 1, 20)
                    department_parent = ''
                    if department.parent_id:
                        department_parent = department.sudo().parent_id.name + '/'
                    sheet.merge_range('B%s:AL%s' % (row, row), department_parent + department.name, department_style)

                    for job_position in job_positions:
                        for content in i.bdns_employees:
                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', content.sudo().employee_id.id), ('department_id', '=', department.id),
                                 ('job_id', '=', job_position.id),
                                 ('company_id', '=', i.sudo().company_id.id)])
                            if employee:
                                stt += 1
                                row += 1
                                list_in.append(employee.sudo().name.id)
                                self.employee_list(stt, row, sheet, employee, workbook, objects)

                employee_multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', i.sudo().company_id.id),
                     ('name', 'in', [employee_id.sudo().employee_id.id for employee_id in i.bdns_employees]),
                     ('name', 'not in', list_in)])
                for employee_multi_company in employee_multi_companies:
                    list_not_in.append(employee_multi_company.sudo().name.id)
                if len(list_not_in) > 0:
                    employees = self.env['hr.employee.multi.company'].sudo().search(
                        [('name', 'in', list_not_in), ('company_id', '=', i.sudo().company_id.id)])
                    for employee in employees:
                        stt += 1
                        row += 1
                        self.employee_list(stt, row, sheet, employee, workbook, objects)

                content_noborder_style = workbook.add_format({'bold': True,
                                                              'font_size': 9,
                                                              'font_name': "Times New Roman",
                                                              'font_color': '#000000',
                                                              'align': 'center',
                                                              'text_wrap': True,
                                                              'valign': 'vcenter'})
                row += 2
                sheet.merge_range('A%s:C%s' % (row, row), 'TỔNG HỢP THÁNG', content_noborder_style)
                if objects.update_date:
                    sheet.merge_range('AA%s:AF%s' % (row, row),
                                      ',ngày ' + str(objects.update_date.day) + ' tháng ' + str(
                                          objects.update_date.month) + ' năm ' + str(objects.update_date.year),
                                      content_noborder_style)
                row += 1
                sheet.merge_range('AA%s:AF%s' % (row, row), 'Người lập', content_noborder_style)
                row += 1
                sheet.write('B%s' % row, 'STT', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NỘI DUNG TỔNG HỢP', header_style)
                sheet.write('F%s' % row, 'SL', header_style)
                sheet.merge_range('G%s:H%s' % (row, row), 'GHI CHÚ', header_style)
                row += 1
                sheet.write('B%s' % row, '1', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LĐ THÁNG TRƯỚC (ĐẦU KỲ)', header_style)
                sheet.write('F%s' % row, i.employee_previous_month_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)
                row += 1
                sheet.write('B%s' % row, '2', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TĂNG', header_style)
                sheet.write('F%s' % row, i.employee_increase, header_style)
                current_month = objects.month
                current_year = objects.year
                if i.employee_increase > 0:
                    tangs = self.env.cr.execute(
                        'SELECT b.name, b.id, a.joining_date FROM hr_employee as b, hr_employee_multi_company as a WHERE b.id = a.name and a.active = true and a.company_id = %s and a.employee_current_status != \'resigned\' and a.joining_date is not null and EXTRACT(MONTH FROM a.joining_date) = %s and EXTRACT(YEAR FROM a.joining_date) = %s',
                        (i.sudo().company_id.id, current_month, current_year))

                    tangs = self.env.cr.dictfetchall()
                    tang_s = ''
                    for tang in tangs:
                        if tang['name']:
                            tang_s += tang['name'] + ' '
                            # company_joining = self.env['hr.contract'].sudo().search(
                            #     [('employee_id', '=', tang['name'].id), ('state', '!=', 'cancel'),
                            #      ('type_id', 'in', [1, 4]), ('company_id', '=', i.sudo().company_id.id)],
                            #     order='date_start asc', limit=1)
                            # if company_joining:
                            #     tang_s += '(' + company_joining.sudo().date_start.strftime("%d/%m/%Y") + '), '
                        if tang['joining_date']:
                            tang_s += '(' + tang['joining_date'].strftime("%d/%m/%Y") + '), '
                    sheet.merge_range('G%s:H%s' % (row, row), str(tang_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)
                row += 1
                sheet.write('B%s' % row, '3', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'GIẢM', header_style)
                sheet.write('F%s' % row, i.employee_decrease, header_style)
                if i.employee_decrease > 0:
                    giams = self.env.cr.execute(
                        'SELECT b.name, b.id, a.resignation_date FROM hr_employee_multi_company as a, hr_employee as b WHERE b.id = a.name and a.active = true and a.company_id = %s and a.employee_current_status = \'resigned\' and a.resignation_date is not null and EXTRACT(MONTH FROM a.resignation_date) = %s and EXTRACT(YEAR FROM a.resignation_date) = %s',
                        (i.sudo().company_id.id, current_month, current_year))
                    giams = self.env.cr.dictfetchall()
                    giam_s = ''
                    for giam in giams:
                        if giam['name']:
                            giam_s += giam['name'] + ' '
                        if giam['resignation_date']:
                            giam_s += '(' + giam['resignation_date'].strftime("%d/%m/%Y") + '),  '
                    sheet.merge_range('G%s:H%s' % (row, row), str(giam_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                if self.env.user.employee_id:
                    sheet.merge_range('AA%s:AF%s' % (row, row), self.env.user.employee_id.name, content_noborder_style)
                row += 1
                sheet.write('B%s' % row, '4', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ THAI SẢN', header_style)
                sheet.write('F%s' % row, i.nghi_thai_san, header_style)
                print(i.sudo().company_id.name)
                print("thai san")
                print(i.nghi_thai_san)
                if i.nghi_thai_san > 0:
                    '''Nghi Thai San'''
                    thai_sans = self.env.cr.execute(
                        'SELECT c.name, c.id, b.resignation_date, b.leaving_to_date \
                        FROM sea_employee_history_current_status b \
                        INNER JOIN hr_employee c on c.active = true and c.active = true \
                        INNER JOIN hr_employee_multi_company a \
                            on a.name = c.id and b.employee_multi_id = a.id and a.active = true and a.company_id = %s \
                         where b.active = true and b.resignation_date <= %s and \
                                b.employee_current_status = \'maternity_leave\' and \
                                (b.leaving_to_date >= %s or b.leaving_to_date is null)',
                        (i.sudo().company_id.id, objects.update_date, objects.update_date))

                    thai_sans = self.env.cr.dictfetchall()
                    thai_san_s = ''
                    for thai_san in thai_sans:
                        if thai_san['name']:
                            thai_san_s += thai_san['name'] + ' '
                        if thai_san['resignation_date']:
                            thai_san_s += '(' + thai_san['resignation_date'].strftime("%d/%m/%Y")
                            thai_san_s += ' - ' + thai_san['leaving_to_date'].strftime("%d/%m/%Y") + '), ' \
                                if thai_san['leaving_to_date'] not in [None, False] else '), '
                    sheet.merge_range('G%s:H%s' % (row, row), str(thai_san_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '5', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ ỐM ĐAU', header_style)
                sheet.write('F%s' % row, i.nghi_om_dau, header_style)
                print("om dau")
                print(i.nghi_om_dau)
                if i.nghi_om_dau > 0:
                    '''Nghi Om Dau'''
                    benhs = self.env.cr.execute(
                        'SELECT c.name, c.id, b.resignation_date, b.leaving_to_date\
                        FROM sea_employee_history_current_status b \
                        INNER JOIN hr_employee c on c.active = true and c.active = true \
                        INNER JOIN hr_employee_multi_company a \
                            on a.name = c.id and b.employee_multi_id = a.id and a.active = true and a.company_id = %s \
                         where b.active = true and b.resignation_date <= %s and \
                                b.employee_current_status = \'sick_leave\' and \
                                (b.leaving_to_date >= %s or b.leaving_to_date is null)',
                        (i.sudo().company_id.id, objects.update_date, objects.update_date))

                    benhs = self.env.cr.dictfetchall()

                    benh_s = ''
                    for benh in benhs:
                        if benh['name']:
                            benh_s += benh['name'] + ' '
                        if benh['resignation_date']:
                            benh_s += '(' + benh['resignation_date'].strftime("%d/%m/%Y")
                            benh_s += ' - ' + benh['leaving_to_date'].strftime("%d/%m/%Y") + '), ' \
                                if benh['leaving_to_date'] not in [None, False] else '), '
                    sheet.merge_range('G%s:H%s' % (row, row), str(benh_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '6', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ KHÔNG LƯƠNG', header_style)
                sheet.write('F%s' % row, i.nghi_khong_luong, header_style)
                print("khong luong")
                print(i.nghi_khong_luong)
                if i.nghi_khong_luong > 0:
                    '''Nghi khong luong'''
                    khong_luongs = self.env.cr.execute(
                        'SELECT c.name, c.id, b.resignation_date, b.leaving_to_date \
                        FROM sea_employee_history_current_status b \
                        INNER JOIN hr_employee c on c.active = true and c.active = true \
                        INNER JOIN hr_employee_multi_company a \
                            on a.name = c.id and b.employee_multi_id = a.id and a.active = true and a.company_id = %s \
                         where b.active = true and b.resignation_date <= %s and \
                                b.employee_current_status = \'leaving\' and \
                                (b.leaving_to_date >= %s or b.leaving_to_date is null)',
                        (i.sudo().company_id.id, objects.update_date, objects.update_date))

                    khong_luongs = self.env.cr.dictfetchall()

                    khong_luong_s = ''
                    for khong_luong in khong_luongs:
                        if khong_luong['name']:
                            khong_luong_s += str(khong_luong['name']) + ' '
                        if khong_luong['resignation_date']:
                            khong_luong_s += '(' + khong_luong['resignation_date'].strftime("%d/%m/%Y")
                            khong_luong_s += ' - ' + khong_luong['leaving_to_date'].strftime("%d/%m/%Y") + '), ' \
                                if khong_luong['leaving_to_date'] not in [None, False] else '), '
                    sheet.merge_range('G%s:H%s' % (row, row), str(khong_luong_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '7', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LĐ LÀM VIỆC', header_style)
                sheet.write('F%s' % row, i.employee_current_working_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '8', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LAO ĐỘNG', header_style)
                sheet.write('F%s' % row, i.employee_working_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                sheet.set_column('A:A', 4)
                sheet.set_column('B:B', 11)
                sheet.set_column('C:C', 28)
                sheet.set_column('F:G', 28)
                sheet.set_column('AG:AL', 28)
                sheet.freeze_panes(10, 3)


class DanhSachBienDongNhanSu(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_biendong_nhansu_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def employee_list(self, stt, row, sheet, employee_id, workbook, objects):
        salary_style = workbook.add_format({'bold': False,
                                            'font_size': 9,
                                            'font_name': "Times New Roman",
                                            'font_color': '#000000',
                                            'align': 'center',
                                            'border': 1,
                                            'text_wrap': True,
                                            'num_format': '#,###',
                                            'valign': 'vcenter'})
        content_style = workbook.add_format({'bold': False,
                                             'font_size': 9,
                                             'font_name': "Times New Roman",
                                             'font_color': '#000000',
                                             'align': 'center',
                                             'border': 1,
                                             'text_wrap': True,
                                             'valign': 'vcenter'})
        sheet.write('A%s' % row, stt, content_style)
        if employee_id.sudo().name.s_identification_id:
            sheet.write('B%s' % row, employee_id.sudo().name.s_identification_id, content_style)
        else:
            sheet.write('B%s' % row, '', content_style)
        if employee_id.sudo().name.name:
            sheet.write('C%s' % row, employee_id.sudo().name.name, content_style)
        else:
            sheet.write('C%s' % row, '', content_style)
        if employee_id.sudo().name.gender == 'male':
            sheet.write('D%s' % row, 'Nam', content_style)
        else:
            sheet.write('D%s' % row, 'Nữ', content_style)
        if employee_id.sudo().name.birthday:
            sheet.write('E%s' % row, employee_id.sudo().name.birthday.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('E%s' % row, '', content_style)
        if employee_id.sudo().job_id:
            sheet.write('F%s' % row, employee_id.sudo().job_id.sudo().name, content_style)
        else:
            sheet.write('F%s' % row, '', content_style)
        if employee_id.sudo().job_title:
            sheet.write('G%s' % row, employee_id.sudo().job_title, content_style)
        else:
            sheet.write('G%s' % row, '', content_style)
        if employee_id.sudo().name.social_insurance_number:
            sheet.write('H%s' % row, employee_id.sudo().name.social_insurance_number, content_style)
        else:
            sheet.write('H%s' % row, '', content_style)
        if employee_id.sudo().name.health_insurance_number:
            sheet.write('I%s' % row, employee_id.sudo().name.health_insurance_number, content_style)
        else:
            sheet.write('I%s' % row, '', content_style)
        if employee_id.sudo().name.tax_tncn_code:
            sheet.write('J%s' % row, employee_id.sudo().name.tax_tncn_code, content_style)
        else:
            sheet.write('J%s' % row, '', content_style)

        family = self.env['hr.employee.family'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('member_independent', '=', 'Y')])
        if family:
            sheet.write('K%s' % row, len(family), content_style)
        else:
            sheet.write('K%s' % row, '', content_style)

        if employee_id.sudo().name.sudo().identification_id:
            sheet.write('L%s' % row, employee_id.sudo().name.sudo().identification_id, content_style)
        else:
            sheet.write('L%s' % row, '', content_style)
        if employee_id.sudo().name.sudo().sea_id_issue_date:
            sheet.write('M%s' % row, employee_id.sudo().name.sudo().sea_id_issue_date.strftime("%d/%m/%Y"),
                        content_style)
        if employee_id.sudo().name.sudo().id_issue_place.sudo().name:
            sheet.write('N%s' % row, employee_id.sudo().name.sudo().id_issue_place.sudo().name, content_style)
        else:
            sheet.write('N%s' % row, '', content_style)

        seagroup_tv = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 4), ('contract_category', '=', 'contract')], order='date_start asc', limit=1)
        seagroup_ct = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 1), ('contract_category', '=', 'contract')], order='date_start asc', limit=1)

        company_tv = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 4), ('contract_category', '=', 'contract'),
             ('company_id', '=', employee_id.sudo().company_id.id)], order='date_start asc', limit=1)
        company_ct = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('state', '!=', 'cancel'),
             ('type_id', '=', 1), ('contract_category', '=', 'contract'),
             ('company_id', '=', employee_id.sudo().company_id.id)], order='date_start asc', limit=1)

        if seagroup_tv.sudo().date_start:
            sheet.write('O%s' % row, seagroup_tv.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('O%s' % row, '', content_style)
        if seagroup_ct.sudo().date_start:
            sheet.write('P%s' % row, seagroup_ct.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('P%s' % row, '', content_style)
        if company_tv.sudo().date_start:
            sheet.write('Q%s' % row, company_tv.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('Q%s' % row, '', content_style)
        if company_ct.sudo().date_start:
            sheet.write('R%s' % row, company_ct.sudo().date_start.strftime("%d/%m/%Y"), content_style)
        else:
            sheet.write('R%s' % row, '', content_style)

        tham_nien = ''
        if employee_id.sudo().seagroup_join_date and objects.update_date:
            tham_nien = objects.update_date - employee_id.sudo().seagroup_join_date
            start = date(1, 1, 1)  # This is the "days since" part
            if tham_nien.days > 0:
                delta = timedelta(tham_nien.days - 1)  # Create a time delta object from the number of days
                tham_nien = start + delta
            else:
                tham_nien = date(1, 1, 1)

        if employee_id.sudo().seagroup_join_date and objects.update_date:
            sheet.write('S%s' % row, tham_nien.year - 1, content_style)
        else:
            sheet.write('S%s' % row, '', content_style)
        if employee_id.sudo().seagroup_join_date:
            sheet.write('T%s' % row, tham_nien.month - 1, content_style)
        else:
            sheet.write('T%s' % row, '', content_style)
        if employee_id.sudo().seagroup_join_date:
            sheet.write('U%s' % row, tham_nien.day - 1, content_style)
        else:
            sheet.write('U%s' % row, '', content_style)

        contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending', 'close']), ('type_id', '=', 4)], order='wage desc', limit=1)
        if contract.sudo().wage:
            sheet.write('V%s' % row, float('%.2f' % float(contract.sudo().wage)), salary_style)
        else:
            sheet.write('V%s' % row, '', salary_style)

        salary_contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending']), ('type_id', '=', 1), (
                 'wage', '>', 0)], order='wage desc', limit=1)

        salary_extend = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending']), ('type_id', '=', 1), ('contract_extend_salary', '>', 0),
             ('contract_category', '=', 'addition')], order='contract_extend_salary desc', limit=1)
        tong = 0
        if salary_contract.sudo().wage:
            sheet.write('W%s' % row, float('%.2f' % float(salary_contract.sudo().wage)), salary_style)
            tong += float(salary_contract.sudo().wage)
        else:
            sheet.write('W%s' % row, '', salary_style)

        if salary_extend.sudo().contract_extend_salary:
            sheet.write('X%s' % row,
                        float('%.2f' % float(salary_extend.sudo().contract_extend_salary)), salary_style)
            tong += float(salary_extend.sudo().contract_extend_salary)
        else:
            sheet.write('X%s' % row, '', salary_style)

        if tong > 0:
            sheet.write('Y%s' % row, tong, salary_style)
        else:
            sheet.write('Y%s' % row, '', salary_style)

        contract = self.env['hr.contract'].sudo().search(
            [('employee_id', '=', employee_id.sudo().name.id), ('company_id', '=', employee_id.sudo().company_id.id),
             ('state', 'in', ['open', 'pending']), ('active', '=', True),
             ('contract_category', '=', 'contract')], order='date_start desc', limit=1)
        if contract.sudo():
            if contract.sudo().contract_period_id.sudo().name:
                sheet.write('Z%s' % row, contract.sudo().contract_period_id.sudo().name, content_style)
            else:
                sheet.write('Z%s' % row, '', content_style)

            sheet.write('AA%s' % row, contract.sudo().name, content_style)
            if contract.sudo().date_start:
                sheet.write('AB%s' % row, contract.sudo().date_start.strftime("%d/%m/%Y"), content_style)
            else:
                sheet.write('AB%s' % row, '', content_style)

            if contract.sudo().date_end:
                sheet.write('AC%s' % row, contract.sudo().date_end.strftime("%d/%m/%Y"), content_style)
            else:
                sheet.write('AC%s' % row, '', content_style)
        else:
            sheet.write('Z%s' % row, '', content_style)
            sheet.write('AA%s' % row, '', content_style)
            sheet.write('AB%s' % row, '', content_style)
            sheet.write('AC%s' % row, '', content_style)
        current_status = ''
        if employee_id.sudo().employee_current_status == 'working':
            current_status = 'Đang làm việc'
        elif employee_id.sudo().employee_current_status == 'leaving':
            current_status = 'Nghỉ không lương'
        elif employee_id.sudo().employee_current_status == 'maternity_leave':
            current_status = 'Nghỉ thai sản'
        elif employee_id.sudo().employee_current_status == 'sick_leave':
            current_status = 'Nghỉ đau ốm'
        sheet.write('AD%s' % row, current_status or '', content_style)
        resignation_date = ''
        leaving_to_date = ''
        if employee_id.sudo().employee_current_status != 'working' and employee_id.sudo().leaving_to_date and employee_id.sudo().resignation_date:
            leaving_to_date = employee_id.sudo().leaving_to_date.strftime("%d/%m/%Y")
            resignation_date = employee_id.sudo().resignation_date.strftime("%d/%m/%Y")

        sheet.write('AE%s' % row, resignation_date or '', content_style)
        sheet.write('AF%s' % row, leaving_to_date or '', content_style)

        DC = ''
        DCTT = ''
        if employee_id.sudo().name.sea_permanent_addr:
            DC += employee_id.sudo().name.sea_permanent_addr + ', '
        if employee_id.sudo().name.sudo().permanent_district_id.id:
            DC += employee_id.sudo().name.sudo().permanent_district_id.name + ', '
        if employee_id.sudo().name.sudo().permanent_city_id.id:
            DC += employee_id.sudo().name.sudo().permanent_city_id.name + ', '
        if employee_id.sudo().name.sudo().permanent_country_id.id:
            DC += employee_id.sudo().name.sudo().permanent_country_id.name

        sheet.write('AG%s' % row, DC or '', content_style)

        if employee_id.sudo().name.sea_temp_addr:
            DCTT += employee_id.sudo().name.sea_temp_addr + ', '
        if employee_id.sudo().name.sudo().temporary_district_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_district_id.name + ', '
        if employee_id.sudo().name.sudo().temporary_city_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_city_id.name + ', '
        if employee_id.sudo().name.sudo().temporary_country_id.id:
            DCTT += employee_id.sudo().name.sudo().temporary_country_id.name

        sheet.write('AH%s' % row, DCTT or '', content_style)

        sheet.write('AI%s' % row, employee_id.sudo().name.main_phone_number or '', content_style)
        sheet.write('AJ%s' % row, employee_id.sudo().name.sea_personal_email or '', content_style)
        sheet.write('AK%s' % row, employee_id.sudo().work_email or '', content_style)
        sheet.write('AL%s' % row, '', content_style)

    def get_department_child(self, list_department, id_department, department, department_search, index=1):
        list_department.append([index, department])
        for i in department_search:
            if i.parent_id.id == id_department:
                self.get_department_child(list_department=list_department, id_department=i.id, department=i,
                                          department_search=department_search, index=index + 1)

    def get_job_position(self, employee_id):
        search = self.env['hr.employee'].sudo().search([('id', '=', employee_id)], limit=1)

        if search.job_id:
            if search.job_id.sequence == 0:
                return 99
            return search.job_id.sequence
        return 99

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})

        sheet = workbook.add_worksheet(_('TỔNG HỢP'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': False,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center'})
        sheet.write('A1', 'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ', tong_hop_title)

        sheet.merge_range('A1:I1', 'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ', tong_hop_title)
        date = ''
        if objects.update_date is not None:
            if objects.update_date:
                date = 'Từ ' + str(objects.update_date.replace(day=1).strftime("%d/%m/%Y")) + ' đến ' + str(
                    objects.update_date.strftime("%d/%m/%Y"))
        sheet.merge_range('A2:I2', date, tong_hop_date)
        '''STT'''
        tong_hop_stt = workbook.add_format({'bold': True,
                                            'font_size': 13,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_name': "Times New Roman"})
        sheet.merge_range('A3:A4', 'STT', tong_hop_stt)
        sheet.merge_range('B3:B4', 'ĐƠN VỊ', tong_hop_stt)
        tong_hop_tong_laodong_thang_truoc = workbook.add_format({'bold': True,
                                                                 'font_size': 11,
                                                                 'align': 'center',
                                                                 'valign': 'vcenter',
                                                                 'border': 1,
                                                                 'text_wrap': True,
                                                                 'font_color': '#c00000',
                                                                 'bg_color': '#f8cbad',
                                                                 'font_name': "Times New Roman"})
        sheet.merge_range('C3:C4', 'TỔNG LAO ĐỘNG THÁNG TRƯỚC', tong_hop_tong_laodong_thang_truoc)

        tong_hop_tang = workbook.add_format({'bold': True,
                                             'font_size': 11,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'border': 1,
                                             'text_wrap': True,
                                             'font_color': '#000000',
                                             'bg_color': '#bdd7ee',
                                             'font_name': "Times New Roman"})
        sheet.merge_range('D3:J3', 'TỔNG HỢP LAO ĐỘNG PHÁT SINH TRONG THÁNG', tong_hop_tang)
        sheet.write('D4', 'TĂNG', tong_hop_tang)
        sheet.write('E4', 'GIẢM', tong_hop_tang)
        sheet.write('F4', 'NGHỈ THAI SẢN', tong_hop_tang)
        sheet.write('G4', 'NGHỈ ỐM ĐAU', tong_hop_tang)
        sheet.write('H4', 'NGHỈ KHÔNG LƯƠNG', tong_hop_tang)
        sheet.write('I4', 'TỔNG LAO ĐỘNG LÀM VIỆC', tong_hop_tang)

        tong_hop_tong_lao_dong = workbook.add_format({'bold': True,
                                                      'font_size': 11,
                                                      'align': 'center',
                                                      'valign': 'vcenter',
                                                      'border': 1,
                                                      'text_wrap': True,
                                                      'font_color': '#ff0000',
                                                      'bg_color': '#ffff00',
                                                      'font_name': "Times New Roman"})
        sheet.write('J4', 'TỔNG LAO ĐỘNG', tong_hop_tong_lao_dong)
        sheet.set_row(0, 27)
        sheet.set_row(1, 15)
        sheet.set_row(2, 21)
        sheet.set_row(3, 43)
        sheet.set_column('A:A', 8)
        sheet.set_column('B:B', 70)
        sheet.set_column('C:C', 15)
        sheet.set_column('D:E', 8)
        sheet.set_column('F:H', 17)
        sheet.set_column('I:I', 13)
        stt = 0
        tong_hop_stt = workbook.add_format({'bold': True,
                                            'font_size': 11,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'border': 1,
                                            'font_color': '#000000',
                                            'font_name': "Times New Roman"})
        tong_hop_company_name = workbook.add_format({'bold': True,
                                                     'font_size': 11,
                                                     'align': 'center',
                                                     'valign': 'vcenter',
                                                     'border': 1,
                                                     'text_wrap': True,
                                                     'font_color': '#3b63c1',
                                                     'font_name': "Times New Roman"})
        row = 4
        tong_ld_thang_truoc = 0
        tong_tang = 0
        tong_giam = 0
        tong_nghi_thai_san = 0
        tong_nghi_om_dau = 0
        tong_nghi_khong_luong = 0
        tong_current_ld = 0
        tong_ld = 0

        for i in objects.bdns_companies:
            stt += 1
            row += 1
            sheet.set_row(row, 23)
            sheet.write('A%s' % row, stt, tong_hop_stt)
            sheet.write('B%s' % row, i.company_name, tong_hop_company_name)
            sheet.write('C%s' % row, i.employee_previous_month_total, tong_hop_tong_laodong_thang_truoc)
            sheet.write('D%s' % row, i.employee_increase, tong_hop_tang)
            sheet.write('E%s' % row, i.employee_decrease, tong_hop_tang)
            sheet.write('F%s' % row, i.nghi_thai_san, tong_hop_tang)
            sheet.write('G%s' % row, i.nghi_om_dau, tong_hop_tang)
            sheet.write('H%s' % row, i.nghi_khong_luong, tong_hop_tang)
            sheet.write('I%s' % row, i.employee_current_working_total, tong_hop_tang)
            sheet.write('J%s' % row, i.employee_working_total, tong_hop_tong_lao_dong)
            tong_ld_thang_truoc += i.employee_previous_month_total
            tong_tang += i.employee_increase
            tong_giam += i.employee_decrease
            tong_nghi_thai_san += i.nghi_thai_san
            tong_nghi_om_dau += i.nghi_om_dau
            tong_nghi_khong_luong += i.nghi_khong_luong
            tong_current_ld += i.employee_current_working_total
            tong_ld += i.employee_working_total

        tong_cong_style = workbook.add_format({'bold': True,
                                               'font_size': 11,
                                               'align': 'center',
                                               'valign': 'vcenter',
                                               'border': 1,
                                               'text_wrap': True,
                                               'font_color': '#000000',
                                               'font_name': "Times New Roman"})
        row += 1

        sheet.merge_range('A%s:B%s' % (row, row), 'TỔNG CỘNG', tong_cong_style)
        sheet.write('C%s' % row, tong_ld_thang_truoc, tong_cong_style)
        sheet.write('D%s' % row, tong_tang, tong_cong_style)
        sheet.write('E%s' % row, tong_giam, tong_cong_style)
        sheet.write('F%s' % row, tong_nghi_thai_san, tong_cong_style)
        sheet.write('G%s' % row, tong_nghi_om_dau, tong_cong_style)
        sheet.write('H%s' % row, tong_nghi_khong_luong, tong_cong_style)
        sheet.write('I%s' % row, tong_current_ld, tong_cong_style)
        sheet.write('J%s' % row, tong_ld, tong_cong_style)
        sheet.freeze_panes(4, 2)

        '''Add Sheet Company'''
        for i in objects.bdns_companies:

            sheet = workbook.add_worksheet(_(i.sudo().company_id.short_name))
            sheet.set_column('D:E', 10)
            sheet.set_column('F:G', 30)
            sheet.set_column('H:J', 17)
            sheet.set_column('K:K', 12)
            sheet.set_column('L:R', 11)
            sheet.set_column('S:U', 4)
            sheet.set_column('S:U', 10)
            sheet.set_column('AB:AD', 17)
            sheet.set_column('AE:AF', 11)
            sheet.set_row(8, 20)
            sheet.set_row(9, 33)

            if i.sudo().company_id:
                if i.sudo().company_id.logo_web:
                    image_company = io.BytesIO(base64.b64decode(i.sudo().company_id.logo_web))
                    sheet.insert_image('C1', "logocompany.png", {'image_data': image_company, 'x_scale': 1, 'y_scale': 1})
                title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
                title_style_name_company = workbook.add_format({'bold': True,
                                                                'font_size': 20,
                                                                'font_name': "Times New Roman",
                                                                'align': 'left',
                                                                'valign': 'vcenter'})
                sheet.write('D1', i.sudo().company_name, title_style_name_company)
                sheet.write('D2', i.sudo().company_id.sea_company_foreign, title_style_name_company)
                title_style = workbook.add_format({'bold': True,
                                                   'font_size': 20,
                                                   'font_name': "Times New Roman",
                                                   'align': 'center',
                                                   'valign': 'vcenter'})
                sheet.merge_range('A6:AL6', 'DANH SÁCH BIẾN ĐỘNG NHÂN SỰ', title_style)
                date = ''
                if objects.update_date is not None:
                    if objects.update_date:
                        date = 'Từ ' + str(objects.update_date.replace(day=1).strftime("%d/%m/%Y")) + ' đến ' + str(
                            objects.update_date.strftime("%d/%m/%Y"))

                sheet.merge_range('A7:AL7', date, tong_hop_date)
                if objects.update_date is not None:
                    update_date = 'Ngày Cập Nhật: ' + str(objects.update_date.strftime("%d/%m/%Y"))
                    update_date_style = workbook.add_format({'bold': True,
                                                             'font_size': 12,
                                                             'font_name': "Times New Roman",
                                                             'font_color': '#ff0000',
                                                             'valign': 'vcenter'})
                    sheet.write('AB8', update_date, update_date_style)
                address = ''
                if i.sudo().company_id.street:
                    address += i.sudo().company_id.street
                if i.sudo().company_id.street2:
                    address += i.sudo().company_id.street2
                if i.sudo().company_id.city:
                    address += i.sudo().company_id.city
                if i.sudo().company_id.state_id:
                    address += i.sudo().company_id.state_id.name
                if i.sudo().company_id.country_id:
                    address += ', ' + i.sudo().company_id.country_id.name
                sheet.write('D3', address, title_style_address_company)
                sheet.set_row(3, 28)
                header_style = workbook.add_format({'bold': True,
                                                    'font_size': 9,
                                                    'font_name': "Times New Roman",
                                                    'font_color': '#000000',
                                                    'bg_color': '#fce4d6',
                                                    'align': 'center',
                                                    'border': 1,
                                                    'text_wrap': True,
                                                    'valign': 'vcenter'})
                sheet.merge_range('A9:A10', 'STT', header_style)
                sheet.merge_range('B9:B10', 'MÃ NV', header_style)
                sheet.merge_range('C9:C10', 'HỌ TÊN', header_style)
                sheet.merge_range('D9:D10', 'GIỚI TÍNH', header_style)
                sheet.merge_range('E9:E10', 'NGÀY SINH', header_style)
                sheet.merge_range('F9:F10', 'CHỨC VỤ', header_style)
                sheet.merge_range('G9:G10', 'CÔNG VIỆC ĐẢM NHẬN', header_style)
                sheet.merge_range('H9:H10', 'SỐ SỔ BẢO HIỂM', header_style)
                sheet.merge_range('I9:I10', 'MÃ THẺ HIỂM Y TẾ', header_style)
                sheet.merge_range('J9:J10', 'MÃ SỐ THUẾ', header_style)
                sheet.merge_range('K9:K10', 'SỐ NGƯỜI PHỤ THUỘC', header_style)
                sheet.merge_range('L9:N9', 'CMND/THẺ CĂN CƯỢC', header_style)
                sheet.write('L10', 'SỐ', header_style)
                sheet.write('M10', 'NGÀY CẤP', header_style)
                sheet.write('N10', 'NƠI CẤP', header_style)
                sheet.merge_range('O9:P9', 'NGÀY VÀO SEAGROUP', header_style)
                sheet.write('O10', 'TV', header_style)
                sheet.write('P10', 'CHÍNH THỨC', header_style)
                sheet.merge_range('Q9:R9', 'NGÀY VÀO ' + str(i.sudo().company_id.short_name), header_style)
                sheet.write('Q10', 'TV', header_style)
                sheet.write('R10', 'CHÍNH THỨC', header_style)
                sheet.merge_range('S9:U9', 'THÂM NIÊN', header_style)
                sheet.write('S10', 'Y', header_style)
                sheet.write('T10', 'M', header_style)
                sheet.write('U10', 'D', header_style)
                sheet.write('V9', '', header_style)
                sheet.write('V10', 'LƯƠNG KHOÁN/THỬ VIỆC', header_style)
                sheet.merge_range('W9:Y9', 'THU NHẬP', header_style)
                sheet.write('W10', 'LƯƠNG CHÍNH', header_style)
                sheet.write('X10', 'LƯƠNG BỔ SUNG', header_style)
                sheet.write('Y10', 'TỔNG', header_style)
                sheet.merge_range('Z9:AC9', ' HỢP ĐỒNG LAO ĐỘNG(Hợp đồng gần nhất)', header_style)
                sheet.write('Z10', 'LOẠI HĐ', header_style)
                sheet.write('AA10', 'SỐ HĐ', header_style)
                sheet.write('AB10', 'NGÀY KÝ HỢP ĐỒNG (Ghi ngày ký HĐ)', header_style)
                sheet.write('AC10', 'NGÀY HẾT HẠN HỢP ĐỒNG', header_style)
                sheet.merge_range('AD9:AF9', 'TÌNH TRẠNG LAO ĐỘNG', header_style)
                sheet.write('AD10', 'LÀM VIỆC/ NGHỈ CHẾ ĐỘ/ THÔI VIỆC', header_style)
                sheet.write('AE10', 'NGHỈ TỪ NGÀY', header_style)
                sheet.write('AF10', 'ĐẾN NGÀY', header_style)
                sheet.merge_range('AG9:AG10', 'ĐỊA CHỈ THƯỜNG TRÚ', header_style)
                sheet.merge_range('AH9:AH10', 'ĐỊA CHỈ TẠM TRÚ', header_style)
                sheet.merge_range('AI9:AI10', 'ĐIỆN THOẠI DI ĐỘNG', header_style)
                sheet.merge_range('AJ9:AJ10', 'EMAIL CÁ NHÂN', header_style)
                sheet.merge_range('AK9:AK10', 'EMAIL CÔNG TY', header_style)
                sheet.merge_range('AL9:AL10', 'GHI CHÚ', header_style)

                sheet.write('AF10', 'ĐẾN NGÀY', header_style)

                department_style = workbook.add_format({'bold': True,
                                                        'font_size': 9,
                                                        'font_name': "Times New Roman",
                                                        'font_color': '#000000',
                                                        'bg_color': '#e2efda',
                                                        'align': 'left',
                                                        'border': 1,
                                                        'text_wrap': True,
                                                        'valign': 'vcenter'})

                row = 10
                stt = 0
                departments = self.env['hr.department'].sudo().search(
                    [('company_id', '=', i.sudo().company_id.id), ('active', '=', True)], order='sort_name asc')

                list_not_in = []
                list_in = []
                for department in departments:
                    row += 1
                    job_positions = self.env['hr.job'].sudo().search(
                        [('company_id', '=', i.sudo().company_id.id), ('department_id', '=', department.id)],
                        order='sequence asc')
                    sheet.set_row(row - 1, 20)
                    department_parent = ''
                    if department.parent_id:
                        department_parent = department.sudo().parent_id.name + '/'
                    sheet.merge_range('B%s:AL%s' % (row, row), department_parent + department.name, department_style)

                    for job_position in job_positions:
                        for content in i.bdns_employees:
                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', content.sudo().employee_id.id),
                                 ('company_id', '=', i.sudo().company_id.id), ('department_id', '=', department.id),
                                 ('job_id', '=', job_position.id), ('employee_current_status', '!=', 'resigned')])
                            if employee:
                                stt += 1
                                row += 1
                                list_in.append(employee.sudo().name.id)
                                self.employee_list(stt, row, sheet, employee, workbook, objects)

                employee_multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', i.sudo().company_id.id), ('employee_current_status', '!=', 'resigned')])
                for employee_multi_company in employee_multi_companies:
                    have_employee = 0
                    for list in list_in:
                        if employee_multi_company.sudo().name.id == list:
                            have_employee = 1
                            break
                    if have_employee == 0:
                        list_not_in.append(employee_multi_company.sudo().name.id)
                if len(list_not_in) > 0:
                    employees = self.env['hr.employee.multi.company'].sudo().search(
                        [('name', 'in', list_not_in), ('company_id', '=', i.sudo().company_id.id)])
                    for employee in employees:
                        stt += 1
                        row += 1
                        self.employee_list(stt, row, sheet, employee, workbook, objects)

                content_noborder_style = workbook.add_format({'bold': True,
                                                              'font_size': 9,
                                                              'font_name': "Times New Roman",
                                                              'font_color': '#000000',
                                                              'align': 'center',
                                                              'text_wrap': True,
                                                              'valign': 'vcenter'})
                row += 2
                sheet.merge_range('A%s:C%s' % (row, row), 'TỔNG HỢP THÁNG', content_noborder_style)
                if objects.update_date:
                    sheet.merge_range('AA%s:AF%s' % (row, row),
                                      ',ngày ' + str(objects.update_date.day) + ' tháng ' + str(
                                          objects.update_date.month) + ' năm ' + str(objects.update_date.year),
                                      content_noborder_style)
                row += 1
                sheet.merge_range('AA%s:AF%s' % (row, row), 'Người lập', content_noborder_style)
                row += 1
                sheet.write('B%s' % row, 'STT', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NỘI DUNG TỔNG HỢP', header_style)
                sheet.write('F%s' % row, 'SL', header_style)
                sheet.merge_range('G%s:H%s' % (row, row), 'GHI CHÚ', header_style)
                row += 1
                sheet.write('B%s' % row, '1', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LĐ THÁNG TRƯỚC (ĐẦU KỲ)', header_style)
                sheet.write('F%s' % row, i.employee_previous_month_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)
                row += 1
                sheet.write('B%s' % row, '2', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TĂNG', header_style)
                sheet.write('F%s' % row, i.employee_increase, header_style)
                current_month = fields.Datetime.now().month
                current_year = fields.Datetime.now().year
                if i.employee_increase > 0:
                    tangs = self.env.cr.execute(
                        'SELECT b.name, b.id, a.joining_date FROM hr_employee as b, hr_employee_multi_company as a WHERE b.id = a.name and a.active = true and a.company_id = %s and a.employee_current_status != \'resigned\' and a.joining_date is not null and EXTRACT(MONTH FROM a.joining_date) = %s and EXTRACT(YEAR FROM a.joining_date) = %s',
                        (i.sudo().company_id.id, current_month, current_year))

                    tangs = self.env.cr.dictfetchall()
                    tang_s = ''
                    for tang in tangs:
                        if tang['name']:
                            tang_s += tang['name'] + ' '
                            # company_joining = self.env['hr.contract'].sudo().search(
                            #     [('employee_id', '=', tang['name'].id), ('state', '!=', 'cancel'),
                            #      ('type_id', 'in', [1, 4]), ('company_id', '=', i.sudo().company_id.id)],
                            #     order='date_start asc', limit=1)
                            # if company_joining:
                            #     tang_s += '(' + company_joining.sudo().date_start.strftime("%d/%m/%Y") + '), '
                        if tang['joining_date']:
                            tang_s += '(' + tang['joining_date'].strftime("%d/%m/%Y") + '), '
                    sheet.merge_range('G%s:H%s' % (row, row), str(tang_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)
                row += 1
                sheet.write('B%s' % row, '3', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'GIẢM', header_style)
                sheet.write('F%s' % row, i.employee_decrease, header_style)
                if i.employee_decrease > 0:
                    giams = self.env.cr.execute(
                        'SELECT b.name, b.id, a.resignation_date FROM hr_employee_multi_company as a, hr_employee as b WHERE b.id = a.name and a.active = true and a.company_id = %s and a.employee_current_status = \'resigned\' and a.resignation_date is not null and EXTRACT(MONTH FROM a.resignation_date) = %s and EXTRACT(YEAR FROM a.resignation_date) = %s',
                        (i.sudo().company_id.id, current_month, current_year))
                    giams = self.env.cr.dictfetchall()
                    giam_s = ''
                    for giam in giams:
                        if giam['name']:
                            giam_s += giam['name'] + ' '
                        if giam['resignation_date']:
                            giam_s += '(' + giam['resignation_date'].strftime("%d/%m/%Y") + '),  '
                    sheet.merge_range('G%s:H%s' % (row, row), str(giam_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                if self.env.user.employee_id:
                    sheet.merge_range('AA%s:AF%s' % (row, row), self.env.user.employee_id.name, content_noborder_style)
                row += 1
                sheet.write('B%s' % row, '4', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ THAI SẢN', header_style)
                sheet.write('F%s' % row, i.nghi_thai_san, header_style)
                if i.nghi_thai_san > 0:
                    '''Nghi Thai San'''
                    thai_sans = self.env.cr.execute(
                        'SELECT b.name, b.id, a.resignation_date FROM hr_employee_multi_company as a, hr_employee as b WHERE b.id = a.name and a.active = true and  a.company_id = %s and a.employee_current_status = \'maternity_leave\' and a.resignation_date is not null and EXTRACT(MONTH FROM a.resignation_date) <= %s and EXTRACT(YEAR FROM a.resignation_date) <= %s',
                        (i.sudo().company_id.id, current_month, current_year))
                    thai_sans = self.env.cr.dictfetchall()
                    thai_san_s = ''
                    for thai_san in thai_sans:
                        if thai_san['name']:
                            thai_san_s += thai_san['name'] + ' '
                        if thai_san['resignation_date']:
                            thai_san_s += '(' + thai_san['resignation_date'].strftime("%d/%m/%Y") + '),  '
                    sheet.merge_range('G%s:H%s' % (row, row), str(thai_san_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '5', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ ỐM ĐAU', header_style)
                sheet.write('F%s' % row, i.nghi_om_dau, header_style)
                if i.nghi_om_dau > 0:
                    '''Nghi Om Dau'''
                    benhs = self.env.cr.execute(
                        'SELECT b.name, b.id, a.resignation_date FROM hr_employee_multi_company as a, hr_employee as b WHERE b.id = a.name and a.active = true and a.company_id = %s and a.employee_current_status = \'sick_leave\' and a.resignation_date is not null and EXTRACT(MONTH FROM a.resignation_date) <= %s and EXTRACT(YEAR FROM a.resignation_date) <= %s',
                        (i.sudo().company_id.id, current_month, current_year))
                    benhs = self.env.cr.dictfetchall()

                    benh_s = ''
                    for benh in benhs:
                        if benh['name']:
                            benh_s += benh['name'] + ' '
                        if benh['resignation_date']:
                            benh_s += '(' + benh['resignation_date'].strftime("%d/%m/%Y") + '),  '
                    sheet.merge_range('G%s:H%s' % (row, row), str(benh_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '6', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'NGHỈ KHÔNG LƯƠNG', header_style)
                sheet.write('F%s' % row, i.nghi_khong_luong, header_style)
                if i.nghi_khong_luong > 0:
                    '''Nghi khong luong'''
                    khong_luongs = self.env.cr.execute(
                        'SELECT b.name, b.id, a.resignation_date FROM hr_employee_multi_company as a, hr_employee as b WHERE b.id = a.name and a.active = true and  a.company_id = %s and a.employee_current_status = \'leaving\' and a.resignation_date is not null and EXTRACT(MONTH FROM a.resignation_date) <= %s and EXTRACT(YEAR FROM a.resignation_date) <= %s',
                        (i.sudo().company_id.id, current_month, current_year))
                    khong_luongs = self.env.cr.dictfetchall()

                    khong_luong_s = ''
                    for khong_luong in khong_luongs:
                        if khong_luong['name']:
                            khong_luong_s += khong_luong['name'] + ' '
                        if khong_luong['resignation_date']:
                            khong_luong_s += '(' + khong_luong['resignation_date'].strftime("%d/%m/%Y") + '),  '
                    sheet.merge_range('G%s:H%s' % (row, row), str(khong_luong_s), header_style)

                else:
                    sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '7', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LĐ LÀM VIỆC', header_style)
                sheet.write('F%s' % row, i.employee_current_working_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                row += 1
                sheet.write('B%s' % row, '8', header_style)
                sheet.merge_range('C%s:E%s' % (row, row), 'TỔNG LAO ĐỘNG', header_style)
                sheet.write('F%s' % row, i.employee_working_total, header_style)
                sheet.merge_range('G%s:H%s' % (row, row), '', header_style)

                sheet.set_column('A:A', 4)
                sheet.set_column('B:B', 11)
                sheet.set_column('C:C', 28)
                sheet.set_column('F:G', 28)
                sheet.set_column('AG:AL', 28)
                sheet.freeze_panes(10, 3)


class DanhSachLaoDongNu(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_lao_dong_nu_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_company(company, sheet, row, workbook):
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'bg_color': "#BBFFFF"})
        i = row
        if company:
            sheet.merge_range('A%s:K%s' % (i + 1, i + 1), (str(company.code) + '. ' + str(company.name)),
                              data_style_bold)
        else:
            sheet.merge_range('A%s:K%s' % (i + 1, i + 1), '', data_style_bold)
        # sheet.set_row(i, 22.25)
        i += 1
        return i

    # @staticmethod
    def _print_bom_employee(self, tt, data, sheet, row, workbook):
        data_style_center = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_center_date = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'num_format': 'dd-mm-yyyy'})
        data_style = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        i = row
        for ch in data:
            sheet.write(i, 0, tt, data_style_center)
            sheet.write(i, 1, ch.name.s_identification_id or '', data_style_center)
            sheet.write(i, 2, ch.name.name or '', data_style)
            department_parent = ''
            if ch.department_id.parent_id:
                department_parent = ch.department_id.parent_id.name + '/'
            if ch.department_id:
                sheet.write(i, 3, department_parent + ch.department_id.name or '', data_style)
            else:
                sheet.write(i, 3, '', data_style)
            sheet.write(i, 4, ch.job_id.name or '', data_style)
            # Khanh 12/10/2022
            # sheet.write(i, 5, ch.name.seagroup_join_date or '', data_style_center_date)
            if ch.sudo().joining_date:
                sheet.write(i, 5, ch.joining_date.strftime("%d/%m/%Y") or '', data_style_center_date)
            else:
                sheet.write(i, 5, '', data_style_center_date)
            contracts = self.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', ch.name.id),
                 ('company_id', '=', ch.company_id.id),
                 ('state', '!=', 'cancel')])
            if contracts:
                date = [contract.date_start for contract in contracts if contract.date_start not in [False, None]]
                if date:
                    sheet.write(i, 6, min(date).strftime("%d/%m/%Y") or '', data_style_center_date)
                else:
                    sheet.write(i, 6, '', data_style_center_date)
            # sheet.write(i, 6, ch.name.official_contract or '', data_style_center_date)
            # sheet.write(i, 7, ch.name.birthday or '', data_style_center_date)
            if ch.sudo().name.birthday:
                sheet.write(i, 7, ch.sudo().name.birthday.strftime("%d/%m/%Y") or '', data_style_center)
            else:
                sheet.write(i, 7, '', data_style_center)
            sheet.write(i, 8, ch.name.acc_number or '', data_style_center)
            sheet.write(i, 9, ch.name.acc_holder_name or '', data_style_center)
            sheet.write(i, 10, ch.name.bank_id.name or '', data_style_center)
            # sheet.set_row(i, 22.25)
            i += 1
            tt += 1
        return i, tt

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('LAO ĐỘNG NỮ'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': True, 'border': 1,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center', 'bg_color': '#FFFF66'})
        sheet.merge_range('A1:K1', 'DANH SÁCH LAO ĐỘNG NỮ', tong_hop_title)
        sheet.freeze_panes(3, 0)
        sheet.set_row(0, 30)
        sheet.set_row(2, 42)
        sheet.set_column('A:A', 6.15)
        sheet.set_column('B:B', 18)
        sheet.set_column('C:C', 23)
        sheet.set_column('D:D', 50)
        sheet.set_column('E:E', 35)
        sheet.set_column('F:F', 19)
        sheet.set_column('G:G', 30)
        sheet.set_column('H:H', 15)
        sheet.set_column('I:I', 18)
        sheet.set_column('J:J', 25)
        sheet.set_column('K:K', 70)

        sheet.write('A3', 'STT', tong_hop_date)
        sheet.write('B3', 'MÃ NHÂN VIÊN', tong_hop_date)
        sheet.write('C3', 'HỌ TÊN', tong_hop_date)
        sheet.write('D3', 'PHÒNG BAN', tong_hop_date)
        sheet.write('E3', 'CHỨC DANH', tong_hop_date)
        sheet.write('F3', 'NGÀY NHẬN VIỆC', tong_hop_date)
        sheet.write('G3', 'NGÀY KÝ HĐLĐ CHÍNH THỨC', tong_hop_date)
        sheet.write('H3', 'NGÀY SINH', tong_hop_date)
        sheet.write('I3', 'SỐ TÀI KHOẢN', tong_hop_date)
        sheet.write('J3', 'TÊN CHỦ TÀI KHOẢN', tong_hop_date)
        sheet.write('K3', 'TÊN NGÂN HÀNG', tong_hop_date)
        list_company = self.env.user.company_ids
        index = 3
        tt = 1

        for i in list_company:
            if i.id != 1:
                index = self._print_bom_company(i, sheet, index, workbook)
                departments = self.env['hr.department'].sudo().search([('company_id', '=', i.id)],
                                                                      order='sort_name asc')
                multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', i.id), ('employee_current_status', '!=', 'resigned'),
                     ('primary_company', '=', True)])
                list_employee_ids_dep_job = []
                list_employee_ids_not_dep_job = []
                for department in departments:
                    jobs = self.env['hr.job'].sudo().search(
                        [('company_id', '=', i.id), ('department_id', '=', department.id)], order='sequence asc')
                    for job in jobs:
                        list_employee_ids = []
                        for multi_company in multi_companies:
                            if multi_company.department_id.id == department.id and multi_company.job_id.id == job.id:
                                employee = self.env['hr.employee'].sudo().search(
                                    [('id', '=', multi_company.name.id), ('gender', '=', 'female')])
                                if employee:
                                    list_employee_ids.append(multi_company.id)
                                    list_employee_ids_dep_job.append(multi_company.id)

                        brs_employees = self.env['hr.employee.multi.company'].sudo().browse(list_employee_ids)
                        index, tt = self._print_bom_employee(tt, brs_employees, sheet, index, workbook)
                for multi_company in multi_companies:
                    not_in = True
                    for list_employee_id in list_employee_ids_dep_job:
                        if list_employee_id == multi_company.id:
                            not_in = False
                    if not_in:
                        employee = self.env['hr.employee'].sudo().search(
                            [('id', '=', multi_company.name.id), ('gender', '=', 'female')])
                        if employee:
                            list_employee_ids_not_dep_job.append(multi_company.id)
                '''Không có department và job position'''
                brs_employees = self.env['hr.employee.multi.company'].sudo().browse(list_employee_ids_not_dep_job)
                index, tt = self._print_bom_employee(tt, brs_employees, sheet, index, workbook)


class DanhSachQuocTeThieuNhi(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_quoc_te_thieu_nhi_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_company(company, sheet, row, workbook):
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'bg_color': "#BBFFFF"})

        i = row
        sheet.merge_range('A%s:J%s' % (i + 1, i + 1), (company.code + '. ' + company.name), data_style_bold)
        # sheet.set_row(i, 22.25)
        i += 1
        return i

    @staticmethod
    def _print_bom_employee_child(tt, children, data, sheet, row, workbook):
        data_style_center = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_center_date = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'num_format': 'dd-mm-yyyy'})
        data_style = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        i = row
        for ch in children:
            gender = ""
            if ch.member_gender == "M":

                gender = "Nam"
            else:
                gender = "Nữ"
            sheet.write(i, 0, tt, data_style_center)
            sheet.write(i, 1, ch.member_name or '', data_style)
            if ch.member_birthday:
                sheet.write(i, 2, ch.member_birthday.strftime("%d/%m/%Y") or '', data_style_center_date)
            else:
                sheet.write(i, 2, '', data_style_center_date)
            sheet.write(i, 3, gender or '', data_style_center)
            sheet.write(i, 4, data.name.name or '', data_style)
            department_parent = ''
            # Khanh 12/10/2022
            # if data.name.department_id.parent_id:
            #     department_parent = data.name.department_id.parent_id.name + '/'
            # if data.name.department_id:
            #     sheet.write(i, 5, department_parent + data.name.department_id.name or '', data_style)
            # else:
            #     sheet.write(i, 5, '', data_style)
            # sheet.write(i, 6, data.name.job_id.name or '', data_style)
            if data.department_id.parent_id:
                department_parent = data.department_id.parent_id.name + '/'
            if data.department_id:
                sheet.write(i, 5, department_parent + data.department_id.name or '', data_style)
            else:
                sheet.write(i, 5, '', data_style)
            sheet.write(i, 6, data.job_id.name or '', data_style)
            sheet.write(i, 7, data.name.acc_number or '', data_style_center)
            sheet.write(i, 8, data.name.acc_holder_name or '', data_style_center)
            sheet.write(i, 9, data.name.bank_id.name or '', data_style_center)
            i += 1
            tt += 1

        return i, tt

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('QUỐC TẾ THIẾU NHI'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': True, 'border': 1,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center', 'bg_color': '#FFFF66'})
        sheet.merge_range('A1:J1', 'DANH SÁCH CON CỦA NHÂN VIÊN', tong_hop_title)
        sheet.freeze_panes(3, 2)
        sheet.set_row(0, 30)
        sheet.set_row(2, 42)
        sheet.set_column('A:A', 6.15)
        sheet.set_column('B:B', 23)
        sheet.set_column('C:C', 21)
        sheet.set_column('D:D', 21)
        sheet.set_column('E:E', 23)
        sheet.set_column('F:F', 50)
        sheet.set_column('G:G', 35)
        sheet.set_column('H:H', 30)
        sheet.set_column('I:I', 36)
        sheet.set_column('J:J', 70)

        sheet.write('A3', 'STT', tong_hop_date)
        sheet.write('B3', 'HỌ TÊN BÉ', tong_hop_date)
        sheet.write('C3', 'NGÀY SINH CỦA BÉ', tong_hop_date)
        sheet.write('D3', 'GIỚI TÍNH CỦA BÉ', tong_hop_date)
        sheet.write('E3', 'HỌ TÊN CHA/MẸ', tong_hop_date)
        sheet.write('F3', 'PHÒNG BAN LÀM VIỆC CỦA CHA/MẸ', tong_hop_date)
        sheet.write('G3', 'CHỨC DANH CỦA CHA/MẸ', tong_hop_date)
        sheet.write('H3', 'SỐ TÀI KHOẢN CỦA CHA/MẸ', tong_hop_date)
        sheet.write('I3', 'TÊN CHỦ TÀI KHOẢN CỦA CHA/MẸ', tong_hop_date)
        sheet.write('J3', 'TÊN NGÂN HÀNG ', tong_hop_date)
        list_company = self.env.user.company_ids
        index = 3
        for i in list_company:
            tt = 1
            if i.id != 1:
                index = self._print_bom_company(i, sheet, index, workbook)
                departments = self.env['hr.department'].sudo().search([('company_id', '=', i.id)],
                                                                      order='sort_name asc')
                list_in = []

                for department in departments:
                    jobs = self.env['hr.job'].sudo().search(
                        [('company_id', '=', i.id), ('department_id', '=', department.id)], order='sequence asc')
                    for job in jobs:
                        multi_company_employees = self.env['hr.employee.multi.company'].sudo().search(
                            [('company_id', '=', i.id), ('department_id', '=', department.id), ('job_id', '=', job.id),
                             ('employee_current_status', '!=', 'resigned'), ('primary_company', '=', True)])
                        for multi_company_employee in multi_company_employees:
                            children = self.env['hr.employee.family'].sudo().search(
                                [('employee_id', '=', multi_company_employee.name.id), ('relation', '=', "child")])
                            index, tt = self._print_bom_employee_child(tt, children, multi_company_employee, sheet,
                                                                       index, workbook)
                            list_in.append(multi_company_employee.name.id)
                multi_company_employees = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', i.id), ('employee_current_status', '!=', 'resigned'),
                     ('primary_company', '=', True)])
                list_not_in = []
                for multi_company_employee in multi_company_employees:
                    not_in = True
                    for list in list_in:
                        if multi_company_employee.name.id == list:
                            not_in = False
                            break
                    if not_in:
                        list_not_in.append(multi_company_employee.id)
                if len(list_not_in):
                    employees_no_department_job = self.env['hr.employee.multi.company'].sudo().browse(list_not_in)
                    if len(employees_no_department_job):
                        for employee in employees_no_department_job:
                            children = self.env['hr.employee.family'].sudo().search(
                                [('employee_id', '=', employee.name.id), ('relation', '=', "child")])
                            if children and len(children) > 0:
                                index, tt = self._print_bom_employee_child(tt, children, employee, sheet, index,
                                                                           workbook)


class DanhSachBirthDay(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_birthday_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_company(company, sheet, row, workbook):
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'bg_color': "#BBFFFF"})

        i = row
        sheet.merge_range('A%s:L%s' % (i + 1, i + 1), (company.code + '. ' + company.name), data_style_bold)
        # sheet.set_row(i, 22.25)
        i += 1
        return i

    # @staticmethod
    def _print_employee_child(self, tt, data, sheet, row, workbook):
        data_style_center = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_center_date = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'num_format': 'dd-mm-yyyy'})
        data_style = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        i = row
        for ch in data:
            gender = ""
            if ch.sudo().name.gender:
                if ch.sudo().name.gender == "male":

                    gender = "Nam"
                else:
                    gender = "Nữ"
            else:
                gender = ''

            sheet.write(i, 0, tt, data_style_center)
            sheet.write(i, 1, ch.sudo().name.s_identification_id or '', data_style)
            sheet.write(i, 2, ch.sudo().name.name or '', data_style_center_date)
            department_parent = ''
            department = ''
            if ch.sudo().department_id:
                department += ch.sudo().department_id.name
                if ch.sudo().department_id.parent_id:
                    department_parent += ch.sudo().department_id.parent_id.name + '/'

            sheet.write(i, 3, department_parent + department or '', data_style_center)
            sheet.write(i, 4, ch.sudo().job_id.sudo().name or '', data_style)
            if ch.sudo().joining_date:
                sheet.write(i, 5, ch.sudo().joining_date.strftime("%d/%m/%Y") or '', data_style)
            else:
                sheet.write(i, 5, '', data_style)

            contracts = self.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', ch.name.id),
                 ('company_id', '=', ch.company_id.id),
                 ('state', '!=', 'cancel')])
            if contracts:
                date = [contract.date_start for contract in contracts if contract.date_start not in [False, None]]
                if date:
                    sheet.write(i, 6, min(date).strftime("%d/%m/%Y") or '', data_style)
                else:
                    sheet.write(i, 6, '', data_style)

            # if ch.sudo().name.official_contract:
            # sheet.write(i, 6, ch.sudo().name.official_contract.strftime("%d/%m/%Y") or '', data_style)
            # else:
            # sheet.write(i, 6, '', data_style)
            sheet.write(i, 7, gender or '', data_style)
            sheet.write(i, 8, ch.sudo().name.birthday.strftime("%d/%m/%Y") or '', data_style_center)
            sheet.write(i, 9, ch.sudo().name.acc_number or '', data_style_center)
            sheet.write(i, 10, ch.sudo().name.acc_holder_name or '', data_style_center)
            sheet.write(i, 11, ch.sudo().name.bank_id.name or '', data_style_center)

            i += 1
            tt += 1

        return i, tt

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('SINH NHẬT'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': True, 'border': 1,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center', 'bg_color': '#FFFF66'})
        sheet.merge_range('A1:L1', 'DANH SÁCH SINH NHẬT NHÂN VIÊN', tong_hop_title)
        for obj in objects:
            if obj.sudo().birthday:
                sheet.merge_range('A2:L2', 'THÁNG ' + str(obj.sudo().birthday.month), tong_hop_title)
                break
        sheet.freeze_panes(3, 2)
        sheet.set_row(0, 30)
        sheet.set_row(1, 30)
        sheet.set_row(2, 42)
        sheet.set_column('A:A', 6.15)
        sheet.set_column('B:B', 19)
        sheet.set_column('C:C', 21)
        sheet.set_column('D:D', 65)
        sheet.set_column('E:E', 29)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 35)
        sheet.set_column('H:H', 12)
        sheet.set_column('I:I', 12)
        sheet.set_column('J:J', 18)
        sheet.set_column('K:K', 24)
        sheet.set_column('L:L', 70)

        sheet.write('A3', 'STT', tong_hop_date)
        sheet.write('B3', 'MÃ NHÂN VIÊN', tong_hop_date)
        sheet.write('C3', 'HỌ TÊN', tong_hop_date)
        sheet.write('D3', 'PHÒNG BAN', tong_hop_date)
        sheet.write('E3', 'CHỨC DANH', tong_hop_date)
        sheet.write('F3', 'NGÀY NHẬN VIỆC', tong_hop_date)
        sheet.write('G3', 'NGÀY KÝ HĐLĐ CHÍNH THỨC', tong_hop_date)
        sheet.write('H3', 'GIỚI TÍNH', tong_hop_date)
        sheet.write('I3', 'NGÀY SINH', tong_hop_date)
        sheet.write('J3', 'SỐ TÀI KHOẢN ', tong_hop_date)
        sheet.write('K3', 'TÊN CHỦ TÀI KHOẢN', tong_hop_date)
        sheet.write('L3', 'TÊN NGÂN HÀNG', tong_hop_date)
        list_company = self.env.user.company_ids
        index = 3

        for i in list_company:
            tt = 1
            if i.id != 1:
                departments = self.env['hr.department'].sudo().search([('company_id', '=', i.id)],
                                                                      order='sort_name asc')
                index = self._print_bom_company(i, sheet, index, workbook)
                for object in objects:
                    list_not_in = []
                    not_in = True
                    for department in departments:
                        jobs = self.env['hr.job'].sudo().search(
                            [('company_id', '=', i.id), ('department_id', '=', department.id)], order='sequence asc')
                        for job in jobs:
                            employee_multi_company = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', object.id), ('company_id', '=', i.id),
                                 ('department_id', '=', department.id), ('job_id', '=', job.id),
                                 ('employee_current_status', '!=', 'resigned'), ('primary_company', '=', True)])
                            if employee_multi_company:
                                index, tt = self._print_employee_child(tt, employee_multi_company, sheet, index,
                                                                       workbook)
                                not_in = False
                    if not_in:
                        list_not_in.append(object)
                    if len(list_not_in) > 0:
                        for list in list_not_in:
                            employee_multi_company_no_depart_job = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', list.id), ('company_id', '=', i.id),
                                 ('employee_current_status', '!=', 'resigned'), ('primary_company', '=', True)])
                            if employee_multi_company_no_depart_job:
                                index, tt = self._print_employee_child(tt, employee_multi_company_no_depart_job, sheet,
                                                                       index, workbook)


class DanhSachTaiKy(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_tai_ky_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_company(company, sheet, row, workbook):
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'bg_color': "#fabf8f"})

        i = row
        sheet.merge_range('A%s:P%s' % (i + 1, i + 1), (company.code + '. ' + company.name), data_style_bold)
        # sheet.set_row(i, 22.25)
        i += 1
        return i

    @staticmethod
    def _print_employee_child(tt, data, sheet, row, workbook, contract, number_of_contracts):
        data_style_center = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        data_style_center_date = workbook.add_format(
            {'font_size': 11, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'num_format': 'dd-mm-yyyy'})
        data_style = workbook.add_format(
            {'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        i = row
        for ch in data:
            gender = ""
            if ch.sudo().name.gender:
                if ch.sudo().name.gender == "male":
                    gender = "Nam"
                else:
                    gender = "Nữ"
            else:
                gender = ''

            sheet.write(i, 0, tt, data_style_center)
            sheet.write(i, 1, ch.sudo().name.s_identification_id or '', data_style)
            sheet.write(i, 2, ch.sudo().name.name or '', data_style_center_date)
            sheet.write(i, 3, gender or '', data_style)
            if ch.sudo().name.seagroup_join_date:
                sheet.write(i, 4, ch.sudo().name.seagroup_join_date.strftime("%d/%m/%Y") or '', data_style)
            else:
                sheet.write(i, 4, '', data_style)
            department_parent = ''
            department = ''
            if ch.sudo().department_id:
                department += ch.sudo().department_id.name
                if ch.sudo().department_id.parent_id:
                    department_parent += ch.sudo().department_id.parent_id.name + '/'

            sheet.write(i, 5, department_parent + department or '', data_style_center)
            sheet.write(i, 6, ch.sudo().job_id.sudo().name or '', data_style)
            sheet.write(i, 7, ch.sudo().job_title or '', data_style)
            if contract.sudo().type_id.id == 1:
                sheet.write(i, 8, 'Chính thức' or '', data_style)
            else:
                sheet.write(i, 8, 'Thử việc' or '', data_style)
            sheet.write(i, 9, contract.sudo().contract_period_id.name or '', data_style)
            sheet.write(i, 10, contract.sudo().name or '', data_style)
            sheet.write(i, 11, contract.sudo().date_start.strftime("%d/%m/%Y") or '', data_style)
            if contract.sudo().date_end:
                sheet.write(i, 12, contract.sudo().date_end.strftime("%d/%m/%Y") or '', data_style)
            else:
                sheet.write(i, 12, '', data_style)
            hinh_thuc = ''
            if contract.sudo().type_id.id == 1 and contract.sudo().date_end:
                days = contract.sudo().date_end - date.today()
                if int(days.days) < 0:
                    hinh_thuc = 'Đã hết hạn'
                elif int(days.days) <= 45:
                    hinh_thuc = 'Tái ký'
            elif contract.sudo().type_id.id == 4 and not contract.sudo().trial_date_end:
                hinh_thuc = ''
            elif contract.sudo().type_id.id == 4 and contract.sudo().trial_date_end:
                days = contract.sudo().date_end - date.today()
                if int(days.days) < 0:
                    hinh_thuc = 'Đã hết hạn'
                elif int(days.days) <= 7:
                    hinh_thuc = 'Chính thức'
            sheet.write(i, 13, hinh_thuc or '', data_style)
            sheet.write(i, 14, number_of_contracts or '', data_style)
            sheet.write(i, 15, '', data_style)

            # sheet.set_row(i, 22.25)
            i += 1
            tt += 1

        return i, tt

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('DS TÁI KÝ HĐLĐ'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 16,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': True, 'border': 1,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'text_wrap': True,
                                             'align': 'center', 'bg_color': '#FFFFFF'})
        tong_hop_hopdong = workbook.add_format({'bold': True, 'border': 1,
                                                'font_size': 11,
                                                'font_name': "Times New Roman",
                                                'valign': 'vcenter',
                                                'align': 'center', 'bg_color': '#92cddc'})
        sheet.merge_range('A1:L1', 'DANH SÁCH TÁI KÝ HỢP ĐỒNG LAO ĐỘNG', tong_hop_title)
        sheet.freeze_panes(5, 4)
        sheet.set_row(0, 30)
        sheet.set_row(1, 30)
        sheet.set_row(2, 42)
        sheet.set_row(3, 24)
        sheet.set_row(4, 39)
        sheet.set_column('A:A', 6.15)
        sheet.set_column('B:B', 19)
        sheet.set_column('C:C', 21)
        sheet.set_column('D:D', 12)
        sheet.set_column('E:E', 29)
        sheet.set_column('F:F', 70)
        sheet.set_column('G:G', 35)
        sheet.set_column('H:H', 44)
        sheet.set_column('I:I', 19)
        sheet.set_column('J:J', 18)
        sheet.set_column('K:K', 24)
        sheet.set_column('L:L', 34)
        sheet.set_column('M:M', 22)
        sheet.set_column('N:N', 14)
        sheet.set_column('O:O', 20)
        sheet.set_column('P:P', 20)
        sheet.merge_range('A4:A5', 'STT', tong_hop_date)
        sheet.merge_range('B4:B5', 'MÃ NHÂN VIÊN', tong_hop_date)
        sheet.merge_range('C4:C5', 'HỌ TÊN', tong_hop_date)
        sheet.merge_range('D4:D5', 'GIỚI TÍNH', tong_hop_date)
        sheet.merge_range('E4:E5', 'NGÀY VÀO HỆ THỐNG SEACORP', tong_hop_date)
        sheet.merge_range('F4:F5', 'PHÒNG BAN', tong_hop_date)
        sheet.merge_range('G4:G5', 'CHỨC VỤ', tong_hop_date)
        sheet.merge_range('H4:H5', 'CÔNG VIỆC ĐẢM NHẬN', tong_hop_date)
        sheet.merge_range('I4:M4', 'THÔNG TIN HỢP ĐỒNG(Hợp đồng gần nhất)', tong_hop_date)
        sheet.write('I5', 'Hình thức hợp đồng', tong_hop_hopdong)
        sheet.write('J5', 'Thời hạn hợp đồng', tong_hop_hopdong)
        sheet.write('K5', 'Số hợp đồng', tong_hop_hopdong)
        sheet.write('L5', 'Ngày ký HĐ(Ghi ngày bắt đầu HĐ)', tong_hop_hopdong)
        sheet.write('M5', 'Ngày hết hạn hợp đồng', tong_hop_hopdong)
        sheet.merge_range('N4:N5', 'HÌNH THỨC', tong_hop_date)
        sheet.merge_range('O4:O5', 'SỐ LẦN KÝ HĐLĐ', tong_hop_date)
        sheet.merge_range('P4:P5', 'GHI CHÚ', tong_hop_date)
        list_company = self.env.user.company_ids
        index = 5
        for i in list_company:
            tt = 1
            if i.id != 1:
                index = self._print_bom_company(i, sheet, index, workbook)
                departments = self.env['hr.department'].sudo().search(
                    [('company_id', '=', i.id), ('active', '=', True)],
                    order='sort_name asc')
                employee_multi_companies = self.env.cr.execute(
                    'SELECT b.name,b.department_id,b.job_id FROM hr_employee a,hr_employee_multi_company b where b.active=true and a.id=b.name and b.employee_current_status!=\'resigned\' and b.company_id  = %s group by b.name, b.department_id,b.job_id',
                    (i.id,))
                employee_multi_companies = self.env.cr.dictfetchall()
                list_not_in = []
                list_in = []
                for employee_multi_company in employee_multi_companies:
                    for department in departments:
                        jobs = self.env['hr.job'].sudo().search(
                            [('company_id', '=', i.id), ('department_id', '=', department.id)], order='sequence asc')
                        for job in jobs:
                            if employee_multi_company['department_id'] == department.id and employee_multi_company[
                                'job_id'] == job.id:
                                list_in.append(employee_multi_company['name'])
                                employees = self.env['hr.employee.multi.company'].sudo().search(
                                    [('name', '=', employee_multi_company['name']), ('company_id', '=', i.id)])
                                for employee in employees:
                                    contracts = self.env['hr.contract'].sudo().search(
                                        [('employee_id', '=', employee.name.id), ('company_id', '=', i.id),
                                         ('date_start', '!=', None), ('state', '!=', 'cancel'),
                                         ('state', '!=', 'close'), ('contract_category', '=', 'contract')],
                                        order="date_start desc")
                                    for contract in contracts:
                                        if contract.date_end:
                                            if contract.sudo().type_id.id == 1 and contract.sudo().date_end:
                                                days = contract.sudo().date_end - date.today()
                                                if int(days.days) <= 45:
                                                    index, tt = self._print_employee_child(tt, employee, sheet, index,
                                                                                           workbook, contract,
                                                                                           len(contracts))
                                            elif contract.sudo().type_id.id == 4 and contract.sudo().date_end:
                                                days = contract.sudo().date_end - date.today()
                                                if int(days.days) <= 7:
                                                    index, tt = self._print_employee_child(tt, employee, sheet, index,
                                                                                           workbook, contract,
                                                                                           len(contracts))
                                        break
                for employee_multi_company in employee_multi_companies:
                    have_employee = 0
                    for list in list_in:
                        if employee_multi_company['name'] == list:
                            have_employee = 1
                            break
                    if have_employee == 0:
                        list_not_in.append(employee_multi_company['name'])
                if len(list_not_in) > 0:
                    employees = self.env['hr.employee.multi.company'].sudo().search(
                        [('name', 'in', list_not_in), ('company_id', '=', i.id)])
                    for employee in employees:
                        contracts = self.env['hr.contract'].sudo().search(
                            [('employee_id', '=', employee.name.id), ('company_id', '=', i.id),
                             ('date_start', '!=', None), ('state', '!=', 'cancel'), ('state', '!=', 'close'),
                             ('contract_category', '=', 'contract')], order="date_start desc")
                        for contract in contracts:
                            if contract.date_end:
                                if contract.sudo().type_id.id == 1 and contract.sudo().date_end:
                                    days = contract.sudo().date_end - date.today()
                                    if int(days.days) <= 45:
                                        index, tt = self._print_employee_child(tt, employee, sheet, index,
                                                                               workbook, contract,
                                                                               len(contracts))
                                elif contract.sudo().type_id.id == 4 and contract.sudo().date_end:
                                    days = contract.sudo().date_end - date.today()
                                    if int(days.days) <= 7:
                                        index, tt = self._print_employee_child(tt, employee, sheet, index,
                                                                               workbook, contract,
                                                                               len(contracts))


class DanhSachNhanSuCoQLTTNghiViec(models.AbstractModel):
    _name = 'report.sea_employee_reports.report_manager_leave_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def employee_by_company(self, employee_data_lines):
        companys = {}
        for line in employee_data_lines:
            company_name = line.company_name
            if company_name not in companys:
                companys[company_name] = []
            if company_name in companys:
                companys[company_name].append(line)
        return companys

    def int_to_roman(self, n):
        roman_numerals = {
            1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
            50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
        }
        result = ''
        for value, numeral in sorted(roman_numerals.items(), reverse=True):
            while n >= value:
                result += numeral
                n -= value
        return result

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})

        sheet = workbook.add_worksheet(_('TỔNG HỢP'))

        # style
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 18,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center'})
        tong_hop_date = workbook.add_format({'bold': False,
                                             'font_size': 12,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'left'})
        table_title = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'font_name': "Times New Roman",
            'valign': 'vcenter',
            'align': 'center',
            'bg_color': '#FFC000',
            'text_wrap': True,
            'font_color': '#4D4C4C',
            'border': 1
        })
        company_title = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'font_name': "Times New Roman",
            'valign': 'vcenter',
            'align': 'left',
            'bg_color': '#A9D08E',
            'text_wrap': True,
            'font_color': '#4D4C4C',
            'border': 1
        })
        table_content = workbook.add_format({
            'font_size': 12,
            'font_name': "Times New Roman",
            'valign': 'vcenter',
            'align': 'left',
            'text_wrap': True,
            'font_color': '#4D4C4C',
            'border': 1
        })

        # set width
        sheet.set_column('A:A', 5)
        sheet.set_column('B:C', 25)
        sheet.set_column('D:G', 32)

        # title
        # sheet.write('A2', 'DANH SÁCH CÁC NHÂN SỰ CẦN PHẢI CẬP NHẬT LẠI QLTT VÀ CẤP TRÊN QLTT', tong_hop_title)
        sheet.merge_range('A2:G2', 'DANH SÁCH CÁC NHÂN SỰ CẦN PHẢI CẬP NHẬT LẠI QLTT VÀ CẤP TRÊN QLTT', tong_hop_title)
        date = ''
        if objects.update_date is not None:
            if objects.update_date:
                date = 'Tại thời điểm: ' + str(objects.update_date.strftime("%d/%m/%Y"))
        sheet.write('F3', date, tong_hop_date)
        sheet.merge_range('A5:E5',
                          'Lưu ý: Những cột QLTT hoặc cấp trên QLTT để trống là những trường hợp QLTT/Cấp trên QLTT vẫn còn đang làm việc hoặc không tồn tại',
                          tong_hop_date)

        # content
        sheet.write('A7', 'STT', table_title)
        sheet.write('B7', 'Họ và tên', table_title)
        sheet.write('C7', 'SC nhân sự', table_title)
        sheet.write('D7', 'SC QLTT hiện tại đã nghỉ việc nhưng chưa cập nhật lại', table_title)
        sheet.write('E7', 'Tên của QLTT đã nghỉ việc nhưng chưa cập nhật lại', table_title)
        sheet.write('F7', 'SC cấp trên QLTT hiện tại đã nghỉ việc nhưng chưa cập nhật lại', table_title)
        sheet.write('G7', 'Tên của cấp trên QLTT đã nghỉ việc nhưng chưa cập nhật lại', table_title)

        stt_company = 0
        stt = 0
        row = 7

        data = self.employee_by_company(objects.employee_data_lines)

        for key, value in data.items():
            row += 1
            stt_company += 1
            range_str = 'A{}:G{}'.format(row, row)
            company_name = self.int_to_roman(stt_company) + '. ' + key

            sheet.merge_range(range_str, company_name, company_title)

            for line in value:
                row += 1
                stt += 1

                sheet.write('A%s' % row, stt, table_content)
                sheet.write('B%s' % row, line.employee_name, table_content)
                sheet.write('C%s' % row, line.employee_scid, table_content)

                manager_scid = line.manager_scid if line.manager_scid else ' '
                sheet.write('D%s' % row, manager_scid, table_content)
                manager_name = line.manager_name if line.manager_name else ' '
                sheet.write('E%s' % row, manager_name, table_content)

                upper_manager_scid = line.upper_manager_scid if line.upper_manager_scid else ' '
                sheet.write('F%s' % row, upper_manager_scid, table_content)
                upper_manager_name = line.upper_manager_name if line.upper_manager_name else ' '
                sheet.write('G%s' % row, upper_manager_name, table_content)
