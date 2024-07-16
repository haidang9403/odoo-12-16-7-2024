from odoo import api, models, fields
import random

class EmployeeUserInherit(models.Model):
    _inherit = 'hr.employee'

    # send_to_mails= fields.Many2many('res.users', string='Send to mails')
    def _super_manager_compute_(self):
        for rec in self:
            rec.super_manager = (rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id)])).super_manager_company


    def _is_ceo_compute_(self):
        for rec in self:
            rec.is_ceo_compute = (rec.env['hr.employee.multi.company'].sudo().search(
                ['|', ('active', '=', False), ('active', '=', True), ('name', '=', rec.id),
                 ('company_id', '=', rec.company_id_compute.id)])).is_ceo

    super_manager = fields.Many2one('hr.employee', string="Super Manager",
                                    domain="[('manager','=',True)],",
                                    compute='_super_manager_compute_')

    is_ceo_compute = fields.Boolean(string="CEO/Giám Đốc đơn vị", default=False, compute="_is_ceo_compute_")

    # @api.model
    # def create(self, vals):
    #     # print(vals)
    #     password = 'helloseatek'
    #     user = self.env['res.users'].create(
    #         {'name': vals['name'], 'login': vals['s_identification_id'], 'password': password})
    #     vals.update({'user_id': user.id})
    #     values ={}
    #     values.update(vals)
    #     values.update({'user_id': user.id, 'password': str(password)})
    #     # self.send_mail(values)
    #     res = super(EmployeeUserInherit, self).create(vals)
    #
    #     #multi company
    #
    #     if vals['sea_company_ids']:
    #         for company in vals['sea_company_ids'][0][2]:
    #             if company !=  vals['company_id']:
    #                 # print("compamnty: ", company)
    #                 self.env['hr.employee.multi.company'].create({
    #                         'name':  self.env['hr.employee'].sudo().search([], order="id desc", limit=1).id,
    #                         'company_id': company,
    #                         'seagroup_join_date': vals['seagroup_join_date'],
    #                         's_identification_id': vals['s_identification_id'],
    #                         'manager': vals['manager'],
    #                         'sea_employee_level': vals['sea_employee_level'],
    #                         'employee_current_status': vals['employee_current_status'],
    #                         'active': vals['active'],
    #                         'joining_date': vals['joining_date_compute'],
    #                         'primary_company': False,
    #                         'user_id': user.id})
    #             # else:
    #                 # print('primary')
    #
    #     return res

    # def send_mail(self, vals):
    #     body = '<center><table style="width: 500px; background-color: bisque; font-size: 16pt;" border="0">'  \
    #                     '<tr> <td colspan="2">User account: <b>' + vals['name'] + '</b> has been created </td>'  \
    #                     '</tr> <tr> <td colspan="2">Login Information: </td></tr>'  \
    #                     '<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td>' \
    #                             '<u>Username:</u> <b>' + vals['s_identification_id'] +'</b> <br />' \
    #                             '<u>Password:</u> <b>' + vals['password'] + '</b>'  \
    #                         '</td></tr><tr><td colspan="2"> ' \
    #                             '<a href="https://docs.google.com/document/d/1YvMdrRLcgURfUJaXRyi9GcIkB2N3BUQHF6sCw6ou9V4/edit?usp=share_link">Click here </a>' \
    #                             ' to see instructions for changing password</td></tr></table></center>'
    #     mail_to = 'user@seacorp.vn'
    #     mail_from = '"seaerp" <info@seacorp.vn>'
    #     template_obj = self.env['mail.mail']
    #     template_data = {
    #         'subject': 'Welcome to Seaerp',
    #         'body_html': body,
    #         'email_from': mail_from,
    #         'email_to': mail_to
    #     }
    #     template_id = template_obj.create(template_data)
    #     template_obj.send(template_id)
    #     print('Mail ID 1: ', template_id)
    #
    #     if vals['sea_personal_email']:
    #         template_data.update({'email_to': vals['sea_personal_email']})
    #         template_id = template_obj.create(template_data)
    #         template_obj.send(template_id)
    #         print('Mail ID 2: ', template_id)
    #     # if vals['send_to_mails']:
    #     #     for id_user in vals['send_to_mails'][0][2]:
    #     #         print('user id: ', id_user)
    #     #         login_user = self.env['res.users'].sudo().search([('id', '=', id_user)])['login']
    #     #         employee_mail = self.env['hr.employee'].sudo().search([('s_identification_id', '=', login_user)])['sea_personal_email']
    #     #         if employee_mail:
    #     #             template_data.update({'email_to': employee_mail})
    #     #             template_id = template_obj.create(template_data)
    #     #             template_obj.send(template_id)
    #
    #     return


