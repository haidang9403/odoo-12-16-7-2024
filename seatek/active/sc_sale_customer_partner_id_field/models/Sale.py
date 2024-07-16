from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    customer_partner_id = fields.Many2one('res.partner', string='Customer Partner', readonly=True,
                                          states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                          change_default=True, index=True, track_visibility='always', track_sequence=1,
                                          help="You can find a customer by its Name, TIN, Email or Internal Reference.")

    total = fields.Monetary(string='Total Amount', readonly=True, track_sequence=5)

    def total_amount(self, tax):
        self.total = float(self.amount_untaxed * (tax / 100) + self.amount_untaxed)

