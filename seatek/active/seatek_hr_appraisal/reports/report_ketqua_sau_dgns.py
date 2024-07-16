# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import io
import logging
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class KetQuaSauDGNS(models.AbstractModel):
    _name = 'report.seatek_hr_appraisal.report_ketqua_sau_dgns_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_children(tt, title, data, sheet, row, workbook):
        data_style_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_center_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,'bold': True,
             'font_name': "Times New Roman"})
        data_style = workbook.add_format(
            {'font_size': 10, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})

        i = row
        sheet.set_row(i, 22.25)

        if data is not None:
            ch = data
            sheet.write(i, 0, tt, data_style)
            sheet.write(i, 1, ch.sc_code or '', data_style)
            sheet.write(i, 2, ch.name or '', data_style)
            sheet.write(i, 3, ch.job_position or '', data_style)
            sheet.write(i, 4, ch.seagroup_join_date or '', data_style_center)
            sheet.write(i, 5, ch.official_contract or '', data_style_center)
            sheet.write(i, 6, ch.contract_period or '', data_style_center)
            sheet.write(i, 8, ch.user_seacorp or '', data_style_center)
            sheet.write(i, 9, ch.user_kpi or '',data_style_center)
            sheet.write(i, 10, ch.rating1_value or '', data_style_center)
            sheet.write(i, 11, ch.manager_seacorp or '', data_style_center)
            sheet.write(i, 12, ch.manager_kpi or '', data_style_center)
            sheet.write(i, 13, ch.rating2_value or '', data_style_center)
            sheet.write(i, 14, ch.smanager_seacorp or '', data_style_center)
            sheet.write(i, 15, ch.smanager_kpi or '', data_style_center)
            sheet.write(i, 16, ch.rating3_value or '', data_style_center)
            sheet.write(i, 17, ch.hddg_seacorp or '', data_style_center)
            sheet.write(i, 18, ch.hddg_kpi or '', data_style_center)
            sheet.write(i, 19, ch.rating4_value_compute or '', data_style_center)
            sheet.write(i, 20, ch.ct_seacorp or '', data_style_center)
            sheet.write(i, 21, ch.ct_kpi or '', data_style_center)
            sheet.write(i, 22, ch.ct_xl or '', data_style_center)
            sheet.write(i, 23, ch.ghichu_ket_qua_dgns or '', data_style_center)

        else:
            sheet.write(i, 0, tt, data_style_center_bold)
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
        sheet = workbook.add_worksheet(_('KQ DGNS'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)

        title_style_name_company = workbook.add_format({'bold': True,
                                                        'font_size': 16,
                                                        'font_name': "Times New Roman",
                                                        'valign': 'vcenter'})
        title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
        title_style_kqdgns_company = workbook.add_format({'bold': True, 'font_size': 20, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter'})
        title_style_kqdgns1_company = workbook.add_format({'bold': True, 'font_size': 15, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter'})

        title_style_tieude_ns_table = workbook.add_format({'bold': True,
                                                            'font_size': 9,
                                                            'align': 'center',
                                                            'bg_color': '#B4EEB4',
                                                            'valign': 'vcenter',
                                                            'border': 1,
                                                            'font_name': "Times New Roman"})
        title_style_tieude1_ns_table = workbook.add_format({'font_size': 9,
                                                            'align': 'center',
                                                            'bg_color': '#B4EEB4',
                                                            'border': 1,
                                                            'valign': 'vcenter',
                                                            'font_name': "Times New Roman"})
        title_style_tieude2_ns_table = workbook.add_format({'bold': True,
                                                            'font_size': 9,
                                                            'font_color': '#FF0000',
                                                            'bg_color': '#B4EEB4',
                                                            'border': 1,
                                                            'align': 'center',
                                                            'valign': 'vcenter',
                                                            'font_name': "Times New Roman"})

        # ------------------------

        title_style_tieude_pttt_table = workbook.add_format({'bold': True,
                                                            'font_size': 9,
                                                             'bg_color': '#CAE1FF',
                                                             'align': 'center',
                                                             'valign': 'vcenter',
                                                             'border': 1,
                                                             'font_name': "Times New Roman"})
        title_style_tieude1_pttt_table = workbook.add_format({'font_size': 9,
                                                             'align': 'center',
                                                              'bg_color': '#CAE1FF',
                                                              'border': 1,
                                                              'valign': 'vcenter',
                                                              'font_name': "Times New Roman"})
        title_style_tieude2_pttt_table = workbook.add_format({'bold': True,
                                                             'font_size': 9,
                                                              'bg_color': '#CAE1FF',
                                                              'font_color': '#FF0000',
                                                              'border': 1,
                                                              'align': 'center',
                                                              'valign': 'vcenter',
                                                              'font_name': "Times New Roman"})

        # ------------------------
        title_style_tieude_ctpttt_table = workbook.add_format({'bold': True,
                                                                'font_size': 9,
                                                                'align': 'center',
                                                                'bg_color': '#EECBAD',
                                                                'valign': 'vcenter',
                                                                'border': 1,
                                                                'font_name': "Times New Roman"})
        title_style_tieude1_ctpttt_table = workbook.add_format({'font_size': 9,
                                                                'align': 'center',
                                                                'border': 1,
                                                                'bg_color': '#EECBAD',
                                                                'valign': 'vcenter',
                                                                'font_name': "Times New Roman"})
        title_style_tieude2_ctpttt_table = workbook.add_format({'bold': True,
                                                                'font_size': 9,
                                                                'font_color': '#FF0000',
                                                                'bg_color': '#EECBAD',
                                                                'border': 1,
                                                                'align': 'center',
                                                                'valign': 'vcenter',
                                                                'font_name': "Times New Roman"})

        # ------------------------

        title_style_tieude_hdgg_table = workbook.add_format({'bold': True,
                                                            'font_size': 9,
                                                             'align': 'center',
                                                             'bg_color': '#B5B5B5',
                                                             'valign': 'vcenter',
                                                             'border': 1,
                                                             'font_name': "Times New Roman"})
        title_style_tieude1_hddg_table = workbook.add_format({'font_size': 9,
                                                                'align': 'center',
                                                                'border': 1,
                                                                'bg_color': '#B5B5B5',
                                                                'valign': 'vcenter',
                                                                'font_name': "Times New Roman"})
        title_style_tieude2_hddg_table = workbook.add_format({'bold': True,
                                                                'font_size': 9,
                                                                'font_color': '#FF0000',
                                                                'bg_color': '#B5B5B5',
                                                                'border': 1,
                                                                'align': 'center',
                                                                'valign': 'vcenter',
                                                                'font_name': "Times New Roman"})

        # ------------------------

        title_style_tieude_table = workbook.add_format({'bold': True,
                                                        'font_size': 9,
                                                        'align': 'center',
                                                        'valign': 'vcenter',
                                                        'border': 1,
                                                        'font_name': "Times New Roman"})
        title_style_tieude_n_table = workbook.add_format({'bold': True,
                                                            'font_size': 9,
                                                            'align': 'center',
                                                            'valign': 'vcenter',
                                                            'border': 1,
                                                            'text_wrap': True,
                                                            'font_name': "Times New Roman"})
        title_style_tieude1_table = workbook.add_format({'font_size': 9,
                                                              'align': 'center',
                                                              'border': 1,
                                                              'valign': 'vcenter',
                                                              'font_name': "Times New Roman"})
        title_style_tieude2_table = workbook.add_format({'bold': True,
                                                              'font_size': 9,
                                                              'font_color': '#FF0000',
                                                              'border': 1,
                                                              'align': 'center',
                                                              'valign': 'vcenter',
                                                              'font_name': "Times New Roman"})

        sheet.freeze_panes(11, 0)
        sheet.set_column('H:H', None, None, {'hidden': 1})
        sheet.set_row(0, 35)
        sheet.set_row(1, 35)
        sheet.set_row(3, 10)
        sheet.set_row(4, 45)
        sheet.set_column('A:A', 7)
        sheet.set_column('B:B', 15)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 30)
        sheet.set_column('E:E', 12)
        sheet.set_column('F:F', 12)
        sheet.set_column('G:G', 23)
        sheet.set_column('X:X', 20)
        sheet.set_column('I:W', 5)
        image_company = io.BytesIO(base64.b64decode(self.env.user.company_id.logo_web))
        sheet.insert_image('C1',"logocompany.png",{'image_data': image_company, 'x_scale': 1, 'y_scale': 1})
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

        # Merge 9 cells.
        sheet.merge_range('A5:X5', 'KẾT QUẢ ĐÁNH GIÁ NHÂN SỰ', title_style_kqdgns_company)
        # sheet.merge_range('A6:X6', 'KỲ ĐÁNH GIÁ: KỲ 1/2022  (06 THÁNG ĐẦU NĂM 2022)', title_style_kqdgns1_company)
        sheet.merge_range('A6:X6', objects.appraisal_period.sudo().name, title_style_kqdgns1_company)

        sheet.merge_range('A8:A11', 'TT', title_style_tieude_table)
        sheet.merge_range('B8:B11', 'Mã NV', title_style_tieude_table)
        sheet.merge_range('C8:C11', 'HỌ VÀ TÊN', title_style_tieude_table)
        sheet.merge_range('D8:D11', 'CHỨC DANH', title_style_tieude_table)
        sheet.merge_range('E8:E11', 'NGÀY VÀO SEACORP', title_style_tieude_n_table)

        sheet.merge_range('F8:G9', 'HĐLĐ Chính thức', title_style_tieude_n_table)
        sheet.merge_range('F10:F11', 'NGÀY', title_style_tieude_table)
        sheet.merge_range('G10:G11', 'LOẠI HĐ', title_style_tieude_table)

        sheet.merge_range('H8:H11', 'QLTT (CHỨC DANH)', title_style_tieude_n_table)

        sheet.merge_range('I8:T8', 'ĐIỂM TB - XẾP LOẠI', title_style_tieude_table)

        sheet.merge_range('I9:K9', 'NS', title_style_tieude_ns_table)
        sheet.merge_range('I10:J10', 'TB', title_style_tieude1_ns_table)
        sheet.write('I11', 'SC', title_style_tieude1_ns_table)
        sheet.write('J11', 'KPIs', title_style_tieude1_ns_table)
        sheet.merge_range('K10:K11', 'XL', title_style_tieude2_ns_table)

        sheet.merge_range('L9:N9', 'PTTT', title_style_tieude_pttt_table)
        sheet.merge_range('L10:M10', 'TB', title_style_tieude1_pttt_table)
        sheet.write('L11', 'SC', title_style_tieude1_pttt_table)
        sheet.write('M11', 'KPIs', title_style_tieude1_pttt_table)
        sheet.merge_range('N10:N11', 'XL', title_style_tieude2_pttt_table)

        sheet.merge_range('O9:Q9', 'Cấp trên PTTT', title_style_tieude_ctpttt_table)
        sheet.merge_range('O10:P10', 'TB', title_style_tieude1_ctpttt_table)
        sheet.write('O11', 'SC', title_style_tieude1_ctpttt_table)
        sheet.write('P11', 'KPIs', title_style_tieude1_ctpttt_table)
        sheet.merge_range('Q10:Q11', 'XL', title_style_tieude2_ctpttt_table)

        sheet.merge_range('R9:T9', 'HĐĐG', title_style_tieude_hdgg_table)
        sheet.merge_range('R10:S10', 'TB', title_style_tieude1_hddg_table)
        sheet.write('R11', 'SC', title_style_tieude1_hddg_table)
        sheet.write('S11', 'KPIs', title_style_tieude1_hddg_table)
        sheet.merge_range('T10:T11', 'XL', title_style_tieude2_hddg_table)

        sheet.merge_range('U8:W9', 'CHỦ TỊCH THÔNG QUA', title_style_tieude_n_table)
        sheet.merge_range('U10:V10', 'TB', title_style_tieude1_table)
        sheet.write('U11', 'SC', title_style_tieude1_table)
        sheet.write('V11', 'KPIs', title_style_tieude1_table)
        sheet.merge_range('W10:W11', 'XL', title_style_tieude2_table)

        sheet.merge_range('X8:X11', 'GHI CHÚ', title_style_tieude_table)

        users_input = self.env['hr.survey.user.input'].sudo().search(
            [('company_id', '=', self.env.user.company_id.id),('appraisal_id', '=', objects[0].id)])
        for user_input in users_input:
            employees = self.env['hr.employee'].sudo().search(
                [('id', '=', user_input.employee_id.id), '|', ('active', '=', False), ('active', '=', True)])
        department_user_input_search = users_input.search([('company_id', '=', self.env.user.company_id.id),('appraisal_id', '=', objects[0].id)], order='s_identification_id asc')
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

        index = 11
        for i in data:
            if i[2]:
                for employee in i[2]:
                    contract = self.env['hr.contract'].sudo().search(
                        [('employee_id', '=', employee.employee_multi_id.sudo().name.id), ('active', '=', True), ('company_id', '=', employee.company_id.id),
                         ('date_start', '<=', employee.create_date.strftime('%Y-%m-%d')), ('state', '!=', 'cancel'),
                         ('type_id', '=', 1), ('contract_category', '=', 'contract')],
                        order="date_start desc",
                        limit=1)
                    if contract:
                        employee.official_contract = contract.date_start.strftime("%d/%m/%Y")
                        employee.contract_period= contract.contract_period_id.name

                    else:
                        employee.official_contract = ''
                        employee.contract_period = ''

                    # contract=self.env['hr.contract'].sudo().search([('employee_id','=',employee.employee_id.id),('active','=',True)],order="date_start desc",limit=1)
                    # if contract:
                    #     employee.official_contract=contract.date_start.strftime("%d/%m/%Y")
                    #     employee.contract_period= contract.contract_period_id.name
                    # else:
                    #     employee.official_contract = ''
                    #     employee.contract_period = ''
            index = self._print_bom_children(i[0], i[1], i[2], sheet, index, workbook)
            index += 1