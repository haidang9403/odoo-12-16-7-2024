from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    print_product_label = fields.Boolean('Print Product Label')
    logo_label = fields.Binary(string="Logo Product Label", attachment=True, store=True)
