from odoo import models, fields, api


class ConsignmentProcessEpt(models.Model):
    _inherit = 'consignment.process.ept'

    @api.multi
    def get_warehouse_consignment_user(self):
        res = []
        for item in self.env.user.sea_user_warehouse_ids:
            if self.env.user.company_id == item.company_id:
                res.append(item.id)
        if res:
            return res
        else:
            result = []
            for i in self.env['stock.warehouse'].search([]):
                result.append(i.id)
            return result

    @api.model
    def _get_warehouse_consignment_default_user(self):
        return self.env['stock.warehouse'].search([
            ('id', 'in', self.get_warehouse_consignment_user())], limit=1).id

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse',
                                   default=_get_warehouse_consignment_default_user, required=True,
                                   domain=lambda self: [('id', 'in', self.get_warehouse_consignment_user())])
