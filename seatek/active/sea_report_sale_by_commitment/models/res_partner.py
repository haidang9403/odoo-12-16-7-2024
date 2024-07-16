from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    sea_partner_sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel')
    sea_sales_department = fields.Selection([
        ('si', 'Sỉ'),
        ('le', 'Lẻ'),
    ], string='Sales Department')
