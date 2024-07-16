from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def get_operation_type_purchase(self):
        res = []
        for item in self.env.user.sea_user_operation_type_ids:
            if self.env.user.company_id == item.warehouse_id.company_id or \
                    self.env.user.company_id == item.company_id or \
                    not item.warehouse_id and not item.company_id:
                if item.code == 'incoming':
                    res.append(item.id)
        if res:
            return res
        else:
            result = []
            for i in self.env['stock.picking.type'].search([('code', '=', 'incoming')]):
                result.append(i.id)
            return result

    @api.model
    def _get_purchase_default_picking_type(self):
        return self.env['stock.picking.type'].search([
            ('code', '=', 'incoming'),
            ('id', 'in', self.get_operation_type_purchase())], limit=1).id

    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type',
                                      default=_get_purchase_default_picking_type,
                                      domain=lambda self: [('id', 'in', self.get_operation_type_purchase())])
