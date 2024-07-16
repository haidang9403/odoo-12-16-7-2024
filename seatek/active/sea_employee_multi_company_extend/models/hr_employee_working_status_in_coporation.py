import datetime

from odoo import models, api, fields
from datetime import date
class EmployeeWorkingStatus(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee Working Status in Coporation'

    # working_status_in_coporation = fields.Selection([
    #     ('working', 'Working'),
    #     ('resigned', 'Resigned')
    # ], default='working', string='Employee Working Status In Coporation', help='Employee Working Status In Coporation')

    # auto_deactive_user_resigned= fields.Boolean(string='Automatically Deactivate User Resigned', default=0)
    #
    @api.multi
    def write(self, vals):
        print(vals)
        if vals.get('super_manager') is None:
            print('none')

        else:
            if vals.get('super_manager') & vals.get('super_manager') is False:
                # print('Super manager Is Null')
                for rec in self.env['hr.employee.multi.company'].sudo().search(
                        ['&', ('name', '=', self.id), ('company_id', '=', self.company_id_compute.id)]):
                    rec.write({'super_manager_company': vals['super_manager']})

            if vals.get('super_manager'):
                # print('Super manager not null')
                for rec in self.env['hr.employee.multi.company'].sudo().search(
                        ['&', ('name', '=', self.id), ('company_id', '=', self.company_id_compute.id)]):
                    rec.write({'super_manager_company': vals['super_manager']})

        if vals.get('is_ceo_compute') is None:
            print('none')
        else:
                for rec in self.env['hr.employee.multi.company'].sudo().search(
                        ['&', ('name', '=', self.id), ('company_id', '=', self.company_id_compute.id)]):
                    rec.write({'is_ceo': vals['is_ceo_compute']})

        # # auto_deactive = self.auto_deactive_user_resigned
        # # if vals.get('auto_deactive_user_resigned') == None:
        # #     print(' None auto_deactive_user_resigned')
        # #     self.env['hr.employee'].sudo().search([('id', '=', self['id'])])['auto_deactive_user_resigned']
        # # else:
        # #     auto_deactive = vals.get('auto_deactive_user_resigned')
        # #     print('auto_deactive_user_resigned2: ', vals.get('auto_deactive_user_resigned'))
        # #
        # # # auto_deactive= self.auto_deactive_user_resigned
        # # print('auto_deactive_user_resigned: ', auto_deactive)
        #
        #
        # if vals.get('working_status_in_coporation'):
        #     if vals.get('working_status_in_coporation') == 'working':
        #         vals.update({'active': 1})
        #         res = super(EmployeeWorkingStatus, self).write(vals)
        #         s_identification_id = \
        #             self.env['hr.employee'].sudo().search([('id', '=', self['id'])])[
        #                 's_identification_id']
        #
        #         print('s_ID:', s_identification_id)
        #         vals.update({'active': 1, 'employee_current_status': 'working'})
        #         # for e in self.env['hr.employee.multi.company'].sudo().search(
        #         #         ['&', ('s_identification_id', '=', s_identification_id), ('active', '=', 0)]):
        #         #     e.write({'employee_current_status': 'working', 'active': 1, 'resignation_date': None})
        #
        #         for e in self.env['hr.employee.multi.company'].sudo().search(
        #                 [('s_identification_id', '=', s_identification_id)]):
        #             e.write({'employee_current_status': 'working', 'active': 1, 'resignation_date': None})
        #         self.env['res.users'].sudo().search(
        #             ['&', ('login', '=', s_identification_id), ('active', '=', 0)]).write({'active': 1})
        #
        #     if vals.get('working_status_in_coporation') == 'resigned':
        #         # if auto_deactive == 1:
        #         #     print('resigned true')
        #         #     vals.update({'active': 0})
        #         #     s_identification_id = self.env['hr.employee'].sudo().search([('id', '=', self['id'])])[
        #         #         's_identification_id']
        #         #     for e in self.env['hr.employee.multi.company'].sudo().search(
        #         #             [('s_identification_id', '=', s_identification_id)]):
        #         #         e.write({'employee_current_status': 'resigned', 'active': 0, 'resignation_date': date.today()})
        #         #     self.env['res.users'].sudo().search([('login', '=', s_identification_id)]).write({'active': 0})
        #         # else:
        #         #     print("resigned false")
        #             s_identification_id = self.env['hr.employee'].sudo().search([('id', '=', self['id'])])[
        #                 's_identification_id']
        #             print('s_id: ', s_identification_id)
        #             vals.update({'active': 0, 'employee_current_status': 'resigned'})
        #
        #             for e in self.env['hr.employee.multi.company'].sudo().search(
        #                     ['&',('s_identification_id', '=', s_identification_id), ('employee_current_status', '=', 'working')]):
        #                 e.write({'employee_current_status': 'resigned', 'resignation_date': date.today(), 'active': 0})
        #             # self.env['res.users'].sudo().search(
        #             #     [('login', '=', s_identification_id)]).write({'active': 0})
        return super(EmployeeWorkingStatus, self).write(vals)
