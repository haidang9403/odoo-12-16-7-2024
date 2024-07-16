# Update 13/12/2021

from odoo import models, fields


class SeaCompanyForeign(models.Model):
    _inherit = ['res.company']

    sea_company_foreign = fields.Text(string='Name (Foregin)', store=True, default="")