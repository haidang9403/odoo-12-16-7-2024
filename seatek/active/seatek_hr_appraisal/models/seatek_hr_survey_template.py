import binascii
import tempfile

import xlrd
from odoo import api, models, fields, _
from odoo.exceptions import UserError
from odoo.tools import pycompat


class SurveyImportTemplate(models.Model):
    _name = 'survey.import.template'
    _description = 'Survey Import Template'

    company_id = fields.Many2one('res.company', string='Công Ty', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', string='Bộ Phận',
                                    domain=lambda self: [('company_id', '=', self.env.user.company_id.id), (
                                        'manager_id', '=',
                                        # self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)],
                                        #                                       limit=1).id),('manager_id','!=',False)])
                                        self.env['hr.employee.multi.company'].sudo().search(
                                            [('user_id', '=', self.env.user.id),
                                             ('company_id', '=', self.env.user.company_id.id)],
                                            limit=1).name.id), ('manager_id', '!=', False)])

    @api.model
    def compute_job_position_id_compute(self):
        self.job_position_id_compute = self.user_input_id.job_position_id.id
        self.job_position_id = self.user_input_id.job_position_id.id

    job_position_id_compute = fields.Many2one('hr.job', string='Chức Vụ', compute='compute_job_position_id_compute')
    job_position_id = fields.Many2one('hr.job', string='Chức Vụ')
    user_input_id = fields.Many2one('hr.survey.user.input', string='User Input ID')
    survey_template_id = fields.Many2one('survey.kpis.template', string='Template',
                                         domain="[('job_position_id', '=',job_position_id_compute)]")

    kpis_template_line = fields.One2many('survey.import.template.line', 'survey_import_template_id',
                                         string='KPIs Template Lines', )
    user_id = fields.Many2one('res.users', string='User')

    @api.onchange('survey_template_id')
    def _onchange_survey_template_id(self):
        line_order = 110
        lines = [(5, 0, 0)]
        self.kpis_template_line = lines
        line_order = 110
        line_order = self.add_default_data("1", line_order)
        if self.survey_template_id.question_lines_thuong_xuyen:
            line_order = self.add_template_data("2", 120, self.survey_template_id.question_lines_thuong_xuyen)
        else:
            line_order = self.add_default_data("2", 120)
        self.add_default_data("3", 130)

    def add_template_data(self, parent_prefix, line_order, questions):
        lines = []
        input_line = self.env['hr.survey.user.input.line'].sudo().search(
            [('user_input_id', '=', self._origin.user_input_id.id), ('survey_level_2', '!=', False),
             ('prefix', '=', parent_prefix), ('enable_edit_percentage', '=', True)], limit=1)
        if input_line:
            vals = {
                'question_name': input_line.question_name,
                'percentage': input_line.percentage,
                'prefix': input_line.prefix,
                'summary_level': 1,
                'is_parent': True,
                'line_order': line_order,
            }
            lines.append((0, 0, vals))
            line_order += 1
            for i in range(5):
                child_prefix = str(parent_prefix) + '.' + str(i + 1)
                if i < len(questions):
                    vals = {
                        'question_name': questions[i].name,
                        'percentage': 0,
                        'prefix': child_prefix,
                        'summary_level': 2,
                        'is_parent': False,
                        'line_order': line_order,
                    }
                    lines.append((0, 0, vals))
                    line_order += 1
                else:
                    prefix = float(child_prefix)
                    child_input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                        [('user_input_id', '=', self._origin.user_input_id.id), ('summary_id', '=', input_line.id),
                         ('prefix', '=', child_prefix)])
                    for child_input_line in child_input_lines:
                        vals = {
                            'question_name': child_input_line.question_name,
                            'percentage': child_input_line.percentage,
                            'prefix': child_input_line.prefix,
                            'summary_level': child_input_line.summary_level,
                            'is_parent': False,
                            'line_order': line_order,
                        }
                        lines.append((0, 0, vals))
                        line_order += 1
        self.kpis_template_line = lines

        return line_order + 1

    def add_default_data(self, parent_prefix, line_order):
        lines = []
        input_lines = self.env['hr.survey.user.input.line'].sudo().search(
            [('user_input_id', '=', self._origin.user_input_id.id), ('survey_level_2', '!=', False),
             ('prefix', '=', parent_prefix), ('enable_edit_percentage', '=', True)])

        for input_line in input_lines:
            if str(input_line.prefix) == str(parent_prefix):
                vals = {
                    'question_name': input_line.question_name,
                    'percentage': input_line.percentage,
                    'prefix': input_line.prefix,
                    'summary_level': input_line.summary_level,
                    'is_parent': True,
                    'line_order': line_order,
                }
                lines.append((0, 0, vals))
                line_order += 1
                child_input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                    [('user_input_id', '=', self._origin.user_input_id.id), ('summary_id', '=', input_line.id)])
                for child_input_line in child_input_lines:
                    vals = {
                        'question_name': child_input_line.question_name,
                        'percentage': child_input_line.percentage,
                        'prefix': child_input_line.prefix,
                        'summary_level': child_input_line.summary_level,
                        'is_parent': False,
                        'line_order': line_order,
                    }
                    lines.append((0, 0, vals))
                    line_order += 1
        self.kpis_template_line = lines
        return line_order + 1

    def import_kpis_template_action(self):
        try:
            if self.check_percentage():
                self.write_template_data_v2()

        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

    def check_percentage(self):
        try:
            massage = ' '
            parent_percentage = 0
            percentage = []
            question_name = []
            number_of_question = []
            prefix = 0
            not_check = False
            for rec in self.kpis_template_line:
                if rec.is_parent:
                    parent_percentage += rec.percentage
                    question_name.append(rec.question_name)
                    percentage.append(0)
                    number_of_question.append(0)
                    prefix = int(rec.prefix)
                else:
                    if float(rec.prefix) - float(prefix) > 0 and (float(rec.prefix) - float(prefix)) < 1:
                        if not_check:
                            percentage[prefix - 1] = 100
                        else:
                            percentage[prefix - 1] += rec.percentage
                        number_of_question[prefix - 1] += 1
            if parent_percentage != 100:
                massage += 'Wrong format. \nTổng phần trăm các câu hỏi  phải là 100%! (Phần trăm hiện tại ' + str(
                    parent_percentage) + ' )\n'
            i = 0
            for percent in percentage:
                if percent != 100:
                    massage += 'Wrong format. \nTổng phần trăm các câu hỏi trong "' + str(
                        question_name[i]) + '" phải là 100%! (Phần trăm hiện tại ' + str(percent) + ' )\n'
                if number_of_question[i] > 10:
                    massage += 'Wrong format. \nTổng số các câu hỏi trong "' + str(
                        question_name[i]) + '" nhỏ hơn hoặc bằng 10' + ' )\n'
                i += 1
            if massage != ' ':
                raise UserError(massage)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        return True

    def write_template_data_v2(self):
        user_input = self.env['hr.survey.user.input'].sudo().browse(
            [(self.user_input_id.id)])
        data = []
        for line in user_input.questions_6:
            for rec in self.kpis_template_line:
                if rec.prefix == line.prefix:
                    if rec.is_parent:
                        data.append([1, line.id, {'percentage': rec.percentage}])
                    else:

                        data.append([1, line.id, {'percentage': rec.percentage, 'question_name': rec.question_name}])
                    break
        self.env['hr.survey.user.input'].sudo().search(
            [('id', '=', self.user_input_id.id)]).write({'questions_6': data})

    def write_template_data(self):
        '''' Write parent'''
        self.write_parent_prefix_template()
        self.write_child_prefix_template()
        lines = [(5, 0, 0)]
        self.kpis_template_line = lines

    def write_parent_prefix_template(self):
        for i in range(3):
            parent_prefix = str(i + 1)
            for rec in self.kpis_template_line:
                if str(rec.prefix) == str(parent_prefix):
                    input_line = self.env['hr.survey.user.input.line'].sudo().search(
                        [('user_input_id', '=', self.user_input_id.id),
                         ('line_open_state', '=', True),
                         ('prefix', '=', rec.prefix),
                         ('enable_edit_percentage', '=', True)])
                    if input_line:
                        self.env['hr.survey.user.input.line'].sudo().search(
                            [('user_input_id', '=', self.user_input_id.id),
                             ('line_open_state', '=', True),
                             ('prefix', '=', parent_prefix),
                             ('enable_edit_percentage', '=', True)]).write(
                            {'percentage': rec.percentage, 'line_order': rec.line_order})

    def write_child_prefix_template(self):
        list_prefix = []
        line_order = 0
        for i in range(3):
            parent_prefix = str(i + 1)
            input_line = self.env['hr.survey.user.input.line'].sudo().search(
                [('user_input_id', '=', self.user_input_id.id), ('prefix', '=', parent_prefix),
                 ('line_open_state', '=', True), ('enable_edit_percentage', '=', True)], limit=1)

            if input_line:
                summary_id = input_line.id
                parent_page_id = input_line.parent_page_id.id
            line_order = 100 + ((i + 1) * 10) + 1
            for child in range(5):
                child_prefix = str(parent_prefix) + '.' + str(child + 1)
                for rec in self.kpis_template_line:
                    if str(rec.prefix) == str(child_prefix):
                        input_line = self.env['hr.survey.user.input.line'].sudo().search(
                            [('user_input_id', '=', self.user_input_id.id),
                             ('line_open_state', '=', True),
                             ('prefix', '=', rec.prefix),
                             ('enable_edit_percentage', '=', True)])
                        if input_line:
                            self.env['hr.survey.user.input.line'].sudo().search(
                                [('user_input_id', '=', self.user_input_id.id),
                                 ('line_open_state', '=', True),
                                 ('prefix', '=', rec.prefix),
                                 ('enable_edit_percentage', '=', True)]).write(
                                {'prefix': rec.prefix, 'question_name': rec.question_name, 'percentage': rec.percentage,
                                 'line_order': line_order})
                            line_order += 1
                            list_prefix.append(str(rec.prefix))
                        else:
                            self.env['hr.survey.user.input.line'].sudo().create({'name': 'General',
                                                                                 'page_name': 'KPIS',
                                                                                 'prefix': rec.prefix,
                                                                                 'question_name': rec.question_name,
                                                                                 'can_input': True,
                                                                                 'summary_id': summary_id,
                                                                                 'enable_edit_title': True,
                                                                                 'enable_edit_percentage': True,
                                                                                 'question_6': self.user_input_id.id,
                                                                                 'max_score': 5,
                                                                                 'parent_page_id': parent_page_id,
                                                                                 'user_input_id': self.user_input_id.id,
                                                                                 'line_open_state': True,
                                                                                 'percentage': rec.percentage,
                                                                                 'summary_level': 2,
                                                                                 'summary_level_report': 3,
                                                                                 'line_order': rec.line_order})
                            line_order += 1
                            list_prefix.append(str(rec.prefix))
                        break
        # '''Xóa các câu hỏi không có trong template'''
        # input_lines = self.env['hr.survey.user.input.line'].sudo().search(
        #     [('user_input_id', '=', self.user_input_id), ('enable_edit_title', '=', True),
        #      ('line_open_state', '=', True)])
        # for input_line in input_lines:
        #     not_in = True
        #     for pre in list_prefix:
        #         if input_line.prefix == pre:
        #             not_in = False
        #     if not_in:
        #         input_line.unlink()


