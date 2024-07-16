from odoo import models, fields


class ResConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    sea_sale_order_take_invoice_enable = fields.Boolean(related='company_id.sea_sale_order_take_invoice_enable',
                                                        readonly=False)
