# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64
import io
import logging
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class DexuatSauDGNS(models.AbstractModel):
    _name = 'report.seatek_hr_appraisal.report_dexuat_sau_dgns_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_children(tt, title, data, sheet, row, workbook):
        data_style_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})

        data_style = workbook.add_format(
            {'font_size': 10, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})

        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 10, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})

        i = row
        sheet.set_row(i, 22.25)

        if data is not None:
            ch = data
            sheet.write(i, 0, tt, data_style)
            sheet.write(i, 1, ch.sc_code or '', data_style)
            sheet.write(i, 2, ch.name or '', data_style)
            sheet.write(i, 3, ch.job_position or '', data_style)

            # colum 3 -> 15 hide

            # sheet.write(i, 16, ch.dexuat_salary_user or '0', data_style_center)
            # sheet.write(i, 17, ch.dexuat_salary_manager or '0', data_style_center)
            # sheet.write(i, 18, ch.dexuat_salary_smanager or '0', data_style_center)
            # sheet.write(i, 19, ch.dexuat_salary_hddg or '0', data_style_center)
            #
            # sheet.write(i, 20, ch.dexuat_thuong_user or '0', data_style_center)
            # sheet.write(i, 21, ch.dexuat_thuong_manager or '0', data_style_center)
            # sheet.write(i, 22, ch.dexuat_thuong_smanager or '0', data_style_center)
            # sheet.write(i, 23, ch.dexuat_thuong_hddg or '0', data_style_center)
            #
            # sheet.write(i, 24, ch.dexuat_thuyenchuyen_user or '', data_style)
            # sheet.write(i, 25, ch.dexuat_thuyenchuyen_manager or '', data_style)
            # sheet.write(i, 26, ch.dexuat_thuyenchuyen_smanager or '', data_style)
            # sheet.write(i, 27, ch.dexuat_thuyenchuyen_hddg or '', data_style)
            #
            # sheet.write(i, 28, ch.user_opinion or '', data_style)
            # sheet.write(i, 29, ch.manager_opinion or '', data_style)
            # sheet.write(i, 30, ch.smanager_opinion or '', data_style)
            # sheet.write(i, 31, ch.hddg_opinion or '', data_style)
            #
            # sheet.write(i, 32, ch.ct_luong or '0', data_style_center)
            # sheet.write(i, 33, ch.ct_thuong or '0', data_style_center)
            # sheet.write(i, 34, ch.ct_thuyenchuyen or '', data_style)
            # sheet.write(i, 35, ch.ct_other or '', data_style)
            # sheet.write(i, 36, ch.ghichu_dexuat_sau_dgns or '', data_style)

            sheet.write(i, 3, ch.dexuat_salary_user or '0', data_style_center)
            sheet.write(i, 4, ch.dexuat_salary_manager or '0', data_style_center)
            sheet.write(i, 5, ch.dexuat_salary_smanager or '0', data_style_center)
            sheet.write(i, 6, ch.dexuat_salary_hddg or '0', data_style_center)

            sheet.write(i, 7, ch.dexuat_thuong_user or '0', data_style_center)
            sheet.write(i, 8, ch.dexuat_thuong_manager or '0', data_style_center)
            sheet.write(i, 9, ch.dexuat_thuong_smanager or '0', data_style_center)
            sheet.write(i, 10, ch.dexuat_thuong_hddg or '0', data_style_center)

            sheet.write(i, 11, ch.dexuat_thuyenchuyen_user or '', data_style)
            sheet.write(i, 12, ch.dexuat_thuyenchuyen_manager or '', data_style)
            sheet.write(i, 13, ch.dexuat_thuyenchuyen_smanager or '', data_style)
            sheet.write(i, 14, ch.dexuat_thuyenchuyen_hddg or '', data_style)

            sheet.write(i, 15, ch.user_opinion or '', data_style)
            sheet.write(i, 16, ch.manager_opinion or '', data_style)
            sheet.write(i, 17, ch.smanager_opinion or '', data_style)
            sheet.write(i, 18, ch.hddg_opinion or '', data_style)

            sheet.write(i, 19, ch.ct_luong or '0', data_style_center)
            sheet.write(i, 20, ch.ct_thuong or '0', data_style_center)
            sheet.write(i, 21, ch.ct_thuyenchuyen or '', data_style)
            sheet.write(i, 22, ch.ct_other or '', data_style)
            sheet.write(i, 23, ch.ghichu_dexuat_sau_dgns or '', data_style)

        else:
            sheet.write(i, 0, tt, data_style_bold)
            sheet.merge_range('B%s:X%s' % (i + 1, i + 1), title, data_style_bold)
        return i

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
        sheet = workbook.add_worksheet(_('DE XUAT SAU DGNS'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)

        title_style_dexuatsaudanhgia_company = workbook.add_format(
            {'bold': True, 'font_size': 20, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter'})
        title_style_name_company = workbook.add_format(
            {'bold': True, 'font_size': 16, 'font_name': "Times New Roman", 'valign': 'vcenter'})
        title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
        title_style_table = workbook.add_format(
            {'bold': True, 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'text_wrap': True})
        title_style_table_red = workbook.add_format(
            {'bold': True, 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'text_wrap': True, 'font_color': '#FF0000'})

        sheet.freeze_panes(9, 0)
        sheet.set_row(0, 21)
        sheet.set_row(1, 21)
        sheet.set_row(2, 21)
        sheet.set_row(3, 10)
        sheet.set_row(4, 35)
        sheet.set_row(5, 21)
        image_company = io.BytesIO(base64.b64decode(self.env.user.company_id.logo_web))
        sheet.insert_image('C1', "logocompany.png", {'image_data': image_company, 'x_scale': 1, 'y_scale': 1})
        sheet.write('D1', self.env.user.company_id.name, title_style_name_company)
        sheet.write('D2', self.env.user.company_id.sea_company_foreign, title_style_name_company)
        address = ''
        if self.env.user.company_id.street:
            address += self.env.user.company_id.street
        if self.env.user.company_id.street2:
            address += self.env.user.company_id.street2
        if self.env.user.company_id.city:
            address += self.env.user.company_id.city
        if self.env.user.company_id.state_id:
            address += self.env.user.company_id.state_id.name
        if self.env.user.company_id.country_id:
            address += ', ' + self.env.user.company_id.country_id.name
        sheet.write('D3', address, title_style_address_company)
        # title file excel
        sheet.merge_range('A5:X5', objects.name, title_style_dexuatsaudanhgia_company)
        sheet.merge_range('A6:X6', None, workbook.add_format({'bottom': 1}))
        sheet.merge_range('A7:A9', 'TT', title_style_table)
        sheet.set_column('A:A', 6)
        sheet.merge_range('B7:B9', 'Mã NV', title_style_table)
        sheet.set_column('B:B', 10)
        sheet.merge_range('C7:C9', 'HỌ VÀ TÊN', title_style_table)
        sheet.set_column('C:C', 32)
        sheet.merge_range('D7:S7', 'ĐỀ XUẤT  SAU ĐGNS', title_style_table)
        sheet.merge_range('D8:G8', 'TĂNG LƯƠNG', title_style_table_red)
        sheet.merge_range('H8:K8', 'THƯỞNG', title_style_table)
        sheet.merge_range('L8:O8', 'ĐIỀU CHUYỂN/QUY HOẠCH QUẢN LÝ', title_style_table)
        sheet.merge_range('P8:S8', 'ĐỀ XUẤT KHÁC', title_style_table)
        sheet.write('D9', 'NS', title_style_table)
        sheet.write('E9', 'QLTT', title_style_table)
        sheet.write('F9', 'Cấp trên QLTT', title_style_table)
        sheet.write('G9', 'HĐĐG', title_style_table_red)
        sheet.write('H9', 'NS', title_style_table)
        sheet.write('I9', 'QLTT', title_style_table)
        sheet.write('J9', 'Cấp trên QLTT', title_style_table)
        sheet.write('K9', 'HĐĐG', title_style_table_red)
        sheet.write('L9', 'NS', title_style_table)
        sheet.write('M9', 'QLTT', title_style_table)
        sheet.write('N9', 'Cấp trên QLTT', title_style_table)
        sheet.write('O9', 'HĐĐG', title_style_table_red)
        sheet.write('P9', 'NS', title_style_table)
        sheet.write('Q9', 'QLTT', title_style_table)
        sheet.write('R9', 'Cấp trên QLTT', title_style_table)
        sheet.write('S9', 'HĐĐG', title_style_table_red)
        sheet.merge_range('T7:W7', 'CHỦ TỊCH THÔNG QUA', title_style_table)
        sheet.merge_range('T8:T9', 'LƯƠNG ', title_style_table)
        sheet.merge_range('U8:U9', 'THƯỞNG ', title_style_table)
        sheet.merge_range('V8:V9', 'ĐIỀU CHUYỂN/QUY HOẠCH ', title_style_table)
        sheet.merge_range('W8:W9', 'KHÁC ', title_style_table)
        sheet.merge_range('X7:X9', 'GHI CHÚ ', title_style_table)
        department_user_input_search=self.env['hr.survey.user.input'].search([('company_id', '=', self.env.user.company_id.id),('appraisal_id', '=', objects[0].id)],order='s_identification_id asc')
        department_search = self.env['hr.department'].sudo().search([('company_id', '=', self.env.user.company_id.id)])
        department_parent = []
        for i in department_search:
            if i.sort_name:
                department_parent.append([i.sort_name, i])
        department_parent.sort(key=lambda x: x[0])
        list_department = []
        for id_department, data in department_parent:
            self.get_department_child(list_department=list_department, id_department=id_department, department=data,
                                      department_search=department_search)

        list_data = []

        for index, data in list_department:
            list_user = []
            for i in department_user_input_search:
                if data == i.department_compute:
                    list_user.append(i)
            list_data.append([index, data, list_user])

        list_result = []
        index1 = ''
        index2 = 0
        index3 = 0
        index4 = 0
        index5 = 0
        index6 = 0
        for i, data, list_user in list_data:
            if data.sort_name:
                index1 = data.sort_name
            if i == 1:  # parent (cung cap bang giam doc)
                list_result.append([index1, data.name, data])
            if i == 2:
                index2 += 1
                list_result.append(['%s.%s' % (index1, index2), data.name, data])
            if i == 3:
                index3 += 1
                list_result.append(['%s.%s.%s' % (index1, index2, index3), data.name, data])
            if i == 4:
                index4 += 1
                list_result.append(['%s.%s.%s.%s' % (index1, index2, index3, index4), data.name, data])
            if i == 5:
                index5 += 1
                list_result.append(['%s.%s.%s.%s.%s' % (index1, index2, index3, index4, index5), data.name, data])
            if i == 6:
                index6 += 1
                list_result.append(
                    ['%s.%s.%s.%s.%s.%s' % (index1, index2, index3, index4, index5, index6), data.name, data])

        data = []
        stt = 0
        for tt, title, data_result in list_result:
            data.append([tt, title, None])
            list_user_temp = []
            for i in department_user_input_search:
                if data_result == i.department_compute:

                    job_sequence = self.get_job_position(i.employee_id.id)
                    list_user_temp.append([str(job_sequence), i])
            if len(list_user_temp)>0:
                list_user_temp.sort(key=lambda x: x[0])

            for i, user in list_user_temp:
                stt += 1
                data.append([stt, None, user])
        for i in department_user_input_search:
            if not i.department_compute:
                data.append(['', 'KHÔNG CÓ BỘ PHẬN', None])
                break
        # them employee k co department
        for i in department_user_input_search:
            if not i.department_compute:
                stt += 1
                data.append([stt, None, i])
        index = 9
        for i in data:
            index = self._print_bom_children(i[0], i[1], i[2], sheet, index, workbook)
            index += 1

