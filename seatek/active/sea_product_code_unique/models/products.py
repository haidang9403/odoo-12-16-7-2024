from odoo import models, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        unique_default_code = super(ProductProduct, self).create(vals)
        if 'default_code' in vals:
            check_unique = self.env['product.product'].search([
                ('default_code', '=', vals['default_code']),
                ('company_id', '=', vals['company_id'])])
            if len(check_unique) > 1:
                raise UserError(_('Internal references already exist for this company.!'))
        return unique_default_code

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'default_code' in vals:
            check_unique = self.env['product.product'].search([
                ('default_code', '=', vals['default_code']),
                ('company_id', '=', self.company_id.id)])
            if len(check_unique) > 1:
                raise UserError(_('Internal references already exist for this company.!'))
        return res
