from odoo import models, fields, api


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.multi
    def get_domain_company_picking_type(self):
        return self.env.user.company_id.id

    company_id = fields.Many2one('res.company', string='Company',
                                 domain=lambda self: [('id', '=', self.get_domain_company_picking_type())])

    @api.multi
    def write(self, values):
        if 'company_id' in values:
            if values['company_id']:
                if self.warehouse_id and self.warehouse_id.company_id:
                    values['company_id'] = self.warehouse_id.company_id.id
                else:
                    values['company_id'] = self.env.user.company_id.id
            else:
                values['company_id'] = ''

        return super(StockPickingType, self).write(values)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def get_operation_type(self):
        res = []
        for item in self.env.user.sea_user_operation_type_ids:
            if self.env.user.company_id == item.warehouse_id.company_id:
                res.append(item.id)
        if res:
            return res
        else:
            result = []
            # for i in self.env['stock.picking.type'].search(['|',('company_id','=',self.env.user.company_id.id),('company_id','=',False)]):
            for i in self.env['stock.picking.type'].search([]):
                result.append(i.id)
            return result

    picking_type_id = fields.Many2one(
        'stock.picking.type', 'Operation Type',
        domain=lambda self: [('id', 'in', self.get_operation_type())])
