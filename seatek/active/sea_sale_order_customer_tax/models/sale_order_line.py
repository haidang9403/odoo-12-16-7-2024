from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)], store=True)

    @api.onchange('tax_id')
    def _compute_tax(self):
        if self.product_id:
            for obj in self.env['customer.product.tax'].search(
                    [('customer_category_id', '=', self.order_id.partner_id.sea_customer_type_id.id),
                     ('category_id', '=', self.product_id.categ_id.id)]):
                if obj:
                    self.tax_id = obj.tax_id
