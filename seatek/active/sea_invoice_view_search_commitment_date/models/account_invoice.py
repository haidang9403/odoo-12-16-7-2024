from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def _get_commitment_date(self):
        for rec in self:
            if rec.id:
                rec.sea_commitment_date = rec.commitment_date

    sea_commitment_date = fields.Datetime(compute='_get_commitment_date')
    sea_view_commitment_date = fields.Datetime('Commitment Date', related='sea_commitment_date', store=True)
