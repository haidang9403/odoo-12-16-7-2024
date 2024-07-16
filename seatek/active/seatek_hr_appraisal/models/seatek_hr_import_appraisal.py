import binascii
import tempfile

import xlrd
from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.tools import pycompat


# class SurveyImportExcelTemplateLine(models.TransientModel):
#     _name = 'survey.import.excel.template.line'
#     _description = 'KPIS Template Lines'
#     _order = 'line_order'
#
#     name = fields.Char(string='Name')
#     prefix = fields.Char(string='Prefix')
#     question_name = fields.Char(string='Question Name')
#     percentage = fields.Float(string='Percentage')
#     survey_import_excel_template_id = fields.Many2one('survey.import.excel.template')
#     line_order = fields.Integer(string='Line Order')
#     summary_level = fields.Integer(string="Level")
#     is_parent = fields.Boolean(string='Is Parent', default=False)


class ImportAppraisalKPIExcelTemplate(models.TransientModel):
    _name = 'import.excel.appraisal'

    template_path = fields.Binary(string='Path')

    # def compute_appraisal_user(self):
    #     print("ne")
    #     for rec in self:
    #         name = "Khanh"
    #         if rec.template_path:
    #             fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    #             fp.write(binascii.a2b_base64(rec.template_path))
    #             fp.seek(0)
    #             book = xlrd.open_workbook(fp.name)
    #             if book:
    #                 stt_sheet = 0
    #                 for sheet in book.sheets():
    #                     if stt_sheet == 0:
    #                         row_no = 0
    #                         for row in pycompat.imap(sheet.row, range(sheet.nrows)):
    #                             if row_no == 8:
    #                                 company = self.env['res.company'].sudo().search(
    #                                     [('short_name', '=', row[2].value.upper())])
    #                                 if company:
    #                                     employee = self.env['hr.employee.multi.company'].sudo().search(
    #                                         [('s_identification_id', '=', row[5].value),
    #                                          ('company_id', '=', company.id)])
    #                                 if employee:
    #                                     name = employee.name.name
    #                             row_no += 1
    #                         break
    #                     stt_sheet += 1
    #         rec.appraisal_user = name
    #
    # appraisal_user = fields.Char(string='Appraisal User', compute='compute_appraisal_user')
    name = fields.Char(string='Name')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')

    user_input_id = fields.Many2one('hr.survey.user.input', string='User Input ID')



    user_id = fields.Many2one('res.users', string='User')

    @api.onchange('template_path')
    def _onchange_template_path(self):
        try:
            if self.template_path:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.template_path))
                fp.seek(0)
                book = xlrd.open_workbook(fp.name)

                if book:
                    stt_sheet = 0
                    user_input_id = False
                    message = 'STT lỗi hoặc không tìm thấy người được đánh giá và điểm phải là số hoặc K'
                    for sheet in book.sheets():
                        if stt_sheet == 0:
                            row_no = 0
                            for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                                if row_no == 5:
                                    short_name = str(row[2].value)
                                if row_no == 7:
                                    s_identification_id = str(row[5].value)
                                if row_no == 8:
                                    try:
                                        role = str(row[2].value)
                                        company = self.env['res.company'].sudo().search(
                                            [('short_name', '=', short_name.upper())])
                                        if company:

                                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                                [('s_identification_id', '=', s_identification_id.upper()),
                                                 ('company_id', '=', company.id)])
                                            if employee:
                                                user_input = self.env['hr.survey.user.input'].sudo().search(
                                                    [('company_id', '=', company.id),
                                                     ('employee_multi_id', '=', employee.id),
                                                     ('open_state', '=', True)])
                                                if user_input:

                                                    if str(role)=='1' and user_input.user_open_state==False:
                                                        message = 'Bài đánh giá đã đóng.'
                                                        raise UserError(message)
                                                    elif str(role)=='2' and user_input.manager_open_state==False:
                                                        message = 'Bài đánh giá đã đóng.'
                                                        raise UserError(message)
                                                    elif str(role)=='3' and user_input.smanager_open_state==False:
                                                        message = 'Bài đánh giá đã đóng.'
                                                        raise UserError(message)
                                                    elif str(role)=='4' and user_input.colleague_open_state==False:
                                                        message = 'Bài đánh giá đã đóng.'
                                                        raise UserError(message)
                                                    user_input_id = user_input.id
                                                else:
                                                    message = 'Không tìm thấy dữ liệu người dùng'
                                                    raise UserError(message)
                                            else:
                                                message='Không tồn tại mã SeaCode'
                                                raise UserError(message)
                                        else:
                                            message = 'Không tồn tại mã SeaCode!'
                                            raise UserError(message)
                                    except Exception as e:
                                        if message:
                                            error_message=message
                                        else:
                                            error_message = e
                                        raise UserError(e)
                                elif row_no == 9:
                                    try:
                                        role = str(row[2].value)
                                    except:
                                        raise UserError('Chức vụ phải là một trong các ký tự (NS, QLTT, CTQLTT)')
                                row_no += 1
                        else:
                            row_no = 0
                            composite_density_all = False
                            composite_density_all_1 = False
                            composite_density_all_2 = False
                            composite_density_all_3 = False
                            for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                                if row_no >= 6:
                                    if row_no > 8 and stt_sheet == 1 or row_no > 33 and stt_sheet == 2 or row_no > 20 \
                                            and stt_sheet == 3 or row_no > 28 and stt_sheet == 4 or row_no > 40 and \
                                            stt_sheet == 5 or row_no > 23 and stt_sheet == 6:
                                        break
                                    else:
                                        try:
                                            if stt_sheet == 6:
                                                composite_density = float(row[2].value) * 100
                                                if row_no == 6 or row_no == 12 or row_no == 18:
                                                    composite_density_all += composite_density
                                                elif 6 < row_no < 12:
                                                    composite_density_all_1 += composite_density
                                                elif 12 < row_no < 18:
                                                    composite_density_all_2 += composite_density
                                                elif 18 < row_no < 24:
                                                    composite_density_all_3 += composite_density

                                                if composite_density > 0 and len(str(row[1].value)) == 0:
                                                    message = 'Khi tỷ trọng lớn hơn 0% thì CÔNG VIỆC/TIÊU CHÍ không được để trống'
                                                    raise UserError(message)

                                                check_score = str(row[4].value)
                                                if check_score.upper() != "K" :
                                                    check_score = float(check_score)
                                                    if check_score > 5 or check_score <0:

                                                        message='Điểm nhập phải lớn 0 và nhỏ hơn 5'
                                                        raise UserError(message)
                                                prefix = str(row[0].value)
                                                search = self.env['hr.survey.user.input.line'].sudo().search(
                                                    [('user_input_id', '=', user_input_id), ('prefix', '=', prefix),
                                                     ('enable_edit_percentage', '=', True)])
                                            else:
                                                check_score = str(row[3].value)
                                                if check_score.upper() != "K":
                                                    check_score = float(check_score)
                                                    if check_score > 5 or check_score <0:
                                                        message='Điểm nhập phải lớn 0 và nhỏ hơn 5'

                                                        raise UserError(message)
                                                if row_no == 6:
                                                    prefix = "I." + str(row[0].value)
                                                else:
                                                    prefix = str(row[0].value)

                                                search = self.env['hr.survey.user.input.line'].sudo().search(
                                                    [('user_input_id', '=', user_input_id), ('prefix', '=', prefix),
                                                     ('enable_edit_percentage', '=', False)])
                                        except:
                                            raise UserError(message)
                                row_no += 1
                            if stt_sheet == 6:
                                if (composite_density_all>0 and composite_density_all != 100 )or (composite_density_all_1>0 and composite_density_all_1 != 100) or \
                                        (composite_density_all_2>0 and composite_density_all_2 != 100) or (composite_density_all_3>0 and  composite_density_all_3 != 100):
                                    message = 'Tổng điểm đánh giá thực hiện công việc phải là 100%'
                                    raise UserError(message)
                        stt_sheet += 1

        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

    def import_appraisal_excel_action(self):
        try:
            if self.template_path:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.template_path))
                fp.seek(0)
                book = xlrd.open_workbook(fp.name)
                user_input=''
                if book:
                    list_value = {}
                    value = []
                    company=False
                    stt_sheet = 0
                    user_input_id = False
                    de_xuat_dg_tai_hddg=False
                    de_xuat_lydo=False
                    dexuat_salary=False
                    dexuat_thuong=False
                    dexuat_chucvu=False
                    dexuat_thuyenchuyen=False
                    user_opinion=False
                    role_value = False
                    role_comment = False
                    user_id=False
                    user_manager_id=False
                    user_smanager_id=False
                    user_colleague_id=False
                    user_colleague2_id=False
                    user_colleague3_id=False
                    is_manager=False
                    is_colleague=False
                    colleague_num=0
                    message=''
                    s_identification_id=False
                    nguoi_danh_gia_s_identification_id=False
                    dexuat_data={}
                    result=False
                    for sheet in book.sheets():
                        if stt_sheet == 0:
                            row_no = 0
                            for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                                if row_no==5:
                                    short_name = str(row[2].value)
                                if row_no == 6:
                                    nguoi_danh_gia_s_identification_id=str(row[5].value)
                                if row_no == 7:
                                    try:
                                        s_identification_id = str(row[5].value)
                                        company = self.env['res.company'].sudo().search(
                                            [('short_name', '=', short_name.upper())])
                                        if company:
                                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                                [('s_identification_id', '=', s_identification_id.upper()),
                                                 ('company_id', '=', company.id)])
                                            if employee:
                                                user_input = self.env['hr.survey.user.input'].sudo().search(
                                                    [('company_id', '=', company.id),
                                                     ('employee_multi_id', '=', employee.id),
                                                     ('open_state', '=', True)])
                                                is_manager=employee.manager

                                                if user_input:

                                                    user_input_id = user_input.id

                                                    if user_input.user_id:
                                                        user_id = user_input.user_id.id
                                                    if user_input.user_manager_id:
                                                        user_manager_id = user_input.user_manager_id.id
                                                    if user_input.user_smanager_id:
                                                        user_smanager_id = user_input.user_smanager_id.id
                                                    if user_input.user_colleague_id and user_input.user_colleague_id.id == self.env.user.id:
                                                        user_colleague_id = user_input.user_colleague_id.id
                                                        colleague_num=1
                                                    if user_input.user_colleague2_id and user_input.user_colleague2_id.id == self.env.user.id:
                                                        user_colleague_id = user_input.user_colleague2_id.id
                                                        colleague_num = 2
                                                    if user_input.user_colleague3_id and user_input.user_colleague3_id.id == self.env.user.id:
                                                        user_colleague_id = user_input.user_colleague3_id.id
                                                        colleague_num = 3
                                                else:
                                                    message = 'Không tìm thấy dữ liệu người dùng.'
                                                    raise UserError(message)
                                            else:
                                                message='Mã SeaCode chưa đúng.'
                                                raise UserError(message)
                                        else:
                                            raise UserError(message)
                                    except:
                                        raise UserError(message)
                                elif row_no == 8:
                                    message='Chức vụ phải là một trong các ký tự (NS, QLTT, CTQLTT)'
                                    try:
                                        role = str(row[2].value)
                                        if role.upper() == "1":
                                            de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_user'
                                            de_xuat_lydo = 'de_xuat_lydo_user'
                                            dexuat_salary = 'dexuat_salary_user'
                                            dexuat_thuong = 'dexuat_thuong_user'
                                            dexuat_chucvu = 'dexuat_chucvu_user'
                                            dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_user'
                                            user_opinion = 'user_opinion'
                                            role_value = 'value'
                                            role_comment = 'user_comment'

                                            if user_id:
                                                if self.env.user.id != user_id:
                                                    message = 'Tài khoản đăng nhập không liên kết với nhân viên có mã SC_Code: ' +str(s_identification_id)
                                                    raise UserError(message)
                                            else:
                                                message = 'Tài khoản đăng nhập không liên kết với nhân viên có mã SC_Code: ' + str(s_identification_id)
                                                raise UserError(message)

                                        elif role.upper() == "2":
                                            de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_manager'
                                            de_xuat_lydo = 'de_xuat_lydo_manager'
                                            dexuat_salary = 'dexuat_salary_manager'
                                            dexuat_thuong = 'dexuat_thuong_manager'
                                            dexuat_chucvu = 'dexuat_chucvu_manager'
                                            dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_manager'
                                            user_opinion = 'manager_opinion'
                                            role_value = 'value_manager'
                                            role_comment = 'manager_comment'
                                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                                [('s_identification_id', '=', nguoi_danh_gia_s_identification_id.upper()),
                                                 ('company_id', '=', company.id)])
                                            if user_manager_id:
                                                if self.env.user.id!=user_manager_id:
                                                    message = 'Tài khoản đăng nhập không phải QLTT'
                                                    raise UserError(message)
                                                if employee.user_id.id!=self.env.user.id:
                                                    message = 'SC_CODE: ' +nguoi_danh_gia_s_identification_id+' không phải QLTT'
                                                    raise UserError(message)

                                            else:
                                                message = 'Tài khoản đăng nhập không phải QLTT'
                                                raise UserError(message)


                                        elif role.upper() == "3":
                                            de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_smanager'
                                            de_xuat_lydo = 'de_xuat_lydo_smanager'
                                            dexuat_salary = 'dexuat_salary_smanager'
                                            dexuat_thuong = 'dexuat_thuong_smanager'
                                            dexuat_chucvu = 'dexuat_chucvu_smanager'
                                            dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_smanager'
                                            user_opinion = 'smanager_opinion'
                                            role_value = 'value_smanager'
                                            role_comment = 'smanager_comment'
                                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                                [('s_identification_id', '=', nguoi_danh_gia_s_identification_id.upper()),
                                                 ('company_id', '=', company.id)])
                                            if user_smanager_id:
                                                if self.env.user.id!=user_smanager_id:
                                                    message='Tài khoản đăng nhập không phải CẤP TRÊN QLTT'
                                                    raise UserError(message)
                                                if employee.user_id.id!=self.env.user.id:
                                                    message = 'SC_CODE: ' +nguoi_danh_gia_s_identification_id+' không phải CẤP TRÊN QLTT'
                                                    raise UserError(message)
                                            else:
                                                message='Tài khoản đăng nhập không phải CẤP TRÊN QLTT'
                                                raise UserError(message)
                                        elif role.upper() == "4":
                                            is_colleague=True
                                            if colleague_num==1:
                                                de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_colleague'
                                                de_xuat_lydo = 'de_xuat_lydo_colleague'
                                                dexuat_salary = 'dexuat_salary_colleague'
                                                dexuat_thuong = 'dexuat_thuong_colleague'
                                                dexuat_chucvu = 'dexuat_chucvu_colleague'
                                                dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_colleague'
                                                user_opinion = 'colleague_opinion'
                                                role_value = 'value_colleague'
                                                role_comment = 'colleague_comment'
                                            elif colleague_num==2:
                                                de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_colleague2'
                                                de_xuat_lydo = 'de_xuat_lydo_colleague2'
                                                dexuat_salary = 'dexuat_salary_colleague2'
                                                dexuat_thuong = 'dexuat_thuong_colleague2'
                                                dexuat_chucvu = 'dexuat_chucvu_colleague2'
                                                dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_colleague2'
                                                user_opinion = 'colleague2_opinion'
                                                role_value = 'value_colleague2'
                                                role_comment = 'colleague2_comment'
                                            elif colleague_num==3:
                                                de_xuat_dg_tai_hddg = 'de_xuat_dg_tai_hddg_colleague3'
                                                de_xuat_lydo = 'de_xuat_lydo_colleague3'
                                                dexuat_salary = 'dexuat_salary_colleague3'
                                                dexuat_thuong = 'dexuat_thuong_colleague3'
                                                dexuat_chucvu = 'dexuat_chucvu_colleague3'
                                                dexuat_thuyenchuyen = 'dexuat_thuyenchuyen_colleague3'
                                                user_opinion = 'colleague3_opinion'
                                                role_value = 'value_colleague3'
                                                role_comment = 'colleague3_comment'
                                            employee = self.env['hr.employee.multi.company'].sudo().search(
                                                [('s_identification_id', '=', nguoi_danh_gia_s_identification_id.upper())],limit= 1)
                                            if user_colleague_id:
                                                if self.env.user.id!=user_colleague_id:
                                                    message='Tài khoản đăng nhập không phải Đồng Nghiệp'
                                                    raise UserError(message)

                                                if employee.user_id.id!=self.env.user.id:
                                                    message = 'SC_CODE: ' +nguoi_danh_gia_s_identification_id+' không phải Đồng Nghiệp'
                                                    raise UserError(message)
                                                is_colleague = True

                                            else:
                                                message='Tài khoản đăng nhập không phải Đồng Nghiệp'
                                                raise UserError(message)

                                    except:
                                        raise UserError(message)
                                elif row_no ==11:
                                    if str(row[2].value)=='Có':
                                        list_value.update({de_xuat_dg_tai_hddg:True})
                                    else:
                                        list_value.update({de_xuat_dg_tai_hddg: False})
                                elif row_no==12:
                                    list_value.update({de_xuat_lydo: str(row[2].value)})
                                elif row_no==16:
                                    list_value.update({dexuat_salary: str(row[1].value)})
                                    list_value.update({dexuat_thuong: str(row[2].value)})
                                    list_value.update({dexuat_chucvu: str(row[3].value)})
                                    list_value.update({dexuat_thuyenchuyen: str(row[4].value)})
                                    list_value.update({user_opinion: str(row[5].value)})
                                row_no += 1
                        else:
                            value = []
                            row_no = 0
                            for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                                if row_no >= 6:
                                    if row_no > 8 and stt_sheet == 1 or row_no > 33 and stt_sheet == 2 or row_no > 20 \
                                            and stt_sheet == 3 or row_no > 28 and stt_sheet == 4 or row_no > 40 and \
                                            stt_sheet == 5 or row_no > 23 and stt_sheet == 6:
                                        break
                                    else:
                                        message = 'STT phải là ký tự số và điểm phải là số hoặc K'
                                        try:
                                            if stt_sheet == 6:
                                                composite_density = float(row[2].value) * 100
                                                if composite_density > 0 and len(str(row[1].value)) == 0:
                                                    message = 'Khi tỷ trọng lớn hơn 0% thì CÔNG VIỆC/TIÊU CHÍ không được để trống'
                                                    raise UserError(message)
                                                check_score = str(row[4].value)
                                                if check_score.upper() != "K":
                                                    check_score = float(check_score)
                                                    if check_score > 5 or check_score <0:
                                                        message='Điểm nhập phải lớn 0 và nhỏ hơn 5'
                                                        raise UserError(message)
                                                prefix = str(row[0].value)
                                                search = self.env['hr.survey.user.input.line'].sudo().search(
                                                    [('user_input_id', '=', user_input_id), ('prefix', '=', prefix),
                                                     ('enable_edit_percentage', '=', True)])

                                                value_list = {}
                                                if role_value == "value_manager" or role_value == "value":
                                                    value_list.update(
                                                        {"question_name": str(row[1].value),
                                                         "percentage": str(float(row[2].value) * 100),
                                                         role_value: row[4].value, role_comment: row[3].value})
                                                else:
                                                    value_list.update(
                                                        {role_value: row[4].value, role_comment: row[3].value})
                                                value.append([1, search.id, value_list])
                                            else:
                                                check_score = str(row[3].value)
                                                if check_score.upper() != "K":
                                                    check_score = float(check_score)
                                                    if check_score > 5 or check_score <0:
                                                        message='Điểm nhập phải lớn 0 và nhỏ hơn 5'
                                                        raise UserError(message)

                                                if row_no == 6:
                                                    prefix = "I." + str(row[0].value)
                                                else:
                                                    prefix = str(row[0].value)

                                                search = self.env['hr.survey.user.input.line'].sudo().search(
                                                    [('user_input_id', '=', user_input_id), ('prefix', '=', prefix),
                                                     ('enable_edit_percentage', '=', False)])
                                                value_list = {}
                                                if search.can_input is False:
                                                    value_list.update(
                                                        {role_comment: row[2].value})
                                                else:
                                                    value_list.update(
                                                        {role_value: row[3].value, role_comment: row[2].value})
                                                value.append([1, search.id, value_list])
                                        except:
                                            raise UserError(message)

                                row_no += 1
                            try:
                                if stt_sheet == 1:
                                    list_value.update({'questions_1': value})
                                elif stt_sheet == 2:
                                    list_value.update({'questions_2': value})
                                elif stt_sheet == 3:
                                    list_value.update({'questions_3': value})
                                elif stt_sheet == 4:
                                    list_value.update({'questions_4': value})
                                elif stt_sheet == 5 and is_manager:
                                    list_value.update({'questions_5': value})
                                elif stt_sheet == 6 and not is_colleague:
                                    list_value.update({'questions_6': value})
                            except:
                                raise UserError('Sheet error!')
                        stt_sheet += 1

                    result=self.env['hr.survey.user.input'].sudo().search([('id', '=', user_input_id)]).write(list_value)
                    if result:
                        return {
                            'name': 'Import Appraisal',
                            'type': 'ir.actions.act_window',
                            'res_model': 'appraisal.wizard',
                            'view_mode': 'form',
                            'view_type': 'form',
                            'target': 'new'
                        }



        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

    @api.multi
    def get_survey_template(self):
        return {
            'type': 'ir.actions.act_url',
            'name': 'contract',
            'url': '/seatek_hr_appraisal/static/src/xls/Template_DGNS.xlsx?download=true',
        }

    @api.multi
    def write(self, values):
        return super(ImportAppraisalKPIExcelTemplate, self).write(values)
#
class hr_wizard(models.AbstractModel):

    _name = 'appraisal.wizard'

    _description = 'Appraisal wizard'

    message = fields.Text(string="Import!", readonly=True, default='Import Complete')

