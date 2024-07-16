import logging

from odoo import api, models, fields, _
from odoo.exceptions import UserError

from odoo.tools import  pycompat

_logger = logging.getLogger(__name__)


class HR_Appraisal(models.Model):
    _name = 'hr.appraisal'
    _description = 'HR Appraisal'
    name = fields.Char(string='Comment', requre=True)
    survey_id = fields.Many2one('hr.survey', string='MẪU ĐÁNH GIÁ', domain=[('state_done', '=', True)],
                                ondelete='cascade', require=True)
    date_appraisal = fields.Date(string='Date')
    appraisal_period = fields.Many2one('hr.appraisal.period', string='ĐỢT', require=True, ondelete='cascade')

    company_id = fields.Many2one('res.company', readonly=True,
                                 default=lambda self: self.env.user.company_id, string='NHÂN VIÊN', ondelete='cascade')

    @api.depends()
    def _compute_hr_survey_user_input(self):
        data_survey_user_ids = self.env['hr.survey.user.input'].search(
            [('company_id', '=', self.company_id.id), ('appraisal_id', '=', self.id)])
        self.hr_survey_user_input = data_survey_user_ids

    mark_as_todo = fields.Boolean(string='Mark as todo', default=False)
    state_done = fields.Boolean(string='Done')
    user_id = fields.Many2one('res.users', string='User', ondelete='cascade')
    hddg_template = fields.Many2many('hr.employee', 'hr_survey_user_hddg_template_rel', 'empl_id', 'hddg_id',
                                     string="HĐĐG")

    def close_appraisal(self):
        user_inputs = self.env['hr.survey.user.input'].sudo().search([('appraisal_id', '=', self.id)])
        for user_input in user_inputs:
            user_input.open_state = False
            lines = self.env['hr.survey.user.input.line'].sudo().search([('user_input_id', '=', user_input.id)])
            for line in lines:
                line.line_open_state = False
        self.appraisal_mode = 'close'

    appraisal_mode = fields.Selection([('open', 'Open'), ('close', 'Close')], default='open')
    # @api.onchange('hr_survey_user_input')
    # def _onchange_hr_survey_user_input(self):
    #     for rec in self:
    #         for input in rec.hr_survey_user_input:
    #             input.employee_ids = rec.employee_ids

    hr_survey_user_input = fields.One2many('hr.survey.user.input', 'appraisal_id', string='Appraisal Input',
                                           domain=lambda self: [('company_id', '=', self.env.user.company_id.id)])

    # @api.onchange('company_id')
    # def _onchange_company_id(self):
    #     data_survey_user_ids = self.env['hr.survey.user.input'].search(
    #         [('company_id', '=', self.company_id.id), ('appraisal_id', '=', self._origin.id)])
    #     self.hr_survey_user_input = data_survey_user_ids

    @api.depends()
    def compute_employees(self):
        user_inputs = self.env['hr.survey.user.input'].sudo().search([('appraisal_id', '=', self.id)])
        employees = []
        for user_input in user_inputs:
            employees.append(user_input.employee_id.id)
        empls = self.env['hr.employee.multi.company'].sudo().search(
            [('name', 'not in', employees), ('company_id', '=', self.env.user.company_id.id)])
        empl = []
        for em in empls:
            empl.append(em.name)
        self.employee_ids = empls

    employee_ids = fields.Many2many('hr.employee', compute='compute_employees')

    @api.model
    def create(self, values):
        rec = super(HR_Appraisal, self).create(values)
        rec.mark_as_todo = True
        return rec

    @api.multi
    def action_confirm(self):
        self.mark_as_todo = False
        self.state_done = True
        return True

    def create_appraisal(self):

        if self.appraisal_period:
            if self.company_id.id == 1:
                companies = self.env['res.company'].sudo().search([])
                for company in companies:
                    employees = self.env['hr.employee.multi.company'].sudo().search(
                        [('company_id', '=', company.id), ('employee_current_status', '!=', 'resigned'),
                         ('active', '=', True)])
                    for employee in employees:
                        survey_user_input = self.env['hr.survey.user.input'].sudo().search(
                            [('employee_multi_id', '=', employee.id), ('appraisal_id', '=', self.id)])
                        if not survey_user_input:
                            user = employee.user_id
                            employee_manager = None
                            employee_smanager = None
                            smanager_employee = None
                            manager_employee = None
                            manager_user_id = None
                            smanager_user_id = None
                            if employee.parent_id:
                                employee_manager = employee.parent_id.id
                                manager_employee = self.env['hr.employee.multi.company'].sudo().search(
                                    [('name', '=', employee_manager), ('company_id', '=', company.id)])
                                employee_manager = manager_employee.id
                                if manager_employee.parent_id:
                                    manager_user_id = manager_employee.user_id.id
                                    employee_smanager = manager_employee.parent_id.id
                                    smanager_employee = self.env['hr.employee.multi.company'].sudo().search(
                                        [('name', '=', employee_smanager), ('company_id', '=', company.id)])
                                    employee_smanager = smanager_employee.id
                                    if smanager_employee:
                                        smanager_user_id = smanager_employee.user_id.id
                            '''Không cần check ràng buộc employee phải có user'''
                            # if user.id:
                            hr_user_input = self.env['hr.survey.user.input'].sudo().search(
                                [('employee_multi_id', '=', employee.id), ('appraisal_period', '=', self.id)])
                            if len(hr_user_input) == 0:
                                survey_user_id = self.env['hr.survey.user.input'].sudo().create(
                                    {'name': employee.name.name,
                                     'appraisal_id': self.id,
                                     'employee_multi_id': employee.id,
                                     'company_id': employee.company_id.id,
                                     'appraisal_period': self.appraisal_period.id,
                                     'manager_multi_id': employee_manager,
                                     'smanager_multi_id': employee_smanager,
                                     'survey_id': self.survey_id.id,
                                     'user_id': user.id,
                                     'user_manager_id': manager_user_id,
                                     'department_id': employee.department_id.id,
                                     'operating_unit_id': employee.operating_unit_id.id,
                                     'job_position_id': employee.job_id.id,
                                     'user_smanager_id': smanager_user_id})

            else:
                employees = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', self.company_id.id), ('employee_current_status', '!=', 'resigned'),
                     ('active', '=', True)])
                for employee in employees:
                    survey_user_input = self.env['hr.survey.user.input'].sudo().search(
                        [('employee_multi_id', '=', employee.id), ('appraisal_id', '=', self.id)])
                    if not survey_user_input:
                        user = employee.user_id
                        employee_manager = None
                        employee_smanager = None
                        manager_employee = None
                        smanager_employee = None
                        manager_user_id = None
                        smanager_user_id = None
                        if employee.parent_id:
                            employee_manager = employee.parent_id.id
                            manager_employee = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', employee_manager), ('company_id', '=', self.company_id.id)])
                            employee_manager = manager_employee.id
                            if manager_employee.parent_id:
                                manager_user_id = manager_employee.user_id.id
                                employee_smanager = manager_employee.parent_id.id
                                smanager_employee = self.env['hr.employee.multi.company'].sudo().search(
                                    [('name', '=', employee_smanager), ('company_id', '=', self.company_id.id)])
                                employee_smanager = smanager_employee.id
                                if smanager_employee:
                                    smanager_user_id = smanager_employee.user_id.id
                        '''Không cần check ràng buộc employee phải có user'''
                        # if user.id:
                        hr_user_input = self.env['hr.survey.user.input'].sudo().search(
                            [('employee_multi_id', '=', employee.name.id), ('appraisal_period', '=', self.id)])

                        if len(hr_user_input) == 0:
                            survey_user_id = self.env['hr.survey.user.input'].sudo().create({'name': employee.name.name,
                                                                                             'appraisal_id': self.id,
                                                                                             'employee_multi_id': employee.id,
                                                                                             'is_manager': employee.name.manager,
                                                                                             'company_id': self.company_id.id,
                                                                                             'appraisal_period': self.appraisal_period.id,
                                                                                             'manager_multi_id': employee_manager,
                                                                                             'smanager_multi_id': employee_smanager,
                                                                                             'survey_id': self.survey_id.id,
                                                                                             'user_id': user.id,
                                                                                             'user_manager_id': manager_user_id,
                                                                                             'department_id': employee.department_id.id,
                                                                                             'operating_unit_id': employee.operating_unit_id.id,
                                                                                             'job_position_id': employee.job_id.id,
                                                                                             'user_smanager_id': smanager_user_id})

    @api.multi
    def action_send_survey(self):
        local_context = dict(
            self.env.context,
            default_model='hr.survey',
            default_res_id=self.survey_id.id,
            default_survey_id=self.survey_id.id,
            default_composition_mode='comment',
            notif_layout='mail.mail_notification_light',
        )
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.survey.mail.compose.message',
            'target': 'new',
            'context': local_context,
        }

    @api.multi
    def write(self, values):
        for rec in self:
            periods = self.env['hr.appraisal.period'].sudo().search([('id', '=', rec.appraisal_period.id)])
            for period in periods:
                period.appraisal_id = rec.id
        return super(HR_Appraisal, self).write(values)

    def print_dexuat_sau_danhgia(self):
        return self.env.ref('seatek_hr_appraisal.action_report_dexuat_sau_dgns').report_action(self)

    def print_ketqua_sau_danhgia(self):
        return self.env.ref('seatek_hr_appraisal.action_report_ketqua_sau_dgns').report_action(self)

    # TKK
    def in_baocao_dgns(self):
        return self.env.ref('seatek_hr_appraisal.action_report_baocao_dgns').report_action(self)

    company_open_close=fields.Many2one('res.company',string='Company')
    def action_close_company(self):
        values=[]
        if self.close_open_all_role:
            values.append('close_open_all_role')
        else:
            if self.close_open_user_role:
                values.append('close_open_user_role')
            if self.close_open_manager_role:
                values.append('close_open_manager_role')
            if self.close_open_smanager_role:
                values.append('close_open_smanager_role')
            if self.close_open_colleague_role:
                values.append('close_open_colleague_role')
            if self.close_open_hddg_role:
                values.append('close_open_hddg_role')
        if self.company_open_close:
            self.close_role_company(self.company_open_close,values)
        else:
            company_ids=self.env['res.company'].sudo().search([('id','!=',1)])
            for company in company_ids:
                self.close_role_company(company,values)

    def action_open_company(self):
        values = []
        if self.close_open_all_role:
            values.append('close_open_all_role')
        else:
            if self.close_open_user_role:
                values.append('close_open_user_role')
            if self.close_open_manager_role:
                values.append('close_open_manager_role')
            if self.close_open_smanager_role:
                values.append('close_open_smanager_role')
            if self.close_open_colleague_role:
                values.append('close_open_colleague_role')
            if self.close_open_hddg_role:
                values.append('close_open_hddg_role')
        if self.company_open_close:
            self.close_role_company(self.company_open_close, values,True)
        else:
            company_ids = self.env['res.company'].sudo().search([('id', '!=', 1)])
            for company in company_ids:
                self.close_role_company(company, values,True)

    def close_role_company(self,company,values='',close_or_open=False):
        user_inputs = self.env['hr.survey.user.input'].sudo().search([('company_id', '=', company.id), ('appraisal_id', '=', self.id)])
        for user_input in user_inputs:
            if 'close_open_all_role' in values:
                user_input.open_state = close_or_open
                if close_or_open:
                    user_input.user_open_state = close_or_open
                    user_input.manager_open_state = close_or_open
                    user_input.smanager_open_state = close_or_open
                    user_input.colleague_open_state = close_or_open
                    user_input.hddg_open_state = close_or_open
                else:
                    user_input.user_open_state = close_or_open
                    user_input.manager_open_state = close_or_open
                    user_input.smanager_open_state = close_or_open
                    user_input.colleague_open_state = close_or_open

            else:
                if 'close_open_user_role' in values:
                    user_input.user_open_state = close_or_open
                if 'close_open_manager_role' in values:
                    user_input.manager_open_state = close_or_open
                if 'close_open_smanager_role' in values:
                    user_input.smanager_open_state = close_or_open
                if 'close_open_colleague_role' in values:
                    user_input.colleague_open_state = close_or_open
                if 'close_open_hddg_role' in values:
                    user_input.hddg_open_state = close_or_open
            # lines = self.env['hr.survey.user.input.line'].sudo().search([('user_input_id', 'in', user_input.ids)])
            # for line in lines:
                # user_open_state = fields.Boolean(string='Trạng Thái Đóng User', default=True)
                # manager_open_state = fields.Boolean(string='Trạng Thái Đóng Manager', default=True)
                # smanager_open_state = fields.Boolean(string='Trạng Thái Đóng Smanager', default=True)
                # colleague_open_state = fields.Boolean(string='Trạng Thái Đóng Colleague', default=True)
                # hddg_open_state = fields.Boolean(string='Trạng Thái Đóng HDDG', default=True)
                # if 'close_open_all_role' in values:
                #     line.line_open_state = False




    close_open_all_role=fields.Boolean(string="Close-Open all")
    close_open_user_role=fields.Boolean(string="Close-Open user")
    close_open_manager_role=fields.Boolean(string="Close-Open manager")
    close_open_smanager_role=fields.Boolean(string="Close-Open smanager")
    close_open_colleague_role=fields.Boolean(string="Close-Open colleague")
    close_open_hddg_role=fields.Boolean(string="Close-Open hddg")



class HrAppraisalPeriod(models.Model):
    _name = 'hr.appraisal.period'
    _description = 'HR Appraisal Period'
    name = fields.Char(string='Tên')

    description = fields.Char(string='Ghi chú')
    from_date = fields.Date(string='Từ ngày')
    to_date = fields.Date(string='Đến ngày')
    period_state = fields.Selection([('open', 'Open'), ('process', 'Process'), ('finish', 'Finish')], default='open')


