from odoo import api, models, fields
# import random

class MultiCompanyInherit(models.Model):
    _inherit = 'hr.employee.multi.company'

    super_manager_company = fields.Many2one('hr.employee', string="Super Manager")
    is_ceo= fields.Boolean(string="CEO/Giám Đốc đơn vị", default=False)
