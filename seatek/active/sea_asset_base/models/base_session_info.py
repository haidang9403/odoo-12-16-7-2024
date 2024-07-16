from odoo import models
class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        employee = self.env['hr.employee.multi.company'].sudo().search(
            [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)],limit=1)
        if employee:
            result['user_context'].update({'employee_id': employee.ids})
        else:
            result['user_context'].update({'employee_id': []})
        employees = self.env['hr.employee.multi.company'].sudo().search([('user_id', '=', self.env.user.id)])
        if employees:
            result['user_context'].update({'employee_ids': employee.ids})
        else:
            result['user_context'].update({'employee_ids': []})
        return result