class HR_Survey_User_Input(models.Model):
    _name = 'hr.survey.user.input'
    _description = 'HR Survey User Input'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # TKK add _order [company_code, department_id, job_position_id and s_identification_id]
    _order = 'company_code, department_code, job_code, s_identification_id'



    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     if self._context.get('get_short_name'):
    #         new_args=[]
    #         for arg in args:
    #             if arg[0]=='company_id':
    #                 if type( arg[2])== str:
    #                     result=self.env['res.company'].sudo().search([('short_name','ilike',arg[2])])
    #                     arg=['company_id','in',result.ids]
    #             new_args.append(arg)
    #         return super(HR_Survey_User_Input, self).search(new_args, offset=offset,
    #                                                      limit=limit, order=order,
    #                                                      count=count)
    #     else:
    #         return super(HR_Survey_User_Input, self).search(args, offset=offset,
    #                                                         limit=limit, order=order,
    #                                                         count=count)
    # @api.model
    # def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    #     if self._context.get('get_short_name'):
    #         new_domain=[]
    #         for arg in domain:
    #             if arg[0]=='company_id' and arg[1]=='ilike':
    #                 result = self.env['res.company'].sudo().search([('short_name', 'ilike', arg[2])])
    #                 arg = ['company_id', 'in', result.ids]
    #             new_domain.append(arg)
    #         return super(HR_Survey_User_Input, self).read_group(domain=new_domain, fields=fields,groupby=groupby, offset=offset, limit=limit, orderby=orderby,lazy=lazy)
    #     else:
    #         return super(HR_Survey_User_Input, self).read_group(domain=domain, fields=fields, groupby=groupby, offset=offset, limit=limit, orderby=orderby,
    #                                                             lazy=lazy)
    def _compute_manager_role_name(self):
        for rec in self:
            if rec.user_id.id == self.env.user.id:
                rec.manager_role_name = 'Tự đánh giá'
            elif rec.user_manager_id.id == self.env.user.id:
                rec.manager_role_name = 'QLTT'
            elif rec.user_smanager_id.id == self.env.user.id:
                rec.manager_role_name = 'Cấp trên QLTT'
            elif rec.user_colleague_id.id == self.env.user.id:
                rec.manager_role_name = 'Đồng nghiệp'
            elif rec.user_colleague2_id.id == self.env.user.id:
                rec.manager_role_name = 'Đồng nghiệp'
            elif rec.user_colleague3_id.id == self.env.user.id:
                rec.manager_role_name = 'Đồng nghiệp'
            else:
                rec.manager_role_name = 'Không có vai trò đánh giá'

    manager_role_name = fields.Char(string='Vai trò đánh giá', compute='_compute_manager_role_name')


    def _compute_job_code_compute(self):
        for rec in self:
            rec.sudo().write({'job_code': rec.job_position_id.sudo().sequence})
            rec.sudo().write({'department_code': rec.department_id.sudo().sort_name})
            rec.sudo().write({'company_code': rec.company_id.sudo().code})

    job_code_compute = fields.Char(compute='_compute_job_code_compute')
    job_code = fields.Char(string='Job Code')
    department_code = fields.Char(string='Department Code')
    company_code = fields.Char(string='Company Code')
    # job_code = fields.Char(string='Job Code', related='job_position_id.sequence', store=True)
    # department_code = fields.Char(string='Department Code', related='department_id.sort_name', store=True)
    # company_code = fields.Char(string='Company Code', related='company_id.code', store=True)

    name = fields.Char(string='Họ Và Tên')
    appraisal_name = fields.Char(string='Bảng Đánh Giá.')
    appraisal_id = fields.Many2one('hr.appraisal', string='Bảng Đánh Giá')
    def nhansu_status_action(self):
        if not self.nhansu_status:
            self.nhansu_status = True
            self.activity_schedule(
                'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type',
                user_id=self.user_manager_id.id)
        else:
            self.nhansu_status = False
        self.set_user_input_status()

    nhansu_status = fields.Boolean(string='Trạng Thái NS', default=False)

    def _compute_nhansu_status_name(self):
        for rec in self:
            if rec.nhansu_status:
                rec.nhansu_status_name = "Đã Hoàn Thành"
            else:
                rec.nhansu_status_name = "Đang Tiến Hành"

    nhansu_status_name = fields.Char(string='Trạng Thái Nhân Sự.', compute="_compute_nhansu_status_name")

    def manager_status_action(self):
        if not self.manager_status:
            self.manager_status = True
        else:
            self.manager_status = False
        self.set_user_input_status()

    def _compute_manager_status_name(self):
        for rec in self:
            if rec.manager_status:
                rec.manager_status_name = "Đã Hoàn Thành"
            else:
                rec.manager_status_name = "Đang Tiến Hành"

    manager_status_name = fields.Char(string='Trạng Thái QLTT.', compute="_compute_manager_status_name")
    manager_status = fields.Boolean(string='Trạng Thái QLTT', default=False)

    def smanager_status_action(self):
        for rec in self:
            if not rec.smanager_status:
                rec.smanager_status = True
            else:
                rec.smanager_status = False
            rec.set_user_input_status()

    smanager_status = fields.Boolean(string='Trạng Thái Cấp Trên QLTT', default=False)

    def _compute_smanager_status_name(self):
        for rec in self:
            if rec.smanager_status:
                rec.smanager_status_name = "Đã Hoàn Thành"
            else:
                rec.smanager_status_name = "Đang Tiến Hành"

    smanager_status_name = fields.Char(string='Trạng Thái Cấp Trên QLTT.', compute="_compute_smanager_status_name")

    def hddg_status_action(self):
        for rec in self:
            if not rec.hddg_status:
                rec.hddg_status = True
            else:
                rec.hddg_status = False
            rec.set_user_input_status()

    hddg_status = fields.Boolean(string='Trạng Thái HĐĐG', default=False)

    employee_ids = fields.Many2many('hr.employee')

    employee_id = fields.Many2one('hr.employee', string='Nhân Viên', ondelete='cascade')
    appraisal_period = fields.Many2one('hr.appraisal.period', string='Period', ondelete='cascade')
    survey_id = fields.Many2one('hr.survey', string='Survey')

    company_id = fields.Many2one('res.company', string='Công Ty', ondelete='cascade',
                                 default=lambda self: self.env.user.company_id.id)
    manager_id = fields.Many2one('hr.employee', string='QLTT', ondelete='cascade')
    smanager_id = fields.Many2one('hr.employee', string="Cấp Trên QLTT", ondelete='cascade')
    hddg = fields.Many2one('hr.employee', string="HĐĐG", ondelete='cascade')
    colleague_id = fields.Many2one('hr.employee', string="Đồng Nghiệp",
                                   ondelete='cascade')

    @api.onchange('employee_multi_id')
    def _onchange_employee_multi_id(self):
        pass

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string='Nhân Viên')
    s_identification_id=fields.Char(string="SeaCode",related='employee_multi_id.s_identification_id')
    s_identification_id_manager=fields.Char(string="SeaCode",related='manager_multi_id.s_identification_id')
    s_identification_id_smanager=fields.Char(string="SeaCode",related='smanager_multi_id.s_identification_id')
    manager_multi_id = fields.Many2one('hr.employee.multi.company', string='QLTT',
                                       domain="[('company_id','=',company_id)]")
    smanager_multi_id = fields.Many2one('hr.employee.multi.company', string='Cấp Trên QLTT',
                                        domain="[('company_id','=',company_id)]")
    colleague_multi_id = fields.Many2one('hr.employee.multi.company', string='Đồng Nghiệp 1')
    colleague2_multi_id = fields.Many2one('hr.employee.multi.company', string='Đồng Nghiệp 2')
    colleague3_multi_id = fields.Many2one('hr.employee.multi.company', string='Đồng Nghiệp 3')

    def _compute_role(self):
        # for rec in self:
        #     emp = self.env['hr.employee'].sudo().search([('id', '=', rec.colleague_id.id)])
        #     if emp:
        #         if emp.user_id.id == self.env.user.id:
        #             rec.appraisal_role = 'colleague'
        #     emp = self.env['hr.employee'].sudo().search([('id', '=', rec.smanager_id.id)])
        #     if emp:
        #         if emp.user_id.id == self.env.user.id:
        #             rec.appraisal_role = 'smanager'
        #     emp = self.env['hr.employee'].sudo().search([('id', '=', rec.manager_id.id)])
        #     if emp:
        #         if emp.user_id.id == self.env.user.id:
        #             rec.appraisal_role = 'manager'
        for rec in self:
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague_multi_id.id)])
            emp2 = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague2_multi_id.id)])
            emp3 = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague3_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    rec.appraisal_role = 'colleague'
            if emp2:
                if emp2.user_id.id == self.env.user.id:
                    rec.appraisal_role = 'colleague2'
            if emp3:
                if emp3.user_id.id == self.env.user.id:
                    rec.appraisal_role = 'colleague3'

            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.smanager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    rec.appraisal_role = 'smanager'
            emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.manager_multi_id.id)])
            if emp:
                if emp.user_id.id == self.env.user.id:
                    rec.appraisal_role = 'manager'
    appraisal_role = fields.Char(string='role', default='', compute='_compute_role')

    def _compute_employee_name(self):
        for rec in self:
            # employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
            # for employee in employees:
            #     rec.employee_name = employee.name
            employees = self.env['hr.employee.multi.company'].sudo().search(
                [('id', '=', rec.employee_multi_id.id), ('active', 'in', [True, False])])

            for employee in employees:
                if employee.name:
                    rec.employee_name = employee.name.sudo().name

    employee_name = fields.Char(string='Họ Và Tên.', ondelete='cascade', compute='_compute_employee_name')

    def _compute_manager_name(self):
        # for rec in self:
        #     employees = self.env['hr.employee'].sudo().search([('id', '=', rec.manager_id.id)])
        #     for employee in employees:
        #         rec.manager_name = employee.name
        for rec in self:
            if rec.manager_multi_id:
                employees = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', rec.manager_multi_id.id), ('active', 'in', [True, False])])
                for employee in employees:
                    if employee.name:
                        rec.manager_name = employee.name.sudo().name

    manager_name = fields.Char(string='Người Quản Lý Trực Tiếp (QLTT)', ondelete='cascade',
                               compute='_compute_manager_name')

    def _compute_smanager_name(self):
        # for rec in self:
        #     employees = self.env['hr.employee'].sudo().search([('id', '=', rec.smanager_id.id)])
        #     for employee in employees:
        #         rec.smanager_name = employee.name
        for rec in self:
            if rec.smanager_multi_id:
                employees = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', rec.smanager_multi_id.id), ('active', 'in', [True, False])])
                for employee in employees:
                    if employee.name:
                        rec.smanager_name = employee.name.sudo().name

    smanager_name = fields.Char(string='Cấp Trên Quản Lý Trực Tiếp (Cấp Trên QLTT)', ondelete='cascade',
                                compute='_compute_smanager_name')

    # @api.multi
    # @api.depends('employee_id')
    # def _compute_job_position(self):
    #     for rec in self:
    #         employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
    #         for employee in employees:
    #             jobs = self.env['hr.job'].sudo().search([('id', '=', employee.job_id.id)])
    #             for job in jobs:
    #                 rec.job_position = job.name

    @api.multi
    @api.depends('employee_multi_id')
    def _compute_job_position(self):
        for rec in self:
            # if rec.employee_multi_id:
            #     employees = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)])
            #     for employee in employees:
            #         if employee.job_id:
            #             jobs = self.env['hr.job'].sudo().search([('id', '=', employee.job_id.id)])
            #             if jobs:
            #                 for job in jobs:
            #                     rec.job_position = job.name
            if rec.job_position_id:
                rec.job_position = rec.job_position_id.sudo().name

    job_position = fields.Char(string='Chức Vụ', compute='_compute_job_position')
    job_position_id = fields.Many2one('hr.job', string='Chức Vụ')

    def compute_manager_job_position(self):
        for rec in self:
            manager_user_input = rec.env['hr.survey.user.input'].sudo().search(
                [('appraisal_id', '=', rec.appraisal_id.id), ('employee_multi_id', '=', rec.manager_multi_id.id)],
                limit=1)

            rec.manager_job_position = manager_user_input.job_position_id.sudo().name

    manager_job_position = fields.Char(string='Chức Vụ QLTT', compute="compute_manager_job_position")

    def compute_smanager_job_position(self):
        for rec in self:
            smanager_user_input = rec.env['hr.survey.user.input'].sudo().search(
                [('appraisal_id', '=', rec.appraisal_id.id), ('employee_multi_id', '=', rec.smanager_multi_id.id)],
                limit=1)
            rec.smanager_job_position = smanager_user_input.job_position_id.sudo().name

    smanager_job_position = fields.Char(string='Chức Vụ Cấp trên QLTT', compute="compute_smanager_job_position")

    def _compute_from_date(self):
        for rec in self:
            appraisals = self.env['hr.appraisal'].sudo().search([('id', '=', rec.appraisal_id.id)])
            for appraisal in appraisals:
                period = self.env['hr.appraisal.period'].sudo().search([('id', '=', appraisal.appraisal_period.id)])
                if period:
                    rec.period_fromdate = period.from_date

    period_fromdate = fields.Char(string='Period Name', compute=_compute_from_date)

    def _compute_period_name(self):
        for rec in self:
            appraisals = self.env['hr.appraisal'].sudo().search([('id', '=', rec.appraisal_id.id)])
            for appraisal in appraisals:
                period = self.env['hr.appraisal.period'].sudo().search([('id', '=', appraisal.appraisal_period.id)])
                if period:
                    rec.period_name = period.name

    period_name = fields.Char(string='Từ Ngày', compute=_compute_period_name)

    def _compute_to_date(self):
        for rec in self:
            appraisals = self.env['hr.appraisal'].sudo().search([('id', '=', rec.appraisal_id.id)])
            for appraisal in appraisals:
                period = self.env['hr.appraisal.period'].sudo().search([('id', '=', appraisal.appraisal_period.id)])
                if period:
                    rec.period_todate = period.from_date

    period_todate = fields.Char(string='Đến Ngày', compute=_compute_to_date)
    department_id = fields.Many2one('hr.department', string='Đơn Vị')
    operating_unit_id = fields.Many2one('operating.unit', 'Đơn Vị Hoạt Động')

    # ------------------------------------------------------------------------------------------------------------
    # @api.multi
    # @api.depends('employee_id')
    # def _compute_department_name(self):
    #     for rec in self:
    #         rec.department_name = rec.department_id.name

    @api.multi
    @api.depends('employee_multi_id')
    # department cố định để khi đóng đánh giá thì thay đổi department của employee cũng sẽ khôn đổi
    def _compute_department_name(self):
        for rec in self:
            if rec.department_id:
                rec.department_name = rec.department_id.sudo().name

    department_name = fields.Char(string='Đơn Vị', compute='_compute_department_name')

    @api.multi
    @api.depends('employee_multi_id')
    def _compute_operating_unit_name(self):
        for rec in self:
            if rec.operating_unit_id:
                rec.operating_unit_name = rec.operating_unit_id.sudo().name

    operating_unit_name = fields.Char(string='Đơn Vị', compute='_compute_operating_unit_name')

    def _compute_department_compute(self):
        # for rec in self:
        #     employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
        #     for employee in employees:
        #         departments = self.env['hr.department'].sudo().search([('id', '=', employee.department_id.id)])
        #         for department in departments:
        #             rec.department_compute = department.id
        for rec in self:
            if rec.department_id:
                rec.department_compute = rec.department_id

    department_compute = fields.Many2one('hr.department', string='Đơn Vị ID.', compute='_compute_department_compute')

    def _compute_operating_unit_compute(self):
        for rec in self:
            if rec.operating_unit_id:
                rec.operating_unit_compute = rec.operating_unit_id

    operating_unit_compute = fields.Many2one('operating.unit', 'Đơn Vị Hoạt Động',
                                             compute='_compute_operating_unit_compute')

    def _compute_job_position_sequence(self):
        # for rec in self:
        #     employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
        #     for employee in employees:
        #         jobs = self.env['hr.job'].sudo().search([('id', '=', employee.job_id.id)])
        #         for job in jobs:
        #             rec.job_position_sequence = job.sequence

        for rec in self:
            if rec.job_position_id:
                rec.job_position_sequence = rec.job_position_id.sequence

    job_position_sequence = fields.Char(string='Sequence', compute='_compute_job_position_sequence')

    def _compute_user_id_compute(self):
        for rec in self:
            if rec.employee_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.user_id_compute = user_id
            # if rec.employee_multi_id:
            #     user_id = rec.employee_multi_id.user_id.id
            #     if user_id:
            #         rec.user_id_compute = user_id

    user_id_compute = fields.Integer(string='User', ondelete='cascade', compute='_compute_user_id_compute')

    def _compute_manager_user_id_compute(self):

        for rec in self:
            if rec.manager_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.manager_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.manager_user_id_compute = user_id
        # for rec in self:
        #     if rec.manager_multi_id:
        #         user_id = rec.manager_multi_id.user_id.id
        #         if user_id:
        #             rec.manager_user_id_compute = user_id

    manager_user_id_compute = fields.Integer(string='User', ondelete='cascade',
                                             compute='_compute_manager_user_id_compute')

    def _compute_smanager_user_id_compute(self):
        for rec in self:
            if rec.smanager_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.smanager_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.smanager_user_id_compute = user_id
        # for rec in self:
        #     if rec.smanager_multi_id:
        #         user_id = rec.smanager_multi_id.user_id.id
        #         if user_id:
        #             rec.smanager_user_id_compute = user_id

    smanager_user_id_compute = fields.Integer(string='User', ondelete='cascade',
                                              compute='_compute_smanager_user_id_compute')

    def _compute_colleague_user_id_compute(self):
        for rec in self:
            if rec.colleague_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.colleague_user_id_compute = user_id

    colleague_user_id_compute = fields.Integer(string='User', ondelete='cascade',
                                               compute='_compute_colleague_user_id_compute')

    def _compute_colleague2_user_id_compute(self):
        for rec in self:
            if rec.colleague2_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague2_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.colleague2_user_id_compute = user_id
        # for rec in self:
        #     if rec.colleague_multi_id:
        #         user_id = rec.colleague_multi_id.user_id.id
        #         if user_id:
        #             rec.colleague_user_id_compute = user_id

    colleague2_user_id_compute = fields.Integer(string='User', ondelete='cascade',
                                               compute='_compute_colleague2_user_id_compute')

    def _compute_colleague3_user_id_compute(self):
        for rec in self:
            if rec.colleague3_multi_id:
                user_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.colleague3_multi_id.id)],
                                                                              limit=1).user_id.id
                if user_id:
                    rec.colleague3_user_id_compute = user_id
        # for rec in self:
        #     if rec.colleague_multi_id:
        #         user_id = rec.colleague_multi_id.user_id.id
        #         if user_id:
        #             rec.colleague_user_id_compute = user_id

    colleague3_user_id_compute = fields.Integer(string='User', ondelete='cascade',
                                               compute='_compute_colleague3_user_id_compute')

    user_id = fields.Many2one('res.users', string='User', ondelete='cascade')
    user_manager_id = fields.Many2one('res.users', string='User QLTT', ondelete='cascade')
    user_smanager_id = fields.Many2one('res.users', string="User CẤP TRÊN QLTT", ondelete='cascade')
    hddg_user = fields.Many2one('res.users', string="User HĐĐG", ondelete='cascade')
    user_colleague_id = fields.Many2one('res.users', string="Đồng nghiệp user 1", ondelete='cascade')
    user_colleague2_id = fields.Many2one('res.users', string="Đồng nghiệp user 2", ondelete='cascade')
    user_colleague3_id = fields.Many2one('res.users', string="Đồng nghiệp user 3", ondelete='cascade')

    def _compute_is_manager(self):
        # for rec in self:
        #     employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
        #     if employees:
        #         rec.is_manager = employees.manager
        for rec in self:
            if rec.employee_multi_id:
                employees = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)])
                if employees:
                    if employees:
                        rec.is_manager = employees.manager

    is_manager = fields.Boolean(string='Is Manager', compute='_compute_is_manager')
    user_opinion = fields.Text(string='Ý Kiến Người Được Đánh Giá')
    manager_opinion = fields.Text(string='Ý Kiến QLTT')
    smanager_opinion = fields.Text(string='Ý Kiến Cấp Trên QLTT')
    hddg_opinion = fields.Text(string='Ý Kiến HĐĐG')
    colleague_opinion = fields.Text(string='Ý Kiến Đồng Nghiệp')
    colleague2_opinion = fields.Text(string='Ý Kiến Đồng Nghiệp 2')
    colleague3_opinion = fields.Text(string='Ý Kiến Đồng Nghiệp 3')
    dexuat_salary_user = fields.Float(string='NS Đề Xuất Lương')
    dexuat_thuong_user = fields.Float(string='NS Đề Xuất Thưởng')
    dexuat_chucvu_user = fields.Char(string='NS Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_user = fields.Text(string='NS Đề Xuất Thuyên Chuyển')

    dexuat_salary_manager = fields.Float(string='QLTT Đề Xuất Lương')
    dexuat_thuong_manager = fields.Float(string='QLTT Đề Xuất Thưởng')
    dexuat_chucvu_manager = fields.Char(string='QLTT Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_manager = fields.Text(string='QLTT Đề Xuất Thuyên Chuyển')

    dexuat_salary_smanager = fields.Float(string='Cấp Trên QLTT Đề Xuất Lương')
    dexuat_thuong_smanager = fields.Float(string='Cấp Trên QLTT Đề Xuất Thưởng')
    dexuat_chucvu_smanager = fields.Char(string='Cấp Trên QLTT Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_smanager = fields.Text(string='Cấp Trên QLTT Đề Xuất Thuyên Chuyển')

    dexuat_salary_hddg = fields.Float(string='HĐĐG Đề Xuất Lương')
    dexuat_thuong_hddg = fields.Float(string='HĐĐG Đề Xuất Thưởng')
    dexuat_chucvu_hddg = fields.Char(string='HĐĐG Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_hddg = fields.Text(string='HĐĐG Đề Xuất Thuyên Chuyển')

    dexuat_salary_colleague = fields.Float(string='Đồng Nghiệp Đề Xuất Lương')
    dexuat_thuong_colleague = fields.Float(string='Đồng Nghiệp Đề Xuất Thưởng')
    dexuat_chucvu_colleague = fields.Char(string='Đồng Nghiệp Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_colleague = fields.Text(string='Đồng Nghiệp Đề Xuất Thuyên Chuyển')

    dexuat_salary_colleague2 = fields.Float(string='Đồng Nghiệp Đề Xuất Lương')
    dexuat_thuong_colleague2 = fields.Float(string='Đồng Nghiệp Đề Xuất Thưởng')
    dexuat_chucvu_colleague2 = fields.Char(string='Đồng Nghiệp Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_colleague2 = fields.Text(string='Đồng Nghiệp Đề Xuất Thuyên Chuyển')

    dexuat_salary_colleague3 = fields.Float(string='Đồng Nghiệp Đề Xuất Lương')
    dexuat_thuong_colleague3 = fields.Float(string='Đồng Nghiệp Đề Xuất Thưởng')
    dexuat_chucvu_colleague3 = fields.Char(string='Đồng Nghiệp Đề Xuất Chức Vụ')
    dexuat_thuyenchuyen_colleague3 = fields.Text(string='Đồng Nghiệp Đề Xuất Thuyên Chuyển')

    rating1_value = fields.Char(string='NS', default='KK')
    rating2_value = fields.Char(string='QLTT', default='KK')
    rating3_value = fields.Char(string='Cấp Trên QLTT', default='KK')
    rating4_value = fields.Char(string='HDDG', default='KK')
    rating5_value = fields.Char(string='Đồng Nghiệp 1', default='KK')
    rating6_value = fields.Char(string='Đồng Nghiệp 2', default='KK')
    rating7_value = fields.Char(string='Đồng Nghiệp 3', default='KK')

    def _compute_rating4_value_compute(self):
        for rec in self:
            if rec.rating4_value:
                rec.rating4_value_compute = rec.rating4_value
            else:
                rec.rating4_value_compute = 'KK'

    rating4_value_compute = fields.Char(string='HDDG', compute='_compute_rating4_value_compute')

    def _compute_sc_code(self):
        for rec in self:
            if rec.employee_multi_id:
                e = self.env['hr.employee'].sudo().search(
                    [('id', '=', rec.employee_multi_id.sudo().name.id), '|', ('active', '=', False),
                     ('active', '=', True)])
                if e:
                    rec.sc_code = e.s_identification_id

    sc_code = fields.Char(string="Mã số NV", compute='_compute_sc_code')
    # s_identification_id = fields.Char(string='SC Code', default='')
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)

    def _compute_seagroup_join_date(self):
        for rec in self:
            if rec.employee_multi_id:
                e = self.env['hr.employee'].sudo().search(
                    [('id', '=', rec.employee_multi_id.sudo().name.id), '|', ('active', '=', False),
                     ('active', '=', True)])
                if e.seagroup_join_date:
                    rec.seagroup_join_date = e.seagroup_join_date.strftime("%d/%m/%Y")

    seagroup_join_date = fields.Char(string="Ngày Vào SEACORP", compute='_compute_seagroup_join_date')

    def _compute_official_contract(self):
        for rec in self:
            if rec.employee_multi_id:
                e = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)])
                if e.name:
                    contract = self.env['hr.contract'].sudo().search(
                        [('employee_id', '=', e.name.id), ('active', '=', True), ('company_id', '=', e.company_id.id),
                         ('date_start', '<=', rec.appraisal_period.sudo().to_date.strftime('%Y-%m-%d')), ('state', '!=', 'cancel'),
                         ('type_id', '=', 1), ('contract_category', '=', 'contract')],
                        order="date_start desc",
                        limit=1)
                    if contract:
                        rec.official_contract = contract.date_start.strftime("%d/%m/%Y")
                    else:
                        rec.official_contract = ''

    official_contract = fields.Char(string="Ngày HĐ", compute='_compute_official_contract')

    def _compute_contract_type(self):
        for rec in self:
            if rec.employee_multi_id:
                e = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)])
                if e.name:
                    # employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
                    contracts = self.env['hr.contract'].sudo().search(
                        [('employee_id', '=', e.sudo().name.id), ('active', '=', True),
                         ('company_id', '=', e.company_id.id), ('state', '!=', 'cancel'),
                         ('date_start', '<=', rec.appraisal_period.sudo().to_date.strftime('%Y-%m-%d')),
                         ('contract_category', '=', 'contract')],
                        order="date_start desc",
                        limit=1)
                    for contract in contracts:
                        if contract:
                            rec.contract_type = contract.type_id

    contract_type = fields.Many2one('hr.contract.type', string="Loại HĐ", compute='_compute_contract_type')

    def _compute_contract_period(self):
        for rec in self:
            if rec.employee_multi_id:
                e = self.env['hr.employee.multi.company'].sudo().search([('id', '=', rec.employee_multi_id.id)])
                if e.name:
                    # employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
                    contract = self.env['hr.contract'].sudo().search(
                        [('employee_id', '=', e.name.id), ('active', '=', True), ('company_id', '=', e.company_id.id),
                         ('date_start', '<=', rec.appraisal_period.sudo().to_date.strftime('%Y-%m-%d')), ('state', '!=', 'cancel'),
                         ('type_id', '=', 1), ('contract_category', '=', 'contract')],
                        order="date_start desc",
                        limit=1)
                    if contract:
                        rec.contract_period = contract.contract_period_id.sudo().name
                    else:
                        rec.contract_period = ''

    contract_period = fields.Char(string="Thời hạn HĐ.", compute="_compute_contract_period")

    def _compute_user_seacorp(self):
        for rec in self:
            input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                [('user_input_id', '=', rec.id), ('question_name', 'like', '%SEACORP%'),
                 ('summary_level_report', '=', 1)])
            if input_lines:
                rec.user_seacorp = input_lines.value
                rec.manager_seacorp = input_lines.value_manager
                rec.smanager_seacorp = input_lines.value_smanager
                rec.colleague_seacorp = input_lines.value_colleague
                rec.colleague2_seacorp = input_lines.value_colleague2
                rec.colleague3_seacorp = input_lines.value_colleague3
                rec.hddg_seacorp = input_lines.value_hddg

    user_seacorp = fields.Char(string='SC', compute='_compute_user_seacorp')

    def _compute_user_kpi(self):
        for rec in self:
            input_lines = self.env['hr.survey.user.input.line'].sudo().search(
                [('user_input_id', '=', rec.id), ('question_name', 'like', '%KPI%'), ('summary_level_report', '=', 1)])
            if input_lines:
                rec.user_kpi = input_lines.value
                rec.manager_kpi = input_lines.value_manager
                rec.smanager_kpi = input_lines.value_smanager
                rec.hddg_kpi = input_lines.value_hddg

    user_kpi = fields.Char(string='KPI', compute='_compute_user_kpi')

    def _compute_manager_seacorp(self):
        pass

    manager_seacorp = fields.Char(string='SC', compute='_compute_manager_seacorp')

    def _compute_manager_kpi(self):
        pass

    manager_kpi = fields.Char(string='KPI', compute='_compute_manager_kpi')

    def _compute_smanager_seacorp(self):
        pass

    smanager_seacorp = fields.Char(string='SC', compute='_compute_smanager_seacorp')

    def _compute_smanager_kpi(self):
        pass

    smanager_kpi = fields.Char(string='KPI', compute='_compute_smanager_kpi')

    def _compute_colleague_seacorp(self):
        pass

    colleague_seacorp = fields.Char(string='SC', compute='_compute_colleague_seacorp')

    def _compute_colleague2_seacorp(self):
        pass

    colleague2_seacorp = fields.Char(string='SC', compute='_compute_colleague2_seacorp')

    def _compute_colleague3_seacorp(self):
        pass

    colleague3_seacorp = fields.Char(string='SC', compute='_compute_colleague3_seacorp')

    def _compute_hddg_seacorp(self):
        pass

    hddg_seacorp = fields.Char(string='SC', compute='_compute_hddg_seacorp')

    def _compute_hddg_kpi(self):
        pass

    hddg_kpi = fields.Char(string='KPI', compute='_compute_hddg_kpi')

    def split_word(self, word):
        return [char for char in word]

    def _compute_achievement_name(self):
        for rec in self:
            if rec.rating1_value:
                pass

    achievement_name = fields.Char(string='Thành Tích NS', compute='_compute_achievement_name')

    rating1_achievements = fields.Char(string='Thành Tích Do NS ĐG', default='KK')
    rating2_achievements = fields.Char(string='Thành Tích Do QLTT ĐG', default='KK')
    rating3_achievements = fields.Char(string='Thành Tích Do Cấp Trên QLTT ĐG', default='KK')
    rating4_achievements = fields.Char(string='Thành Tích Do HDDG ĐG', default='KK')
    rating5_achievements = fields.Char(string='Thành Tích Đồng Nghiệp ĐG', default='KK')
    rating6_achievements = fields.Char(string='Thành Tích Đồng Nghiệp ĐG', default='KK')
    rating7_achievements = fields.Char(string='Thành Tích Đồng Nghiệp ĐG', default='KK')

    de_xuat_dg_tai_hddg_user = fields.Boolean(string='NS Đề Xuất Đánh Giá Tại HĐĐG ')
    de_xuat_lydo_user = fields.Char(string='Lý Do')
    de_xuat_dg_tai_hddg_manager = fields.Boolean(string='QLTT Đề Xuất HĐĐG')
    de_xuat_lydo_manager = fields.Char(string='Lý Do')
    de_xuat_dg_tai_hddg_smanager = fields.Boolean(string='Cấp Trên QLTT Đề Xuất Đánh Giá Tại HĐĐG')
    de_xuat_lydo_smanager = fields.Char(string='Lý Do')
    de_xuat_dg_tai_hddg_colleague = fields.Boolean(string='Đồng Nghiệp Đề Xuất Đánh Giá Tại HĐĐG')
    de_xuat_lydo_colleague = fields.Char(string='Lý Do')
    de_xuat_dg_tai_hddg_colleague2 = fields.Boolean(string='Đồng Nghiệp Đề Xuất Đánh Giá Tại HĐĐG')
    de_xuat_lydo_colleague2 = fields.Char(string='Lý Do')
    de_xuat_dg_tai_hddg_colleague3 = fields.Boolean(string='Đồng Nghiệp Đề Xuất Đánh Giá Tại HĐĐG')
    de_xuat_lydo_colleague3 = fields.Char(string='Lý Do')

    question_general = fields.One2many('hr.survey.user.input.line', 'question_general', copy=True)
    questions_1 = fields.One2many('hr.survey.user.input.line', 'question_1', copy=True)
    questions_2 = fields.One2many('hr.survey.user.input.line', 'question_2', copy=True)
    questions_3 = fields.One2many('hr.survey.user.input.line', 'question_3', copy=True)
    questions_4 = fields.One2many('hr.survey.user.input.line', 'question_4', copy=True)
    questions_5 = fields.One2many('hr.survey.user.input.line', 'question_5', copy=True)
    questions_6 = fields.One2many('hr.survey.user.input.line', 'question_6', copy=True)
    questions_7 = fields.One2many('hr.survey.user.input.line', 'question_7', copy=True)
    questions_8 = fields.One2many('hr.survey.user.input.line', 'question_8', copy=True)
    questions_9 = fields.One2many('hr.survey.user.input.line', 'question_9', copy=True)
    questions_10 = fields.One2many('hr.survey.user.input.line', 'question_10', copy=True)

    ct_luong = fields.Float(string='LƯƠNG')
    ct_thuong = fields.Float(string='THƯỞNG')
    ct_thuyenchuyen = fields.Text(string='ĐIỀU CHUYỂN/QUY HOẠCH')
    ct_other = fields.Text(string='KHÁC')

    ct_seacorp = fields.Char(string='SC')
    ct_kpi = fields.Char(string='KPI')
    ct_xl = fields.Text(string='XL')
    ct_xetduyet = fields.Boolean(string='Duyệt', default=False)

    ghichu_dexuat_sau_dgns = fields.Text(string='Ghi Chú')
    ghichu_ket_qua_dgns = fields.Text(string='Ghi Chú.')

    def _compute_dieuchuyen_quyhoach_user(self):
        for rec in self:
            if rec.dexuat_chucvu_user:
                rec.dieuchuyen_quyhoach_user = rec.dexuat_chucvu_user
            elif rec.dexuat_thuyenchuyen_user:
                if not rec.dieuchuyen_quyhoach_user:
                    rec.dieuchuyen_quyhoach_user=''
                rec.dieuchuyen_quyhoach_user += ' ' + rec.dexuat_thuyenchuyen_user

            if rec.dexuat_chucvu_manager:
                rec.dieuchuyen_quyhoach_manager = rec.dexuat_chucvu_manager
            elif rec.dexuat_thuyenchuyen_manager:
                if not rec.dieuchuyen_quyhoach_manager:
                    rec.dieuchuyen_quyhoach_manager=''
                rec.dieuchuyen_quyhoach_manager += ' ' + rec.dexuat_thuyenchuyen_manager

            if rec.dexuat_chucvu_smanager:
                rec.dieuchuyen_quyhoach_smanager = rec.dexuat_chucvu_smanager
            elif rec.dexuat_thuyenchuyen_smanager:
                if not rec.dieuchuyen_quyhoach_smanager:
                    rec.dieuchuyen_quyhoach_smanager=''
                rec.dieuchuyen_quyhoach_smanager += ' ' + rec.dexuat_thuyenchuyen_smanager

            if rec.dexuat_chucvu_hddg:
                rec.dieuchuyen_quyhoach_hddg = rec.dexuat_chucvu_hddg
            elif rec.dexuat_thuyenchuyen_hddg:
                if not rec.dieuchuyen_quyhoach_hddg:
                    rec.dieuchuyen_quyhoach_hddg=''
                rec.dieuchuyen_quyhoach_hddg += ' ' + rec.dexuat_thuyenchuyen_hddg

    dieuchuyen_quyhoach_user = fields.Char(compute='_compute_dieuchuyen_quyhoach_user')

    def _compute_dieuchuyen_quyhoach_manager(self):
        pass

    dieuchuyen_quyhoach_manager = fields.Char(compute='_compute_dieuchuyen_quyhoach_manager')

    def _compute_dieuchuyen_quyhoach_smanager(self):
        pass

    dieuchuyen_quyhoach_smanager = fields.Char(compute='_compute_dieuchuyen_quyhoach_smanager')

    def _compute_dieuchuyen_quyhoach_hddg(self):
        pass

    dieuchuyen_quyhoach_hddg = fields.Char(compute='_compute_dieuchuyen_quyhoach_hddg')

    '''lock_state=True là được đánh giá'''
    '''lock_state=False là không được đánh giá'''

    def lock_appraisal(self):
        if self.lock_state == 'yes':
            self.lock_state = 'no'
            self.user_input_status = 'khong_danh_gia'
            self.lock_state_compute = False
        else:
            self.lock_state = 'yes'
            self.lock_state_compute = True
            self.set_user_input_status()

    @api.model
    @api.onchange('lock_state')
    def _onchange_lock_state(self):
        if self.lock_state == 'no':
            user_input = self.env['hr.survey.user.input'].sudo().search([('id', '=', self._origin.id)])
            if user_input:
                user_input.sudo().write({'user_input_status': 'khong_danh_gia'})
        else:
            user_input = self.env['hr.survey.user.input'].sudo().search([('id', '=', self._origin.id)])
            if user_input:
                user_input.sudo().write({'user_input_status': 'dang_tien_hanh'})

    lock_state = fields.Selection([('yes', 'Có'), ('no', 'Không')], string='Đủ Điều Kiện ĐG', default='yes')
    reason_lock = fields.Text(string="Lý Do Không Đánh Giá")

    def _compute_lock_state_compute(self):
        for rec in self:

            if rec.lock_state == 'yes':
                rec.lock_state_compute = True
            else:
                rec.lock_state_compute = False

    lock_state_compute = fields.Boolean(string="Không Đánh Giá", compute='_compute_lock_state_compute')

    def set_user_input_status(self):

        if self.lock_state:
            if self.ct_xetduyet:
                self.user_input_status = 'hoan_thanh'
            elif self.smanager_status:
                self.user_input_status = 'qlcc_da_danh_gia'
            elif self.manager_status:
                self.user_input_status = 'qltt_da_danh_gia'
            elif self.nhansu_status:
                self.user_input_status = 'ns_da_danh_gia'
            else:
                self.user_input_status = 'dang_tien_hanh'
        else:
            self.user_input_status = 'khong_danh_gia'

    user_input_status = fields.Selection(
        [('khong_danh_gia', 'Không Đánh Giá'), ('hoan_thanh', 'Đã duyệt'), ('qltt_da_danh_gia', 'QLTT Đã Đánh Giá'),
         ('ns_da_danh_gia', 'Nhân Viên Đã Đánh Giá'), ('dang_tien_hanh', 'Đang Tiến Hành'),
         ('qlcc_da_danh_gia', 'Cấp Trên QLTT Đã Đánh Giá')], default='dang_tien_hanh')
    last_displayed_page_id = fields.Many2one('hr.survey.summary', string='Last displayed page', ondelete='cascade')
    open_state = fields.Boolean(string='Trạng Thái Đóng', default=True)

    user_open_state = fields.Boolean(string='Trạng Thái Đóng User', default=True)
    manager_open_state = fields.Boolean(string='Trạng Thái Đóng Manager', default=True)
    smanager_open_state = fields.Boolean(string='Trạng Thái Đóng Smanager', default=True)
    colleague_open_state = fields.Boolean(string='Trạng Thái Đóng Colleague', default=True)
    hddg_open_state = fields.Boolean(string='Trạng Thái Đóng HDDG', default=True)

    def isNumberic(self, string):
        if string:
            try:
                float(string)
                return True
            except ValueError:
                return False
        else:
            return False

    def convertNumber(self, string):
        if string:
            try:
                a = float(string)
                return a
            except ValueError:
                return 0
        else:
            return 0

    def TinhRating(self, user_input_id):
        rating = self.env['hr.survey.user.input.line'].sudo().search(
            [('user_input_id', '=', user_input_id.id), ('is_rating', '=', True)])
        if rating:
            search_parent_sum = self.env['hr.survey.user.input.line'].sudo().search(
                [('user_input_id', '=', user_input_id.id), ('summary_id', '=', None),
                 ('is_rating', '=', False)])
            total = ""
            total_manager = ""
            total_smanager = ""
            total_hddg = ""
            total_colleague = ""
            total_colleague2 = ""
            total_colleague3 = ""
            achievement = ""
            achievement_manager = ""
            achievement_smanager = ""
            achievement_hddg = ""
            achievement_colleague = ""
            achievement_colleague2 = ""
            achievement_colleague3 = ""

            for i in search_parent_sum:
                survey_id = i.question_id.hr_survey_id.id
                value = i.value
                value_manager = i.value_manager
                value_smanager = i.value_smanager
                value_hddg = i.value_hddg
                value_colleague = i.value_colleague
                value_colleague2 = i.value_colleague2
                value_colleague3 = i.value_colleague3
                summary_id = i.question_id.id
                search_in_classification_link = self.env['hr.survey.classification.link'].sudo().search(
                    [('survey_id', '=', survey_id), ('summary_id', '=', summary_id)])
                if search_in_classification_link:
                    search_in_classification = self.env['hr.survey.classification'].sudo().search(
                        [('classification_link', '=', search_in_classification_link.id)])
                    # max score in search_in_classification
                    max_score = 0
                    name = ''
                    thanh_tich = ''
                    for find_max in search_in_classification:
                        if max_score < find_max.max_score:
                            max_score = find_max.max_score
                            name = find_max.name
                            thanh_tich = find_max.classification

                    if self.convertNumber(value) == max_score:
                        total += name
                        achievement += thanh_tich
                    if self.convertNumber(value_manager) == max_score:
                        total_manager += name
                        achievement_manager += thanh_tich
                    if self.convertNumber(value_smanager) == max_score:
                        total_smanager += name
                        achievement_smanager += thanh_tich
                    if self.convertNumber(value_hddg) == max_score:
                        total_hddg += name
                        achievement_hddg += thanh_tich
                    if self.convertNumber(value_colleague) == max_score:
                        total_colleague += name
                        achievement_colleague += thanh_tich
                    if self.convertNumber(value_colleague2) == max_score:
                        total_colleague2 += name
                        achievement_colleague2 += thanh_tich
                    if self.convertNumber(value_colleague3) == max_score:
                        total_colleague3 += name
                        achievement_colleague3 += thanh_tich
                    if not self.isNumberic(value):
                        total += 'K'
                    else:
                        for classification in search_in_classification:
                            if (float(classification.min_score) <= float(self.convertNumber(value))) and (
                                    float(self.convertNumber(value)) < classification.max_score):
                                total += classification.name
                                achievement += '-' + classification.classification
                                break

                    if not self.isNumberic(value_manager):
                        total_manager += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(self.convertNumber(value_manager)) < float(
                                    classification.max_score):
                                total_manager += classification.name
                                achievement_manager += '-' + classification.classification
                                break
                    if not self.isNumberic(value_smanager):
                        total_smanager += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(self.convertNumber(value_smanager)) < float(
                                    classification.max_score):
                                total_smanager += classification.name
                                achievement_smanager += '-' + classification.classification
                                break
                    if not self.isNumberic(value_hddg):
                        total_hddg += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(self.convertNumber(value_hddg)) < float(
                                    classification.max_score):
                                total_hddg += classification.name
                                achievement_hddg += '-' + classification.classification
                                break
                    if not self.isNumberic(value_colleague):
                        total_colleague += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(
                                    self.convertNumber(value_colleague)) < float(classification.max_score):
                                total_colleague += classification.name
                                achievement_colleague += classification.classification
                                break
                    if not self.isNumberic(value_colleague2):
                        total_colleague2 += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(
                                    self.convertNumber(value_colleague2)) < float(classification.max_score):
                                total_colleague2 += classification.name
                                achievement_colleague2 += classification.classification
                                break
                    if not self.isNumberic(value_colleague3):
                        total_colleague3 += 'K'
                    else:
                        for classification in search_in_classification:
                            if float(classification.min_score) <= float(
                                    self.convertNumber(value_colleague3)) < float(classification.max_score):
                                total_colleague3 += classification.name
                                achievement_colleague3 += classification.classification
                                break

            rating.write({'value': total})
            rating.write({'value_manager': total_manager})
            rating.write({'value_smanager': total_smanager})
            rating.write({'value_hddg': total_hddg})
            rating.write({'value_colleague': total_colleague})
            rating.write({'value_colleague2': total_colleague2})
            rating.write({'value_colleague3': total_colleague3})

            # rating.write({'user_comment': achievement})
            # rating.write({'manager_comment': achievement_manager})
            # rating.write({'smanager_comment': achievement_smanager})
            # rating.write({'hddg_comment': achievement_hddg})
            # rating.write({'colleague_comment': achievement_colleague})

            user_inputs = self.env['hr.survey.user.input'].sudo().search([('id', '=', user_input_id.id)])
            user_inputs.write({'rating1_value': total})
            user_inputs.write({'rating2_value': total_manager})
            user_inputs.write({'rating3_value': total_smanager})
            user_inputs.write({'rating4_value': total_hddg})
            user_inputs.write({'rating5_value': total_colleague})
            user_inputs.write({'rating6_value': total_colleague2})
            user_inputs.write({'rating7_value': total_colleague3})
            user_inputs.write({'rating1_achievements': achievement})
            user_inputs.write({'rating2_achievements': achievement_manager})
            user_inputs.write({'rating3_achievements': achievement_smanager})
            user_inputs.write({'rating4_achievements': achievement_hddg})
            user_inputs.write({'rating5_achievements': achievement_colleague})
            user_inputs.write({'rating6_achievements': achievement_colleague2})
            user_inputs.write({'rating7_achievements': achievement_colleague3})

    def tinh_trung_binh_v2(self, parents, giatri):
        parent_of_parents = []
        for parent in parents:
            field_sum_childs = self.env['hr.survey.summary.field.sum'].sudo().search(
                [('id_parent', '=', parent.question_id.id)])

            if field_sum_childs:
                # have_parent = False
                # parent_of_parent = self.env['hr.survey.user.input.line'].sudo().search(
                #     [('id', '=', parent.summary_id.id)])
                # for par in parent_of_parents:
                #     if par.id == parent_of_parent:
                #         have_parent = True
                # if have_parent == False:
                #     if parent_of_parent:
                #         parent_of_parents.append(parent_of_parent)

                so_lan = 0
                tong_field_sum_user = 0

                so_lan_manager = 0
                tong_field_sum_user_manager = 0

                so_lan_smanager = 0
                tong_field_sum_user_smanager = 0

                so_lan_hddg = 0
                tong_field_sum_user_hddg = 0

                so_lan_colleague = 0
                tong_field_sum_user_colleague = 0
                so_lan_colleague2 = 0
                tong_field_sum_user_colleague2 = 0
                so_lan_colleague3 = 0
                tong_field_sum_user_colleague3 = 0

                for field_sum_child in field_sum_childs:

                    childs_user_input_line = self.env[
                        'hr.survey.user.input.line'].sudo().search(
                        [('question_id', '=', field_sum_child.id_child.id),
                         ('user_input_id', '=', parent.user_input_id.id)])
                    if self.isNumberic(childs_user_input_line.value):
                        so_lan += 1
                        tong_field_sum_user += float(childs_user_input_line.value)

                    if self.isNumberic(childs_user_input_line.value_manager):
                        so_lan_manager += 1
                        tong_field_sum_user_manager += float(childs_user_input_line.value_manager)

                    if self.isNumberic(childs_user_input_line.value_smanager):
                        so_lan_smanager += 1
                        tong_field_sum_user_smanager += float(childs_user_input_line.value_smanager)

                    if self.isNumberic(childs_user_input_line.value_hddg):
                        so_lan_hddg += 1
                        tong_field_sum_user_hddg += float(childs_user_input_line.value_hddg)

                    if self.isNumberic(childs_user_input_line.value_colleague):
                        so_lan_colleague += 1
                        tong_field_sum_user_colleague += float(childs_user_input_line.value_colleague)
                    if self.isNumberic(childs_user_input_line.value_colleague2):
                        so_lan_colleague2 += 1
                        tong_field_sum_user_colleague2 += float(childs_user_input_line.value_colleague2)
                    if self.isNumberic(childs_user_input_line.value_colleague3):
                        so_lan_colleague3 += 1
                        tong_field_sum_user_colleague3 += float(childs_user_input_line.value_colleague3)
                if so_lan > 0:
                    fieldsum_value_user = float('%.2f' % (tong_field_sum_user / so_lan))
                    parent.sudo().write({'value': fieldsum_value_user})
                else:
                    parent.sudo().write({'value': 'K'})
                if so_lan_manager > 0:
                    fieldsum_value_user_manager = float('%.2f' % (tong_field_sum_user_manager / so_lan_manager))
                    parent.sudo().write({'value_manager': fieldsum_value_user_manager})
                else:
                    parent.sudo().write({'value_manager': 'K'})
                if so_lan_smanager > 0:
                    fieldsum_value_user_smanager = float('%.2f' % (tong_field_sum_user_smanager / so_lan_smanager))
                    parent.sudo().write({'value_smanager': fieldsum_value_user_smanager})
                else:
                    parent.sudo().write({'value_smanager': 'K'})
                if so_lan_hddg > 0:
                    fieldsum_value_user_hddg = float('%.2f' % (tong_field_sum_user_hddg / so_lan_hddg))
                    parent.sudo().write({'value_hddg': fieldsum_value_user_hddg})
                else:
                    parent.sudo().write({'value_hddg': 'K'})
                if so_lan_colleague > 0:
                    fieldsum_value_user_colleague = float('%.2f' % (tong_field_sum_user_colleague / so_lan_colleague))
                    parent.sudo().write({'value_colleague': fieldsum_value_user_colleague})
                else:
                    parent.sudo().write({'value_colleague': 'K'})
                if so_lan_colleague2 > 0:
                    fieldsum_value_user_colleague2 = float('%.2f' % (tong_field_sum_user_colleague2 / so_lan_colleague2))
                    parent.sudo().write({'value_colleague2': fieldsum_value_user_colleague2})
                else:
                    parent.sudo().write({'value_colleague2': 'K'})
                if so_lan_colleague3 > 0:
                    fieldsum_value_user_colleague3 = float('%.2f' % (tong_field_sum_user_colleague3 / so_lan_colleague3))
                    parent.sudo().write({'value_colleague3': fieldsum_value_user_colleague3})
                else:
                    parent.sudo().write({'value_colleague3': 'K'})

                # self.tinh_trung_binh_v2(parent_user_input_line,giatri)

            else:
                if parent:
                    childs = self.env['hr.survey.user.input.line'].sudo().search(
                        [('summary_id', '=', parent.id)])
                    percentage_editable_flag = False
                    '''USer'''
                    tong_value_user = 0
                    tong_percentage = 0
                    so_lan = 0
                    tong_tile_thuchien_user = 0
                    ketqua_thuchien_user = 0
                    trung_binh_user = 0
                    '''Manager'''
                    tong_value_user_manager = 0
                    tong_percentage_manager = 0
                    so_lan_manager = 0
                    tong_tile_thuchien_user_manager = 0
                    ketqua_thuchien_user_manager = 0
                    trung_binh_user_manager = 0
                    '''SManager'''
                    tong_value_user_smanager = 0
                    tong_percentage_smanager = 0
                    so_lan_smanager = 0
                    tong_tile_thuchien_user_smanager = 0
                    ketqua_thuchien_user_smanager = 0
                    trung_binh_user_smanager = 0
                    '''HDDG'''
                    tong_value_user_hddg = 0
                    tong_percentage_hddg = 0
                    so_lan_hddg = 0
                    tong_tile_thuchien_user_hddg = 0
                    ketqua_thuchien_user_hddg = 0
                    trung_binh_user_hddg = 0
                    '''Colleague'''
                    tong_value_user_colleague = 0
                    tong_percentage_colleague = 0
                    so_lan_colleague = 0
                    tong_tile_thuchien_user_colleague = 0
                    '''Colleague2'''
                    tong_value_user_colleague2 = 0
                    tong_percentage_colleague2 = 0
                    so_lan_colleague2 = 0
                    tong_tile_thuchien_user_colleague2 = 0
                    '''Colleague3'''
                    tong_value_user_colleague3 = 0
                    tong_percentage_colleague3 = 0
                    so_lan_colleague3 = 0
                    tong_tile_thuchien_user_colleague3 = 0
                    ketqua_thuchien_user_colleague = 0
                    trung_binh_user_colleague = 0

                    for child in childs:
                        tile_thuchien_user = 0
                        tile_thuchien_user_manager = 0
                        tile_thuchien_user_smanager = 0
                        tile_thuchien_user_hddg = 0
                        tile_thuchien_user_colleague = 0
                        tile_thuchien_user_colleague2 = 0
                        tile_thuchien_user_colleague3 = 0
                        '''User'''
                        if self.isNumberic(child.value):
                            tong_value_user += float(child.value)
                            so_lan += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage += child.percentage
                                tile_thuchien_user = float(float(child.value)) * float(child.percentage) / float(
                                    child.max_score)
                                child.sudo().write({'tile_thuchien_user': tile_thuchien_user})
                        '''Manager'''
                        if self.isNumberic(child.value_manager):
                            tong_value_user_manager += float(child.value_manager)
                            so_lan_manager += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_manager += child.percentage
                                tile_thuchien_user_manager = float(float(child.value_manager)) * float(
                                    child.percentage) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_manager': tile_thuchien_user_manager})
                        '''Smanager'''
                        if self.isNumberic(child.value_smanager):
                            tong_value_user_smanager += float(child.value_smanager)
                            so_lan_smanager += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_smanager += child.percentage
                                tile_thuchien_user_smanager = float(float(child.value_smanager)) * float(
                                    child.percentage) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_smanager': tile_thuchien_user_smanager})
                        '''HDDG'''
                        if self.isNumberic(child.value_hddg):
                            tong_value_user_hddg += float(child.value_hddg)
                            so_lan_hddg += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_hddg += child.percentage
                                tile_thuchien_user_hddg = float(float(child.value_hddg)) * float(
                                    child.percentage) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_hddg': tile_thuchien_user_hddg})
                        '''Colleague'''
                        if self.isNumberic(child.value_colleague):
                            tong_value_user_colleague += float(child.value_colleague)
                            so_lan_colleague += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_colleague += child.percentage
                                tile_thuchien_user_colleague = float(float(child.value_colleague)) * float(
                                    child.percentage) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_colleague': tile_thuchien_user_colleague})
                        '''Colleague2'''
                        if self.isNumberic(child.value_colleague2):
                            tong_value_user_colleague2 += float(child.value_colleague2)
                            so_lan_colleague2 += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_colleague2 += child.percentage
                                tile_thuchien_user_colleague2 = float(float(child.value_colleague2)) * float(
                                    child.percentage2) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_colleague2': tile_thuchien_user_colleague2})
                        '''Colleague3'''
                        if self.isNumberic(child.value_colleague3):
                            tong_value_user_colleague3 += float(child.value_colleague3)
                            so_lan_colleague3 += 1
                            if child.enable_edit_percentage:
                                percentage_editable_flag = True
                                tong_percentage_colleague3 += child.percentage
                                tile_thuchien_user_colleague3 = float(float(child.value_colleague3)) * float(
                                    child.percentage) / float(child.max_score)
                                child.sudo().write({'tile_thuchien_colleague3': tile_thuchien_user_colleague3})

                        tong_tile_thuchien_user += tile_thuchien_user
                        tong_tile_thuchien_user_manager += tile_thuchien_user_manager
                        tong_tile_thuchien_user_smanager += tile_thuchien_user_smanager
                        tong_tile_thuchien_user_hddg += tile_thuchien_user_hddg
                        tong_tile_thuchien_user_colleague += tile_thuchien_user_colleague
                        tong_tile_thuchien_user_colleague2 += tile_thuchien_user_colleague2
                        tong_tile_thuchien_user_colleague3 += tile_thuchien_user_colleague3

                    if percentage_editable_flag:
                        trung_binh_user = tong_tile_thuchien_user * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_user': tong_tile_thuchien_user})
                        ketqua_thuchien_user = (float(tong_tile_thuchien_user) * float(parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_user': ketqua_thuchien_user})
                        '''Manager'''
                        trung_binh_user_manager = tong_tile_thuchien_user_manager * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_manager': tong_tile_thuchien_user_manager})
                        ketqua_thuchien_user_manager = (float(tong_tile_thuchien_user_manager) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_manager': ketqua_thuchien_user_manager})
                        '''Smanager'''
                        trung_binh_user_smanager = tong_tile_thuchien_user_smanager * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_smanager': tong_tile_thuchien_user_smanager})
                        ketqua_thuchien_user_smanager = (float(tong_tile_thuchien_user_smanager) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_smanager': ketqua_thuchien_user_smanager})
                        '''HĐDG'''
                        trung_binh_user_hddg = tong_tile_thuchien_user_hddg * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_hddg': tong_tile_thuchien_user_hddg})
                        ketqua_thuchien_user_hddg = (float(tong_tile_thuchien_user_hddg) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_hddg': ketqua_thuchien_user_hddg})
                        '''Colleague'''
                        trung_binh_user_colleague = tong_tile_thuchien_user_colleague * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_colleague': tong_tile_thuchien_user_colleague})
                        ketqua_thuchien_user_colleague = (float(tong_tile_thuchien_user_colleague) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_colleague': ketqua_thuchien_user_colleague})
                        '''Colleague2'''
                        trung_binh_user_colleague2 = tong_tile_thuchien_user_colleague2 * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_colleague2': tong_tile_thuchien_user_colleague2})
                        ketqua_thuchien_user_colleague2 = (float(tong_tile_thuchien_user_colleague2) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_colleague2': ketqua_thuchien_user_colleague2})
                        '''Colleague3'''
                        trung_binh_user_colleague3 = tong_tile_thuchien_user_colleague3 * parent.max_score / 100
                        parent.sudo().write({'tile_thuchien_colleague2': tong_tile_thuchien_user_colleague3})
                        ketqua_thuchien_user_colleague3 = (float(tong_tile_thuchien_user_colleague3) * float(
                            parent.percentage)) / 100
                        parent.sudo().write({'ketqua_thuchien_colleague3': ketqua_thuchien_user_colleague3})
                    else:
                        '''User'''
                        if so_lan > 0:
                            trung_binh_user = tong_value_user / so_lan
                        else:
                            trung_binh_user = -1
                        '''Manager'''
                        if so_lan_manager > 0:
                            trung_binh_user_manager = tong_value_user_manager / so_lan_manager
                        else:
                            trung_binh_user_manager = -1
                        '''Smanager'''
                        if so_lan_smanager > 0:
                            trung_binh_user_smanager = tong_value_user_smanager / so_lan_smanager
                        else:
                            trung_binh_user_smanager = -1

                        '''HDDG'''
                        if so_lan_hddg > 0:
                            trung_binh_user_hddg = tong_value_user_hddg / so_lan_hddg
                        else:
                            trung_binh_user_hddg = -1

                        '''Colleague'''
                        if so_lan_colleague > 0:
                            trung_binh_user_colleague = tong_value_user_colleague / so_lan_colleague
                        else:
                            trung_binh_user_colleague = -1
                        '''Colleague2'''
                        if so_lan_colleague2 > 0:
                            trung_binh_user_colleague2 = tong_value_user_colleague2 / so_lan_colleague2
                        else:
                            trung_binh_user_colleague2 = -1
                        '''Colleague3'''
                        if so_lan_colleague3 > 0:
                            trung_binh_user_colleague3 = tong_value_user_colleague3 / so_lan_colleague3
                        else:
                            trung_binh_user_colleague3 = -1

                    '''User'''
                    if 'value' in giatri:
                        if trung_binh_user > 0:
                            trung_binh = float('%.2f' % trung_binh_user)
                            parent.sudo().write({'value': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)

                    if 'value_manager' in giatri:
                        '''Manager'''
                        if trung_binh_user_manager > 0:
                            trung_binh = float('%.2f' % trung_binh_user_manager)
                            parent.sudo().write({'value_manager': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_manager': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)
                    if 'value_smanager' in giatri:
                        '''Smanager'''
                        if trung_binh_user_smanager > 0:
                            trung_binh = float('%.2f' % trung_binh_user_smanager)
                            parent.sudo().write({'value_smanager': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_smanager': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)
                    if 'value_hddg' in giatri:
                        '''HDDG'''
                        if trung_binh_user_hddg > 0:
                            trung_binh = float('%.2f' % trung_binh_user_hddg)
                            parent.sudo().write({'value_hddg': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_hddg': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)
                    if 'value_colleague' in giatri:
                        '''DongNghiep'''
                        if trung_binh_user_colleague > 0:
                            trung_binh = float('%.2f' % trung_binh_user_colleague)
                            parent.sudo().write({'value_colleague': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_colleague': 'K'})
                    '''DongNghiep2'''
                    if 'value_colleague2' in giatri:
                        if trung_binh_user_colleague2 > 0:
                            trung_binh = float('%.2f' % trung_binh_user_colleague2)
                            parent.sudo().write({'value_colleague2': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_colleague2': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)
                    '''DongNghiep3'''
                    if 'value_colleague3' in giatri:
                        if trung_binh_user_colleague3 > 0:
                            trung_binh = float('%.2f' % trung_binh_user_colleague3)
                            parent.sudo().write({'value_colleague3': trung_binh})
                            # self.tinh_trung_binh_v2(parent,giatri)
                        else:
                            parent.sudo().write({'value_colleague3': 'K'})
                            # self.tinh_trung_binh_v2(parent,giatri)
                # else:
                #     self.TinhRating(child_id.user_input_id)
                # fields_sum = self.env['hr.survey.summary.field.sum'].sudo().search(
                #     [('id_child', '=', child_id.question_id.id)])
                # if fields_sum:
                #     for field_sum in fields_sum:
                #         parent_user_input_line = self.env['hr.survey.user.input.line'].sudo().search(
                #             [('question_id', '=', field_sum.id_parent.id),
                #              ('user_input_id', '=', child_id.user_input_id.id)])
                #         if parent_user_input_line:
                #             field_sum_childs = self.env['hr.survey.summary.field.sum'].sudo().search(
                #                 [('id_parent', '=', parent_user_input_line.question_id.id)])
                #             so_lan = 0
                #             tong_field_sum_user = 0
                #
                #             so_lan_manager = 0
                #             tong_field_sum_user_manager = 0
                #
                #             so_lan_smanager = 0
                #             tong_field_sum_user_smanager = 0
                #
                #             so_lan_hddg = 0
                #             tong_field_sum_user_hddg = 0
                #
                #             so_lan_colleague = 0
                #             tong_field_sum_user_colleague = 0
                #
                #             for field_sum_child in field_sum_childs:
                #
                #                 childs_user_input_line = self.env[
                #                     'hr.survey.user.input.line'].sudo().search(
                #                     [('question_id', '=', field_sum_child.id_child.id),
                #                      ('user_input_id', '=', child_id.user_input_id.id)])
                #                 if child_id:
                #                     if self.isNumberic(childs_user_input_line.value):
                #                         so_lan += 1
                #                         tong_field_sum_user += float(childs_user_input_line.value)
                #
                #                     if self.isNumberic(childs_user_input_line.value_manager):
                #                         so_lan_manager += 1
                #                         tong_field_sum_user_manager += float(childs_user_input_line.value_manager)
                #
                #                     if self.isNumberic(childs_user_input_line.value_smanager):
                #                         so_lan_smanager += 1
                #                         tong_field_sum_user_smanager += float(childs_user_input_line.value_smanager)
                #
                #                     if self.isNumberic(childs_user_input_line.value_hddg):
                #                         so_lan_hddg += 1
                #                         tong_field_sum_user_hddg += float(childs_user_input_line.value_hddg)
                #
                #                     if self.isNumberic(childs_user_input_line.value_colleague):
                #                         so_lan_colleague += 1
                #                         tong_field_sum_user_colleague += float(childs_user_input_line.value_colleague)
                #             if so_lan>0:
                #                 fieldsum_value_user=float('%.2f' %(tong_field_sum_user/so_lan))
                #                 parent_user_input_line.sudo().write({'value': fieldsum_value_user})
                #             else:
                #                 parent_user_input_line.sudo().write({'value': 'K'})
                #             if so_lan_manager>0:
                #                 fieldsum_value_user_manager = float('%.2f' % (tong_field_sum_user_manager / so_lan_manager))
                #                 parent_user_input_line.sudo().write({'value_manager': fieldsum_value_user_manager})
                #             else:
                #                 parent_user_input_line.sudo().write({'value_manager': 'K'})
                #             if so_lan_smanager>0:
                #                 fieldsum_value_user_smanager = float('%.2f' % (tong_field_sum_user_smanager / so_lan_smanager))
                #                 parent_user_input_line.sudo().write({'value_smanager': fieldsum_value_user_smanager})
                #             else:
                #                 parent_user_input_line.sudo().write({'value_smanager': 'K'})
                #             if so_lan_hddg>0:
                #                 fieldsum_value_user_hddg = float('%.2f' % (tong_field_sum_user_hddg / so_lan_hddg))
                #                 parent_user_input_line.sudo().write({'value_hddg': fieldsum_value_user_hddg})
                #             else:
                #                 parent_user_input_line.sudo().write({'value_hddg': 'K'})
                #             if so_lan_colleague>0:
                #                 fieldsum_value_user_colleague = float('%.2f' % (tong_field_sum_user_colleague / so_lan_colleague))
                #                 parent_user_input_line.sudo().write({'value_colleague': fieldsum_value_user_colleague})
                #             else:
                #                 parent_user_input_line.sudo().write({'value_colleague': 'K'})
                #
                #             self.tinh_trung_binh_v2(parent_user_input_line,giatri)

            have_parent = False
            parent_of_parent = self.env['hr.survey.user.input.line'].sudo().search([('id', '=', parent.summary_id.id)])
            if parent_of_parent:
                for par in parent_of_parents:
                    if par.id == parent_of_parent.id:
                        have_parent = True
                if have_parent == False:
                    if parent_of_parent:
                        parent_of_parents.append(parent_of_parent)
            else:
                self.TinhRating(parent.user_input_id)
            fields_sums = self.env['hr.survey.summary.field.sum'].sudo().search(
                [('id_child', '=', parent.question_id.id)])

            if fields_sums:
                for fields_sum in fields_sums:
                    parent_user_input_line = self.env['hr.survey.user.input.line'].sudo().search(
                        [('question_id', '=', fields_sum.id_parent.id),
                         ('user_input_id', '=', parent.user_input_id.id)])
                    if parent_user_input_line:
                        have_parent = False
                        for par in parent_of_parents:
                            if par.id == parent_user_input_line.id:
                                have_parent = True
                        if have_parent == False:
                            parent_of_parents.append(parent_user_input_line)
        # if 'value' in giatri:
        if parent_of_parents is not None:
            if len(parent_of_parents) > 0:
                self.tinh_trung_binh_v2(parent_of_parents, giatri)

    def check_percentage_user(self, values):
        for val in values:
            if 'question' in val:
                parent_ids = []
                for i in values.get(val):
                    if self.isNumberic((i[1])):
                        parent_ids.append(i[1])
                parents = self.env['hr.survey.user.input.line'].sudo().browse(parent_ids)

                for parent in parents:
                    if not parent.can_input:
                        temp = []
                        for child in parents:
                            if child.summary_id.id == parent.id:
                                for i in values.get(val):
                                    if i[1] == child.id:
                                        temp.append(i)

                        total = -1
                        for va in temp:
                            percentage = self.env['hr.survey.user.input.line'].sudo().search(
                                [('id', '=', va[1]), ('enable_edit_percentage', '=', True)])
                            if percentage:
                                if not va[2]:
                                    if percentage.value != 'K':
                                        if total == -1:
                                            total = 0
                                        total += percentage.percentage
                                else:
                                    if va[2].get('percentage') is not None and va[2].get('value') is not None:
                                        if va[2].get('value') != 'K':
                                            if total == -1:
                                                total = 0
                                            total += va[2].get('percentage')
                                    elif va[2].get('percentage') is not None:
                                        if percentage.value != 'K':
                                            if total == -1:
                                                total = 0
                                            total += va[2].get('percentage')
                                    elif va[2].get('value') is not None:
                                        if va[2].get('value') != 'K':
                                            if total == -1:
                                                total = 0
                                            total += percentage.percentage
                                    else:
                                        if percentage.value != 'K':
                                            if total == -1:
                                                total = 0
                                            total += percentage.percentage

                        if total == -1 or total == 100.0:
                            pass
                        else:
                            raise UserError(_("Tổng phần trăm các câu hỏi phải = 100%!"))

    def check_percentage_user_manager_v2(self, values):
        for val in values:
            if 'question' in val:
                parent_ids = []
                for i in values.get(val):
                    if self.isNumberic((i[1])):
                        parent_ids.append(i[1])
                parents = self.env['hr.survey.user.input.line'].sudo().browse(parent_ids)
                parent_percent = -1
                for parent in parents:
                    if not parent.can_input:
                        '''Tính phần trăm parent'''
                        if self.isNumberic(parent.id):
                            for p in values.get(val):
                                if p[1] == parent.id:
                                    if p[2]:
                                        if p[2].get('percentage') is not None:
                                            if parent_percent == -1:
                                                parent_percent = 0
                                            parent_percent += p[2].get('percentage')
                                        else:
                                            pars = self.env['hr.survey.user.input.line'].sudo().search(
                                                [('id', '=', parent.id), ('enable_edit_percentage', '=', True)])
                                            if pars:
                                                if parent_percent == -1:
                                                    parent_percent = 0
                                                parent_percent += pars.percentage
                                    else:
                                        pars = self.env['hr.survey.user.input.line'].sudo().search(
                                            [('id', '=', parent.id), ('enable_edit_percentage', '=', True)])
                                        if pars:
                                            if parent_percent == -1:
                                                parent_percent = 0
                                            parent_percent += pars.percentage
                                        break

                        '''Tính phần trăm childs'''
                        temp = []
                        for child in parents:
                            if child.summary_id.id == parent.id:
                                for i in values.get(val):
                                    if i[1] == child.id:
                                        temp.append(i)

                        total = -1
                        for va in temp:
                            percentage = self.env['hr.survey.user.input.line'].sudo().search(
                                [('id', '=', va[1]), ('enable_edit_percentage', '=', True)])
                            if percentage:
                                if not va[2]:
                                    if total == -1:
                                        total = 0
                                    total += percentage.percentage
                                else:
                                    if va[2].get('percentage') is not None and va[2].get('value_manager') is not None:
                                        if total == -1:
                                            total = 0
                                        total += va[2].get('percentage')
                                    elif va[2].get('percentage') is not None:
                                        if total == -1:
                                            total = 0
                                        total += va[2].get('percentage')
                                    elif va[2].get('value_manager') is not None:
                                        if total == -1:
                                            total = 0
                                        total += percentage.percentage
                                    else:
                                        if total == -1:
                                            total = 0
                                        total += percentage.percentage

                        if total == -1 or total == 100.0 or total == 0:
                            pass
                        else:
                            raise UserError(_("Tổng phần trăm các câu hỏi phải = 100%!"))
                if parent_percent == -1 or parent_percent == 100.0 or parent_percent == 100:
                    pass
                else:
                    raise UserError(_("Tổng phần trăm các câu hỏi phải = 100%!"))

    def check_percentage_user_v2(self, values):
        for val in values:
            if 'question' in val:
                parent_ids = []

                for i in values.get(val):
                    if self.isNumberic((i[1])):
                        parent_ids.append(i[1])
                parents = self.env['hr.survey.user.input.line'].sudo().browse(parent_ids)
                parent_percent = -1

                for parent in parents:
                    per_parent_percentage = 0
                    if not parent.can_input:
                        '''Tính phần trăm parent'''
                        if self.isNumberic(parent.id):
                            for p in values.get(val):
                                if p[1] == parent.id:
                                    if p[2]:
                                        if p[2].get('percentage') is not None:
                                            if parent_percent == -1:
                                                parent_percent = 0

                                            parent_percent += p[2].get('percentage')
                                            per_parent_percentage += p[2].get('percentage')
                                        else:
                                            pars = self.env['hr.survey.user.input.line'].sudo().search(
                                                [('id', '=', parent.id), ('enable_edit_percentage', '=', True)])
                                            if pars:
                                                if parent_percent == -1:
                                                    parent_percent = 0
                                                parent_percent += pars.percentage
                                                per_parent_percentage += pars.percentage
                                    else:
                                        pars = self.env['hr.survey.user.input.line'].sudo().search(
                                            [('id', '=', parent.id), ('enable_edit_percentage', '=', True)])
                                        if pars:
                                            if parent_percent == -1:
                                                parent_percent = 0
                                            parent_percent += pars.percentage
                                            per_parent_percentage += pars.percentage
                                        break

                        '''Tính phần trăm childs'''
                        temp = []
                        if per_parent_percentage > 0:
                            for child in parents:
                                if child.summary_id.id == parent.id:
                                    for i in values.get(val):
                                        if i[1] == child.id:
                                            temp.append(i)
                            total = -1
                            for va in temp:
                                percentage = self.env['hr.survey.user.input.line'].sudo().search(
                                    [('id', '=', va[1]), ('enable_edit_percentage', '=', True)])
                                if percentage:
                                    if not va[2]:
                                        if total == -1:
                                            total = 0
                                        total += percentage.percentage
                                    else:
                                        if va[2].get('percentage') is not None and va[2].get('value') is not None:
                                            if total == -1:
                                                total = 0
                                            total += va[2].get('percentage')
                                        elif va[2].get('percentage') is not None:
                                            if total == -1:
                                                total = 0
                                            total += va[2].get('percentage')
                                        elif va[2].get('value') is not None:
                                            if total == -1:
                                                total = 0
                                            total += percentage.percentage
                                        else:
                                            if total == -1:
                                                total = 0
                                            total += percentage.percentage
                            if total == -1 or total == 100.0 or total == 0:
                                pass
                            else:
                                raise UserError(_("Tổng phần trăm các câu hỏi phải = 100%!"))
                if parent_percent == -1 or parent_percent == 100.0 or parent_percent == 100:
                    pass
                else:
                    raise UserError(_("Tổng phần trăm các câu hỏi phải = 100%!"))

    @api.multi
    def write(self, values):
        '''Khi sử dụng Mass edit để apply cho nhiều dòng'''
        if len(self) > 1:

            for rec in self:
                if values.get('lock_state') is not None:
                    if values.get('lock_state') == 'yes':
                        if rec.ct_xetduyet:
                            rec.user_input_status = 'hoan_thanh'
                        elif rec.manager_status:
                            rec.user_input_status = 'qltt_da_danh_gia'
                        elif rec.smanager_status:
                            rec.user_input_status = 'qlcc_da_danh_gia'
                        elif rec.nhansu_status:
                            rec.user_input_status = 'ns_da_danh_gia'

                        else:
                            rec.user_input_status = 'dang_tien_hanh'
                    else:
                        rec.user_input_status = 'khong_danh_gia'
                manager_multi_id = values.get('manager_multi_id')
            if values.get('manager_multi_id'):
                user_manager_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('manager_multi_id'))],
                    limit=1).user_id.id
                values.update({'user_manager_id': user_manager_id, })
            if values.get('smanager_multi_id'):
                user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('smanager_multi_id'))],
                    limit=1).user_id.id
                values.update({'user_smanager_id': user_smanager_id, })
            if values.get('colleague_multi_id'):
                user_colleague_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague_multi_id'))],
                    limit=1).user_id.id
                values.update({'user_colleague_id': user_colleague_id, })
                self.activity_schedule(
                    'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                    user_id=user_colleague_id)
            if values.get('colleague2_multi_id'):
                user_colleague2_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague2_multi_id'))],
                    limit=1).user_id.id
                values.update({'user_colleague2_id': user_colleague2_id, })
                self.activity_schedule(
                    'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                    user_id=user_colleague2_id)
            if values.get('colleague3_multi_id'):
                user_colleague3_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague3_multi_id'))],
                    limit=1).user_id.id
                values.update({'user_colleague3_id': user_colleague3_id, })
                self.activity_schedule(
                    'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                    user_id=user_colleague3_id)
            super(HR_Survey_User_Input, self).write(values)
        else:
            if values.get('lock_state') is not None:
                if values.get('lock_state') == 'yes':
                    if self.ct_xetduyet:
                        self.user_input_status = 'hoan_thanh'

                    elif self.manager_status:
                        self.user_input_status = 'qltt_da_danh_gia'
                    elif self.smanager_status:
                        self.user_input_status = 'qlcc_da_danh_gia'
                    elif self.nhansu_status:
                        self.user_input_status = 'ns_da_danh_gia'

                    else:
                        self.user_input_status = 'dang_tien_hanh'
                else:
                    self.user_input_status = 'khong_danh_gia'
            if values.get('ct_xetduyet') is not None:
                if values.get('ct_xetduyet'):
                    self.user_input_status = 'hoan_thanh'
                elif self.manager_status:
                    self.user_input_status = 'qltt_da_danh_gia'
                elif self.smanager_status:
                    self.user_input_status = 'qlcc_da_danh_gia'
                elif self.nhansu_status:
                    self.user_input_status = 'ns_da_danh_gia'

                else:
                    self.user_input_status = 'dang_tien_hanh'
            '''Get Manager User ID'''

            manager_multi_id = values.get('manager_multi_id')
            if manager_multi_id is not None:
                user_manager_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', manager_multi_id)],
                                                                                      limit=1).user_id.id
                if user_manager_id:
                    self.user_manager_id = user_manager_id
                else:
                    self.user_manager_id = None
            '''Get Super Manager User ID'''
            if values.get('smanager_multi_id') is not None:
                user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('smanager_multi_id'))], limit=1).user_id.id
                if user_smanager_id:
                    self.user_smanager_id = user_smanager_id
                else:
                    self.user_smanager_id = None
            '''Get BOD User ID'''
            hddg = values.get('hddg')
            if hddg:
                hddg_employees = self.env['hr.employee'].sudo().search([('id', '=', hddg)])
                if hddg_employees is not None:
                    for hddg_employee in hddg_employees:
                        self.hddg_user = hddg_employee.user_id.id
                else:
                    self.hddg_user = None
            '''Đồng nghiệp User ID'''
            if values.get('colleague_multi_id') is not None:
                user_colleague_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague_multi_id'))], limit=1).user_id.id
                if user_colleague_id:
                    self.user_colleague_id = user_colleague_id
                    self.activity_schedule(
                        'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                        user_id=user_colleague_id)
                else:
                    self.user_colleague_id = None
            '''Đồng nghiệp 2 User ID'''
            if values.get('colleague2_multi_id') is not None:
                user_colleague2_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague2_multi_id'))], limit=1).user_id.id
                if user_colleague2_id:
                    self.user_colleague2_id = user_colleague2_id
                    self.activity_schedule('seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',user_id=user_colleague2_id)
                else:
                    self.user_colleague2_id = None
            '''Đồng nghiệp 3 User ID'''
            if values.get('colleague3_multi_id') is not None:
                user_colleague3_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague3_multi_id'))], limit=1).user_id.id
                if user_colleague3_id:
                    self.user_colleague3_id = user_colleague3_id
                    self.activity_schedule(
                        'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                        user_id=user_colleague3_id)
                else:
                    self.user_colleague3_id = None

            if self.user_manager_id.id == self.env.user.id:
                self.check_percentage_user_manager_v2(values)
            if self.user_id.id == self.env.user.id:
                self.check_percentage_user_v2(values)
            # Tính điểm
            rec = super(HR_Survey_User_Input, self).write(values)
            parents = []
            for value in values:
                if 'question' in value:
                    for val in values.get(value):
                        if val[2]:
                            if self.isNumberic(val[1]):
                                child_get_summary_id = self.env['hr.survey.user.input.line'].sudo().search(
                                    [('id', '=', val[1])])
                                have_parent = False
                                for par in parents:
                                    if child_get_summary_id.summary_id.id == par.id:
                                        have_parent = True
                                if have_parent == False:
                                    parent = self.env['hr.survey.user.input.line'].sudo().search(
                                        [('id', '=', child_get_summary_id.summary_id.id)])
                                    if parent:
                                        parents.append(parent)
                                fields_sum_childs = self.env['hr.survey.summary.field.sum'].sudo().search(
                                    [('id_child', '=', child_get_summary_id.question_id.id)])
                                if fields_sum_childs:
                                    for fields_sum_child in fields_sum_childs:
                                        parent_user_input_line = self.env['hr.survey.user.input.line'].sudo().search(
                                            [('question_id', '=', fields_sum_child.id_parent.id),
                                             ('user_input_id', '=', child_get_summary_id.user_input_id.id)])
                                        if parent_user_input_line:
                                            have_parent = False
                                            for par in parents:
                                                if parent_user_input_line.id == par.id:
                                                    have_parent = True
                                            if have_parent == False:
                                                parents.append(parent_user_input_line)
                    '''dkh add'''
                    giatri = []
                    for val in values.get(value):
                        if val[2]:
                            if self.isNumberic(val[1]):
                                child_get_summary_id = self.env['hr.survey.user.input.line'].sudo().search(
                                    [('id', '=', val[1])])

                                if child_get_summary_id:
                                    user_inputs = self.env['hr.survey.user.input'].sudo().search(
                                        [('id', '=', child_get_summary_id.user_input_id.id)])
                                    if val[2].get('value') is not None:
                                        giatri.append('value')
                                    if val[2].get('value_manager') is not None:
                                        giatri.append('value_manager')
                                    if val[2].get('value_smanager') is not None:
                                        giatri.append('value_smanager')
                                    if val[2].get('value_hddg') is not None:
                                        giatri.append('value_hddg')
                                    if val[2].get('value_colleague') is not None:
                                        giatri.append('value_colleague')
                                    if val[2].get('value_colleague2') is not None:
                                        giatri.append('value_colleague2')
                                    if val[2].get('value_colleague3') is not None:
                                        giatri.append('value_colleague3')
                                    if val[2].get('percentage') is not None:
                                        giatri.append('percentage')
                    if 'percentage' in giatri:
                        self.tinh_trung_binh_v2(parents, ['value'])
                        self.tinh_trung_binh_v2(parents, ['value_manager'])
                        self.tinh_trung_binh_v2(parents, ['value_smanager'])
                        self.tinh_trung_binh_v2(parents, ['value_hddg'])
                        self.tinh_trung_binh_v2(parents, ['value_colleague'])
                        self.tinh_trung_binh_v2(parents, ['value_colleague2'])
                        self.tinh_trung_binh_v2(parents, ['value_colleague3'])
                    else:
                        self.tinh_trung_binh_v2(parents, giatri)
            return rec

    @api.model
    def create(self, values):
        if values.get('employee_multi_id') is None or values.get('appraisal_id') is None:
            return
        appraisal_id = values.get('appraisal_id')
        survey_id = None
        if values.get('survey_id'):
            survey_id = values.get('survey_id')
        else:
            appraisals = self.env['hr.appraisal'].sudo().search([('id', '=', appraisal_id)])
            for appraisal in appraisals:
                survey_id = appraisal.survey_id.id
        if not survey_id:
            return
        if values.get('name') is None:
            employee = values.get('employee_multi_id')
            search = self.env['hr.employee.multi.company'].sudo().search([('id', '=', values.get('employee_multi_id'))])
            department = self.env['hr.department'].sudo().search([('id', '=', search.department_id.id)])
            operating_unit = self.env['operating.unit'].sudo().search([('id', '=', search.operating_unit_id.id)])
            job = self.env['hr.job'].sudo().search([('id', '=', search.job_id.id)])

            search_appraisal = self.env['hr.appraisal'].sudo().search([('id', '=', values.get('appraisal_id'))],
                                                                      limit=1)
            '''Manager'''
            user_manager_id = False
            manager_multi_id = False
            if values.get('manager_multi_id') is not None:
                if values['manager_multi_id']:
                    user_manager_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('id', '=', values.get('manager_multi_id'))]).user_id.id
                else:
                    if search.parent_id:
                        manager_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                            [('name', '=', search.parent_id.sudo().id),
                             ('company_id', '=', self.env.user.company_id.id)]).id
                        user_manager_id = self.env['hr.employee.multi.company'].sudo().search(
                            [('id', '=', manager_multi_id)]).user_id.id

            else:
                if search.parent_id:
                    manager_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('name', '=', search.parent_id.sudo().id),
                         ('company_id', '=', self.env.user.company_id.id)]).id
                    user_manager_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('id', '=', manager_multi_id)]).user_id.id

            user_smanager_id = False
            smanager_multi_id = False
            if values.get('smanager_multi_id') is not None:
                if values['smanager_multi_id']:
                    user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('id', '=', values.get('smanager_multi_id'))]).user_id.id
                else:
                    if manager_multi_id:
                        multi_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', manager_multi_id)])
                        if multi_id.parent_id:
                            smanager_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                                [('name', '=', multi_id.parent_id.sudo().id),
                                 ('company_id', '=', self.env.user.company_id.id)]).id
                            user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                                [('id', '=', smanager_multi_id)]).user_id.id

            else:
                if manager_multi_id:
                    multi_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', manager_multi_id)])
                    if multi_id.parent_id:
                        smanager_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                            [('name', '=', multi_id.parent_id.sudo().id),
                             ('company_id', '=', self.env.user.company_id.id)]).id
                        user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                            [('id', '=', smanager_multi_id)]).user_id.id

            user_colleague_id = False
            if values.get('colleague_multi_id') is not None:
                user_colleague_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague_multi_id'))]).user_id.id
                if user_colleague_id:
                    self.activity_schedule(
                        'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                        user_id=user_colleague_id)
            user_colleague2_id = False
            if values.get('colleague2_multi_id') is not None:
                user_colleague2_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague2_multi_id'))]).user_id.id
                if user_colleague2_id:
                    self.activity_schedule(
                        'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                        user_id=user_colleague2_id)
            user_colleague3_id = False
            if values.get('colleague3_multi_id') is not None:
                user_colleague3_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', values.get('colleague3_multi_id'))]).user_id.id
                if user_colleague3_id:
                    self.activity_schedule(
                        'seatek_hr_appraisal.mail_act_hr_survey_user_input_active_type_colleague',
                        user_id=user_colleague3_id)
            if values.get('company_id'):
                company = values.get('company_id')
            else:
                company = self.env.user.company_id.id
            if values.get('manager_multi_id'):
                manager_multi_id = values.get('manager_multi_id')
                user_manager_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', manager_multi_id)]).user_id.id
            if values.get('smanager_multi_id'):
                smanager_multi_id = values.get('smanager_multi_id')
                user_smanager_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', smanager_multi_id)]).user_id.id
            values.update(
                {'name': search.name.sudo().name, 'is_manager': search.manager, 'user_id': search.user_id.id,
                 'user_manager_id': user_manager_id,
                 'user_smanager_id': user_smanager_id,
                 'manager_multi_id': manager_multi_id,
                 'smanager_multi_id': smanager_multi_id,
                 'user_colleague_id': user_colleague_id,
                 'survey_id': search_appraisal.survey_id.id,
                 'appraisal_period': search_appraisal.appraisal_period.id,
                 'company_id': company,
                 'department_id': department.id,
                 'operating_unit_id': operating_unit.id,
                 'job_position_id': job.id})

        res = super(HR_Survey_User_Input, self).create(values)
        parent_pages = self.env['hr.survey.summary'].sudo().search(
            [('survey_id', '=', survey_id), ('is_parent_page', '=', True)])
        i = 1
        level_report = 1
        order = 0
        for parent_page in parent_pages:

            pages = self.env['hr.survey.summary'].sudo().search([('summary_id', '=', parent_page.id)])

            parent_new_page_line = self.env['hr.survey.user.input.line'].sudo().create({'name': 'General',
                                                                                        'page_id': parent_page.id,
                                                                                        'page_name': 'TỔNG HỢP',
                                                                                        'question_id': parent_page.id,
                                                                                        'question_name': parent_page.name,
                                                                                        'prefix': parent_page.prefix,
                                                                                        'is_rating': parent_page.is_rating,
                                                                                        'can_input': parent_page.can_input,
                                                                                        'enable_edit_title': False,
                                                                                        'data_type': parent_page.data_type,
                                                                                        'validation_required': parent_page.validation_required,
                                                                                        'max_score': parent_page.max_score,
                                                                                        'parent_page_id': parent_page.id,
                                                                                        'percentage': parent_page.percentage,
                                                                                        'user_input_id': res.id,
                                                                                        'summary_level': 1,
                                                                                        'summary_level_report': 1,
                                                                                        'question_general': res.id,
                                                                                        'survey_level_1': parent_page.id,
                                                                                        'department_id': res.department_id.id,
                                                                                        'operating_unit_id': res.operating_unit_id.id,
                                                                                        'line_order': int(order)})
            level_report = 2
            order += 1
            for page in pages:
                # page general
                survey_level_2 = None
                if page.prefix != 'II':
                    survey_level_2 = page.id

                new_page_line = self.env['hr.survey.user.input.line'].sudo().create({'name': 'General',
                                                                                     'page_id': page.id,
                                                                                     'page_name': 'TỔNG HỢP',
                                                                                     'question_id': page.id,
                                                                                     'question_name': page.name,
                                                                                     'prefix': page.prefix,
                                                                                     'can_input': page.can_input,
                                                                                     'summary_id': parent_new_page_line.id,
                                                                                     'enable_edit_title': False,
                                                                                     'data_type': page.data_type,
                                                                                     'validation_required': page.validation_required,
                                                                                     'max_score': page.max_score,
                                                                                     'parent_page_id': page.id,
                                                                                     'user_input_id': res.id,
                                                                                     'percentage': page.percentage,
                                                                                     'summary_level': 2,
                                                                                     'summary_level_report': level_report,
                                                                                     'question_general': res.id,
                                                                                     'survey_level_2': survey_level_2,
                                                                                     'department_id': res.department_id.id,
                                                                                     'operating_unit_id': res.operating_unit_id.id,
                                                                                     'line_order': int(order)})
                order += 1
                order = self.create_user_input_line(new_page_line, res, i, page, page, level_report + 1, parent_page,
                                                    page, order, True)
                i = i + 1
        return res

    def create_user_input_line(self, parent_summary_id, res, number_page, page, parent_page, level_report, level1_page,
                               level2_page, order, set_level_3):
        temp_level_report = level_report
        datas = self.env['hr.survey.summary'].sudo().search([('summary_id', '=', page.id)])
        for data in datas:
            if data.can_input:
                title_editable = data.enable_edit_title
            else:
                title_editable = False
            if number_page == 1:
                question = 'question_1'
            elif number_page == 2:
                question = 'question_2'
            elif number_page == 3:
                question = 'question_3'
            elif number_page == 4:
                question = 'question_4'
            elif number_page == 5:
                question = 'question_5'
            elif number_page == 6:
                question = 'question_6'
                temp_level_report = level_report - 1
            elif number_page == 7:
                question = 'question_7'
            elif number_page == 8:
                question = 'question_8'
            elif number_page == 9:
                question = 'question_9'
            elif number_page == 10:
                question = 'question_10'
            else:
                break
            if res.user_manager_id:
                manager_role = True
            else:
                manager_role = False
            survey_level_3 = None
            survey_level_2 = None
            if set_level_3:

                if data.enable_edit_percentage:
                    survey_level_2 = data.id
                else:
                    survey_level_3 = data.id
            new_page_line = self.env['hr.survey.user.input.line'].sudo().create({'name': page.name,
                                                                                 'page_id': page.id,
                                                                                 'page_name': page.name,
                                                                                 'question_id': data.id,
                                                                                 'question_name': data.name,
                                                                                 'prefix': data.prefix,
                                                                                 'can_input': data.can_input,
                                                                                 'calculation_method': data.calculation_method,
                                                                                 'enable_edit_title': title_editable,
                                                                                 'percentage': data.percentage,
                                                                                 'enable_edit_percentage': data.enable_edit_percentage,
                                                                                 'summary_id': parent_summary_id.id,
                                                                                 'manager_role': manager_role,
                                                                                 'summary_level': data.summary_level,
                                                                                 'summary_level_report': temp_level_report,
                                                                                 'parent_page_id': parent_page.id,
                                                                                 'data_type': data.data_type,
                                                                                 'validation_required': data.validation_required,
                                                                                 'max_score': data.max_score,
                                                                                 'user_input_id': res.id,
                                                                                 'line_order': int(order),
                                                                                 'survey_level_2': survey_level_2,
                                                                                 'survey_level_3': survey_level_3,
                                                                                 'department_id': res.department_id.id,
                                                                                 'operating_unit_id': res.operating_unit_id.id,
                                                                                 question: res.id})
            order += 1
            order = self.create_user_input_line(new_page_line, res, number_page, data, parent_page, level_report + 1,
                                                level1_page, level2_page, order, False)
        return order

    def print_appraisal(self):
        if self.env.user.has_group('seatek_hr_appraisal.hr_appraisal_board_of_manager'):
            ids = []
            for record in self:
                ids.append(record.id)
            user_inputs = self.env['hr.survey.user.input'].browse(ids)
            return self.env.ref('seatek_hr_appraisal.action_report_appraisal').report_action(user_inputs)
        else:
            return False

    def view_manager_comment(self):
        return

    @api.multi
    def button_danh_gia_seacorp(self):
        self.ensure_one()
        return {
            'name': _('Đánh Giá Seacorp'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'hr.survey.user.input',
            'view_id': self.env.ref('seatek_hr_appraisal.hr_survey_user_input_seacorp_view_form').id,
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            # 'context': {'product_ids': self.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')).mapped('product_id').ids + [self.production_id.product_id.id]},
            'target': 'new',
        }

    # @api.multi
    # def import_kpis_excel(self):
    #     self.ensure_one()
    #     return {
    #         'name': _('Import template'),
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'survey.import.template',
    #         'view_id': self.env.ref('seatek_hr_appraisal.import_survey_excel_view_form').id,
    #         'type': 'ir.actions.act_window',
    #         'user_input_id': self.id,
    #         # 'context': {'product_ids': self.move_raw_ids.filtered(lambda x: x.state not in ('done', 'cancel')).mapped('product_id').ids + [self.production_id.product_id.id]},
    #         'target': 'new',
    #     }

    @api.multi
    @api.depends('company_id')
    def _belong_to_company(self):
        for rec in self:
            rec.belongs_to_company = (rec.company_id.id == self.env.user.company_id.id)

    belong_to_company = fields.Boolean(string='Belong To Company', compute='_belong_to_company')

    def compute_security(self):
        for rec in self:
            if not self.env.user.has_group(
                    'seatek_hr_appraisal.hr_appraisal_board_of_manager') and not self.env.user.has_group(
                'seatek_hr_appraisal.hr_appraisal_manager'):
                raise UserError(_("Do not have access!"))
                rec.security_board_of_manager_and_hr_manager = False
            else:
                rec.security_board_of_manager_and_hr_manager = True

    security_board_of_manager_and_hr_manager = fields.Boolean(string='Security', compute='compute_security')

    def export_excel_appraisal(self):
        return self.env.ref('seatek_hr_appraisal.action_export_excel_appraisal').report_action(self)

    def compute_short_name_compute(self):
        for rec in self:
            if rec.company_id:
                rec.short_name_compute = rec.company_id.short_name
            else:
                rec.short_name_compute = self.env.user.company_id.short_name

    def inverse_short_name_compute(self):
        pass

    short_name_compute = fields.Char(string='Short Name', compute='compute_short_name_compute',
                                     inverse='inverse_short_name_compute')

    '''dkh add'''
    assigned_complete_compute = fields.Boolean(compute='compute_asigned_complete_compute',string="Bài đánh giá bạn đã đánh giá xong")
    def compute_asigned_complete_compute(self):
        for res in self:
            if res.user_manager_id.id==self.env.user.id:
                if res.manager_status:
                    res.assigned_complete_compute=True
            elif res.user_smanager_id.id==self.env.user.id:
                if res.smanager_status:
                    res.assigned_complete_compute=True


class HR_Survey_User_Input_Lines(models.Model):
    _name = 'hr.survey.user.input.line'
    _description = 'HR Survey User Lines'
    _order = "line_order"

    @api.multi
    def write(self, values):
        # if 'value' in values:
        #     values['value_write_uid'] = fields.Datetime.now()
        # elif 'value_manager' in values or 'question_name' in values or 'percentage' in values:
        #     values['value_manager_write_uid'] = fields.Datetime.now()
        # elif 'value_smanager' in values:
        #     values['value_smanager_write_uid'] = fields.Datetime.now()
        # elif 'value_hddg' in values:
        #     values['value_hddg_write_uid'] = fields.Datetime.now()
        # elif 'value_colleague' in values:
        #     values['value_colleague_write_uid_1'] = fields.Datetime.now()

        return super(HR_Survey_User_Input_Lines, self).write(values)

    name = fields.Char(string='Value')
    page_id = fields.Many2one('hr.survey.summary', ondelete='cascade')
    page_name = fields.Char(string='Name')
    prefix = fields.Char(string='STT', default='')
    line_order = fields.Integer(string='Line Order')
    survey_level_1 = fields.Many2one('hr.survey.summary', string='Level 1')
    survey_level_2 = fields.Many2one('hr.survey.summary', string='Level 2')
    survey_level_3 = fields.Many2one('hr.survey.summary', string='Level 3')
    question_id = fields.Many2one('hr.survey.summary', ondelete='cascade')
    question_name = fields.Text(string='Tên')
    summary_level = fields.Integer(string="Level")
    can_input = fields.Boolean(string="Can input")
    enable_edit_title = fields.Boolean(string="Title editable")
    summary_id = fields.Many2one('hr.survey.user.input.line', ondelete='cascade')
    calculation_method = fields.Selection([('sum', 'Summary'), ('average', 'Average')],
                                          string='Calculation', default='average')
    manager_role = fields.Boolean(string='Manager role')
    hddg_role = fields.Boolean(string='Manager role')
    score = fields.Float(string='Score', default=0)
    percentage = fields.Float(string='Tỉ Trọng %', default=0)
    enable_edit_percentage = fields.Boolean(string="Percentage editable", default=False)
    user_comment = fields.Text(string="Nhận Xét Cá Nhân")
    manager_comment = fields.Text(string="Nhận Xét QLTT")
    smanager_comment = fields.Text(string="Nhận Xét Cấp Trên QLTT")
    hddg_comment = fields.Text(string="Nhận Xét HĐĐG")
    colleague_comment = fields.Text(string="Nhận Xét Đồng Nghiệp")
    colleague2_comment = fields.Text(string="Nhận Xét Đồng Nghiệp")
    colleague3_comment = fields.Text(string="Nhận Xét Đồng Nghiệp")
    summary_level_report = fields.Integer(string='Report Level')

    # manager_comment_view=fields.Boolean(string='View Comment',default=False)
    def view_manager_comment(self):
        return

    def _compute_all_comment(self):

        for rec in self:
            comment = ''
            if rec.user_comment:
                comment += 'Nhân Viên:' + rec.user_comment + '\n'
            if rec.manager_comment:
                comment += 'QLTT:' + rec.manager_comment + '\n'
            if rec.smanager_comment:
                comment += 'Cấp Trên QLTT:' + rec.smanager_comment + '\n'
            if self.env.user.has_group('seatek_hr_appraisal.hr_appraisal_board_of_manager'):
                if rec.colleague_comment:
                    comment += 'Đồng Nghiệp1:' + rec.colleague_comment + '\n'
                if rec.colleague2_comment:
                    comment += 'Đồng Nghiệp2:' + rec.colleague2_comment + '\n'
                if rec.colleague3_comment:
                    comment += 'Đồng Nghiệp3:' + rec.colleague3_comment + '\n'

            rec.all_comment = comment

    all_comment = fields.Text(string="Tổng Hợp Nhận Xét", compute='_compute_all_comment')

    def _compute_all_comment_no_colleague(self):
        for rec in self:
            comment = ''
            if rec.user_comment:
                comment += 'Nhân Viên:' + rec.user_comment + '\n'
            if rec.manager_comment:
                comment += 'QLTT:' + rec.manager_comment + '\n'
            if rec.smanager_comment:
                comment += 'Cấp Trên QLTT:' + rec.smanager_comment + '\n'
            if rec.hddg_comment:
                comment += 'HĐĐG:' + rec.hddg_comment + '\n'
            rec.all_comment_no_colleague = comment

    all_comment_no_colleague = fields.Text(string="Tổng Hợp Nhận Xét ", compute='_compute_all_comment_no_colleague')

    value = fields.Char(string='Nhân Viên', default='K')
    value_manager = fields.Char(string='QLTT', default='K')
    value_smanager = fields.Char(string='Cấp Trên QLTT', default='K')
    value_hddg = fields.Char(string='HĐĐG', default='K')
    value_colleague = fields.Char(string='Đồng Nghiệp', default='K')
    value_colleague2 = fields.Char(string='Đồng Nghiệp', default='K')
    value_colleague3 = fields.Char(string='Đồng Nghiệp', default='K')

    # Khánh 10/11/2022

    department_id = fields.Many2one('hr.department', string='Đơn Vị')
    operating_unit_id = fields.Many2one('operating.unit', 'Đơn Vị Hoạt Động')

    # ============//========================== #

    tile_thuchien_user = fields.Char(default='0')
    tile_thuchien_manager = fields.Char(default='0')
    tile_thuchien_smanager = fields.Char(default='0')
    tile_thuchien_hddg = fields.Char(default='0')
    tile_thuchien_colleague = fields.Char(default='0')
    ketqua_thuchien_user = fields.Char(default='0')
    ketqua_thuchien_manager = fields.Char(default='0')
    ketqua_thuchien_smanager = fields.Char(default='0')
    ketqua_thuchien_hddg = fields.Char(default='0')
    ketqua_thuchien_colleague = fields.Char(default='0')
    ketqua_thuchien_colleague2 = fields.Char(default='0')
    ketqua_thuchien_colleague3 = fields.Char(default='0')

    current_user = fields.Many2one('res.users', string="Temp user", ondelete='cascade')
    is_rating = fields.Boolean(default=False, string="Is Rating")
    # question one2many
    question_general = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_1 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_2 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_3 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_4 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_5 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_6 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_7 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_8 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_9 = fields.Many2one('hr.survey.user.input', ondelete='cascade')
    question_10 = fields.Many2one('hr.survey.user.input', ondelete='cascade')

    parent_page_id = fields.Many2one('hr.survey.summary', ondelete='cascade')
    skipped = fields.Boolean('Skipped')
    data_type = fields.Selection([('score', 'Score'), ('percentage', 'Percentage (%)')], string='Data Type',
                                 default='score', required=True)
    validation_required = fields.Boolean(string='Required')
    max_score = fields.Integer(string="Scale", default=5)
    user_input_id = fields.Many2one('hr.survey.user.input', string='User Input', ondelete='cascade')

    # Khánh thêm
    # def _compute_department_user_input_id_(self):
    #     for rec in self:
    #         rec.department_user_input_id = rec.user_input_id.sudo().department_id.id
    #
    # department_user_input_id = fields.Many2one('hr.department', string='Department User Input',
    #                                            compute='_compute_department_user_input_id_')

    # def _compute_appraisal_role(self):
    #     is_manager=False
    #     for rec in self:
    #
    #         user_input=self.env['hr.survey.user.input'].sudo().search([('id','=',rec.user_input_id.id)])
    #         if user_input:
    #             emp = self.env['hr.employee'].sudo().search([('id', '=', user_input.manager_id.id)])
    #             if emp:
    #                 if emp.user_id.id == self.env.user.id:
    #                     rec.appraisal_role = 'manager'
    #                     is_manager=True
    #             emp=self.env['hr.employee'].sudo().search([('id','=',user_input.smanager_id.id)])
    #             if emp:
    #                 if emp.user_id.id== self.env.user.id:
    #                     if is_manager:
    #                         rec.appraisal_role='both'
    #                     else:
    #                         rec.appraisal_role = 'smanager'
    #
    def _compute_appraisal_role(self):
        is_manager = False
        for rec in self:

            user_input = self.env['hr.survey.user.input'].sudo().search([('id', '=', rec.user_input_id.id)])
            if user_input:
                emp = self.env['hr.employee.multi.company'].sudo().search([('id', '=', user_input.manager_multi_id.id)])
                if emp:
                    if emp.user_id.id == self.env.user.id:
                        rec.appraisal_role = 'manager'
                        is_manager = True
                emp = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', user_input.smanager_multi_id.id)])
                if emp:
                    if emp.user_id.id == self.env.user.id:
                        if is_manager:
                            rec.appraisal_role = 'both'
                        else:
                            rec.appraisal_role = 'smanager'

    appraisal_role = fields.Char(string='role', default='', compute='_compute_appraisal_role')
    line_open_state = fields.Boolean(string='Trạng thái đóng', default=True)

    def isNumberic(self, string):
        if string:
            try:
                float(string)
                return True
            except ValueError:
                return False
        else:
            return False

    def convertNumber(self, string):
        if string:
            try:
                a = float(string)
                return a
            except ValueError:
                return 0
        else:
            return 0

    def get_classification(self, score):
        classsi = self.env['hr.appraisal.classification'].sudo().search()

        for clas in classsi:
            if score > clas.min_score and score < clas.max_score:
                return clas

    @api.multi
    def validate_question(self, post, answer_tag):
        """ Validate question, depending on question type and parameters """
        self.ensure_one()
        try:
            checker = getattr(self, 'validate_' + self.data_type)
        except AttributeError:
            _logger.warning(self.data_type + ": This type of question has no validation method")
            return {}
        else:
            return checker(post, answer_tag)

    @api.multi
    def validate_score(self, post, answer_tag):
        # self.ensure_one()
        # errors = {}
        # answer = post[answer_tag].strip()
        #
        # if not answer and self.validation_required:
        #     errors.update({answer_tag: 'The answer is required.'})
        #
        # if answer:
        #     try:
        #         float_answer = float(answer)
        #         if not (0 <= float_answer <= self.max_score):
        #             errors.update({answer_tag: 'Input value must be greater than 0 and less than %s' % self.max_score})
        #     except ValueError:
        #         errors.update({answer_tag: _('This is not a number')})

        return False

    @api.onchange('value')
    def _onchange_value(self):
        if self.isNumberic(self.value):
            if float(self.value) > self._origin.max_score or float(self.value) < 0:
                self.value = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value == 'k' or self.value == 'K':
                self.value = 'K'
            else:
                self.value = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_manager')
    def _onchange_value_manager(self):
        if self.isNumberic(self.value_manager):
            if float(self.value_manager) > self._origin.max_score or float(self.value_manager) < 0:
                self.value_manager = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_manager == 'k' or self.value_manager == 'K':
                self.value_manager = 'K'
            else:
                self.value_manager = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_smanager')
    def _onchange_value_smanager(self):
        if self.isNumberic(self.value_smanager):
            if float(self.value_smanager) > self._origin.max_score or float(self.value_smanager) < 0:
                self.value_smanager = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_smanager == 'k' or self.value_smanager == 'K':
                self.value_smanager = 'K'
            else:
                self.value_smanager = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_hddg')
    def _onchange_value_hddg(self):
        if self.isNumberic(self.value_hddg):
            if float(self.value_hddg) > self._origin.max_score or float(self.value_hddg) < 0:
                self.value_hddg = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_hddg == 'k' or self.value_hddg == 'K':
                self.value_hddg = 'K'
            else:
                self.value_hddg = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_colleague')
    def _onchange_value_colleague(self):
        if self.isNumberic(self.value_colleague):
            if float(self.value_colleague) > self._origin.max_score or float(self.value_colleague) < 0:
                self.value_colleague = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_colleague == 'k' or self.value_colleague == 'K':
                self.value_colleague = 'K'
            else:
                self.value_colleague = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_colleague2')
    def _onchange_value_colleague2(self):
        if self.isNumberic(self.value_colleague2):
            if float(self.value_colleague2) > self._origin.max_score or float(self.value_colleague2) < 0:
                self.value_colleague2 = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_colleague2 == 'k' or self.value_colleague2 == 'K':
                self.value_colleague2 = 'K'
            else:
                self.value_colleague2 = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.onchange('value_colleague3')
    def _onchange_value_colleague3(self):
        if self.isNumberic(self.value_colleague3):
            if float(self.value_colleague3) > self._origin.max_score or float(self.value_colleague3) < 0:
                self.value_colleague3 = self._origin.max_score
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}
        else:
            if self.value_colleague3 == 'k' or self.value_colleague3 == 'K':
                self.value_colleague3 = 'K'
            else:
                self.value_colleague3 = 'K'
                return {'value': {}, 'warning': {'title': 'Thông báo',
                                                 'message': 'Bạn chỉ nhập được ký tự K để bỏ qua,\n và giá trị nhập phải nhỏ hơn ' + str(
                                                     self.max_score)}}

    @api.multi
    def validate_percentage(self, post, answer_tag):
        self.ensure_one()
        errors = {}
        answer = post[answer_tag].strip()

        if not answer and self.validation_required:
            errors.update({answer_tag: 'The answer is required.'})

        if answer:
            try:
                float_answer = float(answer)
                if not (0 <= float_answer <= 100):
                    errors.update({answer_tag: 'Input value must be percentage.'})
            except ValueError:
                errors.update({answer_tag: _('This is not a number.')})
        return errors

    @api.model
    def save_lines(self, user_input_id, question, post, answer_tag):
        try:
            saver = getattr(self, 'save_line_' + question.data_type)
        except AttributeError:
            _logger.error(question.data_type + ": This type of question has no saving function")
            return False
        else:
            saver(user_input_id, question, post, answer_tag)

    @api.model
    def save_line_score(self, user_input_id, question, post, answer_tag):

        vals = {
            'user_input_id': user_input_id,
            'question_id': question.question_id.id,
            'skipped': False
        }

        answer_tag_question = '%s_%s' % (answer_tag, 'question')
        if answer_tag_question in post and post[answer_tag_question].strip():
            vals.update({'question_name': post[answer_tag_question]})

        answer_tag_comment = '%s_%s' % (answer_tag, 'comment')
        if answer_tag_comment in post and post[answer_tag_comment].strip():
            vals.update({'user_comment': post[answer_tag_comment]})
        else:
            vals.update({'user_comment': ''})

        if answer_tag in post and post[answer_tag].strip():
            vals.update({'value': float(post[answer_tag])})
        else:
            vals.update({'skipped': True})

        old_uil = self.search([
            ('user_input_id', '=', user_input_id),
            ('question_id', '=', question.question_id.id)
        ])

        if old_uil:
            old_uil.sudo().write(vals)
        # else:
        #     print("Khong duoc create, mac dinh luon luon co data")
        #     # old_uil.create(vals)

        return True

    @api.model
    def save_line_percentage(self, user_input_id, question, post, answer_tag):

        vals = {
            'user_input_id': user_input_id,
            'question_id': question.question_id.id,
            'skipped': False
        }

        answer_tag_question = '%s_%s' % (answer_tag, 'question')
        if answer_tag_question in post and post[answer_tag_question].strip():
            vals.update({'question_name': post[answer_tag_question]})

        answer_tag_comment = '%s_%s' % (answer_tag, 'comment')
        if answer_tag_comment in post and post[answer_tag_comment].strip():
            vals.update({'user_comment': post[answer_tag_comment]})
        else:
            vals.update({'user_comment': ''})

        if answer_tag in post and post[answer_tag].strip():
            vals.update({'value': float(post[answer_tag])})
        else:
            vals.update({'skipped': True})

        old_uil = self.search([
            ('user_input_id', '=', user_input_id),
            ('question_id', '=', question.question_id.id)
        ])

        if old_uil:
            old_uil.sudo().write(vals)
        # else:
        #     print("Khong duoc create, mac dinh luon luon co data")
        # old_uil.create(vals)

        return True

    @api.model
    def _set_user_id(self, user_id):
        self.user_id = user_id

    @api.model
    def create(self, values):
        return super(HR_Survey_User_Input_Lines, self).create(values)


class HRSurveyClassification(models.Model):
    _name = 'hr.survey.classification'
    _description = 'HR Appraisal Classification'

    name = fields.Char(string='Name', require=True)
    min_score = fields.Float(string='Min Score', require=True)
    max_score = fields.Float(string='Max Score', require=True)
    classification = fields.Char(string='Classification', require=True)
    classification_link = fields.Many2one('hr.survey.classification.link', ondelete='cascade')


class HRAppraisalClassification(models.Model):
    _name = 'hr.survey.classification.link'
    _description = 'HR Survey Classification Link'

    name = fields.Char(string='Name', required=True)
    survey_id = fields.Many2one('hr.survey', require=True)

    summary_id = fields.Many2one('hr.survey.summary', require=True, domain="[('survey_id','=',survey_id)]")
    survey_classification = fields.One2many('hr.survey.classification', 'classification_link', require=True, copy=True)

    @api.onchange('survey_id')
    def _onchange_survey_id(self):
        search_classification = self.env['hr.survey.classification.link'].sudo().search(
            [('survey_id', '=', self.survey_id.id)])
        list_classification = []
        for i in search_classification:
            list_classification.append(i.summary_id.id)

        search = self.env['hr.survey.summary'].sudo().search(
            [('survey_id', '=', self.survey_id.id), ('is_rating', '=', False), ('id', 'not in', list_classification)])
        if self.survey_id and search:
            self.summary_id = search[0]
            self.summary_ids = search


class Appraisal_Employee_Users(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def write(self, values):
        if values.get('user_id') is not None:
            rec = super(Appraisal_Employee_Users, self).write(values)
            user_inputs = self.env['hr.survey.user.input'].sudo().search([('employee_id', '=', self.id)])
            for user_input in user_inputs:
                user_input.sudo().write({'user_id': self.user_id.id})
            '''manager'''
            managers = self.env['hr.survey.user.input'].sudo().search([('manager_id', '=', self.id)])
            for manager in managers:
                manager.sudo().write({'user_manager_id': self.user_id.id})

            '''smanager'''
            smanagers = self.env['hr.survey.user.input'].sudo().search([('smanager_id', '=', self.id)])
            for smanager in smanagers:
                smanager.sudo().write({'user_smanager_id': self.user_id.id})

            '''colleague'''
            colleagues = self.env['hr.survey.user.input'].sudo().search([('colleague_id', '=', self.id)])
            for colleague in colleagues:
                colleague.sudo().write({'user_colleague_id': self.user_id.id})
            return rec
        else:
            super(Appraisal_Employee_Users, self).write(values)


# class IrHttp(models.AbstractModel):
#     _inherit = 'ir.http'
#
#     def session_info(self):
#         result = super(IrHttp, self).session_info()
#         if self.env.user.company_id.id != 1:
#             result['user_context'].update({'company_ids': [self.env.user.company_id.id]})
#         else:
#             result['user_context'].update({'company_ids': self.env.user.company_ids.ids})
#         return result
class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        if self.env.user.company_id.id != 1:
            result['user_context'].update({'company_ids': [self.env.user.company_id.id]})
            employee = self.env['hr.employee.multi.company'].sudo().search(
                [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)],
                limit=1)
            if employee:
                departments = self.env['hr.department'].sudo().search(
                    [('manager_ids', 'in', employee.sudo().name.id), ('company_id', '=',
                                                                      self.env.user.company_id.id)])
                if departments:
                    ids = []
                    for department in departments:
                        ids.append(department.id)
                        child_ids = self.get_child_department(department.id)
                        for child in child_ids:
                            ids.append(child)
                    result['user_context'].update({'department_managers': ids})
                # departments = self.env['hr.department'].sudo().search(
                #     [('id', '=', employee.sudo().department_id.id)])
                #
                # if departments and departments.manager_ids:
                #     for department in departments.manager_ids:
                # result['user_context'].update({'department_managers': departments.ids})
                else:
                    result['user_context'].update({'department_managers': []})
            else:
                result['user_context'].update({'department_managers': []})
        else:
            result['user_context'].update({'company_ids': self.env.user.company_ids.ids, 'department_managers': []})
        return result

    def get_child_department(self, department_parent_id):
        child_departments = self.env['hr.department'].sudo().search([('parent_id', '=', department_parent_id)])
        ids = []
        for child in child_departments:
            ids.append(child.id)
            child_ids = self.get_child_department(child.id)
            for id in child_ids:
                ids.append(id)
        return ids


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(
        selection_add=[('appraisal', 'Appraisal'), ('appraisal_colleague', 'Appraisal Colleague'),
                       ('sign_document', 'Sign Document')])

class ResCompanyNameGet(models.Model):
    _inherit='res.company'

    @api.multi
    def name_get(self):
        if self._context.get('get_short_name'):
            result=[]
            for record in self:
                name = record.short_name
                result.append((record.id, name))
            return result
        else:
            result= super(ResCompanyNameGet, self).name_get()
            return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if self._context.get('get_short_name'):
            # private implementation of name_search, allows passing a dedicated user
            # for the name_get part to solve some access rights issues
            args = list(args or [])
            # optimize out the default criterion of ``ilike ''`` that matches everything
            if not self._rec_name:
                _logger.warning("Cannot execute name_search, no _rec_name defined on %s", self._name)
            elif not (name == '' and operator == 'ilike'):
                args += [('short_name', operator, name)]
            access_rights_uid =  self._uid
            ids = self._search(args, limit=limit, access_rights_uid=access_rights_uid)
            recs = self.browse(ids)
            return models.lazy_name_get(recs.sudo(access_rights_uid))
        else:
            return super(ResCompanyNameGet, self).name_search(name=name, args=args,
                                                     operator=operator, limit=limit)