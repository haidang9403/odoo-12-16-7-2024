from odoo import fields, models

class CompanyExtends(models.Model):
    _inherit = 'res.company'

    email_group = fields.Char(string='Email Group')
    fax = fields.Char(string='Fax')