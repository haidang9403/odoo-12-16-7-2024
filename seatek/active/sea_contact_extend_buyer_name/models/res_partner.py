from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sea_full_name = fields.Char("Buyer's name")
