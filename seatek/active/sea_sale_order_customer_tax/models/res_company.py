from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sea_sale_order_take_invoice_enable = fields.Boolean(string='Take Invoice Enable', default=False)
