from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalesDepartment(models.Model):
    _name = 'sales.department'
    _description = 'Sales Department'

    name = fields.Char('Department Name')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, values):
        check_exist = self.env['sales.department'].search([('name', '=', values['name'])])
        if check_exist:
            raise UserError(_("Department already exists. "))
        else:
            return super(SalesDepartment, self).create(values)
