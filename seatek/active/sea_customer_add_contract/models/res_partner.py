from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sea_customer_contract_number = fields.Char('Contract Number')
    sea_contract_start_date = fields.Date('Start Date')
    sea_contract_to_date = fields.Date('To Date')
