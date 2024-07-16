# from  odoo import api, models
# class EmployeeCompanyResign(models.Model):
#     _inherit = "hr.employee.multi.company"
#
#     @api.multi
#     def write(self, vals):
#         res = super(EmployeeCompanyResign, self).write(vals)
#         if vals.get('employee_current_status'):
#             if vals.get('employee_current_status') == 'resigned':
#                 vals.update({'active': 0})
#                 flag = 0
#                 id = self['id']
#                 s_identification_id = self.env['hr.employee.multi.company'].sudo().search([('id', '=', id)])['s_identification_id']
#
#                 for emps in self.env['hr.employee.multi.company'].sudo().search([('s_identification_id', '=', s_identification_id)]):
#                     if emps['active'] == 1:
#                         flag = 1
#
#                 if flag == 0:
#                     rec = self.env['res.users'].sudo().search([('login', '=', s_identification_id)])
#                     rec.write({'active': 0})
#                     emp = self.env['hr.employee'].sudo().search([('s_identification_id', '=', s_identification_id)])
#                     emp.write({'working_status_in_coporation': 'resigned', 'active': 0})
#         return res
#
#
#
