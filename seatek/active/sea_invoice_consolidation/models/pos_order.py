from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _prepare_invoice(self):
        values = super(PosOrder, self)._prepare_invoice()
        values.update({
            'sea_bill_pos': self.pos_reference,
        })
        return values
