# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import base64
import io
import logging
from odoo.exceptions import UserError

from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ExportAppraisal(models.AbstractModel):
    _name = 'report.seatek_hr_appraisal.report_export_appraisal_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def write_excel_data(self, workbook, stt, sheet1, i, user_input,sheet_number=0, kpi=False):
        sheet1.set_row(i, 32)
        sheet1.set_column('B:B', 65)
        style_all = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter', 'border': 1})
        style_all_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter', 'border': 1,'locked':False})
        style_tt_4 = workbook.add_format(
            {'align': 'center', 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter',
             'border': 1, 'italic': True,'locked':True})
        style_tt_4_percent = workbook.add_format(
            {'align': 'center', 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter',
             'border': 1, 'italic': True,'num_format': '0%','locked':False})
        style_tt_4_unlock = workbook.add_format(
            {'align': 'center', 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter',
             'border': 1, 'italic': True,'locked':False})
        style_1 = workbook.add_format(
            {'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'border': 1,
             'valign': 'vcenter'})
        style_tt_2 = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter','underline':True,'locked':True})
        style_tt_2_percent = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter','num_format': '0%','locked':False})
        style_tt_2_unlock = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter','locked':False})
        style_tt_3 = workbook.add_format(
            {'align': 'right', 'color': "#002060", 'bold': True, 'border': 1, 'font_size': 11,
             'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter'})

        style_4 = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter',
             'border': 1, 'italic': True,'locked':True})
        style_4_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter',
             'border': 1, 'italic': True,'locked':False})
        style_2 = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter'})
        style_2_unlock = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter','locked':False})
        style_3 = workbook.add_format(
            {'color': "#002060", 'bold': True, 'border': 1, 'font_size': 11,
             'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter'})


        style_1_k = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman",'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center", 'valign': 'vcenter',
             'num_format': '#,##0.00','underline':True})
        style_2_k = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman",'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center",  'valign': 'vcenter','color': "red",
             'num_format': '#,##0.00','underline':True})
        style_3_k = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center",  'valign': 'vcenter','color': "#002060",
             'num_format': '#,##0.00','underline':True})
        style_4_k = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter','border': 1,
             'align': "center",  'italic': True,
             'num_format': '#,##0.00','underline':True})
        '''Unlock Cell'''
        style_1_k_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center", 'valign': 'vcenter',
             'num_format': '#,##0.00','locked':False})
        style_2_k_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center", 'valign': 'vcenter', 'color': "red",
             'num_format': '#,##0.00','locked':False})
        style_3_k_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'bold': True, 'text_wrap': True, 'border': 1,
             'align': "center", 'valign': 'vcenter', 'color': "#002060",
             'num_format': '#,##0.00','locked':False})
        style_4_k_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter', 'border': 1,
             'align': "center", 'italic': True,
             'num_format': '#,##0.00','locked':False})
        search = self.env['hr.survey.user.input.line'].sudo().search(
            [('user_input_id', '=', user_input.id), ('prefix', '=', stt),
             ('enable_edit_percentage', '=', kpi)])
        comment = "" if not search.user_comment else str(search.user_comment)
        search_value = "K" if not search.value else search.value
        if search_value!="K":
            value=float('%.2f' % float(search_value))
        else:
            value=search_value
        try:
            percentage = search.percentage/100
        except:
            raise UserError('Không thể kết xuất file Excel')

        for rec in user_input:
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    comment = "" if not search.colleague_comment else str(search.colleague_comment)
                    search_value = "K" if not search.value_colleague else search.value_colleague
                    if search_value != "K":
                        value = float('%.2f' % float(search_value))
                    else:
                        value = search_value
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.smanager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    comment = "" if not search.smanager_comment else str(search.smanager_comment)
                    search_value = "" if not search.value_smanager else search.value_smanager
                    if search_value != "K":
                        value = float('%.2f' % float(search_value))
                    else:
                        value = search_value
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.manager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    comment = "" if not search.manager_comment else search.manager_comment
                    search_value = "" if not search.value_manager else search.value_manager
                    if search_value != "K":
                        value = float('%.2f' % float(search_value))
                    else:
                        value = search_value
        if not kpi:
            if stt.count("I") > 0:
                title = 1
                stt = stt[2:]
            else:
                title = 2 if stt.count(".") == 1 or stt == "3.3." else (3 if stt.count(".") == 2 else 4)
            sheet1.write("A" + str(i), stt,
                         style_1 if title == 1 else (
                             style_tt_2 if title == 2 else (style_tt_3 if title == 3 else style_tt_4)))
            sheet1.write("B" + str(i), str(search.question_name),
                         style_1 if title == 1 else (style_2 if title == 2 else (style_3 if title == 3 else style_4)))
            sheet1.write("C" + str(i), comment, style_all_unlock)
            unlock=False
            if sheet_number==1 and str(i)=='7':
                value='=IFERROR(AVERAGE(D8:D9),\"K\")'
            elif sheet_number == 1 and str(i) == '8':
                value='=IFERROR(AVERAGE(\'I.2. THÂN THIỆN TỬ TẾ\'!D8,\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D18,\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D19,' \
                            '\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D21,\'I.4. TIÊU CHÍ CHIẾN MÃ\'!D13,\'I.4. TIÊU CHÍ CHIẾN MÃ\'!D18,\'I.5. TIÊU CHÍ SƯ TỬ\'!D8,\'I.5. TIÊU CHÍ SƯ TỬ\'!D17,\'I.5. TIÊU CHÍ SƯ TỬ\'!D22,\'I.5. TIÊU CHÍ SƯ TỬ\'!D27,\'I.5. TIÊU CHÍ SƯ TỬ\'!D30,\'I.5. TIÊU CHÍ SƯ TỬ\'!D31,\'I.5. TIÊU CHÍ SƯ TỬ\'!D38,\'I.5. TIÊU CHÍ SƯ TỬ\'!D40),\"K\")'
            elif sheet_number == 1 and str(i) == '9':
                value= '=IFERROR(AVERAGE(\'I.2. THÂN THIỆN TỬ TẾ\'!D27,\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D17),\"K\")'
            elif sheet_number==2 and str(i)=='7':
                value='=IFERROR(AVERAGE(D8, D27), \"K\")'
            elif sheet_number == 2 and str(i) == '8':
                value='=IFERROR(AVERAGE(D9, D10, D16, D17, D18, D19, D20, D21, D22, D25, D26), \"K\")'
            elif sheet_number == 2 and str(i) == '10':
                value='=IFERROR(AVERAGE(D11:D15),\"K\")'
            elif sheet_number == 2 and str(i) == '22':
                value='=IFERROR(AVERAGE(D23:D24),\"K\")'
            elif sheet_number == 2 and str(i) == '27':
                value='=IFERROR(AVERAGE(D28:D34),\"K\")'
            elif sheet_number == 3 and str(i) == '7':
                value='=IFERROR(AVERAGE(D8,D9,D13,D16,D19,D20,D21),\"K\")'
            elif sheet_number == 3 and str(i) == '9':
                value='=IFERROR(AVERAGE(D10:D12),\"K\")'
            elif sheet_number == 3 and str(i) == '13':
                value='=IFERROR(AVERAGE(D14:D15),\"K\")'
            elif sheet_number == 3 and str(i) == '16':
                value='=IFERROR(AVERAGE(D17:D18),\"K\")'
            elif sheet_number == 4 and str(i) == '7':
                value='=IFERROR(AVERAGE(D8,D15,D21,D24,D29),\"K\")'
            elif sheet_number == 4 and str(i) == '8':
                value='=IFERROR(AVERAGE(D9,D13,D14),\"K\")'
            elif sheet_number == 4 and str(i) == '9':
                value='=IFERROR(AVERAGE(D10:D12),\"K\")'
            elif sheet_number == 4 and str(i) == '10':
                value='=\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D17'
            elif sheet_number == 4 and str(i) == '13':
                value='=\'I.2. THÂN THIỆN TỬ TẾ\'!D8'
            elif sheet_number == 4 and str(i) == '14':
                value='=\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D13'
            elif sheet_number == 4 and str(i) == '15':
                value='=IFERROR(AVERAGE(D16:D20),\"K\")'
            elif sheet_number == 4 and str(i) == '16':
                value='=\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D19'
            elif sheet_number == 4 and str(i) == '18':
                value='=IFERROR(AVERAGE(\'I.2. THÂN THIỆN TỬ TẾ\'!D26,\'I.2. THÂN THIỆN TỬ TẾ\'!D33),\"K\")'
            elif sheet_number == 4 and str(i) == '21':
                value='=IFERROR(AVERAGE(D22,D23),\"K\")'
            elif sheet_number == 4 and str(i) == '22':
                value='=IFERROR(AVERAGE(\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D9,\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D16),\"K\")'
            elif sheet_number == 4 and str(i) == '24':
                value="=IFERROR(AVERAGE(D25:D28),\"K\")"
            elif sheet_number == 5 and str(i) == '7':
                value='=IFERROR(AVERAGE(D8,D13,D18,D24,D32),\"K\")'
            elif sheet_number == 5 and str(i) == '13':
                value='=IFERROR(AVERAGE(D14:D17),\"K\")'
            elif sheet_number == 5 and str(i) == '18':
                value='=IFERROR(AVERAGE(D19:D23),\"K\")'
            elif sheet_number == 5 and str(i) == '24':
                value='=IFERROR(AVERAGE(D25:D31),\"K\")'
            elif sheet_number == 5 and str(i) == '32':
                value='=IFERROR(AVERAGE(D33:D41),\"K\")'
            else:
                unlock=True
            if unlock:
                sheet1.write("D" + str(i), value,
                             style_1_k_unlock if title == 1 else (style_2_k_unlock if title == 2 else (style_3_k_unlock if title == 3 else style_4_k_unlock)))
            else:
                sheet1.write("D" + str(i), value, style_1_k if title == 1 else (style_2_k if title == 2 else (style_3_k if title == 3 else style_4_k)))
        else:
            title = 1 if stt.count(".") <= 0 else 2
            sheet1.write("A" + str(i), stt, style_tt_2 if title == 1 else style_tt_4)
            sheet1.write("B" + str(i), str(search.question_name), style_2_unlock if title == 1 else style_4_unlock)
            sheet1.write("C" + str(i), (percentage if percentage else str("0")) ,
                         style_tt_2_percent if title == 1 else style_tt_4_percent)
            sheet1.write("D" + str(i), comment, style_tt_2_unlock)
            unlock=False

            if str(i) == '7':
                value = '=SUM((IF(E8=\"K\",0,E8)*C8),(IF(E9=\"K\",0,E9)*C9),(IF(E10=\"K\",0,E10)*C10),(IF(E11=\"K\",0,E11)*C11),(IF(E12=\"K\",0,E12)*C12))'
            elif str(i) == '13':
                value = '=SUM((IF(E14=\"K\",0,E14)*C14),(IF(E15=\"K\",0,E15)*C15),(IF(E16=\"K\",0,E16)*C16),(IF(E17=\"K\",0,E17)*C17),(IF(E18=\"K\",0,' \
                        'E18)*C18))'
            elif str(i) == '19':
                value = '=SUM((IF(E20=\"K\",0,E20)*C20),(IF(E21=\"K\",0,E21)*C21),(IF(E22=\"K\",0,E22)*C22),(IF(E23=\"K\",0,E23)*C23),(IF(E24=\"K\",0,' \
                        'E24)*C24))'
            elif str(i) == '25':
                value = '=C7*E7+C13*E13+C19*E19'
            else:
                unlock=True
            if unlock:
                sheet1.write("E" + str(i), value, style_tt_2_unlock if title == 1 else style_tt_4_unlock)
            else:
                sheet1.write("E" + str(i), value, style_tt_2 if title == 1 else style_tt_4)

    def generate_xlsx_report(self, workbook, data, objects):

        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('TỔNG HỢP'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)

        style_all = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter', 'border': 1})
        style_all_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter', 'border': 1,'locked':False})

        style_all_center = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'text_wrap': True})
        style_all_center_unlock = workbook.add_format(
            {'font_size': 11, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter', 'border': 1,
             'text_wrap': True,'locked':False})
        style_bold = workbook.add_format(
            {'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'border': 1,
             'align':'left','valign': 'vcenter','num_format': '#,##0.00'})
        style_bold_ct = workbook.add_format(
            {'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'border': 1,
             'align':'right','valign': 'vcenter','num_format': '#,##0.00','underline':True})
        style_bold_noboder = workbook.add_format(
            {'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'valign': 'vcenter'})
        style_bold_center_noborder = workbook.add_format(
            {'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True, 'align': 'center',
             'valign': 'vcenter'})
        style_bold_center = workbook.add_format(
            {'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True,
             'align': 'center',
             'valign': 'vcenter'})
        title_style_name_appraisal = workbook.add_format(
            {'bold': True, 'font_size': 12, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True})
        title_style_name_appraisal_italic = workbook.add_format(
            {'bold': True, 'font_size': 12, 'font_name': "Times New Roman", 'align': 'center', 'valign': 'vcenter',
             'text_wrap': True, 'italic':True})

        style_pink = workbook.add_format(
            {'bg_color': "#da9694", 'bold': True, 'font_size': 11, 'valign': 'vcenter', 'font_name': "Times New Roman",
             'text_wrap': True})
        style_blue = workbook.add_format(
            {'bg_color': "#8db4e2", 'bold': True, 'font_size': 11, 'font_name': "Times New Roman", 'align': 'center',
             'valign': 'vcenter', 'border': 1, 'text_wrap': True})
        style_red_bold_center = workbook.add_format(
            {'color': "red", 'bold': True, 'border': 1, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        style_red_bold_center_noborder = workbook.add_format(
            {'color': "red", 'bold': True, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        style_red_bold_underline = workbook.add_format(
            {'color': "red", 'border': 1,'bold': True, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'align': 'center', 'valign': 'vcenter','underline':True})
        style_red_bold_noborder = workbook.add_format(
            {'color': "red", 'bold': True, 'font_size': 11, 'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter'})
        style_red_bold = workbook.add_format(
            {'color': "red", 'border': 1, 'bold': True, 'font_size': 11, 'font_name': "Times New Roman",
             'align':'left','text_wrap': True, 'valign': 'vcenter','num_format': '#,##0.00'})
        style_red_bold_ct = workbook.add_format(
            {'color': "red", 'border': 1, 'bold': True, 'font_size': 11, 'font_name': "Times New Roman",
             'align':'right','text_wrap': True, 'valign': 'vcenter', 'num_format': '#,##0.00'})
        style_red_bold_bg_yellow = workbook.add_format(
            {'bg_color': "#ffff00",
             'color': "red",
             'border': 1,
             'bold': True,
             'font_size': 11,
             'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter',
             'align': 'left',
             'num_format': '#,##0.00'})
        style_red_bold_bg_yellow_ct = workbook.add_format(
            {'bg_color': "#ffff00",
             'color': "red",
             'border': 1,
             'bold': True,
             'font_size': 11,
             'font_name': "Times New Roman",
             'text_wrap': True, 'valign': 'vcenter',
             'align': 'right',
             'num_format': '#,##0.00'})

        style_red = workbook.add_format(
            {'color': "red", 'font_size': 11, 'font_name': "Times New Roman", 'text_wrap': True,
             'valign': 'vcenter'})


        sheet.freeze_panes(4, 0)
        sheet.set_row(3, 40)
        sheet.set_row(25, 33)
        sheet.set_row(18, 25)
        sheet.set_row(14, 28)
        sheet.set_row(13, 28)
        sheet.set_row(12, 30)
        sheet.set_row(32, 33)
        sheet.set_row(33, 21)
        sheet.set_row(34, 21)
        sheet.set_row(35, 33)
        sheet.set_row(36, 33)
        sheet.set_row(37, 21)
        sheet.set_column('A:A', 4)
        sheet.set_column('B:B', 33)
        sheet.set_column('C:C', 17)
        sheet.set_column('E:E', 18)
        sheet.set_column('D:D', 56)
        sheet.set_column('F:F', 16)
        sheet.set_column('I:I', 75)
        sheet.set_column('H:H', 15)
        company=self.env['res.company'].sudo().search([('id','=',3)])
        image_company = io.BytesIO(base64.b64decode(company.logo_web))
        sheet.insert_image('B1', "logocompany.png", {'image_data': image_company, 'x_scale': 0.75, 'y_scale': 0.75})
        sheet.merge_range('C2:E3', "BẢNG ĐÁNH GIÁ NHÂN SỰ STAFF PERFORMANCE EVALUATION", title_style_name_appraisal)
        sheet.write('B10', "Phần dành riêng cho thuyền viên: ", title_style_name_appraisal_italic)
        sheet.merge_range('C10:D10', "Nếu Anh/Chị cần IT Support import file excel vào hệ thống, vui lòng nhập mật khẩu. ", title_style_name_appraisal_italic)
        sheet.merge_range('E10:F10', "Mật khẩu … ", title_style_name_appraisal_italic)
        # sheet.merge_range('C3:E3', "STAFF PERFORMANCE EVALUATION", title_style_name_company)

        # note
        sheet.merge_range('H5:I5', "SƠ BỘ NỘI DUNG VÀ QUY TRÌNH ĐÁNH GIÁ", style_pink)
        sheet.merge_range('H6:I6', "Nội dung đánh giá", style_blue)
        sheet.merge_range('H7:H11', "I. SEACORP", style_bold)
        sheet.write('I7', "(I.1) CÓ MỐI QUAN HỆ TỐT", style_all)
        sheet.write('I8', "(I.2) THÂN THIỆN - TỬ TẾ", style_all)
        sheet.write('I9', "(I.3) CẦN MẪN - TRÁCH NHIỆM", style_all)
        sheet.write('I10', "(i.4) TIÊU CHÍ CHIẾN MÃ", style_all)
        sheet.write('I11',
                    "(I.5) TIÊU CHÍ SƯ TỬ  (Từ cấp Trưởng phòng/ Phó TP phụ trách phòng hoặc tương đương trở lên)",
                    style_all)
        sheet.write('H12', "I. KPIs", style_bold)
        sheet.write('I12', "Phần đánh giá kết quả hoàn thành công việc cho từng nhân sự (chi tiết tại Mục III).",
                    style_all)
        sheet.merge_range('H13:I13', "Quy trình tóm lược", style_blue)
        sheet.write('H14', "Bước 1", style_bold)
        sheet.write('I14',
                    "Người quản lý trực tiếp (QLTT) xây dựng và phân bổ tỉ trọng các chỉ tiêu KPI cho Nhân viên vào "
                    "đầu mỗi kỳ đánh giá nhân sự (ĐGNS).", style_all)
        sheet.write('H15', "Bước 2", style_bold)
        sheet.write('I15', "Nhân viên/QLTT/Cấp trên QLTT/Đồng nghiệp (nếu có chỉ định)/HĐĐG bắt đầu tiến hành đánh "
                           "giá đồng loạt và độc lập theo từng vai trò.", style_all)

        sheet.merge_range('H24:I24', "Công ty", style_blue)
        companys = self.env['res.company'].sudo().search([])
        row = 25
        for company in companys:
            sheet.write('H' + str(row), company.short_name, style_all)
            sheet.write('I' + str(row), company.name, style_all)
            row += 1
        sheet.merge_range('H18:I18', "CHÚ THÍCH", style_pink)
        sheet.merge_range('H19:I19', "Vai trò đánh giá", style_blue)
        sheet.write('H20', "1", style_all_center)
        sheet.write('I20', "Tự đánh giá", style_all)
        sheet.write('H21', "2", style_all_center)
        sheet.write('I21', "Quản lý trực tiếp (QLTT)", style_all)
        sheet.write('H23', "4", style_all_center)
        sheet.write('I23', "Đồng nghiệp", style_all)
        sheet.write('H22', "3", style_all_center)
        sheet.write('I22', "Cấp trên QLTT", style_all)
        '''HDDG Có Không'''
        sheet.write('H45', "Có", style_all_center)
        sheet.write('H46', "Không", style_all_center)
        sheet.data_validation('C12', {'validate': 'list', 'value': '=$H$45:$H$46'})

        # title file excel
        sheet.merge_range('A5:F5', 'I.   THÔNG TIN NHÂN SỰ', style_pink)
        sheet.merge_range("A11:F11", "II.   ĐỀ XUẤT ĐÁNH GIÁ TẠI HỘI ĐỒNG ĐÁNH GIÁ (HĐĐG)", style_pink)
        sheet.merge_range("A15:F15", "III.   ĐỀ XUẤT LƯƠNG -  THƯỞNG - CHỨC VỤ - THUYÊN CHUYỂN", style_pink)
        sheet.merge_range("A19:E19", "IV.   TỔNG ĐIỂM ĐÁNH GIÁ VÀ THÀNH TÍCH:", style_pink)

        # Nội Dung
        appraisal_role = "1"
        appraisal_role_name = "Tự đánh giá"
        name_gdg = "" if not objects.name else objects.name
        s_identification_id = str(objects.employee_multi_id.sudo().s_identification_id)
        de_xuat_dg_tai_hddg = "" if not objects.de_xuat_dg_tai_hddg_user else objects.de_xuat_dg_tai_hddg_user
        de_xuat_lydo = "" if not objects.de_xuat_lydo_user else objects.de_xuat_lydo_user
        dexuat_salary = "" if not objects.dexuat_salary_user else objects.dexuat_salary_user
        dexuat_chucvu = "" if not objects.dexuat_chucvu_user else objects.dexuat_chucvu_user
        dexuat_thuong = "" if not objects.dexuat_thuong_user else objects.dexuat_thuong_user
        dexuat_thuyenchuyen = "" if not objects.dexuat_thuyenchuyen_user else objects.dexuat_thuyenchuyen_user
        opinion = "" if not objects.user_opinion else objects.user_opinion
        for rec in objects:
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    appraisal_role = "4"
                    appraisal_role_name = "Đồng nghiệp"
                    name_gdg = emp.name.sudo().name
                    s_identification_id = str(emp.s_identification_id)
                    de_xuat_dg_tai_hddg = "" if not objects.de_xuat_dg_tai_hddg_colleague else objects.de_xuat_dg_tai_hddg_colleague
                    de_xuat_lydo = "" if not objects.de_xuat_lydo_colleague else objects.de_xuat_lydo_colleague
                    dexuat_salary = "" if not objects.dexuat_salary_colleague else objects.dexuat_salary_colleague
                    dexuat_chucvu = "" if not objects.dexuat_chucvu_colleague else objects.dexuat_chucvu_colleague
                    dexuat_thuong = "" if not objects.dexuat_thuong_colleague else objects.dexuat_thuong_colleague
                    dexuat_thuyenchuyen = "" if not objects.dexuat_thuyenchuyen_colleague else objects.dexuat_thuyenchuyen_colleague
                    opinion = "" if not objects.colleague_opinion else objects.colleague_opinion
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.smanager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    appraisal_role = "3"
                    appraisal_role_name = "Cấp trên QLTT"
                    s_identification_id = str(emp.s_identification_id)
                    name_gdg = emp.name.sudo().name
                    de_xuat_dg_tai_hddg = "" if not objects.de_xuat_dg_tai_hddg_smanager else objects.de_xuat_dg_tai_hddg_smanager
                    de_xuat_lydo = "" if not objects.de_xuat_lydo_smanager else objects.de_xuat_lydo_smanager
                    dexuat_salary = "" if not objects.dexuat_salary_smanager else objects.dexuat_salary_smanager
                    dexuat_chucvu = "" if not objects.dexuat_chucvu_smanager else objects.dexuat_chucvu_smanager
                    dexuat_thuong = "" if not objects.dexuat_thuong_smanager else objects.dexuat_thuong_smanager
                    dexuat_thuyenchuyen = "" if not objects.dexuat_thuyenchuyen_smanager else objects.dexuat_thuyenchuyen_smanager
                    opinion = "" if not objects.smanager_opinion else objects.smanager_opinion
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.manager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    appraisal_role = "2"
                    appraisal_role_name = "Quản lý trực tiếp (QLTT)"
                    s_identification_id = str(emp.s_identification_id)
                    name_gdg = emp.name.sudo().name
                    de_xuat_dg_tai_hddg = "" if not objects.de_xuat_dg_tai_hddg_manager else objects.de_xuat_dg_tai_hddg_manager
                    de_xuat_lydo = "" if not objects.de_xuat_lydo_manager else objects.de_xuat_lydo_manager
                    dexuat_salary = "" if not objects.dexuat_salary_manager else objects.dexuat_salary_manager
                    dexuat_chucvu = "" if not objects.dexuat_chucvu_manager else objects.dexuat_chucvu_manager
                    dexuat_thuong = "" if not objects.dexuat_thuong_manager else objects.dexuat_thuong_manager
                    dexuat_thuyenchuyen = "" if not objects.dexuat_thuyenchuyen_manager else objects.dexuat_thuyenchuyen_manager
                    opinion = "" if not objects.manager_opinion else objects.manager_opinion

        sheet.write('B6', "Công ty đánh giá:", style_all)

        sheet.write('C6', self.env.user.company_id.short_name, style_all_center_unlock)
        sheet.data_validation('C6', {'validate': 'list','value': '=$H$25:$H$43'})
        sheet.write('D6', '=VLOOKUP(C6,$H$25:$I$42,2,FALSE)', style_all_center)
        sheet.write('E6', "", style_all)
        sheet.write('F6', "", style_all)

        sheet.write('B7', "Người đánh giá:", style_all)
        sheet.write('C7', name_gdg, style_all_center_unlock)
        sheet.write('D7', "", style_all_center_unlock)
        sheet.write('E7', "SeaCode", style_all)
        sheet.write('F7', s_identification_id,style_all_unlock)
        sheet.write('B8', "Đánh giá cho nhân sự:", style_all)
        sheet.write('C8', objects.name, style_all_center)
        sheet.write('C8', name_gdg, style_all_center_unlock)
        sheet.write('D8', "", style_all_center_unlock)
        sheet.write('E8', "SeaCode", style_all)
        sheet.write('F8', objects.employee_multi_id.sudo().s_identification_id, style_all_unlock)

        sheet.write('B9', "Đánh giá với vai trò:", style_all)
        sheet.write('C9', appraisal_role, style_all_center_unlock)
        sheet.data_validation('C9', {'validate': 'list', 'value': '=$H$20:$H$23'})
        sheet.write('D9', '=VLOOKUP(C9,$H$20:$I$23,2,FALSE)', style_all_center)
        sheet.write('E9', "", style_all)
        sheet.write('F9', "", style_all)

        sheet.write('B10', "", style_all)
        sheet.write('C10', "", style_all_center)
        sheet.write('D10', "", style_all_center)
        sheet.write('E10', "", style_all)
        sheet.write('F10', "", style_all)

        sheet.write("A20", "TT", style_blue)
        sheet.merge_range("B20:D20", "TIÊU CHÍ ĐÁNH GIÁ", style_blue)
        sheet.write("E20", "NS", style_blue)
        for i in range(8):
            if i not in [6, 7]:
                prefix = "I"
            elif i == 7:
                prefix = "Ʃ"
            elif i == 6:
                prefix = "II"
            sheet.write("A" + str(i + 21), prefix + ("" if i == 7 else ".") + ("" if i in [0, 6, 7] else str(i)),
                        style_bold if i not in [6, 7] else style_red_bold if i == 6 else style_red_bold_bg_yellow)
            sheet.merge_range("B" + str(i + 21) + ":D" + str(i + 21),
                              str(self.env['hr.survey.summary'].sudo().search(
                                  [('prefix', '=', prefix + ("" if i in [0, 6, 7] else "." + str(i)))], limit=1).name),
                              style_bold if i not in [6, 7] else style_red_bold if i == 6 else style_red_bold_bg_yellow)
        sheet.write("E21", '=IFERROR(AVERAGE(E22:E26),"K")',style_red_bold_ct)
        excel_function="=IFERROR(" +"'"+ "I.1 CÓ MQH TỐT"+"'"+"!D7"+",\"K\")"

        sheet.write("E22", excel_function, style_bold_ct)
        sheet.write("E23", '=IFERROR(\'I.2. THÂN THIỆN TỬ TẾ\'!D7,\"K\")', style_bold_ct)
        sheet.write("E24", '=IFERROR(\'I.3. CẦN MẪN TRÁCH NHIỆM\'!D7,\"K\")', style_bold_ct)
        sheet.write("E25", '=IFERROR(\'I.4. TIÊU CHÍ CHIẾN MÃ\'!D7,\"K\")', style_bold_ct)
        sheet.write("E26", '=IFERROR(\'I.5. TIÊU CHÍ SƯ TỬ\'!D7,\"K\")', style_bold_ct)
        sheet.write("E27", '=\'II. KPIs\'!E25', style_red_bold_ct)
        sheet.write("E28", '=(IF(AND(E21>=4.5,E27>=4.5),"AA",IF(AND(E21>=4.5,E27>=3.5),"AB",IF(AND(E21>=4.5,E27>=2.5),"AC",IF(AND(E21>=4.5,E27>=1.5),"AD",'
                           'IF(AND(E21>=4.5,E27>0),"AE",(IF(AND(E21>=3.5,E27>=4.5),"BA",IF(AND(E21>=3.5,E27>=3.5),"BB",IF(AND(E21>=3.5,E27>=2.5),"BC",'
                           'IF(AND(E21>=3.5,E27>=1.5),"BD",IF(AND(E21>=3.5,E27>0),"BE",(IF(AND(E21>=2.5,E27>=4.5),"CA",IF(AND(E21>=2.5,E27>=3.5),"CB",'
                           'IF(AND(E21>=2.5,E27>=2.5),"CC",IF(AND(E21>=2.5,E27>=1.5),"CD",IF(AND(E21>=2.5,E27>0),"CE",(IF(AND(E21>=1.5,E27>=4.5),"DA",IF(AND(E21>=1.5,E27>=3.5),"DB",IF(AND(E21>=1.5,E27>=2.5),"DC",IF(AND(E21>=1.5,E27>=1.5),"DD",IF(AND(E21>=1.5,E27>0),"DE",(IF(AND(E21>0,E27>=4.5),"EA",IF(AND(E21>0,E27>=3.5),"EB",IF(AND(E21>0,E27>=2.5),"EC",IF(AND(E21>0,E27>=1.5),"ED",IF(AND(E21>0,E27>0),"EE","KĐG"))))))))))))))))))))))))))))))', style_red_bold_bg_yellow_ct)

        sheet.write('B12', "Đề xuất tại HĐĐG", style_all)
        sheet.merge_range('C12:F12', de_xuat_dg_tai_hddg, style_all_unlock)
        sheet.write('B13', "Lý do đề xuất", style_all)
        sheet.merge_range('C13:F13', de_xuat_lydo, style_all_unlock)

        sheet.write('B16', "Lương", style_bold_center)
        sheet.write('B17', dexuat_salary, style_all_unlock)
        sheet.write('C16', "Thưởng", style_bold_center)
        sheet.write('C17', dexuat_thuong, style_all_unlock)
        sheet.write('D16', "Chức vụ", style_bold_center)
        sheet.write('D17', dexuat_chucvu, style_all_unlock)
        sheet.write('E16', "Thuyên chuyển", style_bold_center)
        sheet.write('E17', dexuat_thuyenchuyen, style_all_unlock)
        sheet.write('F16', "Khác", style_bold_center)
        sheet.write('F17', opinion, style_all_unlock)

        # Ghi Chú
        sheet.write('B30', "GHI CHÚ:", style_red_bold_center_noborder)
        sheet.write('B31', "HƯỚNG DẪN ĐÁNH GIÁ", style_bold_center_noborder)
        sheet.write('B32', "THANG ĐIỂM", style_blue)
        sheet.merge_range('C32:E32', "DIỄN GIẢI", style_blue)
        thang_diem = 5
        for i in range(6):
            diem = (str(thang_diem) + " - " + str(thang_diem + 0.9)) if i != 0 else str(thang_diem)
            sheet.write('B' + str(i + 33), diem, style_red_bold_center)
            thang_diem -= 1

        sheet.merge_range('C33:E33', "Có đầy đủ và thực hành tốt 100%  tố chất/yêu cầu theo tiêu chí đánh giá."
                                     " Thể hiện được năng Có đầy đủ và thực hành tốt 100%  tố chất/yêu cầu theo"
                                     " tiêu chí đánh giá. Thể hiện được năng lực, chuyên môn, đạo đức vượt trội."
                          , style_all)
        sheet.merge_range('C34:E34',
                          "Có các tố chất và cố gắng phát huy, cố gắng thực hành đạt từ 80% trở lên các yêu cầu"
                          " theo tiêu chí đánh giá.", style_all)
        sheet.merge_range('C35:E35',
                          "Có cố gắng trau dồi các tố chất, thể hiện đạt yêu cầu từ 60% đến dưới 80% các yêu cầu"
                          " theo tiêu chí đánh giá. ", style_all)
        sheet.merge_range('C36:E36',
                          "Thể hiện đạt yêu cầu của nội dung tiêu chí đánh giá và thực hành các tố chất ở mức độ"
                          " đảm bảo hoàn thành công việc được giao (thể hiện đạt yêu cầu từ 40% đến dưới 60% các"
                          " nội dung tiêu chí đánh giá). ", style_all)
        sheet.merge_range('C37:E37',
                          "Không thể hiện được các tố chất và yêu cầu của các tiêu chí đánh giá.", style_all)
        sheet.merge_range('C38:E38',
                          "Có các hành vi, lời nói, biểu hiện đi ngược lại các yêu cầu, tố chất"
                          " và tiêu chí cần có để đánh giá ", style_all)

        sheet.write('B40', "HƯÓNG DẪN XẾP LOẠI", style_bold_center_noborder)
        sheet.merge_range('B41:B42', "XẾP LOẠI", style_blue)
        sheet.merge_range('C41:C42', "ĐIỂM TB CHUNG", style_blue)
        sheet.merge_range('D41:E41', "THÀNH TÍCH", style_blue)
        sheet.write('D42', "SEACORP", style_blue)
        sheet.write('E42', "KPIs", style_blue)

        DTBC = 5.0
        for i in range(5):
            so_tru = 0.5 if i == 0 else 1
            if i != 4:
                name = "Từ " + str(DTBC - so_tru) + " đến dưới " + str(DTBC)
            else:
                name = "Dưới " + str(DTBC) + " điểm"

            sheet.write('C' + str(i + 43), name, style_all)
            DTBC -= so_tru

        sheet.write('E43', "CHUYÊN NGHIỆP", style_all)
        sheet.write('D43', "TIÊU BIỂU", style_all)
        sheet.write('B43', "A", style_red_bold_center)
        sheet.write('E44', "HOÀN THÀNH TỐT", style_all)
        sheet.write('D44', "PHÁT HUY TỐT", style_all)
        sheet.write('B44', "B", style_red_bold_center)
        sheet.write('E45', "HOÀN THÀNH", style_all)
        sheet.write('D45', "PHÁT HUY", style_all)
        sheet.write('B45', "C", style_red_bold_center)
        sheet.write('E46', "KHÔNG HOÀN THÀNH", style_all)
        sheet.write('D46', "CHƯA PHÁT HUY", style_all)
        sheet.write('B46', "D", style_red_bold_center)
        sheet.write('E47', "KHÔNG PHÙ HỢP", style_all)
        sheet.write('D47', "KHÔNG PHÙ HỢP", style_all)
        sheet.write('B47', "E", style_red_bold_center)

        sheet.write('B49', "HƯƠNG DẪN TỔNG KẾT", style_bold_center_noborder)
        sheet.merge_range('B50:D50', "Tổng  kết đánh giá bao gồm 2 phần: Xếp loại (I) - "
                                     "SEACORP và  Xếp loại (II) - KPIs", style_bold_noboder)
        sheet.write('B51', "Tổng kết", style_blue)
        sheet.merge_range('C51:E51', "Ý nghĩa", style_blue)

        list_1 = ["AA", "AB", "BC", "CB", "EC"]
        tk = 52
        for i in list_1:
            sheet.write("B" + str(tk), str(i), style_red_bold_center)
            sheet.merge_range("C" + str(tk) + ":E" + str(tk),
                              "Văn hóa SeaCorp xếp loại " + str(i[0]) + " - Hiệu quả Công việc xếp loại " + str(i[1]),
                              style_all_center)
            tk += 1

        # sheet.write("A59", "Lưu ý:", style_red)
        sheet.merge_range("B59:D59", "Lưu ý: Tại các Ô có định dạng gạch dưới là đã cài công thức.", style_red)

        # 1======================================= #
        sheet1 = workbook.add_worksheet(_('I.1 CÓ MQH TỐT'))
        sheet1.set_landscape()
        sheet1.fit_to_pages(2, 0)
        sheet1.set_zoom(85)

        sheet1.freeze_panes(6, 0)
        sheet1.set_row(6, 25.5)
        sheet1.set_row(7, 49.5)
        sheet1.set_row(8, 49.5)

        sheet1.set_column('A:A', 6)
        sheet1.set_column('B:B', 45)
        sheet1.set_column('C:C', 40)

        sheet1.merge_range("A2:D2", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet1.merge_range("A3:B3", "I.   CHUYÊN NGHIỆP", style_red_bold_noborder)

        sheet1.merge_range("A4:A6", "TT", style_blue)
        sheet1.merge_range("B4:B6", "TIÊU CHÍ", style_blue)
        sheet1.merge_range("C4:D4", "ĐÁNH GIÁ", style_blue)
        sheet1.merge_range("C5:D5", "NHÂN SỰ", style_blue)
        sheet1.write("C6", "NHẬN XÉT", style_blue)
        sheet1.write("D6", "ĐIỂM", style_blue)

        for i in range(3):
            stt = "I." + str(i + 1) if i == 0 else "1." + str(i)
            self.write_excel_data(workbook, stt, sheet1, i + 7, objects,1)

        sheet1.write("A11", "Lưu ý:", style_red)
        sheet1.merge_range("B11:D11", "Tại các Ô có định dạng gạch dưới là đã cài công thức.", style_red_bold_noborder)

        # 2======================================= #
        sheet2 = workbook.add_worksheet(_('I.2. THÂN THIỆN TỬ TẾ'))
        sheet2.set_landscape()
        sheet2.fit_to_pages(2, 0)
        sheet2.set_zoom(85)

        sheet2.freeze_panes(6, 0)

        sheet2.set_column('A:A', 7)
        sheet2.set_column('B:B', 40)
        sheet2.set_column('C:C', 45)

        sheet2.merge_range("A2:D2", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet2.merge_range("A3:B3", "I.   CHUYÊN NGHIỆP", style_red_bold_noborder)

        sheet2.merge_range("A4:A6", "TT", style_blue)
        sheet2.merge_range("B4:B6", "TIÊU CHÍ", style_blue)
        sheet2.merge_range("C4:D4", "ĐÁNH GIÁ", style_blue)
        sheet2.merge_range("C5:D5", "NHÂN SỰ", style_blue)
        sheet2.write("C6", "NHẬN XÉT", style_blue)
        sheet2.write("D6", "ĐIỂM", style_blue)
        tt = 7
        for i in range(3):
            stt = "I." + str(i + 2) if i == 0 else "2." + str(i)
            self.write_excel_data(workbook, stt, sheet2, tt, objects,2)
            tt += 1
            if i != 0:
                for j in range(11):
                    stt1 = stt + "." + str(j + 1)
                    self.write_excel_data(workbook, stt1, sheet2, tt, objects,2)
                    tt += 1
                    if i == 1:
                        if j == 1 or j == 8:
                            for m in range(5):
                                if m == 2 and j == 8:
                                    break
                                else:
                                    stt2 = stt1 + "." + str(m + 1)
                                    self.write_excel_data(workbook, stt2, sheet2, tt, objects,2)
                                    tt += 1
                    elif i == 2 and j == 6:
                        break
                    # if j == 8:
                    #     for m in range(2):
                    #         stt2 = stt1 + "." + str(m+1)
                    #         self.write_excel_data(stt2, sheet2, tt, object)
                    #         tt += 1
            # if i == 2:
            #     for j in range(7):
            #         stt1 = stt + "." + str(j + 1)
            #         self.write_excel_data(stt1, sheet2, tt, object)
            #         tt += 1

        sheet2.write("A" + str(tt + 1), "Lưu ý:", style_red)
        sheet2.merge_range("B" + str(tt + 1) + ":D" + str(tt + 1),
                           "Tại các Ô có định dạng gạch dưới là đã cài công thức.", style_red_bold_noborder)
        # sheet2.write("B" + str(tt + 2), 'Nếu Cấp trên TT và Hội đồng ĐGNS không đánh giá (ghi nhận "K") => KĐG')

        # 3======================================= #
        sheet3 = workbook.add_worksheet(_('I.3. CẦN MẪN TRÁCH NHIỆM'))
        sheet3.set_landscape()
        sheet3.fit_to_pages(2, 0)
        sheet3.set_zoom(85)

        sheet3.freeze_panes(6, 0)
        sheet3.set_row(6, 25.5)

        sheet3.set_column('A:A', 7)
        sheet3.set_column('B:B', 40)
        sheet3.set_column('C:C', 45)

        sheet3.merge_range("A2:D2", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet3.merge_range("A3:B3", "I.   CHUYÊN NGHIỆP", style_red_bold_noborder)

        sheet3.merge_range("A4:A6", "TT", style_blue)
        sheet3.merge_range("B4:B6", "TIÊU CHÍ", style_blue)
        sheet3.merge_range("C4:D4", "ĐÁNH GIÁ", style_blue)
        sheet3.merge_range("C5:D5", "NHÂN SỰ", style_blue)
        sheet3.write("C6", "NHẬN XÉT", style_blue)
        sheet3.write("D6", "ĐIỂM", style_blue)
        tt = 7
        for i in range(8):
            stt = "I." + str(i + 3) if i == 0 else "3." + str(i)
            if i == 3:
                stt += "."
            self.write_excel_data(workbook, stt, sheet3, tt, objects,3)
            tt += 1
            if i == 3:
                stt = "3.3"
            if i == 2 or i == 3 or i == 4:
                for j in range(3):
                    if j == 2:
                        if i == 3 or i == 4:
                            break
                    stt1 = stt + "." + str(j + 1)
                    self.write_excel_data(workbook, stt1, sheet3, tt, objects,3)
                    tt += 1

        sheet3.write("A" + str(tt + 1), "Lưu ý:", style_red)
        sheet3.merge_range("B" + str(tt + 1) + ":D" + str(tt + 1),
                           "Tại các Ô có định dạng gạch dưới là đã "
                           "cài công thức.",
                           style_red_bold_noborder)
        # sheet3.write("B" + str(tt + 2), 'Nếu Cấp trên TT và Hội đồng ĐGNS không đánh giá (ghi nhận "K") => KĐG')

        # 4======================================= #
        sheet4 = workbook.add_worksheet(_('I.4. TIÊU CHÍ CHIẾN MÃ'))
        sheet4.set_landscape()
        sheet4.fit_to_pages(2, 0)
        sheet4.set_zoom(85)

        sheet4.freeze_panes(6, 0)
        sheet4.set_row(6, 25.5)

        sheet4.set_column('A:A', 7)
        sheet4.set_column('B:B', 40)
        sheet4.set_column('C:C', 45)

        sheet4.merge_range("A2:D2", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet4.merge_range("A3:B3", "I.   CHUYÊN NGHIỆP", style_red_bold_noborder)

        sheet4.merge_range("A4:A6", "TT", style_blue)
        sheet4.merge_range("B4:B6", "TIÊU CHÍ", style_blue)
        sheet4.merge_range("C4:D4", "ĐÁNH GIÁ", style_blue)
        sheet4.merge_range("C5:D5", "NHÂN SỰ", style_blue)
        sheet4.write("C6", "NHẬN XÉT", style_blue)
        sheet4.write("D6", "ĐIỂM", style_blue)
        tt = 7
        for i in range(6):
            stt = "I." + str(i + 4) if i == 0 else "4." + str(i)
            self.write_excel_data(workbook, stt, sheet4, tt, objects,4)
            tt += 1
            if i != 5 and i != 0:
                for j in range(5):
                    stt1 = stt + "." + str(j + 1)
                    self.write_excel_data(workbook, stt1, sheet4, tt, objects,4)
                    tt += 1
                    if j == 0 and i == 1:
                        for m in range(3):
                            stt2 = stt1 + "." + str(m + 1)
                            self.write_excel_data(workbook, stt2, sheet4, tt, objects,4)
                            tt += 1
                    if j == 2 and i == 1 or j == 1 and i == 3 or j == 3 and i == 4:
                        break

        sheet4.write("A" + str(tt + 1), "Lưu ý:", style_red)
        sheet4.merge_range("B" + str(tt + 1) + ":D" + str(tt + 1),
                           "Tại các Ô có định dạng gạch dưới là đã cài công thức.",
                           style_red_bold_noborder)
        # sheet4.write("B" + str(tt + 2), 'Nếu Cấp trên TT và Hội đồng ĐGNS không đánh giá (ghi nhận "K") => KĐG')


            # 5======================================= #
        sheet5 = workbook.add_worksheet(_('I.5. TIÊU CHÍ SƯ TỬ'))
        sheet5.set_landscape()
        sheet5.fit_to_pages(2, 0)
        sheet5.set_zoom(85)

        sheet5.freeze_panes(6, 0)
        sheet5.set_row(6, 25.5)
        sheet5.set_row(2, 42)
        sheet5.merge_range('A3:D3', 'Tiêu chí này dành riêng cho từ Cấp Trưởng phòng và Phó phòng Phụ trách phòng '
                                    '(hoặc tương đương) trở lên. Các nhân sự còn lại không đánh giá (thống nhất ghi'
                                    ' nhận "K")', style_red_bold_center_noborder)

        sheet5.set_column('A:A', 7)
        sheet5.set_column('B:B', 40)
        sheet5.set_column('C:C', 45)

        sheet5.merge_range("A1:D1", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet5.merge_range("A2:B2", "I.   CHUYÊN NGHIỆP", style_red_bold_noborder)

        sheet5.merge_range("A4:A6", "TT", style_blue)
        sheet5.merge_range("B4:B6", "TIÊU CHÍ", style_blue)
        sheet5.merge_range("C4:D4", "ĐÁNH GIÁ", style_blue)
        sheet5.merge_range("C5:D5", "NHÂN SỰ", style_blue)
        sheet5.write("C6", "NHẬN XÉT", style_blue)
        sheet5.write("D6", "ĐIỂM", style_blue)
        tt = 7
        for i in range(6):
            stt = "I." + str(i + 5) if i == 0 else "5." + str(i)
            self.write_excel_data(workbook, stt, sheet5, tt, objects,5)
            tt += 1
            if i != 0:
                for j in range(9):
                    stt1 = stt + "." + str(j + 1)
                    self.write_excel_data(workbook, stt1, sheet5, tt, objects,5)
                    tt += 1
                    if j == 3 and i == 1 or j == 3 and i == 2 or j == 4 and i == 3 or j == 6 and i == 4:
                        break

        sheet5.write("A" + str(tt + 1), "Lưu ý:", style_red)
        sheet5.merge_range("B" + str(tt + 1) + ":D" + str(tt + 1),
                           "Tại các Ô có định dạng gạch dưới là đã cài công thức.", style_red_bold_noborder)
        # sheet5.write("B" + str(tt + 2), 'Nếu Cấp trên TT và Hội đồng ĐGNS không đánh giá (ghi nhận "K") => KĐG')
        # 6======================================= #
        sheet6 = workbook.add_worksheet(_('II. KPIs'))
        sheet6.set_landscape()
        sheet6.fit_to_pages(2, 0)
        sheet6.set_zoom(85)

        # sheet6.freeze_panes(5, 0)
        sheet6.set_row(1, 25)
        sheet6.set_row(2, 25)
        sheet6.set_row(3, 60)
        sheet6.set_row(4, 50)
        sheet6.set_row(5, 50)
        sheet6.set_row(7, 30)

        sheet6.set_column('A:A', 6)
        sheet6.set_column('B:B', 60)
        sheet6.set_column('C:C', 9)
        sheet6.set_column('D:D', 40)
        sheet6.set_column('E:E', 15)
        sheet6.set_column('G:G', 33)
        sheet6.set_column('H:H', 130)

        sheet6.merge_range("A2:D2", "NỘI DUNG ĐÁNH GIÁ:", title_style_name_appraisal)
        sheet6.merge_range("A3:B3", "II.   HIỆU QUẢ (KẾT QUẢ /MỨC ĐỘ HOÀN THÀNH CÔNG VIỆC)", style_red_bold_noborder)

        sheet6.merge_range("A4:A5", "TT", style_blue)
        sheet6.merge_range("B4:B5", "CÔNG VIỆC/TIÊU CHÍ (Các công việc được phân công"
                                    " và/hoặc các tiêu chí KPIs được giao)", style_blue)
        sheet6.merge_range("C4:C5", "Tỷ trọng tổng hợp", style_blue)
        sheet6.merge_range("D4:E4", "NHÂN SỰ", style_blue)
        sheet6.write("D5", "NHẬN XÉT", style_blue)
        sheet6.write("E5", "ĐIỂM", style_blue)

        sheet6.write("A6", "(1)", style_all_center)
        sheet6.write("B6", "(2)", style_all_center)
        sheet6.write("C6", "(3)", style_all_center)
        sheet6.write("D6", "", style_all_center)
        sheet6.write("E6", "", style_all_center)

        tt = 7
        for i in range(3):
            stt = str(i + 1)
            self.write_excel_data(workbook, stt, sheet6, tt, objects,6, True)
            tt += 1
            for j in range(5):
                stt1 = stt + "." + str(j + 1)
                self.write_excel_data(workbook, stt1, sheet6, tt, objects,6, True)
                tt += 1
        sheet6.merge_range('A' + str(tt) + ':B' + str(tt), "Tổng điểm đánh giá thực hiện công việc",
                           style_bold_center)
        sheet6.write('C' + str(tt), '=SUM(C19,C13,C7)*100',style_red_bold_underline)
        sheet6.write('D' + str(tt), '',style_red_bold_underline)
        sheet6.write('E' + str(tt), '==C7*E7+C13*E13+C19*E19',style_red_bold_underline)

        sheet6.write("A" + str(tt + 2), "Lưu ý:", style_red)
        sheet6.merge_range("B" + str(tt + 2) + ":D" + str(tt + 2),
                           "Tại các Ô có định dạng gạch dưới là đã cài công thức.",
                           style_red_bold_noborder)
        # sheet6.write("B" + str(tt + 2), 'Nếu Cấp trên TT và Hội đồng ĐGNS không đánh giá (ghi nhận "K") => KĐG')
        # note KPIs
        sheet6.merge_range('G2:H2', "CÁCH NHẬP NỘI DUNG CHO CÁC CÔNG VIỆC/ TIÊU CHÍ DÀNH CHO QLTT",
                           style_red_bold_noborder)
        sheet6.merge_range('G10:H10', "QUY ƯỚC VỀ CÁCH TÍNH ĐIỂM KẾT QUẢ THỰC HIỆN",
                           style_red_bold_noborder)

        sheet6.write('G3', "CÔNG VIỆC/ TIÊU CHÍ", style_blue)
        sheet6.write('H3', "CHÚ THÍCH", style_blue)
        sheet6.write('G11', "ĐIỂM", style_blue)
        sheet6.write('H11', "KẾT QUẢ THỰC HIỆN", style_blue)

        sheet6.write('G4', "1. Mục tiêu cá nhân (Gắn liền với KPIs của Đơn vị) (nếu có)", style_all)
        sheet6.write('G5', "2. Các công việc thường xuyên (theo MTCV) (bắt buộc)", style_all)
        sheet6.write('G6', "3. Các công việc đột xuất/ được phân công khác (nếu có)", style_all)
        sheet6.write('H4', "QLTT điền tối đa 05 mục tiêu cho kỳ ĐGNS, tỉ trọng của mỗi mục tiêu ít hay "
                           "nhiều sẽ căn cứ vào mức độ quan trọng của từng mục tiêu, mục tiêu nào quan trọng "
                           "hơn sẽ chiếm tỉ trọng cao hơn sao cho tổng tỉ trọng của các mục tiêu là đủ 100%.",
                     style_all)
        sheet6.write('H5', "Các công việc thường xuyên (theo Mô tả và phân công công việc): QLTT điền tối đa "
                           "05 công việc thường xuyên theo mô tả công việc của Nhân viên, tỉ trọng của mỗi công "
                           "việc ít hay nhiều sẽ căn cứ vào mức độ quan trọng của từng công việc, công việc nào quan "
                           "trọng hơn sẽ chiếm tỉ trọng cao hơn, sao cho tổng tỉ trọng của các công việc là đủ 100%.",
                     style_all)
        sheet6.write('H6', "Các công việc đột xuất /được phân công khác: Trong suốt kỳ ĐGNS, QLTT điền tối đa 05 công "
                           "việc phát sinh đột xuất của Nhân viên, tỉ trọng của mỗi công việc ít hay nhiều sẽ căn cứ "
                           "vào mức độ quan trọng của từng công việc, công việc nào quan trọng hơn sẽ chiếm tỉ trọng"
                           " cao hơn, sao cho tổng tỉ trọng của các công việc là đủ 100%. Lưu ý: phần này có thể điều "
                           "chỉnh cho phù hợp thực tế trong suốt kỳ đánh giá.", style_all)

        sheet6.merge_range('G7:H8', "Ghi chú: Phần 2 là bắt buộc phải thực hiện. VD: Nếu không có Phần 1 thì chỉ cần "
                                    "điền nội dung các mục tiêu tại Phần 2 và Phần 3 (VD: Phần 2: 80%, Phần 3: 20%); "
                                    "Nếu không có Phần 1 và Phần 3 thì Phần 2: 100%).", style_bold)

        diem = 5.0
        phantram = 100
        for i in range(6):
            sott = i + 12

            diemm = str(diem) if i == 0 else str(diem) + " - " + str(diem + 0.9)
            sheet6.write('G' + str(sott), diemm, style_red_bold_center)
            diem -= 1
            if i == 0:
                sophantram = "Đạt từ " + str(phantram) + "% " + "KPIs (tiêu chí/công việc) trở lên"
            elif i == 5:
                sophantram = "Đạt dưới " + str(phantram) + "% KPIs (tiêu chí/công việc)"
            else:
                sophantram = "Đạt từ " + str(phantram - 20) + "% - dưới " + str(
                    phantram) + "% KPIs (tiêu chí/công việc)"
            if i != 0: phantram -= 20
            sheet6.write('H' + str(sott), sophantram, style_all)
        sheet.protect('123')
        sheet1.protect('123')
        sheet2.protect('123')
        sheet3.protect('123')
        sheet4.protect('123')
        sheet5.protect('123')
        sheet6.protect('123')
