import xml.etree.ElementTree as xee
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    sea_sale_channel = fields.Many2one('sale.channel', 'Channel Name')
    sea_sale_channel_item = fields.Many2one('sale.channel.item', 'Channel Item',
                                            domain="[('channel_catalog', '=', sea_sale_channel)]")

    @api.onchange('sea_sale_channel')
    def _onchange_channel_clear_item(self):
        if self.sea_sale_channel:
            self.sea_sale_channel_item = {}