class SurveyImportExcelTemplateLine(models.TransientModel):
    _name = 'survey.import.template.line'
    _description = 'KPIS Template Lines'
    _order = 'line_order'

    name = fields.Char(string='Name')
    prefix = fields.Char(string='Prefix')
    question_name = fields.Char(string='Question Name')
    percentage = fields.Float(string='Percentage')
    survey_import_template_id = fields.Many2one('survey.import.template')
    line_order = fields.Integer(string='Line Order')
    summary_level = fields.Integer(string="Level")
    is_parent = fields.Boolean(string='Is Parent', default=False)


class SurveyImportExcelTemplate(models.TransientModel):
    _name = 'survey.import.excel.template'

    template_path = fields.Binary(string='Path')
    name = fields.Char(string='Name')
    import_option = fields.Selection([('csv', 'CSV File'), ('xls', 'XLS File')], string='Select', default='csv')
    user_input_id = fields.Many2one('hr.survey.user.input', string='User Input ID')
    kpis_template_line = fields.One2many('survey.import.excel.template.line', 'survey_import_excel_template_id',
                                         string='KPIs Template Lines')
    user_id = fields.Many2one('res.users', string='User')

    @api.onchange('template_path')
    def _onchange_template_path(self):
        try:
            line_order = 110
            lines = [(5, 0, 0)]
            self.kpis_template_line = lines
            if self.template_path:
                fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
                fp.write(binascii.a2b_base64(self.template_path))
                fp.seek(0)
                book = xlrd.open_workbook(fp.name)

                if book:
                    for i in range(3):
                        have_parent_prefix = False
                        parent_prefix = i + 1
                        for sheet in book.sheets():
                            row_no = 0
                            for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                                if row_no > 0:
                                    prefix = str(row[0].value)
                                    try:
                                        check = float(prefix)
                                    except:
                                        prefix = '0'
                                    try:
                                        if str(float(prefix)) == str(float(parent_prefix)):
                                            have_parent_prefix = True
                                    except:
                                        raise UserError('STT phải là ký tự số')
                                row_no += 1
                        if not have_parent_prefix:
                            line_order = self.add_default_data(parent_prefix, line_order)
                        else:
                            line_order = self.add_excel_data(book, parent_prefix, line_order)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

    def add_default_data(self, parent_prefix, line_order):
        lines = []
        input_lines = self.env['hr.survey.user.input.line'].sudo().search(
            [('user_input_id', '=', self._origin.user_input_id.id), ('survey_level_2', '!=', False),
             ('prefix', '=', parent_prefix), ('enable_edit_percentage', '=', True)])

        for input_line in input_lines:

            if str(input_line.prefix) == str(parent_prefix):
                vals = {
                    'question_name': input_line.question_name,
                    'percentage': input_line.percentage,
                    'prefix': input_line.prefix,
                    'summary_level': input_line.summary_level,
                    'is_parent': True,
                    'line_order': line_order,
                }
                lines.append((0, 0, vals))
                line_order += 1
                child_input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                    [('user_input_id', '=', self._origin.user_input_id.id), ('summary_id', '=', input_line.id)])
                for child_input_line in child_input_lines:
                    vals = {
                        'question_name': child_input_line.question_name,
                        'percentage': child_input_line.percentage,
                        'prefix': child_input_line.prefix,
                        'summary_level': child_input_line.summary_level,
                        'is_parent': False,
                        'line_order': line_order,
                    }
                    lines.append((0, 0, vals))
                    line_order += 1
        self.kpis_template_line = lines
        return line_order + 1

    def add_excel_data(self, book, parent_prefix, line_order):
        for sheet in book.sheets():
            try:
                row_no = 0
                lines = []
                parent_percent = -1
                input_line = self.env['hr.survey.user.input.line'].sudo().search(
                    [('user_input_id', '=', self._origin.user_input_id.id), ('survey_level_2', '!=', False),
                     ('prefix', '=', parent_prefix), ('enable_edit_percentage', '=', True)], limit=1)
                if input_line:
                    for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                        if row_no > 0:
                            try:
                                prefix = float(row[0].value)
                            except:
                                prefix = 0
                            if str(float('%.2f' % prefix)) == str(float('%.2f' % parent_prefix)):
                                try:
                                    parent_percent = float(row[2].value)
                                except:
                                    parent_percent = 0
                        row_no += 1
                    if parent_percent != -1:
                        vals = {
                            'question_name': input_line.question_name,
                            'percentage': parent_percent,
                            'prefix': input_line.prefix,
                            'summary_level': 1,
                            'is_parent': True,
                            'line_order': line_order,
                        }
                        lines.append((0, 0, vals))
                        line_order += 1
                    else:
                        raise UserError('Sai định dạng. \nPercent "%s" phải là số' % input_line.question_name)

                    for child in range(5):
                        child_prefix = str(parent_prefix) + '.' + str(child + 1)
                        have_child = False
                        for row in pycompat.imap(sheet.row, range(sheet.nrows)):
                            if row_no > 0:
                                prefix = str(row[0].value)
                                try:
                                    check = float(row[0].value)
                                except:
                                    prefix = '0'

                                if prefix == child_prefix:
                                    have_child = True
                                    percentage = 0
                                    try:
                                        percentage = float(row[2].value)
                                    except:
                                        percentage = 0
                                    vals = {
                                        'prefix': child_prefix,
                                        'question_name': child_prefix + '.' + row[1].value,
                                        'percentage': percentage,
                                        'summary_level': 2,
                                        'is_parent': False,
                                        'line_order': line_order,
                                    }
                                    lines.append((0, 0, vals))
                                    line_order += 1
                                    break
                            row_no += 1

                        if not have_child:
                            child_input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                                [('user_input_id', '=', self._origin.user_input_id.id),
                                 ('summary_id', '=', input_line.id), ('prefix', '=', child_prefix)])
                            for child_input_line in child_input_lines:
                                vals = {
                                    'question_name': child_input_line.question_name,
                                    'percentage': child_input_line.percentage,
                                    'prefix': child_input_line.prefix,
                                    'summary_level': child_input_line.summary_level,
                                    'is_parent': False,
                                    'line_order': line_order,
                                }
                                lines.append((0, 0, vals))
                                line_order += 1
                else:
                    raise UserError('Sai định dạng.')
                self.kpis_template_line = lines
                massage = ' '
                if massage != ' ':
                    raise UserError(massage)
            except IndexError:
                raise UserError('Sai định dạng.')
            break
        return line_order + 1

    def import_kpis_excel_action(self):
        try:
            if self.check_percentage():
                self.write_template_data_v2()

        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

    def check_percentage(self):
        try:
            massage = ' '
            parent_percentage = 0
            percentage = []
            question_name = []
            number_of_question = []
            prefix = 0
            not_check = False
            for rec in self.kpis_template_line:
                if rec.is_parent:
                    parent_percentage += rec.percentage
                    question_name.append(rec.question_name)
                    percentage.append(0)
                    number_of_question.append(0)
                    prefix = int(rec.prefix)
                    not_check = False
                    if rec.percentage == 0:
                        not_check = True
                else:
                    if float(rec.prefix) - float(prefix) > 0 and (float(rec.prefix) - float(prefix)) < 1:
                        if not_check:
                            percentage[prefix - 1] = 100
                        else:
                            percentage[prefix - 1] += rec.percentage
                        number_of_question[prefix - 1] += 1
            if parent_percentage != 100:
                massage += 'Wrong format. \nTổng phần trăm các câu hỏi  phải là 100%! (Phần trăm hiện tại ' + str(
                    parent_percentage) + ' )\n'
            i = 0
            for percent in percentage:
                if percent != 100:
                    massage += 'Wrong format. \nTổng phần trăm các câu hỏi trong "' + str(
                        question_name[i]) + '" phải là 100%! (Phần trăm hiện tại ' + str(percent) + ' )\n'
                if number_of_question[i] > 10:
                    massage += 'Wrong format. \nTổng số các câu hỏi trong "' + str(
                        question_name[i]) + '" nhỏ hơn hoặc bằng 10' + ' )\n'
                i += 1
            if massage != ' ':
                raise UserError(massage)
        except FileNotFoundError:
            raise UserError('No such file or directory found. \n%s.' % self.file_name)
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')
        return True

    def write_template_data_v2(self):
        user_input = self.env['hr.survey.user.input'].sudo().browse(
            [(self.user_input_id.id)])
        data = []
        for line in user_input.questions_6:
            for rec in self.kpis_template_line:
                if rec.prefix == line.prefix:
                    if rec.is_parent:
                        data.append([1, line.id, {'percentage': rec.percentage}])
                    else:

                        data.append([1, line.id, {'percentage': rec.percentage, 'question_name': rec.question_name}])
                    break
        self.env['hr.survey.user.input'].sudo().search(
            [('id', '=', self.user_input_id.id)]).write({'questions_6': data})

    def write_template_data(self):
        '''' Write parent'''
        self.write_parent_prefix_template()
        self.write_child_prefix_template()
        lines = [(5, 0, 0)]
        self.kpis_template_line = lines

    def write_parent_prefix_template(self):
        for i in range(3):
            parent_prefix = str(i + 1)
            for rec in self.kpis_template_line:
                if str(rec.prefix) == str(parent_prefix):
                    input_line = self.env['hr.survey.user.input.line'].sudo().search(
                        [('user_input_id', '=', self.user_input_id.id),
                         ('line_open_state', '=', True),
                         ('prefix', '=', rec.prefix),
                         ('enable_edit_percentage', '=', True)])
                    if input_line:
                        self.env['hr.survey.user.input.line'].sudo().search(
                            [('user_input_id', '=', self.user_input_id.id),
                             ('line_open_state', '=', True),
                             ('prefix', '=', parent_prefix),
                             ('enable_edit_percentage', '=', True)]).write(
                            {'percentage': rec.percentage, 'line_order': rec.line_order})

    def write_child_prefix_template(self):
        list_prefix = []
        for i in range(3):
            parent_prefix = str(i + 1)
            input_line = self.env['hr.survey.user.input.line'].sudo().search(
                [('user_input_id', '=', self.user_input_id.id), ('prefix', '=', parent_prefix),
                 ('line_open_state', '=', True), ('enable_edit_percentage', '=', True)], limit=1)

            if input_line:
                summary_id = input_line.id
                parent_page_id = input_line.parent_page_id.id
            for child in range(5):
                child_prefix = str(parent_prefix) + '.' + str(child + 1)
                for rec in self.kpis_template_line:
                    if str(rec.prefix) == str(child_prefix):
                        input_line = self.env['hr.survey.user.input.line'].sudo().search(
                            [('user_input_id', '=', self.user_input_id.id),
                             ('line_open_state', '=', True),
                             ('prefix', '=', rec.prefix),
                             ('enable_edit_percentage', '=', True)])
                        if input_line:
                            self.env['hr.survey.user.input.line'].sudo().search(
                                [('user_input_id', '=', self.user_input_id.id),
                                 ('line_open_state', '=', True),
                                 ('prefix', '=', rec.prefix),
                                 ('enable_edit_percentage', '=', True)]).write(
                                {'prefix': rec.prefix, 'question_name': rec.question_name, 'percentage': rec.percentage,
                                 'line_order': rec.line_order})
                            list_prefix.append(str(rec.prefix))
                        else:
                            self.env['hr.survey.user.input.line'].sudo().create({'name': 'General',
                                                                                 'page_name': 'KPIS',
                                                                                 'prefix': rec.prefix,
                                                                                 'question_name': rec.question_name,
                                                                                 'can_input': True,
                                                                                 'summary_id': summary_id,
                                                                                 'enable_edit_title': True,
                                                                                 'enable_edit_percentage': True,
                                                                                 'question_6': self.user_input_id.id,
                                                                                 'max_score': 5,
                                                                                 'parent_page_id': parent_page_id,
                                                                                 'user_input_id': self.user_input_id.id,
                                                                                 'line_open_state': True,
                                                                                 'percentage': rec.percentage,
                                                                                 'summary_level': 2,
                                                                                 'summary_level_report': 3,
                                                                                 'line_order': rec.line_order})
                            list_prefix.append(str(rec.prefix))
                        break
        # '''Xóa các câu hỏi không có trong template'''
        # input_lines = self.env['hr.survey.user.input.line'].sudo().search(
        #     [('user_input_id', '=', self.user_input_id), ('enable_edit_title', '=', True),
        #      ('line_open_state', '=', True)])
        # for input_line in input_lines:
        #     not_in = True
        #     for pre in list_prefix:
        #         if input_line.prefix == pre:
        #             not_in = False
        #     if not_in:
        #         input_line.unlink()

    @api.multi
    def get_survey_template(self):
        return {
            'type': 'ir.actions.act_url',
            'name': 'contract',
            'url': '/seatek_hr_appraisal/static/src/xls/KPIS_Template.xls?download=true',
        }

    @api.multi
    def write(self, values):
        return super(SurveyImportExcelTemplate, self).write(values)


