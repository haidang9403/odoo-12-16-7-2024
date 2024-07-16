from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomerCategoryTax(models.Model):
    _name = 'customer.category.tax'

    name = fields.Char('Name')
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.user.company_id)