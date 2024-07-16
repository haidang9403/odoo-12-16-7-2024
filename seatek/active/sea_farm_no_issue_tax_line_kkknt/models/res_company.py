from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    sea_no_issue_invoice_line_tax_kkknt = fields.Boolean('Do Not Issue KKKNT')
