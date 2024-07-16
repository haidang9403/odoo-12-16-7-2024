from odoo import models, fields,api

class HrDirectory(models.Model):
    _name = 'hr.directory'
    _description = 'HR Directory'


    name = fields.Char(string='Name', required=True)
    position = fields.Char(string='Position')
    internal_num = fields.Char(string='Internal Number')
    email = fields.Text(string='Email')
    phone = fields.Text(string='Phone')
    fax = fields.Text(string='Fax')
    note = fields.Text(string='Note')
    parent_directory = fields.Many2one('hr.directory', string='Parent Directory', domain=lambda self: [('company_id.id','=', self.env.user.company_id.id)])
    company_id = fields.Many2one(
        'res.company', default=lambda self: self.env.user.company_id, readonly=True
    )











