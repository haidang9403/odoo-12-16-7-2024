from odoo import api, models, fields


class user_mail(models.Model):
    _name = 'user.mail'
    _description = "User responsible for contracts"

    name = fields.Many2one(
        'res.users', 'Assigned to', index=True, required=True)
    email = fields.Char('Email', related='name.email')


