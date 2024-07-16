from odoo import models, fields


class SalesTeam(models.Model):
    _inherit = "crm.team"

    sea_sales_department = fields.Selection([
        ('si', 'Sỉ'),
        ('le', 'Lẻ'),
    ], string='Sales Department')
