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
    _name = 'report.seatek_hr_appraisal.report_baocao_dgns_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_children(tt, title, data, sheet, row, workbook, tong_cong=False, len_list=False):
        data_style_center = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_center_number = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman", 'num_format': '#,##0'})
        data_style_center_enter = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        data_style_center_bold = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bold': True,
             'font_name': "Times New Roman", 'bg_color': '#a9d08e'})
        data_style = workbook.add_format(
            {'font_size': 10, 'valign': 'vcenter', 'border': 1,
             'font_name': "Times New Roman"})
        data_style_enter = workbook.add_format(
            {'font_size': 10, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        data_style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1, 'bg_color': '#a9d08e',
             'font_name': "Times New Roman"})
        data_style_bold_tc = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1, 'bg_color': '#bdd7ee',
             'font_name': "Times New Roman", 'font_color': '#FF0000', 'align': 'center'})
        data_style_bold_tc_number = workbook.add_format(
            {'bold': True, 'font_size': 11, 'valign': 'vcenter', 'border': 1, 'bg_color': '#bdd7ee',
             'font_name': "Times New Roman", 'font_color': '#FF0000', 'align': 'center', 'num_format': '#,##0'})

        i = row
        sheet.set_row(i, 22.25)

        if data is not None:
            ch = data
            sheet.write(i, 0, tt, data_style)
            sheet.write(i, 1, ch.sc_code or '', data_style)
            sheet.write(i, 2, ch.name or '', data_style)
            sheet.write(i, 3, ch.job_position_id.sudo().name or '', data_style)
            sheet.write(i, 4, ch.seagroup_join_date or '', data_style_center)
            sheet.write(i, 5, ch.official_contract or '', data_style_center)
            sheet.write(i, 6, ch.contract_period or '', data_style_center_enter)
            sheet.write(i, 7, ch.manager_name or '', data_style)
            sheet.write(i, 8, ch.smanager_name or '', data_style)

            sheet.write(i, 9, '', data_style_center_number)

            # ĐIỂM TB - XẾP LOẠI
            sheet.write(i, 10, ch.user_seacorp or '', data_style_center)
            sheet.write(i, 11, ch.user_kpi or '', data_style_center)
            sheet.write(i, 12, ch.rating1_value or '', data_style_center)

            sheet.write(i, 13, ch.manager_seacorp or '', data_style_center)
            sheet.write(i, 14, ch.manager_kpi or '', data_style_center)
            sheet.write(i, 15, ch.rating2_value or '', data_style_center)

            sheet.write(i, 16, ch.smanager_seacorp or '', data_style_center)
            sheet.write(i, 17, ch.smanager_kpi or '', data_style_center)
            sheet.write(i, 18, ch.rating3_value or '', data_style_center)
            sheet.write(i, 19, ch.colleague_seacorp or '', data_style_center)
            sheet.write(i, 20, ch.rating5_value or 'KK', data_style_center)
            sheet.write(i, 21, ch.colleague2_seacorp or '', data_style_center)
            sheet.write(i, 22, ch.rating6_value or 'KK', data_style_center)
            sheet.write(i, 23, ch.colleague3_seacorp or '', data_style_center)
            sheet.write(i, 24, ch.rating7_value or 'KK', data_style_center)


            sheet.write(i, 25, ch.hddg_seacorp or '', data_style_center)
            sheet.write(i, 26, ch.hddg_kpi or '', data_style_center)
            sheet.write(i, 27, ch.rating4_value or 'KK', data_style_center)

            # ĐỀ XUẤT  SAU ĐGNS
            sheet.write(i, 28, ch.dexuat_salary_user or '0', data_style_center_number)
            sheet.write(i, 29, ch.dexuat_salary_manager or '0', data_style_center_number)
            sheet.write(i, 30, ch.dexuat_salary_smanager or '0', data_style_center_number)
            sheet.write(i, 31, ch.dexuat_salary_colleague or '0', data_style_center_number)
            sheet.write(i, 32, ch.dexuat_salary_colleague2 or '0', data_style_center_number)
            sheet.write(i, 33, ch.dexuat_salary_colleague3 or '0', data_style_center_number)
            sheet.write(i, 34, ch.dexuat_salary_hddg or '0', data_style_center_number)

            sheet.write(i, 35, ch.dexuat_thuong_user or '0', data_style_center_number)
            sheet.write(i, 36, ch.dexuat_thuong_manager or '0', data_style_center_number)
            sheet.write(i, 37, ch.dexuat_thuong_smanager or '0', data_style_center_number)
            sheet.write(i, 38, ch.dexuat_thuong_colleague or '0', data_style_center_number)
            sheet.write(i, 39, ch.dexuat_thuong_colleague2 or '0', data_style_center_number)
            sheet.write(i, 40, ch.dexuat_thuong_colleague3 or '0', data_style_center_number)
            sheet.write(i, 41, ch.dexuat_thuong_hddg or '0', data_style_center_number)

            dexuat_user = ''
            dexuat_manager = ''
            dexuat_smanager = ''
            dexuat_colleague = ''
            dexuat_colleague2 = ''
            dexuat_colleague3 = ''
            dexuat_hddg = ''
            if ch.dexuat_chucvu_user:
                dexuat_user = dexuat_user + ch.dexuat_chucvu_user
            if ch.dexuat_thuyenchuyen_user:
                dexuat_user = dexuat_user + ' - ' + ch.dexuat_thuyenchuyen_user
            if ch.dexuat_chucvu_manager:
                dexuat_manager = dexuat_manager + ch.dexuat_chucvu_manager
            if ch.dexuat_thuyenchuyen_manager:
                dexuat_manager = dexuat_manager + ' - ' + ch.dexuat_thuyenchuyen_manager

            if ch.dexuat_chucvu_smanager:
                dexuat_smanager = dexuat_smanager + ch.dexuat_chucvu_smanager
            if ch.dexuat_thuyenchuyen_smanager:
                dexuat_smanager = dexuat_smanager + ' - ' + ch.dexuat_thuyenchuyen_smanager

            if ch.dexuat_chucvu_colleague:
                dexuat_colleague = dexuat_colleague + ch.dexuat_chucvu_colleague
            if ch.dexuat_thuyenchuyen_colleague:
                dexuat_colleague = dexuat_colleague + ' - ' + ch.dexuat_thuyenchuyen_colleague

            if ch.dexuat_chucvu_colleague2:
                dexuat_colleague2 = dexuat_colleague2 + ch.dexuat_chucvu_colleague2
            if ch.dexuat_thuyenchuyen_colleague2:
                dexuat_colleague2 = dexuat_colleague2 + ' - ' + ch.dexuat_thuyenchuyen_colleague2

            if ch.dexuat_chucvu_colleague3:
                dexuat_colleague3 = dexuat_colleague3 + ch.dexuat_chucvu_colleague3
            if ch.dexuat_thuyenchuyen_colleague3:
                dexuat_colleague3 = dexuat_colleague3 + ' - ' + ch.dexuat_thuyenchuyen_colleague3
            if ch.dexuat_chucvu_hddg:
                dexuat_hddg = dexuat_hddg + ch.dexuat_chucvu_hddg
            if ch.dexuat_thuyenchuyen_hddg:
                dexuat_hddg = dexuat_hddg + ' - ' + ch.dexuat_thuyenchuyen_hddg

            sheet.write(i, 42, dexuat_user or '', data_style_enter)
            sheet.write(i, 43, dexuat_manager or '', data_style_enter)
            sheet.write(i, 44, dexuat_smanager or '', data_style_enter)
            sheet.write(i, 45, dexuat_colleague or '', data_style_enter)
            sheet.write(i, 46, dexuat_colleague2 or '', data_style_enter)
            sheet.write(i, 47, dexuat_colleague3 or '', data_style_enter)
            sheet.write(i, 48, dexuat_hddg or '', data_style_enter)

            sheet.write(i, 49, ch.user_opinion or '', data_style_enter)
            sheet.write(i, 50, ch.manager_opinion or '', data_style_enter)
            sheet.write(i, 51, ch.smanager_opinion or '', data_style_enter)
            sheet.write(i, 52, ch.colleague_opinion or '', data_style_enter)
            sheet.write(i, 53, ch.colleague2_opinion or '', data_style_enter)
            sheet.write(i, 54, ch.colleague3_opinion or '', data_style_enter)
            sheet.write(i, 55, ch.hddg_opinion or '', data_style_enter)
            # CHỦ TỊCH THÔNG QUA
            sheet.write(i, 56, '', data_style_center_number)
            sheet.write(i, 57, '', data_style_center_number)
            sheet.write(i, 58, '=SUM(J%s,AT%s)' % ((i + 1), (i + 1)), data_style_center_number)

            # GHI CHÚ
            sheet.write(i, 59, '', data_style_enter)

        elif tong_cong == 3:
            sheet.merge_range('A%s:C%s' % (i + 1, i + 1), 'TỔNG CỘNG (' + tt + ')', data_style_bold_tc)
            sheet.write(i, 3, '', data_style_bold_tc)
            sheet.write(i, 4, '', data_style_bold_tc)
            sheet.write(i, 5, '', data_style_bold_tc)
            sheet.write(i, 6, '', data_style_bold_tc)
            sheet.write(i, 7, '', data_style_bold_tc)
            sheet.write(i, 8, '', data_style_bold_tc)

            sheet.write(i, 9, '=SUM(J%s:J%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)

            # ĐIỂM TB - XẾP LOẠI
            sheet.write(i, 10, '', data_style_bold_tc)
            sheet.write(i, 11, '', data_style_bold_tc)
            sheet.write(i, 12, '', data_style_bold_tc)

            sheet.write(i, 13, '', data_style_bold_tc)
            sheet.write(i, 14, '', data_style_bold_tc)
            sheet.write(i, 15, '', data_style_bold_tc)

            sheet.write(i, 16, '', data_style_bold_tc)
            sheet.write(i, 17, '', data_style_bold_tc)
            sheet.write(i, 18, '', data_style_bold_tc)

            sheet.write(i, 19, '', data_style_bold_tc)
            sheet.write(i, 20, '', data_style_bold_tc)

            sheet.write(i, 21, '', data_style_bold_tc)
            sheet.write(i, 22, '', data_style_bold_tc)
            sheet.write(i, 23, '', data_style_bold_tc)
            sheet.write(i, 24, '', data_style_bold_tc)
            sheet.write(i, 25, '', data_style_bold_tc)
            sheet.write(i, 26, '', data_style_bold_tc)
            sheet.write(i, 27, '', data_style_bold_tc)

            # ĐỀ XUẤT  SAU ĐGNS
            sheet.write(i, 28, '=SUM(AC%s:AC%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 29, '=SUM(AD%s:AD%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 30, '=SUM(AE%s:AE%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 31, '=SUM(AF%s:AF%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 32, '=SUM(AG%s:AG%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)

            sheet.write(i, 33, '=SUM(AH%s:AH%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 34, '=SUM(AI%s:AI%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 35, '=SUM(AJ%s:AJ%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 36, '=SUM(AK%s:AK%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 37, '=SUM(AL%s:AL%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 38, '=SUM(AM%s:AM%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 39, '=SUM(AN%s:AN%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 40, '=SUM(AO%s:AO%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 41, '=SUM(AP%s:AP%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)

            sheet.write(i, 42, '', data_style_bold_tc)
            sheet.write(i, 43, '', data_style_bold_tc)
            sheet.write(i, 44, '', data_style_bold_tc)
            sheet.write(i, 45, '', data_style_bold_tc)
            sheet.write(i, 46, '', data_style_bold_tc)
            sheet.write(i, 47, '', data_style_bold_tc)
            sheet.write(i, 48, '', data_style_bold_tc)
            sheet.write(i, 49, '', data_style_bold_tc)
            sheet.write(i, 50, '', data_style_bold_tc)
            sheet.write(i, 51, '', data_style_bold_tc)
            sheet.write(i, 52, '', data_style_bold_tc)
            sheet.write(i, 53, '', data_style_bold_tc)
            sheet.write(i, 54, '', data_style_bold_tc)
            sheet.write(i, 55, '', data_style_bold_tc)

            # CHỦ TỊCH THÔNG QUA
            sheet.write(i, 56, '=SUM(AS%s:AS%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 57, '=SUM(AT%s:AT%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)
            sheet.write(i, 58, '=SUM(AU%s:AU%s)' % ((i - len_list + 1), i), data_style_bold_tc_number)

            # GHI CHÚ
            sheet.write(i, 59, '', data_style_bold_tc)
        else:
            sheet.write(i, 0, tt, data_style_center_bold)
            sheet.merge_range('B%s:BH%s' % (i + 1, i + 1), title, data_style_bold)
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
        # print(self.env.user.company_ids)
        for company in self.env.user.company_ids:
            if company.id == 1:
                continue
            else:
                sheet = workbook.add_worksheet(_(company.short_name))
                sheet.set_landscape()
                sheet.fit_to_pages(1, 0)
                sheet.set_zoom(85)

                title_style_name_company = workbook.add_format({'bold': True,
                                                                'font_size': 16,
                                                                'font_name': "Times New Roman",
                                                                'valign': 'vcenter'})
                title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
                title_style_kqdgns_company = workbook.add_format(
                    {'bold': True, 'font_size': 20, 'font_name': "Times New Roman", 'align': 'center',
                     'valign': 'vcenter'})
                title_style_kqdgns1_company = workbook.add_format(
                    {'bold': True, 'font_size': 15, 'font_name': "Times New Roman", 'align': 'center',
                     'valign': 'vcenter'})

                title_style_tieude2_hddg_table = workbook.add_format({'bold': True,
                                                                      'font_size': 9,
                                                                      'font_color': '#FF0000',
                                                                      'border': 1,
                                                                      'align': 'center',
                                                                      'valign': 'vcenter',
                                                                      'text_wrap': True,
                                                                      'font_name': "Times New Roman"})
                title_style_tieude2_hddg_table_number = workbook.add_format({'bold': True,
                                                                             'font_size': 9,
                                                                             'font_color': '#FF0000',
                                                                             'border': 1,
                                                                             'align': 'center',
                                                                             'valign': 'vcenter',
                                                                             'text_wrap': True, 'num_format': '#,##0',
                                                                             'font_name': "Times New Roman"})
                title_style_tieude2_hddg_table_1 = workbook.add_format({'bold': True,
                                                                        'font_size': 9,
                                                                        'font_color': '#FF0000',
                                                                        'align': 'center',
                                                                        'valign': 'vcenter',
                                                                        'text_wrap': True,
                                                                        'font_name': "Times New Roman"})
                title_style_tieude2_hddg_table_1_number = workbook.add_format({'bold': True,
                                                                               'font_size': 9,
                                                                               'font_color': '#FF0000',
                                                                               'align': 'center',
                                                                               'valign': 'vcenter',
                                                                               'num_format': '#,##0',
                                                                               'text_wrap': True,
                                                                               'font_name': "Times New Roman"})
                title_style_tieude3_hddg_table = workbook.add_format({'bold': True,
                                                                      'font_size': 9,
                                                                      'font_color': '#002060',
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
                title_style_tieude_n_table_1 = workbook.add_format({'bold': True,
                                                                    'font_size': 9,
                                                                    'align': 'center',
                                                                    'valign': 'vcenter',
                                                                    'text_wrap': True,
                                                                    'font_name': "Times New Roman"})
                title_style_tieude1_table = workbook.add_format({'font_size': 9,
                                                                 'align': 'center',
                                                                 'border': 1,
                                                                 'valign': 'vcenter',
                                                                 'font_name': "Times New Roman"})

                sheet.freeze_panes(10, 0)
                sheet.set_row(0, 35)
                sheet.set_row(1, 35)
                sheet.set_row(3, 10)
                sheet.set_row(4, 45)
                sheet.set_row(8, 25)
                sheet.set_column('A:A', 7)
                sheet.set_column('B:B', 10)
                sheet.set_column('C:C', 25)
                sheet.set_column('D:D', 30)

                sheet.set_column('E:E', 12)

                sheet.set_column('F:F', 10)
                sheet.set_column('G:G', 20)
                sheet.set_column('H:H', 20)
                sheet.set_column('I:I', 20)
                sheet.set_column('J:J', 14)

                sheet.set_column('K:K', 6)
                sheet.set_column('L:L', 6)
                sheet.set_column('M:M', 6)
                sheet.set_column('N:N', 6)
                sheet.set_column('O:O', 6)
                sheet.set_column('P:P', 6)
                sheet.set_column('Q:Q', 6)
                sheet.set_column('R:R', 6)
                sheet.set_column('S:S', 6)
                sheet.set_column('T:T', 6)
                sheet.set_column('U:U', 6)
                sheet.set_column('V:V', 6)
                sheet.set_column('W:W', 6)
                sheet.set_column('X:X', 6)

                sheet.set_column('Y:Y', 12)
                sheet.set_column('Z:Z', 12)
                sheet.set_column('AA:AA', 12)
                sheet.set_column('AB:AB', 12)
                sheet.set_column('AC:AP', 12)

                sheet.set_column('AQ:BD', 30)


                sheet.set_column('BE:BG', 16)
                sheet.set_column('BH:BHV', 30)

                image_company = io.BytesIO(base64.b64decode(company.logo_web))
                sheet.insert_image('C1', "logocompany.png",
                                   {'image_data': image_company, 'x_scale': 1, 'y_scale': 0.75})
                sheet.write('D1', company.name, title_style_name_company)
                sheet.write('D2', company.sea_company_foreign, title_style_name_company)
                address = ''
                if company.street:
                    address += company.street
                if company.street2:
                    address += company.street2
                if company.city:
                    address += company.city
                if company.state_id:
                    address += company.state_id.name
                if company.country_id:
                    address += ', ' + company.country_id.name
                sheet.write('D3', address, title_style_address_company)

                # Merge cells.
                sheet.merge_range('A5:AC5', 'KẾT QUẢ ĐÁNH GIÁ NHÂN SỰ NĂM ' + str(objects.create_date.strftime("%Y")),
                                  title_style_kqdgns_company)
                sheet.merge_range('A6:AC6', objects.appraisal_period.sudo().name, title_style_kqdgns1_company)

                sheet.merge_range('A8:A10', 'TT', title_style_tieude_table)
                sheet.merge_range('B8:B10', 'Mã NV', title_style_tieude_table)
                sheet.merge_range('C8:C10', 'HỌ VÀ TÊN', title_style_tieude_table)
                sheet.merge_range('D8:D10', 'CHỨC DANH HIỆN TẠI', title_style_tieude_table)
                sheet.merge_range('E8:E10', 'NGÀY VÀO SEACORP', title_style_tieude_n_table)

                # HĐLĐ Chính thức
                sheet.merge_range('F8:G9', 'HĐLĐ Chính thức', title_style_tieude_n_table)
                sheet.write('F10', 'NGÀY', title_style_tieude_table)
                sheet.write('G10', 'LOẠI HĐ', title_style_tieude_table)

                sheet.merge_range('H8:H10', 'QLTT', title_style_tieude_n_table)
                sheet.merge_range('I8:I10', 'CT QLTT', title_style_tieude_n_table)

                sheet.merge_range('J8:J10', 'LƯƠNG HIỆN TẠI (VNĐ/THÁNG)', title_style_tieude_n_table)

                # ĐIỂM TB - XẾP LOẠI
                sheet.merge_range('K8:AB8', 'ĐIỂM TB - XẾP LOẠI', title_style_tieude_n_table)
                sheet.merge_range('K9:M9', 'NS', title_style_tieude_table)
                sheet.write('K10', 'SC', title_style_tieude1_table)
                sheet.write('L10', 'KPIs', title_style_tieude1_table)
                sheet.write('M10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('N9:P9', 'QLTT', title_style_tieude_table)
                sheet.write('N10', 'SC', title_style_tieude1_table)
                sheet.write('O10', 'KPIs', title_style_tieude1_table)
                sheet.write('P10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('Q9:S9', 'Cấp trên QLTT', title_style_tieude_table)
                sheet.write('Q10', 'SC', title_style_tieude1_table)
                sheet.write('R10', 'KPIs', title_style_tieude1_table)
                sheet.write('S10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('T9:U9', 'ĐN1', title_style_tieude_table)
                sheet.write('T10', 'SC', title_style_tieude1_table)
                sheet.write('U10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('V9:W9', 'ĐN2', title_style_tieude_table)
                sheet.write('V10', 'SC', title_style_tieude1_table)
                sheet.write('W10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('X9:Y9', 'ĐN3', title_style_tieude_table)
                sheet.write('X10', 'SC', title_style_tieude1_table)
                sheet.write('Y10', 'XL', title_style_tieude2_hddg_table)

                sheet.merge_range('Z9:AB9', 'HĐĐG', title_style_tieude_table)
                sheet.write('Z10', 'SC', title_style_tieude1_table)
                sheet.write('AA10', 'KPIs', title_style_tieude1_table)
                sheet.write('AB10', 'XL', title_style_tieude2_hddg_table)

                # ĐỀ XUẤT  SAU ĐGNS
                sheet.merge_range('AC8:BD8', 'ĐỀ XUẤT  SAU ĐGNS', title_style_tieude_n_table)

                sheet.merge_range('AC9:AI9', 'LƯƠNG (VNĐ/tháng)', title_style_tieude_table)
                sheet.write('AC10', 'NS', title_style_tieude_table)
                sheet.write('AD10', 'QLTT', title_style_tieude3_hddg_table)
                sheet.write('AE10', 'CT QLTT', title_style_tieude3_hddg_table)
                sheet.write('AF10', 'ĐN1', title_style_tieude_table)
                sheet.write('AG10', 'ĐN2', title_style_tieude_table)
                sheet.write('AH10', 'ĐN3', title_style_tieude_table)
                sheet.write('AI10', 'HĐ', title_style_tieude2_hddg_table)

                sheet.merge_range('AJ9:AP9', 'THƯỞNG (VNĐ)', title_style_tieude_n_table)
                sheet.write('AJ10', 'NS', title_style_tieude_n_table)
                sheet.write('AK10', 'QLTT', title_style_tieude3_hddg_table)
                sheet.write('AL10', 'CT QLTT', title_style_tieude3_hddg_table)
                sheet.write('AM10', 'ĐN1', title_style_tieude_n_table)
                sheet.write('AN10', 'ĐN2', title_style_tieude_n_table)
                sheet.write('AO10', 'ĐN3', title_style_tieude_n_table)
                sheet.write('AP10', 'HĐ', title_style_tieude2_hddg_table)

                sheet.merge_range('AQ9:AW9', 'ĐIỀU CHUYỂN THĂNG TIẾN', title_style_tieude_n_table)
                sheet.write('AQ10', 'NS', title_style_tieude_n_table)
                sheet.write('AR10', 'QLTT', title_style_tieude3_hddg_table)
                sheet.write('AS10', 'CT QLTT', title_style_tieude3_hddg_table)
                sheet.write('AT10', 'ĐN1', title_style_tieude_n_table)
                sheet.write('AU10', 'ĐN2', title_style_tieude_n_table)
                sheet.write('AV10', 'ĐN3', title_style_tieude_n_table)
                sheet.write('AW10', 'HĐ', title_style_tieude2_hddg_table)

                sheet.merge_range('AX9:BD9', 'ĐX KHÁC', title_style_tieude_n_table)
                sheet.write('AX10', 'NS', title_style_tieude_n_table)
                sheet.write('AY10', 'QLTT', title_style_tieude3_hddg_table)
                sheet.write('AZ10', 'CT QLTT', title_style_tieude3_hddg_table)
                sheet.write('BA10', 'ĐN1', title_style_tieude_n_table)
                sheet.write('BB10', 'ĐN2', title_style_tieude_n_table)
                sheet.write('BC10', 'ĐN3', title_style_tieude_n_table)
                sheet.write('BD10', 'HĐ', title_style_tieude2_hddg_table)

                # CHỦ TỊCH THÔNG QUA
                sheet.merge_range('BE8:BG8', 'CHỦ TỊCH THÔNG QUA', title_style_tieude_n_table)
                sheet.merge_range('BE9:BE10', 'HỖ TRỢ LƯƠNG NĂM ' + str(objects.create_date.strftime("%Y")) + ' (VNĐ)',
                                  title_style_tieude2_hddg_table)
                sheet.merge_range('BF9:BF10', 'TĂNG LƯƠNG (VNĐ/tháng)', title_style_tieude_n_table)
                sheet.merge_range('BG9:BG10', 'LƯƠNG (VNĐ/tháng)', title_style_tieude2_hddg_table)

                # GHI CHÚ
                sheet.merge_range('BH8:BH10', 'GHI CHÚ', title_style_tieude_n_table)

                users_input = self.env['hr.survey.user.input'].sudo().search(
                    [('company_id', '=', company.id), ('appraisal_id', '=', objects[0].id)])
                department_user_input_search = users_input.search(
                    [('company_id', '=', company.id), ('appraisal_id', '=', objects[0].id)],
                    order='job_position_id, s_identification_id asc')
                department_search = self.env['hr.department'].sudo().search(
                    [('company_id', '=', company.id)])
                department_parent = []
                for i in department_search:
                    if i.sort_name:
                        department_parent.append([i.sort_name, i])
                department_parent.sort(key=lambda x: x[0])

                list_department = []
                for id_department, data in department_parent:
                    self.get_department_child(list_department=list_department, id_department=id_department,
                                              department=data,
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
                        list_result.append(
                            ['%s.%s.%s.%s.%s' % (index1, index2, index3, index4, index5), data.name, data])
                    if i == 6:
                        index6 += 1
                        list_result.append(
                            ['%s.%s.%s.%s.%s.%s' % (index1, index2, index3, index4, index5, index6), data.name, data])

                data = []
                stt = 0
                for tt, title, data_result in list_result:
                    data.append([tt, title, None, None, None])
                    list_user_temp = []
                    for i in department_user_input_search:
                        if data_result == i.department_compute:
                            job_sequence = self.get_job_position(i.employee_id.id)
                            list_user_temp.append([str(job_sequence), i])

                    list_user_temp.sort(key=lambda x: x[0])

                    end = stt + len(list_user_temp)
                    for i, user in list_user_temp:
                        stt += 1
                        data.append([stt, None, user, None, None])
                        if stt == end:
                            data.append([tt, None, None, 3, len(list_user_temp)])

                for i in department_user_input_search:
                    if not i.department_compute:
                        data.append(['', 'KHÔNG CÓ BỘ PHẬN', None, None, None])
                        break
                # them employee k co department
                for i in department_user_input_search:
                    if not i.department_compute:
                        stt += 1
                        data.append([stt, None, i, None, None])

                index = 10
                for i in data:
                    index = self._print_bom_children(i[0], i[1], i[2], sheet, index, workbook, i[3], i[4])
                    index += 1

                sheet.merge_range('A%s:I%s' % (index + 1, index + 1), 'TỔNG CỘNG', title_style_tieude_n_table)

                sheet.write(index, 9, '=SUM(J%s:J%s)/2' % (10, index), title_style_tieude2_hddg_table_number)

                # ĐIỂM TB - XẾP LOẠI
                sheet.write(index, 10, '', title_style_tieude2_hddg_table)
                sheet.write(index, 11, '', title_style_tieude2_hddg_table)
                sheet.write(index, 12, '', title_style_tieude2_hddg_table)

                sheet.write(index, 13, '', title_style_tieude2_hddg_table)
                sheet.write(index, 14, '', title_style_tieude2_hddg_table)
                sheet.write(index, 15, '', title_style_tieude2_hddg_table)

                sheet.write(index, 16, '', title_style_tieude2_hddg_table)
                sheet.write(index, 17, '', title_style_tieude2_hddg_table)
                sheet.write(index, 18, '', title_style_tieude2_hddg_table)

                sheet.write(index, 19, '', title_style_tieude2_hddg_table)
                sheet.write(index, 20, '', title_style_tieude2_hddg_table)

                sheet.write(index, 21, '', title_style_tieude2_hddg_table)
                sheet.write(index, 22, '', title_style_tieude2_hddg_table)
                sheet.write(index, 23, '', title_style_tieude2_hddg_table)
                sheet.write(index, 24, '', title_style_tieude2_hddg_table)
                sheet.write(index, 25, '', title_style_tieude2_hddg_table)
                sheet.write(index, 26, '', title_style_tieude2_hddg_table)
                sheet.write(index, 27, '', title_style_tieude2_hddg_table)

                # ĐỀ XUẤT  SAU ĐGNS
                sheet.write(index, 28, '=SUM(AC%s:AC%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 29, '=SUM(AD%s:AD%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 30, '=SUM(AE%s:AE%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 31, '=SUM(AF%s:AF%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 32, '=SUM(AG%s:AG%s)/2' % (10, index), title_style_tieude2_hddg_table_number)

                sheet.write(index, 33, '=SUM(AH%s:AH%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 34, '=SUM(AI%s:AI%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 35, '=SUM(AJ%s:AJ%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 36, '=SUM(AK%s:AK%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 37, '=SUM(AL%s:AL%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 38, '=SUM(AM%s:AM%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 39, '=SUM(AN%s:AN%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 40, '=SUM(AO%s:AO%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 41, '=SUM(AP%s:AP%s)/2' % (10, index), title_style_tieude2_hddg_table_number)

                sheet.write(index, 42, '', title_style_tieude2_hddg_table)
                sheet.write(index, 43, '', title_style_tieude2_hddg_table)
                sheet.write(index, 44, '', title_style_tieude2_hddg_table)
                sheet.write(index, 45, '', title_style_tieude2_hddg_table)
                sheet.write(index, 46, '', title_style_tieude2_hddg_table)
                sheet.write(index, 47, '', title_style_tieude2_hddg_table)
                sheet.write(index, 48, '', title_style_tieude2_hddg_table)
                sheet.write(index, 49, '', title_style_tieude2_hddg_table)
                sheet.write(index, 50, '', title_style_tieude2_hddg_table)
                sheet.write(index, 51, '', title_style_tieude2_hddg_table)
                sheet.write(index, 52, '', title_style_tieude2_hddg_table)
                sheet.write(index, 53, '', title_style_tieude2_hddg_table)
                sheet.write(index, 54, '', title_style_tieude2_hddg_table)
                sheet.write(index, 55, '', title_style_tieude2_hddg_table)

                # CHỦ TỊCH THÔNG QUA
                sheet.write(index, 56, '=SUM(AS%s:AS%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 57, '=SUM(AT%s:AT%s)/2' % (10, index), title_style_tieude2_hddg_table_number)
                sheet.write(index, 58, '=SUM(AU%s:AU%s)/2' % (10, index), title_style_tieude2_hddg_table_number)

                # GHI CHÚ
                sheet.write(index, 59, '', title_style_tieude2_hddg_table)

                index += 1
                sheet.set_row(index, None, None, {'hidden': 1})
                index += 1
                data_style = workbook.add_format({'font_size': 10, 'valign': 'vcenter',
                                                  'font_name': "Times New Roman"})
                data_style_number = workbook.add_format({'font_size': 10, 'valign': 'vcenter',
                                                  'font_name': "Times New Roman", 'num_format': '#,##0'})
                data_style_i = workbook.add_format(
                    {'font_size': 10, 'valign': 'vcenter',
                     'font_name': "Times New Roman", 'italic': True,
                     'align': 'center',
                     'valign': 'vcenter',
                     })
                sheet.write(index, 3, 'Ghi chú: Quỹ lương dự kiến tăng: ', data_style)
                sheet.write(index, 9, '=AU%s - J%s' % (index - 1, index - 1), title_style_tieude2_hddg_table_1_number)
                sheet.write(index, 11, 'VNĐ/tháng', title_style_tieude2_hddg_table_1)
                sheet.write(index, 18, 'Dự kiến lương tăng: ', data_style)
                sheet.write(index, 25, '=Z%s - J%s' % (index - 1, index - 1), data_style_number)
                sheet.merge_range('AJ%s:AV%s' % ((index + 1), (index + 1)),
                                  'Tp Hồ Chí Minh, ngày ...  tháng ... năm 20..',
                                  data_style_i)
                index += 1
                sheet.set_row(index, None, None, {'hidden': 1})
                index += 1
                sheet.set_row(index, None, None, {'hidden': 1})
                index += 1
                sheet.set_row(index, None, None, {'hidden': 1})
                index += 1
                sheet.set_row(index, None, None, {'hidden': 1})
                index += 1
                sheet.write('C%s' % (index + 1), 'CHỦ TỊCH', title_style_tieude_n_table_1)
                sheet.merge_range('AJ%s:AV%s' % (index + 1, index + 1), 'TM. HỘI ĐỒNG ĐGNS',
                                  title_style_tieude_n_table_1)
                index += 5
                sheet.write('C%s' % index, 'Trần Phong Lan', title_style_tieude_n_table_1)
                sheet.merge_range('AJ%s:AV%s' % (index + 1, index + 1), 'Ngô Ngọc Mai Trang',
                                  title_style_tieude_n_table_1)
