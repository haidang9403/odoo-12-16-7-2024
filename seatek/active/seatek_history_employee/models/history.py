# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class HistoryEmployee(models.Model):
    _inherit = 'hr.employee'

    # @api.onchange('employee_current_status_compute')
    # def onchange_group_ids(self):
    #     self.reason_leaving_compute = None
    #     self.resignation_date_compute = None
    #     self.leaving_to_date_compute = None

    @api.multi
    def sea_salary_history(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hr.group_hr_manager'):
            return {
                'name': _("Salary History"),
                'view_mode': 'tree',
                'view_type': 'form',
                'res_model': 'sea.employee.history.salary',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'domain': [('employee_multi_id', '=', self.env['hr.employee.multi.company'].sudo().search(
                    [('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).id)]
            }
        else:
            raise UserError('You cannot access this field!!!!')

    @api.multi
    def sea_salary_chart(self):
        # pass
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hr.group_hr_manager'):
            view = self.env.ref('seatek_history_employee.sea_employee_salary_history_company_graph')
            return {
                'name': _("Salary Chart"),
                'view_mode': 'graph',
                'view_id': view.id,
                'res_model': 'sea.employee.history.salary',
                'type': 'ir.actions.act_window',
                'domain': [('employee_multi_id', '=', self.env['hr.employee.multi.company'].sudo().search(
                    [('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).id)]
            }
        else:
            raise UserError('You cannot access this field!!!!')

    @api.multi
    def sea_employee_history(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('hr.group_hr_manager'):
            return {
                'name': _("Employee History"),
                'view_mode': 'tree',
                'view_type': 'form',
                'res_model': 'sea.employee.history',
                'type': 'ir.actions.act_window',
                # 'target': 'new',
                'domain': [('employee_multi_id', '=', self.env['hr.employee.multi.company'].sudo().search(
                    [('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).id)]
            }
        else:
            raise UserError('You cannot access this field!!!!')

    @api.multi
    def sea_employee_status_history(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        search_view = self.env.ref('seatek_history_employee.sea_employee_status_history_search')
        if res_user.has_group('hr.group_hr_manager'):
            return {
                'name': _("Employee Status History"),
                'view_mode': 'tree',
                'res_model': 'sea.employee.history.current.status',
                'type': 'ir.actions.act_window',
                'search_view_id': search_view.id,
                # 'target': 'new',
                'domain': [('employee_multi_id', '=', self.env['hr.employee.multi.company'].sudo().search(
                    [('name', '=', self.id), ('company_id', '=', self.env.user.company_id.id)]).id)]
            }
        else:
            raise UserError('You cannot access this field!!!!')

    def current_status(self, current_status='working'):
        current = "Đang làm việc"
        if current_status == 'leaving':
            current = "Nghỉ phép không lương"
        elif current_status == 'maternity_leave':
            current = "Nghỉ thai sản"
        elif current_status == 'sick_leave':
            current = "Nghỉ ốm đau"
        elif current_status == 'resigned':
            current = "Đã nghỉ việc"
        return current

    @api.multi
    def write(self, vals):
        for employee_s in self:
            employee = self.env['hr.employee.multi.company'].sudo().search(
                [('name', '=', employee_s.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
            if employee:
                if 'employee_current_status_compute' in vals:
                    values = {
                        'employee_multi_id': employee.id,
                        'updated_date': datetime.today(),
                        'user_id': self.env.user.id,
                        'changed_field': 'Cập nhật Trạng thái nhân viên',
                        'current_value_before': self.current_status(employee_s.employee_current_status_compute),
                        'current_value_after': self.current_status(vals.get('employee_current_status_compute')),
                    }
                    history = self.env['sea.employee.history'].create(values)
                    values_detail = {
                        'employee_current_status_old': employee_s.employee_current_status_compute,
                        'employee_current_status': vals.get('employee_current_status_compute'),
                        'reason_leaving': vals.get('reason_leaving_compute'),
                        'resignation_date': vals.get('resignation_date_compute'),
                        'leaving_to_date': vals.get('leaving_to_date_compute'),
                        'history_id': history.id,
                        'current': True
                    }
                    current_status = self.env['sea.employee.history.current.status'].sudo().search(
                        [('employee_multi_id', '=', employee.id)])
                    if current_status:
                        for cs in current_status:
                            cs.write({'current': False})
                    self.env['sea.employee.history.current.status'].create(values_detail)

                elif 'resignation_date_compute' in vals or 'reason_leaving_compute' in vals \
                        or 'leaving_to_date_compute' in vals:
                    status = self.env['sea.employee.history.current.status'].sudo().search(
                        [('employee_multi_id', '=', employee.id), ('current', '=', True)], limit=1)
                    if status:
                        if 'reason_leaving_compute' in vals:
                            status.write({'reason_leaving': vals.get('reason_leaving_compute')})
                        if 'resignation_date_compute' in vals:
                            status.write({'resignation_date': vals.get('resignation_date_compute')})
                        if 'leaving_to_date_compute' in vals:
                            status.write({'leaving_to_date': vals.get('leaving_to_date_compute')})

                if 'job_id_compute' in vals:
                    values = {
                        'employee_multi_id': employee.id,
                        'updated_date': datetime.today(),
                        'user_id': self.env.user.id,
                        'changed_field': 'Cập nhật Chức vụ',
                        'current_value_before': employee_s.job_id_compute.sudo().name,
                        'current_value_after': self.env['hr.job'].sudo().search(
                            [('id', '=', vals.get('job_id_compute'))]).name,
                    }
                    self.env['sea.employee.history'].create(values)

                if 'department_id_compute' in vals:
                    values = {
                        'employee_multi_id': employee.id,
                        'updated_date': datetime.today(),
                        'user_id': self.env.user.id,
                        'changed_field': 'Cập nhật Phòng/ Ban',
                        'current_value_before': employee_s.department_id_compute.sudo().name,
                        'current_value_after': self.env['hr.department'].sudo().search(
                            [('id', '=', vals.get('department_id_compute'))]).name,
                    }
                    self.env['sea.employee.history'].create(values)
        return super(HistoryEmployee, self).write(vals)


class HistoryEmployeeMulti(models.Model):
    _inherit = 'hr.employee.multi.company'

    @api.multi
    def create(self, vals):
        rec = super(HistoryEmployeeMulti, self).create(vals)
        if rec.employee_current_status:
            values = {
                'employee_multi_id': rec.id,
                'updated_date': datetime.today(),
                'user_id': self.env.user.id,
                'changed_field': 'Tạo mới nhân viên (Trạng thái làm việc)',
                'current_value_before': rec.name.sudo().current_status(rec.employee_current_status),
                'current_value_after': rec.name.sudo().current_status(rec.employee_current_status),
            }
            history = self.env['sea.employee.history'].create(values)
            values_detail = {
                'employee_current_status_old': rec.employee_current_status,
                'employee_current_status': rec.employee_current_status,
                'reason_leaving': rec.reason_leaving if rec.reason_leaving else "",
                'resignation_date': rec.resignation_date if rec.resignation_date else None,
                'leaving_to_date': rec.leaving_to_date if rec.leaving_to_date else None,
                'history_id': history.id,
                'current': True
            }
            current_status = self.env['sea.employee.history.current.status'].sudo().search(
                [('employee_multi_id', '=', rec.id)])
            if current_status:
                for cs in current_status:
                    cs.write({'current': False})
            self.env['sea.employee.history.current.status'].create(values_detail)

        if rec.job_id:
            values = {
                'employee_multi_id': rec.id,
                'updated_date': datetime.today(),
                'user_id': self.env.user.id,
                'changed_field': 'Tạo mới nhân viên (Chức vụ)',
                'current_value_before': rec.job_id.sudo().name if rec.job_id else "",
                'current_value_after': rec.job_id.sudo().name if rec.job_id else "",
            }
            self.env['sea.employee.history'].create(values)

        if rec.department_id:
            values = {
                'employee_multi_id': rec.id,
                'updated_date': datetime.today(),
                'user_id': self.env.user.id,
                'changed_field': 'Tạo mới nhân viên (Phòng/ Ban)',
                'current_value_before': rec.department_id.sudo().name if rec.department_id else "",
                'current_value_after': rec.department_id.sudo().name if rec.department_id else "",
            }
            self.env['sea.employee.history'].create(values)
        return rec


class WageDetails(models.Model):
    _inherit = 'hr.contract'

    def salary_count(self, company_id):
        sum_salary_seagroup = 0
        salary_contract = self.env['hr.contract'].sudo().search(
            [('contract_category', '=', 'contract'), ('type_id', '=', 1),
             ('employee_id', '=', self.employee_id.id),
             ('company_id', '=', company_id), ('state', 'in', ['pending', 'open']),
             ('wage', '>', 0)], order='wage desc', limit=1)
        salary_extend = self.env['hr.contract'].sudo().search(
            [('contract_category', '=', 'addition'), ('type_id', '=', 1),
             ('employee_id', '=', self.employee_id.id),
             ('company_id', '=', company_id), ('state', 'in', ['pending', 'open']),
             ('wage', '>', 0)], order='wage desc', limit=1)
        salary_s = self.env['hr.contract'].sudo().search(
            [('type_id', '=', 1), ('employee_id', '=', self.employee_id.id),
             ('company_id', '=', company_id), ('state', 'in', ['pending', 'open']),
             ('contract_category', '=', 'addition'), ('contract_extend_salary', '>', 0)],
            order='contract_extend_salary desc', limit=1)

        sum_salary_company = (salary_s.contract_extend_salary if salary_s else 0) + (
            salary_extend.wage if salary_extend else (salary_contract.wage if salary_contract else 0))
        salary_s = self.env['hr.contract'].sudo().search(
            [('contract_category', '=', 'addition'), ('type_id', '=', 1),
             ('employee_id', '=', self.employee_id.id),
             ('state', 'in', ['pending', 'open']), ('contract_extend_salary', '>', 0)])
        if salary_s:
            for salary in salary_s:
                sum_salary_seagroup += salary.contract_extend_salary

        salary_contract = self.env['hr.contract'].sudo().search(
            [('contract_category', '=', 'contract'), ('type_id', '=', 1),
             ('employee_id', '=', self.employee_id.id),
             ('state', 'in', ['pending', 'open'])])
        if salary_contract:
            for salary in salary_contract:
                salary_extend = self.env['hr.contract'].sudo().search(
                    [('contract_category', '=', 'addition'), ('type_id', '=', 1),
                     ('employee_id', '=', self.employee_id.id),
                     ('company_id', '=', salary.company_id.id), ('state', 'in', ['pending', 'open']),
                     ('wage', '>', 0)], order='wage desc', limit=1)
                sum_salary_seagroup += salary_extend.wage if salary_extend else salary.wage

        return sum_salary_company, sum_salary_seagroup

    @api.multi
    def create_history(self, vals, category_contract=0):
        # sum_salary_seagroup = 0
        # salary_contract = self.env['hr.contract'].sudo().search(
        #     [('contract_category', '=', 'contract'), ('type_id', '=', 1),
        #      ('employee_id', '=', self.employee_id.id),
        #      ('company_id', '=', self.company_id.id), ('state', 'in', ['pending', 'open']),
        #      ('wage', '>', 0)], order='wage desc', limit=1)
        # salary_extend = self.env['hr.contract'].sudo().search(
        #     [('contract_category', '=', 'addition'), ('type_id', '=', 1),
        #      ('employee_id', '=', self.employee_id.id),
        #      ('company_id', '=', self.company_id.id), ('state', 'in', ['pending', 'open']),
        #      ('wage', '>', 0)], order='wage desc', limit=1)
        # salary_s = self.env['hr.contract'].sudo().search(
        #     [('type_id', '=', 1), ('employee_id', '=', self.employee_id.id),
        #      ('company_id', '=', self.company_id.id), ('state', 'in', ['pending', 'open']),
        #      ('contract_category', '=', 'addition'), ('contract_extend_salary', '>', 0)],
        #     order='contract_extend_salary desc', limit=1)
        #
        # sum_salary_company = (salary_s.contract_extend_salary if salary_s else 0) + (
        #     salary_extend.wage if salary_extend else (salary_contract.wage if salary_contract else 0))
        # salary_s = self.env['hr.contract'].sudo().search(
        #     [('contract_category', '=', 'addition'), ('type_id', '=', 1),
        #      ('employee_id', '=', self.employee_id.id),
        #      ('state', 'in', ['pending', 'open']), ('contract_extend_salary', '>', 0)])
        # if salary_s:
        #     for salary in salary_s:
        #         sum_salary_seagroup += salary.contract_extend_salary
        #
        # salary_contract = self.env['hr.contract'].sudo().search(
        #     [('contract_category', '=', 'contract'), ('type_id', '=', 1),
        #      ('employee_id', '=', self.employee_id.id),
        #      ('state', 'in', ['pending', 'open'])])
        # if salary_contract:
        #     for salary in salary_contract:
        #         salary_extend = self.env['hr.contract'].sudo().search(
        #             [('contract_category', '=', 'addition'), ('type_id', '=', 1),
        #              ('employee_id', '=', self.employee_id.id),
        #              ('company_id', '=', salary.company_id.id), ('state', 'in', ['pending', 'open']),
        #              ('wage', '>', 0)], order='wage desc', limit=1)
        #         sum_salary_seagroup += salary_extend.wage if salary_extend else salary.wage
        sum_salary_company, sum_salary_seagroup = self.salary_count(self.company_id.id)
        DH_PL = ""
        if 'contract_category' in vals:
            if vals['contract_category'] == 'contract':
                DH_PL = "Hợp đồng "
            elif vals['contract_category'] == 'addition':
                DH_PL = "Phụ lục "
        else:
            if self.contract_category == 'contract':
                DH_PL = "Hợp đồng "
            elif self.contract_category == 'addition':
                DH_PL = "Phụ lục "
        reason_change = ""
        if category_contract in [1, 2]:
            reason_change = reason_change + DH_PL
            if category_contract == 1:
                reason_change = "được tạo mới"
            elif category_contract == 2:
                if self.state == 'close':
                    reason_change = reason_change + 'đã hết hạn'
                elif self.state == 'cancel':
                    reason_change = reason_change + 'đã hủy'
        else:
            reason_change = "Cập nhật "
            for i in vals:
                if reason_change != "Cập nhật ":
                    reason_change = reason_change + ", "
                if 'wage' in vals:
                    reason_change = reason_change + 'tiền công/ tiền lương '
                elif 'contract_extend_salary' in vals:
                    reason_change = reason_change + 'phụ cấp lương '
                elif 'contract_category' in vals:
                    reason_change = reason_change + 'loại hợp đồng '
                elif 'type_id' in vals:
                    reason_change = reason_change + 'loại nhân viên '
                elif 'state' in vals:
                    reason_change = reason_change + 'trạng thái '
            reason_change = reason_change + "của " + DH_PL

        employee_contract = self.env['hr.employee.multi.company'].sudo().search(
            [('name', '=', self.employee_id.id), ('company_id', '=', self.company_id.id)])
        values = {
            'employee_multi_id': employee_contract.id,
            # 'name': employee_contract.name.sudo().name,
            'contract_id': self.id,
            'user_id': self.env.user.id,
            'updated_date': datetime.today(),
            'reason_change': reason_change,
            'sum_salary_company': sum_salary_company,
            'sum_salary_seagroup': sum_salary_seagroup,

        }
        new = self.env['sea.employee.history.salary'].create(values)
        '''update lại filed salary SeaGroup cho các record đang hiện hành ở các CTY khác của NV đó'''
        # for company in new.employee_id.sudo().sea_company_ids:
        #     if company.id != self.company_id.id:
        #         multi = self.env['hr.employee.multi.company'].sudo().search(
        #             [('name', '=', new.employee_id.id), ('company_id', '=', company.id)], limit=1)
        #         if multi:
        #             update = self.env['sea.employee.history.salary'].sudo().search(
        #                 [('employee_multi_id', '=', multi.id)], order='id desc',
        #                 limit=1)
        #             if update:
        #                 update.write({'sum_salary_seagroup': sum_salary_seagroup})
        '''thêm các record history salary mới cho NV ở các CTY khác'''
        for company in new.employee_id.sudo().sea_company_ids:
            if company.id != self.company_id.id:
                sum_salary_company_new, sum_salary_seagroup_new = self.salary_count(company.id)
                employee_contract_new = self.env['hr.employee.multi.company'].sudo().search(
                    [('name', '=', self.employee_id.id), ('company_id', '=', company.id)])
                values_new = {
                    'employee_multi_id': employee_contract_new.id,
                    # 'contract_id': self.id,
                    'user_id': self.env.user.id,
                    'updated_date': datetime.today(),
                    'reason_change': reason_change + " tại " + self.company_id.name,
                    'sum_salary_company': sum_salary_company_new,
                    'sum_salary_seagroup': sum_salary_seagroup_new,

                }
                self.env['sea.employee.history.salary'].create(values_new)

    @api.multi
    def write(self, vals):
        rec = super(WageDetails, self).write(vals)
        if self.state not in ['close', 'cancel', 'draft']:
            if 'wage' in vals or 'contract_extend_salary' in vals:
                self.create_history(vals)
            elif self.wage > 0 or self.contract_extend_salary > 0:
                if 'state' in vals:
                    if vals['state'] == 'open':
                        self.create_history(vals)
                elif 'contract_category' in vals or 'type_id' in vals:
                    self.create_history(vals)

        elif 'state' in vals:
            if vals['state'] in ['close', 'cancel']:
                if 'wage' in vals or 'contract_extend_salary' in vals:
                    self.create_history(vals, 2)
                elif self.wage > 0 or self.contract_extend_salary > 0:
                    self.create_history(vals, 2)
        return rec

    @api.model
    def create(self, vals):
        rec = super(WageDetails, self).create(vals)
        if vals['type_id'] == 1 and 'contract_category' in vals and vals['state'] in ['open', 'pending']:
            if rec.wage > 0 or rec.contract_extend_salary > 0:
                rec.create_history(vals, 1)
        return rec


class EmployeeHistory(models.Model):
    _name = 'sea.employee.history'
    _order = 'id desc'
    employee_multi_id = fields.Many2one('hr.employee.multi.company', string='Employee Multi ID')
    employee_id = fields.Many2one('hr.employee', string='Employee ID', related='employee_multi_id.name', store=False)
    # name = fields.Char(string='Employee Name')
    updated_date = fields.Date(string='Updated On')
    user_id = fields.Many2one('res.users', string='User')
    changed_field = fields.Char(string='Changed Field')
    current_value_before = fields.Char(string='Current Value Before')
    current_value_after = fields.Char(string='Current Value After')


class EmployeeHistoryDetail(models.Model):
    _name = 'sea.employee.history.current.status'
    _order = 'id desc'

    history_id = fields.Many2one('sea.employee.history', string='ID History')
    employee_multi_id = fields.Many2one('hr.employee.multi.company', string='Employee ID',
                                        related='history_id.employee_multi_id', store=True)
    employee_id = fields.Many2one('hr.employee', string='Employee ID', related='history_id.employee_id',
                                  store=False)
    employee_current_status_old = fields.Selection([
        ('working', 'Working'),
        ('leaving', 'Unpaid leave'),
        ('maternity_leave', 'Parental leave'),
        ('sick_leave', 'Sick leave'),
        ('resigned', 'Resigned')
    ], string='Employee Status Old', help='Employee Status Old')

    employee_current_status = fields.Selection([
        ('working', 'Working'),
        ('leaving', 'Unpaid leave'),
        ('maternity_leave', 'Parental leave'),
        ('sick_leave', 'Sick leave'),
        ('resigned', 'Resigned')
    ], string='Employee Status', help='Employee Status')
    reason_leaving = fields.Text(string='Reason Leaving')
    resignation_date = fields.Date(string='Resignation Date')
    leaving_to_date = fields.Date(string='Đến ngày')
    active = fields.Boolean('Active', default=True, required=1)
    current = fields.Boolean('Current Status', default=False)


class SalaryHistory(models.Model):
    _name = 'sea.employee.history.salary'
    _order = 'id desc'

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string='Employee Id')
    employee_id = fields.Many2one('hr.employee', string='Employee Id', related='employee_multi_id.name', store=False)
    company_id = fields.Many2one('res.company', related='employee_multi_id.company_id', store=False)
    user_id = fields.Many2one('res.users', string='User')

    # name = fields.Char(string='Employee Name')
    contract_id = fields.Many2one('hr.contract', string="Contract/Addition")
    updated_date = fields.Date(string='Updated On')
    reason_change = fields.Char(string='Reason For Change')
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True, store=False)
    sum_salary_company = fields.Monetary('Salary Company', digits=(16, 0), help="Salary Company.")
    sum_salary_seagroup = fields.Monetary('Salary SeaGroup', digits=(16, 0), help="Salary SeaGroup.")
