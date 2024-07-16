from lxml import etree
from odoo import api, models, fields
from odoo.addons.base.models.res_partner import _tz_get


class MultiCompany(models.Model):
    _name = 'hr.employee.multi.company'
    _description = 'Multi Company Employee'
    _order = 'company_code,department_code,job_code,s_identification_id asc'

    '''dkh add for sorting'''

    def _compute_job_code_compute(self):
        for rec in self:
            rec.sudo().write({'job_code': rec.job_id.sudo().sequence})
            rec.sudo().write({'department_code': rec.department_id.sudo().sort_name})
            rec.sudo().write({'company_code': rec.company_id.sudo().code})

    job_code_compute = fields.Char(compute='_compute_job_code_compute')
    job_code = fields.Char(string='Job Code')
    department_code = fields.Char(string='Department Code')
    company_code = fields.Char(string='Company Code')

    # def _address_company_(self):
    #     res_company = self.env['res.company'].sudo().search([('id', '=', self.company_id.id)])
    #
    #     self.address = str(res_company.street) + ", " + str(res_company.street2) + ", " + ", " + str(
    #         res_company.state_id.name) + ", " + str(res_company.country_id.name)
    #
    # NOT change
    name = fields.Many2one('hr.employee', "Name", required=True)

    # category_ids = fields.Many2many(
    #     'hr.employee.category', 'employee_category_rel',
    #     'emp_id', 'category_id', related='name.category_ids',
    #     string='Tags')

    seagroup_join_date = fields.Date(string='Seagroup Join Date')
    s_identification_id = fields.Char(string='SeaCode', copy=False)
    manager = fields.Boolean(string='Is a Manager')
    #     Income Information
    sea_employee_level = fields.Many2one('hr.employee.level', string="Employee Level",
                                         default=lambda self: self.env['hr.employee.level'].search([], limit=1))
    employee_current_status = fields.Selection([
        ('working', 'Working'),
        ('leaving', 'Unpaid leave'),
        ('maternity_leave', 'Parental leave'),
        ('sick_leave', 'Sick leave'),
        ('resigned', 'Resigned')

    ], string='Employee Status', help='Employee Status')

    # Change
    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')
    active = fields.Boolean('Active', default=True, store=True, readonly=False, groups='hr.group_hr_manager')

    # with 1 employee only 1 company = true
    primary_company = fields.Boolean('Primary Company', default=False, store=True, readonly=False)

    company_id = fields.Many2one('res.company', required=True, string='Company')
    # address = fields.Char("Work Address", compute="_address_company_")
    department_id = fields.Many2one('hr.department', string='Department', domain="[('company_id','=',company_id)]")
    job_id = fields.Many2one('hr.job', string='Job Position',
                             domain="[('company_id','=',company_id),('department_id','=',department_id)]")
    job_title = fields.Char(string="Job title")
    work_location = fields.Char('Work Location')
    work_phone = fields.Char('Work Phone')
    mobile_phone = fields.Char('Work Mobile')
    work_email = fields.Char('Work Email')
    coach_id = fields.Many2one('hr.employee', 'Coach')
    parent_id = fields.Many2one('hr.employee', string="Manager",
                                domain="[('company_id','=',company_id), ('manager','=',True)]")
    resource_calendar_id = fields.Many2one('resource.calendar', string="Working Hours"
                                           , required=False, domain="[('company_id','=',company_id)]")
    tz = fields.Selection(_tz_get, string='Timezone', compute='_default_multi_tz_multi_')

    reason_leaving = fields.Text(string='Reason Leaving')
    resignation_date = fields.Date(string='Resignation Date')
    leaving_to_date = fields.Date(string='Đến ngày')

    expense_manager_id = fields.Many2one('res.users', string="Expense Responsible",
                                         domain="[('company_id','=',company_id)]")
    user_id = fields.Many2one('res.users', string='Related User')
    # official_contract = fields.Date(string='Official Contract')
    # sea_net_salary = fields.Float('Trial salary', help="Trial Salary.")
    # sea_contract_salary = fields.Float('Contract salary', help="Net Salary.")
    # sea_extend_salary = fields.Float('Extend salary', help="Extend Salary.")
    insurance_status_m = fields.Selection([('join_insurance', 'Có tham gia'), ('not_join_insurance', 'Không tham gia')],
                                          string='Insurance Status')
    note_insurance_status = fields.Text(string='Note Insurance Status')
    joining_date = fields.Date(string='Joining Date')

    # child_ids = fields.One2many('hr.employee.multi.company', 'parent_id', string='Subordinates')

    @api.onchange('job_id')
    def _onchange_job_id_(self):
        # if self.job_id:
        for rec in self:
            rec.job_title = rec.job_id.name
        # print(self.env['res.users'].sudo().search([('id', '=', self.env.user.id)]).company_ids)

    @api.onchange('resource_calendar_id')
    def _onchange_resource_calendar_id_(self):
        for rec in self:
            if rec.resource_calendar_id:
                rec.tz = rec.resource_calendar_id.tz

    @api.multi
    def _default_multi_tz_multi_(self):
        for rec in self:
            rec.tz = rec.env['resource.calendar'].sudo().search(
                [('id', '=', rec.resource_calendar_id.id)]).tz

    # @api.model
    # def fields_view_get(self, view_id='view_multi_company_employee_form', view_type='form', toolbar=False,
    #                     submenu=False):
    #     if self.env.user.has_group('sea_multi_company_employee.group_hr_view_edit'):
    #         if view_type == 'form':
    #             view_id = self.env.ref(
    #                 'sea_multi_company_employee.view_multi_company_employee_form_group_hr_view_edit').id
    #         elif view_type == 'tree':
    #             view_id = self.env.ref('sea_multi_company_employee.view_multi_company_employee_tree_group_hr_view_edit').id
    #
    #     res = super(MultiCompany, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                     submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     res['arch'] = etree.tostring(doc)
    #     return res


