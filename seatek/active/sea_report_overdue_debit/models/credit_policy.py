from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CreditPolicy(models.Model):
    _name = "credit.policy"
    _description = "Credit Policy"

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(string="Name")
    currency_id = fields.Many2one('res.currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    longest_overdue_debt = fields.Integer(string='Longest overdue debt', currency_field='currency_id')
    overdue_debt_limit = fields.Monetary(string='Overdue debt limit', currency_field='currency_id')
    total_debt = fields.Monetary(string='Total debt', currency_field='currency_id')

    check_overdue_debt_limit = fields.Boolean(string='Check Overdue debt limit', default=True)
    check_longest_overdue_debt = fields.Boolean(string='Check Longest overdue debt', default=True)
    check_total_debt = fields.Boolean(string='Check Total debt', default=True)

    note = fields.Char(string='Note')
    company_id = fields.Many2one('res.company', 'Company',
                                 default=lambda self: self.env.user.company_id, readonly=True)

    @api.constrains('longest_overdue_debt', 'overdue_debt_limit', 'total_debt')
    def constrains_overdue_debt_limit(self):
        for rec in self:
            if rec.longest_overdue_debt:
                if rec.longest_overdue_debt < 0:
                    raise UserError(_('Longest overdue debt must be greater than 0'))
            if rec.overdue_debt_limit:
                if rec.overdue_debt_limit < 0:
                    raise UserError(_('Overdue debt limit must be greater than 0'))
            if rec.total_debt:
                if rec.total_debt < 0:
                    raise UserError(_('Total debt must be greater than 0'))
