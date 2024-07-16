from odoo import models, fields


class ResConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    product_uom_select = fields.Boolean(
        related='company_id.product_uom_select',
        string='Unit select in sale order line',
        readonly=False)
