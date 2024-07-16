from odoo import models, fields


class TransactionType(models.Model):
    _inherit = "transaction.type"

    free_of_charge = fields.Boolean('FOC (%)')
