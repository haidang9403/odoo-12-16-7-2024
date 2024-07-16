from odoo import models, fields


class ResConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'

    customer_tax_enabled = fields.Boolean(related='company_id.customer_tax_enabled',
                                          readonly=False)
