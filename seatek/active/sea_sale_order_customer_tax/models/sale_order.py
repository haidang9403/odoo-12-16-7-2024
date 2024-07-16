from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sea_check_customer_for_invoice = fields.Boolean(string='Customer Don\'t Take Invoice', track_visibility='onchange')
    sea_hide_take_invoice_multi_company = fields.Char(
        default=lambda self: self.env.user.company_id.sea_sale_order_take_invoice_enable)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['sea_check_customer_for_invoice'] = self.sea_check_customer_for_invoice
        print('invoice_vals', invoice_vals)
        return invoice_vals

    @api.onchange('partner_id')
    def _onchange_tax_for_partner(self):
        if self.partner_id:
            for line in self.order_line:
                line.tax_id = line.product_id.taxes_id
                for obj in self.env['customer.product.tax'].search([
                    ('customer_category_id', '=', line.order_id.partner_id.sea_customer_type_id.id),
                    ('category_id', '=', line.product_id.categ_id.id)
                ]):
                    if obj:
                        line.tax_id = obj.tax_id

    # @api.multi
    # def get_pos_location(self):
    #     pos_location = []
    #     for item in self.env['pos.config'].search([]):
    #         if item:
    #             for stock in self.env['stock.location'].search([('id', '=', item.stock_location_id.id)]):
    #                 pos_location.append(stock.id)
    #     return pos_location


    # def get_pos_location(self):
    #     pos_location = []
    #     for item in self.env['pos.branch'].search([]):
    #         if item:
    #             for stock in self.env['stock.location'].search([('id', '=', item.config_ids.stock_location_id.id)]):
    #                 pos_location.append(stock.id)
    #     return pos_location
    #
    # sea_ecommerce_pos_location_ids = fields.Many2one('stock.location',
    #                                                  'E-commerce Pos Location',
    #                                                  domain=lambda self: [('id', 'in', self.get_pos_location())])