class SurveyImportExcelTemplateLine(models.TransientModel):
    _name = 'survey.import.excel.template.line'
    _description = 'KPIS Template Lines'
    _order = 'line_order'

    name = fields.Char(string='Name')
    prefix = fields.Char(string='Prefix')
    question_name = fields.Char(string='Question Name')
    percentage = fields.Float(string='Percentage')
    survey_import_excel_template_id = fields.Many2one('survey.import.excel.template')
    line_order = fields.Integer(string='Line Order')
    summary_level = fields.Integer(string="Level")
    is_parent = fields.Boolean(string='Is Parent', default=False)


class SurveyKpisQuestion(models.Model):
    _name = 'survey.kpis.question'
    _description = 'Survey KPIS Question'
    _order = 'line_order'

    name = fields.Char(string='Tiêu Chí', require=True)
    company_id = fields.Many2one('res.company', require=True, string='Công Ty', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', require=True, string='Bộ Phận',
                                    domain=lambda self: [('company_id', '=', self.env.user.company_id.id), (
                                        'manager_id', '=',
                                        # self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)],
                                        #                                       limit=1).id),
                                        self.env['hr.employee.multi.company'].sudo().search(
                                            [('user_id', '=', self.env.user.id),
                                             ('company_id', '=', self.env.user.company_id.id)],
                                            limit=1).name.id), ('manager_id', '!=', False)])

    job_position_id = fields.Many2one('hr.job', require=True, string='Chức Vụ',
                                      domain="[('department_id', '=',department_id)]")
    line_order = fields.Integer(string='Line Order')
    summary_level = fields.Integer(string="Level")


