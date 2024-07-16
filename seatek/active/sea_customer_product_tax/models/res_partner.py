from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sea_customer_type_id = fields.Many2one('customer.category.tax', string='Customer Category Tax')
