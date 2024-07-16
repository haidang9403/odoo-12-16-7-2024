from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleChannel(models.Model):
    _name = 'sale.channel'
    _rec_name = "complete_name"

    name = fields.Char('Name', required=True)
    complete_name = fields.Char(
        'Complete Name', compute='_compute_complete_name',
        store=True)
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")
    parent_id = fields.Many2one('sale.channel', 'Parent Category')
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.user.company_id)

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.model
    def create(self, values):
        res = super(SaleChannel, self).create(values)
        check_exist = self.env['sale.channel'].search([('complete_name', '=', values['name'])])
        parent_id = self.env['sale.channel'].browse(values['parent_id'])
        if parent_id:
            value_complete_name = parent_id.name + ' / ' + values['name']
            check_complete_name_exist = self.env['sale.channel'].search([('complete_name', '=', value_complete_name)])
            if len(check_complete_name_exist) > 1:
                raise UserError(_("Channel already exists. "))
            else:
                return res
        else:
            if len(check_exist) > 1:
                raise UserError(_("Channel already exists. "))
            else:
                return res
