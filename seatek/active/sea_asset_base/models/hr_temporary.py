from odoo import models, fields,api

class HrEmployeeTemporary(models.Model):

    _name = 'hr.employee.temporary'
    _description = 'HR Employee Multi Company Temporary'

    name=fields.Char(string='Name')
    employee_id=fields.Many2one('hr.employee.multi.company',string='Employee',unique=True)
    user_id=fields.Many2one('res.users',string='Employee',unique=True,related='employee_id.user_id')
    company_id=fields.Many2one('res.company',string='Company')
    department_id=fields.Many2one('hr.department',string='Department')
    job_id=fields.Many2one('hr.job',string='Job position',related='employee_id.job_id')
    active=fields.Boolean(string='Active',default=True)
    employee_current_status = fields.Selection([
        ('working', 'Working'),
        ('leaving', 'Unpaid leave'),
        ('maternity_leave', 'Parental leave'),
        ('sick_leave', 'Sick leave'),
        ('resigned', 'Resigned',)

    ], string='Employee Status', help='Employee Status',related='employee_id.employee_current_status')
    @api.multi
    def read(self, fields=None, load='_classic_read'):
        hr_temporary = self.env.cr.execute('SELECT b.id,b.name,b.company_id,b.department_id	FROM public.hr_employee_temporary a, hr_employee_multi_company b where a.employee_id = b.id and a.company_id=b.company_id')

        hr_temporary = self.env.cr.dictfetchall()
        temp_employees=[]
        for temporary in hr_temporary:
            temp_employee_id=temporary.get('id')
            if temp_employee_id:
                temp_employees.append(temporary.get('id'))
        employees = self.env['hr.employee.multi.company'].sudo().search([('active', '=', True), ('employee_current_status', '!=', 'resigned'),('id','not in',
                                                                                                                                               temp_employees)])
        for employee in employees:
            try:
                self.env['hr.employee.temporary'].create({'employee_id': employee.id, 'name': employee.name.sudo().name,'company_id':employee.sudo().company_id.id,'department_id':employee.sudo().department_id.id})
            except:
                continue
            # sql_string='UPDATE public.hr_employee_temporary a SET employee_current_status=b.employee_current_status from public.hr_employee_multi_company b WHERE a.employee_id = b.id  and (a.employee_current_status!=b.employee_current_status or a.employee_current_status is null)'
            # updates = self.env.cr.execute(sql_string)


        result = super(HrEmployeeTemporary, self).read(fields, load=load)

        return result
    @api.multi
    def write(self,values):
        return super(HrEmployeeTemporary,self).write(values)

    _sql_constraints = [
        ('employee_company_uniq', 'unique (employee_id,company_id)', 'The employee must be unique per company!')
    ]
class HrDepartmentTemporary(models.Model):

    _name = 'hr.department.temporary'
    _description = 'HR Department Multi Company Temporary'

    name=fields.Char(string='Name')
    department_id=fields.Many2one('hr.department')
    company_id=fields.Many2one('res.company',string='Company')
    active=fields.Boolean(string='Active',default=True)

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        hr_temporary = self.env.cr.execute('SELECT b.id,b.name,b.company_id	FROM public.hr_department_temporary a, hr_department b where a.department_id = b.id')

        hr_temporary = self.env.cr.dictfetchall()
        temp_employees=[]
        for temporary in hr_temporary:

            temp_department_id=temporary.get('id')
            if temp_department_id:
                temp_employees.append(temporary.get('id'))
        departments = self.env['hr.department'].sudo().search([('active', '=', True), ('id','not in',temp_employees)])
        for department in departments:
            try:
                self.env['hr.department.temporary'].create({'department_id': department.id, 'name': department.complete_name,'company_id':department.sudo(

                ).company_id.id})
            except:
                continue


        result = super(HrDepartmentTemporary, self).read(fields, load=load)

        return result
    @api.multi
    def write(self,values):
        return super(HrDepartmentTemporary,self).write(values)

    _sql_constraints = [
        ('department_company_id', 'unique (department_id,company_id)', 'The department must be unique per company!')
    ]
