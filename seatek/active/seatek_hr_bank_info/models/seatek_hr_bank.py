from odoo import api, models, fields

class Banklist_Import(models.Model):
    _inherit = 'res.bank'
    _description = "Import banklist"

    @api.model
    def get_import_templates(self):
        return [{
            'label': ('Import Template for Bank'),
            'template': '/seatek_hr_bank_info/static/xls/res_bank.xls'
        }]