class HREmployee(models.Model):
    _inherit = "hr.employee"

    # xóa ghi log lương
    sea_net_salary = fields.Float('Trial salary', digits=None, track_visibility="", help="Trial Salary.")
    sea_contract_salary = fields.Float('Contract salary', digits=None, track_visibility="", help="Net Salary.")
    sea_extend_salary = fields.Float('Extend salary', digits=None, track_visibility="", help="Extend Salary.")

    @api.onchange('employee_current_status_compute')
    def onchange_group_ids(self):
        self.reason_leaving_compute = None
        self.resignation_date_compute = None
        self.leaving_to_date_compute = None

    sea_company_ids_temp = fields.Many2many('res.company', string='Sea Companies Temp', compute='_sea_company_ids_tmp_')

    employee_multi_company = fields.One2many('hr.employee.multi.company', 'name',
                                             string="Multi Company Employee")

    def _company_id_compute_(self):
        for rec in self:
            rec.company_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).company_id

    company_id_compute = fields.Many2one('res.company', "Company", compute='_company_id_compute_',
                                         default=lambda self: self.env.user.company_id.id)
    note_insurance_status = fields.Text(string='Insurance Status')
    insurance_status_m = fields.Selection([('join_insurance', 'Có tham gia'), ('not_join_insurance', 'Không tham gia')],
                                          string='Insurance Status')

    def _reason_leaving_compute_(self):
        for rec in self:
            rec.reason_leaving_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).reason_leaving

    def _resignation_date_compute_(self):
        for rec in self:
            rec.resignation_date_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).resignation_date

    def _leaving_to_date_compute_(self):
        for rec in self:
            rec.leaving_to_date_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).leaving_to_date

    def _employee_current_status_compute_(self):
        for rec in self:
            rec.employee_current_status_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).employee_current_status

    employee_current_status_compute = fields.Selection([
        ('working', 'Working'),
        ('leaving', 'Unpaid leave'),
        ('maternity_leave', 'Parental leave'),
        ('sick_leave', 'Sick leave'),
        ('resigned', 'Resigned')
    ], string='Employee Status', help='Employee Status', default='working', compute="_employee_current_status_compute_")
    # def _manager_compute_(self):
    #     self.manager_compute = self.env['hr.employee.multi.company'].sudo().search(
    #         ['|', ('active', '=', False), ('active', '=', True),
    #         ('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).manager
    # manager_compute = fields.Boolean(string='Is a Manager', compute='_manager_compute_')

    reason_leaving_compute = fields.Text(string='Reason Leaving', compute="_reason_leaving_compute_")
    resignation_date_compute = fields.Date(string='Resignation Date', compute="_resignation_date_compute_")
    leaving_to_date_compute = fields.Date(string='Đến ngày', compute="_leaving_to_date_compute_")

    def _insurance_status_m_compute_(self):
        for rec in self:
            rec.insurance_status_m_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).insurance_status_m

    def _note_insurance_status_compute_(self):
        for rec in self:
            rec.note_insurance_status_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).note_insurance_status

    insurance_status_m_compute = fields.Selection(
        [('join_insurance', 'Có tham gia'), ('not_join_insurance', 'Không tham gia')],
        string='Insurance Status', compute='_insurance_status_m_compute_')
    note_insurance_status_compute = fields.Text(string='Note Insurance Status',
                                                compute='_note_insurance_status_compute_')

    def _address_company_(self):
        for rec in self:
            res_company = rec.env.user.company_id
            address = ""
            if res_company.street:
                address += str(res_company.street)
                address += ", "
            if res_company.street2:
                address += str(res_company.street2)
                address += ", "
            if res_company.state_id:
                address += str(res_company.state_id.name)
                address += ", "
            if res_company.country_id:
                address += str(res_company.country_id.name)

            rec.address_compute = address

    address_compute = fields.Char("Work Address", compute="_address_company_")

    def _department_id_compute_(self):
        for rec in self:
            rec.department_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).department_id

    def _job_id_compute_(self):
        for rec in self:
            rec.job_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).job_id

    def _job_title_compute_(self):
        for rec in self:
            rec.job_title_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).job_title

    def _work_location_compute_(self):
        for rec in self:
            rec.work_location_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).work_location

    def _work_phone_compute_(self):
        for rec in self:
            rec.work_phone_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).work_phone

    def _mobile_phone_compute_(self):
        for rec in self:
            rec.mobile_phone_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).mobile_phone

    def _work_email_compute_(self):
        for rec in self:
            rec.work_email_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).work_email

    def _coach_id_compute_(self):
        for rec in self:
            rec.coach_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).coach_id

    # def _manager_compute_(self):
    #     self.manager_compute = self.env['hr.employee.multi.company'].sudo().search(
    #         ['|', ('active', '=', False), ('active', '=', True),
    #         ('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).manager

    def _parent_id_compute_(self):
        for rec in self:
            rec.parent_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).parent_id

    def _resource_calendar_id_compute_(self):
        for rec in self:
            rec.resource_calendar_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).resource_calendar_id

    def _tz_compute_(self):
        for rec in self:
            rec.tz_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).tz

    department_id_compute = fields.Many2one('hr.department', string='Department',
                                            domain="[('company_id','=',company_id_compute)]",
                                            compute="_department_id_compute_")
    job_id_compute = fields.Many2one('hr.job', string='Job Position',
                                     domain="[('company_id','=',company_id_compute),('department_id','=',"
                                            "department_id_compute)]",
                                     compute='_job_id_compute_')
    job_title_compute = fields.Char(string="Job title", compute='_job_title_compute_')
    work_location_compute = fields.Char('Work Location', compute='_work_location_compute_')
    work_phone_compute = fields.Char('Work Phone', compute='_work_phone_compute_')
    mobile_phone_compute = fields.Char('Work Mobile', compute='_mobile_phone_compute_')
    work_email_compute = fields.Char('Work Email', compute='_work_email_compute_')
    coach_id_compute = fields.Many2one('hr.employee', 'Coach', compute='_coach_id_compute_')
    # manager_compute = fields.Boolean(string='Is a Manager', compute='_manager_compute_')
    parent_id_compute = fields.Many2one('hr.employee', string="Manager",
                                        domain="[('manager','=',True)]",
                                        compute='_parent_id_compute_')
    resource_calendar_id_compute = fields.Many2one('resource.calendar', string="Working Hours",
                                                   domain="[('company_id','=',company_id_compute)]",
                                                   required=False, compute='_resource_calendar_id_compute_')
    tz_compute = fields.Selection(_tz_get, string='Timezone', compute='_tz_compute_')

    def _expense_manager_id_compute_(self):
        for rec in self:
            rec.expense_manager_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).expense_manager_id

    # def _user_id_compute_(self):
    #     self.user_id_compute = self.env['hr.employee.multi.company'].sudo().search(
    #         ['|', ('active', '=', False), ('active', '=', True),
    #         ('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).user_id

    def _joining_date_compute_(self):
        for rec in self:
            employee = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)])

            rec.joining_date_compute = employee.joining_date
            rec.primary_company_compute = employee.primary_company
            # print(rec.primary_company_compute)

    expense_manager_id_compute = fields.Many2one('res.users', string="Expense Responsible",
                                                 domain="[('company_id','=',company_id_compute)]",
                                                 compute='_expense_manager_id_compute_')
    # user_id_compute = fields.Many2one('res.users', string='Related User', compute='_user_id_compute_')
    joining_date_compute = fields.Date(string='Joining Date', compute='_joining_date_compute_')

    primary_company_compute = fields.Boolean('Primary Company', readonly=False, compute='_joining_date_compute_')

    def _official_contract_seagroup_compute_(self):
        for rec in self:
            contracts = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('state', '!=', 'cancel')])
            if contracts:
                date = [contract.date_start for contract in contracts if contract.date_start not in [False, None]]
                if date:
                    rec.official_contract_seagroup = min(date)

    def _official_contract_compute_(self):
        for rec in self:
            contracts = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id),
                 ('state', '!=', 'cancel')])
            if contracts:
                date = [contract.date_start for contract in contracts if contract.date_start not in [False, None]]
                if date:
                    rec.official_contract_company = min(date)

    official_contract_seagroup = fields.Date(string='Official Contract SeaGroup',
                                             compute='_official_contract_seagroup_compute_')
    official_contract_company = fields.Date(string='Official Contract', compute='_official_contract_compute_')

    child_ids_m = fields.One2many('hr.employee', 'parent_id_compute', string='Subordinates')

    main_phone_number = fields.Char(string='Main Phone Number')
    second_phone_number = fields.Char(string='Second Phone Number')

    def _sea_net_salary_seagroup_(self):
        for rec in self:
            salary_s = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 4), ('employee_id', '=', rec.id),
                 ('state', '!=', 'cancel')])
            sal = 0
            if salary_s:
                for salary in salary_s:
                    if salary.wage not in [False, None]:
                        sal += salary.wage
            rec.sea_net_salary_seagroup = sal

    def _sea_contract_salary_seagroup_(self):
        for rec in self:
            salary_contract = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('state', 'in', ['pending', 'open'])])
            sal = 0
            if salary_contract:
                for salary in salary_contract:
                    salary_extend = rec.env['hr.contract'].sudo().search(
                        [('contract_category', '=', 'addition'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                         ('company_id', '=', salary.company_id.id), ('state', 'in', ['pending', 'open']),
                         ('wage', '>', 0)], order='wage desc', limit=1)
                    sal += salary_extend.wage if salary_extend else salary.wage
            rec.sea_contract_salary_seagroup = sal

    def _sea_extend_salary_seagroup_(self):
        for rec in self:
            salary_s = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'addition'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('state', 'in', ['pending', 'open']), ('contract_extend_salary', '>', 0)])
            sal = 0
            if salary_s:
                for salary in salary_s:
                    sal += salary.contract_extend_salary
            rec.sea_extend_salary_seagroup = sal

    sea_net_salary_seagroup = fields.Float('Trial salary SeaGroup', help="Trial Salary SeaGroup.",
                                           compute='_sea_net_salary_seagroup_')
    sea_contract_salary_seagroup = fields.Float('Contract salary SeaGroup', help="Net Salary SeaGroup.",
                                                compute='_sea_contract_salary_seagroup_')
    sea_extend_salary_seagroup = fields.Float('Extend salary SeaGroup', help="Extend Salary SeaGroup.",
                                              compute='_sea_extend_salary_seagroup_')

    def _sea_net_salary_company_(self):
        for rec in self:
            salary_s = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 4), ('employee_id', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id), ('state', '!=', 'cancel')],
                order='wage desc', limit=1)

            sal = 0
            if salary_s:
                if salary_s.wage not in [False, None]:
                    sal = salary_s.wage
            #     for salary in salary_s:
            #         if salary.wage not in [False, None]:
            #             sal += salary.wage
            rec.sea_net_salary_company = sal

    def _sea_contract_salary_company_(self):
        for rec in self:
            salary_contract = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'contract'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id), ('state', 'in', ['pending', 'open']),
                 ('wage', '>', 0)], order='wage desc', limit=1)
            salary_extend = rec.env['hr.contract'].sudo().search(
                [('contract_category', '=', 'addition'), ('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id), ('state', 'in', ['pending', 'open']),
                 ('wage', '>', 0)], order='wage desc', limit=1)
            rec.sea_contract_salary_company = salary_extend.wage if salary_extend else (
                salary_contract.wage if salary_contract else 0)

    def _sea_extend_salary_company_(self):
        for rec in self:
            salary_s = rec.env['hr.contract'].sudo().search(
                [('type_id', '=', 1), ('employee_id', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id), ('state', 'in', ['pending', 'open']),
                 ('contract_category', '=', 'addition'), ('contract_extend_salary', '>', 0)],
                order='contract_extend_salary desc', limit=1)
            rec.sea_extend_salary_company = salary_s.contract_extend_salary if salary_s else 0

    sea_net_salary_company = fields.Float('Trial salary', help="Trial Salary.",
                                          compute='_sea_net_salary_company_')
    sea_contract_salary_company = fields.Float('Contract salary', help="Net Salary.",
                                               compute='_sea_contract_salary_company_')
    sea_extend_salary_company = fields.Float('Extend salary', help="Extend Salary.",
                                             compute='_sea_extend_salary_company_')

    # sum_salary_company = fields.Float('Salary Company', help="Salary Company.")
    # sum_salary_seagroup = fields.Float('Sum Salary SeaGroup', help="Sum Salary SeaGroup.")

    def _operating_unit_id_compute_(self):
        for rec in self:
            rec.operating_unit_id_compute = rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.env.user.company_id.id)]).operating_unit_id

    operating_unit_id_compute = fields.Many2one('operating.unit', 'Operating Unit',
                                                compute='_operating_unit_id_compute_')

    place_of_initial_medical_examination_and_treatment = fields.Char(
        string='Place of initial medical examination and treatment')

    @api.multi
    def _sea_company_ids_tmp_(self):
        for rec in self:
            rec.sea_company_ids_temp = rec.env.user.company_ids
            # print([m.id for m in rec.sea_company_ids_temp])

    @api.multi
    def write(self, vals):
        for rec in self:
            if vals.get('sea_company_ids') is not None:
                multi_company_ids = vals.get('sea_company_ids')[0][2]
                if vals.get('user_id') is None:
                    company_ids = self.user_id
                else:
                    company_ids = self.env['res.users'].sudo().search(
                        [('id', '=', vals.get('user_id'))])
                for i in multi_company_ids:
                    if company_ids and i not in [j.id for j in company_ids.company_ids]:
                        company_ids.write({'company_ids': [(4, i)]})
                        print("Insert allowed companies", i)

                    if not rec.env['hr.employee.multi.company'].sudo().search(
                            ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                             ('company_id', '=', i)]):
                        rec.env['hr.employee.multi.company'].sudo().create(
                            {'name': rec.id, 'company_id': i, 'user_id': rec.user_id.id,
                             'seagroup_join_date': rec.seagroup_join_date,
                             's_identification_id': rec.s_identification_id,
                             'sea_employee_level': rec.sea_employee_level.id,
                             'employee_current_status': 'working',
                             'manager': rec.manager,
                             'active': rec.active})
                    else:
                        rec.env['hr.employee.multi.company'].sudo().search(
                            ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                             ('company_id', '=', i)]).write({'active': True})
                list_company = rec.env['hr.employee.multi.company'].sudo().search([('name', '=', rec.id)])

                for l in list_company:
                    if l.company_id.id not in multi_company_ids:
                        rec.env['hr.employee.multi.company'].sudo().search(
                            [('name', '=', rec.id), ('company_id', '=', l.company_id.id)]).write({'active': False})

            multi_company_employee = rec.env['hr.employee.multi.company'].sudo().search(
                [('name', '=', rec.id), ('company_id', '=', rec.env.user.company_id.id)])
            list_company = rec.env['hr.employee.multi.company'].sudo().search([('name', '=', rec.id)])

            if vals.get('reason_leaving_compute') is not None:
                multi_company_employee.write(
                    {'reason_leaving': vals.get('reason_leaving_compute')})
            if vals.get('resignation_date_compute') is not None:
                multi_company_employee.write(
                    {'resignation_date': vals.get('resignation_date_compute')})
            if vals.get('leaving_to_date_compute') is not None:
                multi_company_employee.write(
                    {'leaving_to_date': vals.get('leaving_to_date_compute')})
            if vals.get('insurance_status_m_compute') is not None:
                multi_company_employee.write(
                    {'insurance_status_m': vals.get('insurance_status_m_compute')})
            if vals.get('note_insurance_status_compute') is not None:
                multi_company_employee.write(
                    {'note_insurance_status': vals.get('note_insurance_status_compute')})
            if vals.get('department_id_compute') is not None:
                multi_company_employee.write(
                    {'department_id': vals.get('department_id_compute')})
            if vals.get('job_id_compute') is not None:
                multi_company_employee.write(
                    {'job_id': vals.get('job_id_compute')})
            if vals.get('job_title_compute') is not None:
                multi_company_employee.write(
                    {'job_title': vals.get('job_title_compute')})
            if vals.get('work_location_compute') is not None:
                multi_company_employee.write(
                    {'work_location': vals.get('work_location_compute')})
            if vals.get('work_phone_compute') is not None:
                multi_company_employee.write(
                    {'work_phone': vals.get('work_phone_compute')})
            if vals.get('mobile_phone_compute') is not None:
                multi_company_employee.write(
                    {'mobile_phone': vals.get('mobile_phone_compute')})
            if vals.get('work_email_compute') is not None:
                multi_company_employee.write(
                    {'work_email': vals.get('work_email_compute')})
            if vals.get('coach_id_compute') is not None:
                multi_company_employee.write(
                    {'coach_id': vals.get('coach_id_compute')})
                # if vals.get('manager_compute') is not None:
                #     multi_company_employee.write(
                #         {'manager': vals.get('manager_compute')})
            if vals.get('parent_id_compute') is not None:
                multi_company_employee.write(
                    {'parent_id': vals.get('parent_id_compute')})
            if vals.get('resource_calendar_id_compute') is not None:
                multi_company_employee.write(
                    {'resource_calendar_id': vals.get('resource_calendar_id_compute')})
            if vals.get('tz_compute') is not None:
                multi_company_employee.write(
                    {'tz': vals.get('tz_compute')})
            if vals.get('expense_manager_id_compute') is not None:
                multi_company_employee.write(
                    {'expense_manager_id': vals.get('expense_manager_id_compute')})
            # if vals.get('user_id_compute') is not None:
            #     multi_company_employee.write(
            #         {'user_id': vals.get('user_id_compute')})
            if vals.get('joining_date_compute') is not None:
                multi_company_employee.write(
                    {'joining_date': vals.get('joining_date_compute')})
            if vals.get('employee_current_status_compute') is not None:
                multi_company_employee.write({'employee_current_status': vals.get('employee_current_status_compute')})
                if vals.get('employee_current_status_compute') == 'resigned':
                    contracts = rec.env['hr.contract'].sudo().search(
                        [('employee_id', '=', rec.id), ('company_id', '=', rec.company_id_compute.id)])
                    if contracts:
                        for contract in contracts:
                            contract.write({'state': "close"})
            # primary company
            # print(vals)

            if vals.get('primary_company_compute') is not None and vals.get('primary_company_compute') == True:
                for company in list_company:
                    if company.id != multi_company_employee.company_id.id:
                        company.write({'primary_company': False})
                multi_company_employee.write(
                    {'primary_company': vals.get('primary_company_compute')})
            if vals.get('operating_unit_id_compute'):
                multi_company_employee.write(
                    {'operating_unit_id': vals.get('operating_unit_id_compute')})

            # values change all company
            if vals.get('user_id') is not None:
                if vals.get('sea_company_ids') is None:
                    multi_company_ids = self.sea_company_ids
                    company_ids = self.env['res.users'].sudo().search(
                        [('id', '=', vals.get('user_id'))])
                    for i in multi_company_ids:
                        if company_ids and i.id not in [j.id for j in company_ids.company_ids]:
                            company_ids.write({'company_ids': [(4, i.id)]})
                            print("Insert allowed companies", i.id)
                for company in list_company:
                    company.write({'user_id': vals.get('user_id')})
            if vals.get('seagroup_join_date') is not None:
                for company in list_company:
                    company.write({'seagroup_join_date': vals.get('seagroup_join_date')})
            if vals.get('s_identification_id') is not None:
                for company in list_company:
                    company.write({'s_identification_id': vals.get('s_identification_id')})
            if vals.get('manager') is not None:
                for company in list_company:
                    company.write({'manager': vals.get('manager')})
            if vals.get('sea_employee_level') is not None:
                for company in list_company:
                    company.write({'sea_employee_level': vals.get('sea_employee_level')})
            # if vals.get('employee_current_status') is not None:
            #     for company in list_company:
            #         company.write({'employee_current_status': vals.get('employee_current_status')})
            if vals.get('active') is not None:
                if vals.get('active') == True:
                    list_companyss = rec.env['hr.employee.multi.company'].sudo().search(
                        [('name', '=', rec.id), ('active', '=', False)])
                    # list = []
                    # for ids in list_companyss:
                    #     print(ids.company_id, rec.sea_company_ids)
                    #     if ids.company_id in rec.sea_company_ids:
                    #         list.append(ids.company_id.id)
                    list_company = [i.id for i in list_companyss if i.company_id in rec.sea_company_ids]
                    list_companys = rec.env['hr.employee.multi.company'].sudo().browse(list_company)
                else:
                    list_companys = list_company

                for company in list_companys:
                    company.write({'active': vals.get('active')})

        return super(HREmployee, self).write(vals)

    @api.onchange('sea_company_ids')
    def onchange_sea_company_ids(self):
        for rec in self:
            list_company_ids = rec.env['hr.employee'].sudo().search([('id', '=', self._origin.id)])
            for i in list_company_ids.sea_company_ids:
                if i not in rec.sea_company_ids:
                    if i == rec.env.user.company_id:
                        rec.sea_company_ids = [(4, i.id)]
                        return {'warning': {
                            'title': 'Lỗi xóa working companies',
                            'message': "Bạn không thể xóa CTY này",
                        }}

    @api.model
    def multi_company_copy_action(self):
        employees = self.env['hr.employee'].sudo().search([('active', 'in', [True, False])])
        for employee in employees:
            employee.write({'note_insurance_status': employee.insurance_status})

            if employee.company_id:
                list_company = [i.id for i in employee.sea_company_ids]
                if employee.company_id.id not in list_company:
                    employee.sea_company_ids = [(4, employee.company_id.id)]
                for company in employee.sea_company_ids:
                    if not self.env['hr.employee.multi.company'].sudo().search(
                            [('name', '=', employee.id),
                             ('company_id', '=', company.id)]) and employee.company_id.id != company.id:
                        self.env['hr.employee.multi.company'].sudo().create(
                            {'name': employee.id, 'company_id': company.id, 'user_id': employee.user_id.id,
                             'seagroup_join_date': employee.seagroup_join_date,
                             's_identification_id': employee.s_identification_id,
                             'sea_employee_level': employee.sea_employee_level.id,
                             'employee_current_status': employee.employee_current_status,
                             'manager': employee.manager,
                             'active': employee.active})

                if not self.env['hr.employee.multi.company'].sudo().search(
                        [('name', '=', employee.id), ('company_id', '=', employee.company_id.id)]):
                    # print("not",company.id, employee.id)
                    self.env['hr.employee.multi.company'].sudo().create({
                        'name': employee.id, 'company_id': employee.company_id.id,
                        'department_id': employee.department_id.id, 'job_id': employee.job_id.id,
                        'job_title': employee.job_title, 'work_location': employee.work_location,
                        'work_phone': employee.work_phone,
                        'mobile_phone': employee.mobile_phone, 'work_email': employee.work_email,
                        'coach_id': employee.coach_id.id,
                        'manager': employee.manager, 'parent_id': employee.parent_id.id,
                        'resource_calendar_id': employee.resource_calendar_id.id,
                        'tz': employee.tz,
                        'employee_current_status': employee.employee_current_status,
                        'reason_leaving': employee.reason_leaving,
                        'resignation_date': employee.resignation_date, 'leaving_to_date': employee.leaving_to_date,
                        'expense_manager_id': employee.expense_manager_id.id, 'user_id': employee.user_id.id,
                        'sea_employee_level': employee.sea_employee_level.id,
                        # 'official_contract': employee.official_contract,
                        'insurance_status_m': employee.insurance_status_m,
                        'joining_date': employee.joining_date,
                        'note_insurance_status': employee.note_insurance_status,
                        'seagroup_join_date': employee.seagroup_join_date,
                        's_identification_id': employee.s_identification_id,
                        'active': employee.active,
                        'primary_company': True})
            else:
                list_company = [i.id for i in employee.sea_company_ids]
                if 1 not in list_company:
                    employee.sea_company_ids = [(4, 1)]
                for company in employee.sea_company_ids:
                    if not self.env['hr.employee.multi.company'].sudo().search(
                            [('name', '=', employee.id),
                             ('company_id', '=', company.id)]) and 1 != company.id:
                        self.env['hr.employee.multi.company'].sudo().create(
                            {'name': employee.id, 'company_id': company.id, 'user_id': employee.user_id.id,
                             'seagroup_join_date': employee.seagroup_join_date,
                             's_identification_id': employee.s_identification_id,
                             'sea_employee_level': employee.sea_employee_level.id,
                             'employee_current_status': employee.employee_current_status,
                             'manager': employee.manager,
                             'active': employee.active})

                if not self.env['hr.employee.multi.company'].sudo().search(
                        [('name', '=', employee.id), ('company_id', '=', 1)]):
                    # print("not",company.id, employee.id)
                    self.env['hr.employee.multi.company'].sudo().create({
                        'name': employee.id, 'company_id': 1,
                        'department_id': employee.department_id.id, 'job_id': employee.job_id.id,
                        'job_title': employee.job_title, 'work_location': employee.work_location,
                        'work_phone': employee.work_phone,
                        'mobile_phone': employee.mobile_phone, 'work_email': employee.work_email,
                        'coach_id': employee.coach_id.id,
                        'manager': employee.manager, 'parent_id': employee.parent_id.id,
                        'resource_calendar_id': employee.resource_calendar_id.id,
                        'tz': employee.tz,
                        'employee_current_status': employee.employee_current_status,
                        'reason_leaving': employee.reason_leaving,
                        'resignation_date': employee.resignation_date, 'leaving_to_date': employee.leaving_to_date,
                        'expense_manager_id': employee.expense_manager_id.id, 'user_id': employee.user_id.id,
                        'sea_employee_level': employee.sea_employee_level.id,
                        # 'official_contract': employee.official_contract,
                        'insurance_status_m': employee.insurance_status_m,
                        'joining_date': employee.joining_date,
                        'note_insurance_status': employee.note_insurance_status,
                        'seagroup_join_date': employee.seagroup_join_date,
                        's_identification_id': employee.s_identification_id,
                        'active': employee.active,
                        'primary_company': True})

    @api.onchange('department_id_compute')
    def _onchange_department_id_compute_(self):
        for rec in self:
            # if self.job_id:
            rec.job_id_compute = None
            rec.job_title_compute = None
            rec.job_title_compute = None
            # print(rec.env['res.users'].sudo().search([('id', '=', rec.env.user.id)]).company_ids)

    @api.onchange('job_id_compute')
    def _onchange_job_id_compute_(self):
        for rec in self:
            # if self.job_id:
            rec.job_title_compute = rec.job_id_compute.name
            # print(self.env['res.users'].sudo().search([('id', '=', self.env.user.id)]).company_ids)

    @api.onchange('resource_calendar_id_compute')
    def _onchange_resource_calendar_id_compute_(self):
        for rec in self:
            if rec.resource_calendar_id_compute:
                rec.tz_compute = rec.resource_calendar_id_compute.tz

    @api.model
    def create(self, vals):
        # print(vals)
        # print(vals['sea_company_ids'][0][2])
        if 'sea_company_ids' in vals:
            if self.env.user.company_id.id not in vals['sea_company_ids'][0][2]:
                vals['sea_company_ids'][0][2].append(self.env.user.company_id.id)
                # print(vals['sea_company_ids'])
        else:
            vals.update({'sea_company_ids': [[6, False, [self.env.user.company_id.id]]]})
            # print(vals['sea_company_ids'])
        result = super(HREmployee, self).create(vals)

        self.env['hr.employee.multi.company'].sudo().create({
            'name': self.env['hr.employee'].sudo().search([], order="id desc", limit=1).id,
            'company_id': self.env.user.company_id.id,
            'department_id': vals.get('department_id_compute'), 'job_id': vals.get('job_id_compute'),
            'job_title': vals.get('job_title_compute'), 'work_location': vals.get('work_location_compute'),
            'work_phone': vals.get('work_phone_compute'),
            'mobile_phone': vals.get('mobile_phone_compute'), 'work_email': vals.get('work_email_compute'),
            'coach_id': vals.get('coach_id_compute'),
            'manager': vals.get('manager'), 'parent_id': vals.get('parent_id_compute'),
            'resource_calendar_id': vals.get('resource_calendar_id_compute'),
            'tz': vals.get('tz_compute'),
            'employee_current_status': vals.get('employee_current_status_compute'),
            # 'reason_leaving': vals['reason_leaving_compute'],
            # 'resignation_date': vals['resignation_date_compute'], 'leaving_to_date': vals['leaving_to_date_compute'],
            'expense_manager_id': vals.get('expense_manager_id_compute'), 'user_id': vals.get('user_id'),
            'sea_employee_level': vals.get('sea_employee_level'),
            'insurance_status_m': vals.get('insurance_status_m_compute'),
            'joining_date': vals.get('joining_date_compute'),
            'note_insurance_status': vals.get('note_insurance_status_compute'),
            'seagroup_join_date': vals.get('seagroup_join_date'),
            's_identification_id': vals.get('s_identification_id'),
            'primary_company': True})
        print("end")

        return result

    # @api.model
    # def fields_view_get(self, view_id='hr_employee_view_form', view_type='form', toolbar=False, submenu=False):
    #     if self.env.user.has_group('sea_multi_company_employee.group_hr_view_edit'):
    #         if view_type == 'form':
    #             view_id = self.env.ref('sea_multi_company_employee.hr_employee_view_form_group_edit_view').id
    #         elif view_type == 'tree':
    #             view_id = self.env.ref('sea_multi_company_employee.view_employee_tree_group_edit_view').id
    #
    #     res = super(HREmployee, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                   submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     res['arch'] = etree.tostring(doc)
    #     return res

    @api.model
    def fields_view_get(self, view_id='hr_employee_view_form_multiple_company', view_type='form', toolbar=False,
                        submenu=False):
        res = super(HREmployee, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                      submenu=submenu)
        doc = etree.XML(res['arch'])
        if view_type == 'form':
            if self.env.user.company_id.id != 1:
                for node in doc.xpath("//field[@name='joining_date_compute']"):
                    node.set('modifiers', '{"required": true}')
            else:
                for node in doc.xpath("//field[@name='resignation_date_compute']"):
                    node.set('modifiers', '{"required": false}')

        '''control view base group'''
        if self.env.user.has_group('hr.group_hr_user') and \
                view_type == 'form':
            for node in doc.xpath("//page[@name='personal_information']"):
                '''Page 01'''
                node.set('modifiers', '{"invisible": false}')
            for node in doc.xpath("//page[@name='public']"):
                '''Page 02'''
                node.set('modifiers', '{"invisible": false}')
            for node in doc.xpath("//page[@name='hr_settings']"):
                '''Page 03'''
                node.set('modifiers', '{"invisible": false}')
            # for node in doc.xpath("//notebook/page[6]"):
            #     node.set('modifiers', '{"invisible": false}')
            for node in doc.xpath("//notebook/page[7]"):
                node.set('modifiers', '{"invisible": false}')
            for node in doc.xpath("//notebook/page[8]"):
                node.set('modifiers', '{"invisible": false}')
            for node in doc.xpath("//notebook/page[9]"):
                node.set('modifiers', '{"invisible": false}')

        res['arch'] = etree.tostring(doc)
        return res

    # '''control view base group'''

    @api.depends('user_id')
    def _compute_display_personal_data(self):
        for employee in self:
            employee.employee_display_personal_data = False
            if employee.user_id == self.env.user:
                employee.employee_display_personal_data = True

    employee_display_personal_data = fields.Boolean(
        compute='_compute_display_personal_data'
    )
