from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InvoiceUnitOfMeasure(models.Model):
    _name = 'invoice.unit.of.measure'
    _description = 'Create a new unit of measure list for issue invoice'

    name = fields.Char(string='Unit of Measure', required=True)
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    @api.model
    def create(self, values):
        res = super(InvoiceUnitOfMeasure, self).create(values)
        check_exist = self.env['invoice.unit.of.measure'].search([('name', '=', values['name'])])
        if len(check_exist) > 1:
            raise UserError(
                _("%s IS EXIST") % (values['name']))
        return res

    @api.multi
    def unlink(self):
        if len(self) > 1:
            raise UserError(_("You need to check each line before delete."))
        check_use = self.env['product.product'].search([('sea_unit_of_measure', '=', self.name)])
        if len(check_use) > 0:
            raise UserError(_("You cannot delete because it is used by the system."))
        else:
            return models.Model.unlink(self)