class SurveyKpisTemplate(models.Model):
    _name = 'survey.kpis.template'
    _description = 'Survey KPIS Template'

    name = fields.Char(string='Tên', require=True)
    company_id = fields.Many2one('res.company', string='Công Ty', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', require=True, string='Bộ Phận',
                                    domain=lambda self: [('company_id', '=', self.env.user.company_id.id), (
                                        'manager_id', '=',
                                        # self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)],
                                        #                                       limit=1).id),
                                        self.env['hr.employee.multi.company'].sudo().search(
                                            [('user_id', '=', self.env.user.id),
                                             ('company_id', '=', self.env.user.company_id.id)],
                                            limit=1).name.id), ('manager_id', '!=', False)])

    job_position_id = fields.Many2one('hr.job', require=True, string='Chức Vụ',
                                      domain="[('department_id', '=',department_id)]")
    percentage_thuong_xuyen = fields.Float(string='Tỉ Trọng')
    question_lines_thuong_xuyen = fields.Many2many('survey.kpis.question', 'survey_template_question_rel',
                                                   'survey_kpis_template_id', 'survey_kpis_question_id',
                                                   string='Câu Hỏi', domain="[('job_position_id','=',job_position_id)]")

    @api.onchange('question_lines_thuong_xuyen')
    def onchange_question_lines_thuong_xuyen(self):
        lines = []

        for rec in self.question_lines_thuong_xuyen:
            if rec.job_position_id == self.job_position_id:
                lines.append(rec.id)
        new_lines = self.env['survey.kpis.question'].browse(lines)
        self.question_lines_thuong_xuyen = new_lines


