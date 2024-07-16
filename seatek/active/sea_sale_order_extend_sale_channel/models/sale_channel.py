from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleChannel(models.Model):
    _name = 'sale.channel'

    name = fields.Char('Name')
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    @api.model
    def create(self, values):
        res = super(SaleChannel, self).create(values)
        check_exist = self.env['sale.channel'].search([('name', '=', values['name'])])
        if len(check_exist) > 1:
            raise UserError(_("Name already exists. "))
        else:
            return res

    @api.multi
    def unlink(self):
        if len(self) > 1:
            raise UserError(_("You need to check each line before delete."))
        check_use = self.env['sale.order'].search([('sea_sale_channel', '=', self.name)])
        print(check_use)
        if len(check_use) > 0:
            raise UserError(_("You cannot delete this Channel because it is used by the system."))
        else:
            return models.Model.unlink(self)


class SaleChannelItem(models.Model):
    _name = 'sale.channel.item'

    name = fields.Char('Name')
    channel_catalog = fields.Many2one('sale.channel', 'Parent Channel')
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name')
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    def _compute_complete_name(self):
        for channel in self:
            if channel.channel_catalog:
                channel.complete_name = channel.channel_catalog.name + ' / ' + channel.name


    @api.multi
    def unlink(self):
        if len(self) > 1:
            raise UserError(_("You need to check each line before delete."))
        check_use = self.env['sale.order'].search([('sea_sale_channel_item', '=', self.name)])
        print(check_use)
        if len(check_use) > 0:
            raise UserError(_("You cannot delete this Channel Item because it is used by the system."))
        else:
            return models.Model.unlink(self)