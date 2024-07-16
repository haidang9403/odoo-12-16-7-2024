from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sea_sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel')
    sea_sale_department = fields.Selection([
        ('si', 'Sỉ'),
        ('le', 'Lẻ'),
    ], string='Sales Department')

    @api.onchange('partner_id')
    def onchange_sale_channel(self):
        if self.partner_id:
            self.sea_sale_channel_id = self.partner_id.sea_partner_sale_channel_id
            self.sea_sale_department = self.partner_id.sea_sales_department