class AssignQuestionToTemplate(models.TransientModel):
    _name = "survey.assign.question.template"

    name = fields.Char(string='Tên')
    company_id = fields.Many2one('res.company', string='Công Ty', readonly=True,
                                 default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', string='Bộ Phận',
                                    domain=lambda self: [('company_id', '=', self.env.user.company_id.id), (
                                        'manager_id', '=',
                                        # self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)],
                                        #                                       limit=1).id),
                                        self.env['hr.employee.multi.company'].sudo().search(
                                            [('user_id', '=', self.env.user.id),
                                             ('company_id', '=', self.env.user.company_id.id)],
                                            limit=1).name.id), ('manager_id', '!=', False)])

    job_position_id = fields.Many2one('hr.job', string='Chức Vụ', domain="[('department_id', '=',department_id)]")
    template = fields.Many2one('survey.kpis.template', string='Template',
                               domain="[('job_position_id','=',job_position_id)]")
    user_id = fields.Many2one('res.users', string='User')
    questions = []

    def get_questions(self, records):
        self.questions.clear()
        for record in records:
            self.questions.append(record.id)

    def button_assign_question_to_template(self):
        if len(self.questions) > 0:
            questions = self.env['survey.kpis.question'].sudo().browse(self.questions)
            right_job_position = True
            for question in questions:
                if question.job_position_id != self.job_position_id:
                    right_job_position = False
                    break
            if right_job_position:
                template = self.env['survey.kpis.template'].sudo().search([('id', '=', self.template.id)])
                if template:
                    lines = [(5, 0, 0)]
                    template.question_lines_thuong_xuyen = lines
                    template.question_lines_thuong_xuyen = questions
            else:
                raise UserError(_("Xin hãy chọn các câu hỏi cùng Job Position"))
