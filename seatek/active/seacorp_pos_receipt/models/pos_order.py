from odoo import fields, models, api
from odoo.addons import decimal_precision as dp


class PosOrder(models.Model):
    _inherit = 'pos.order'


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    discount_ref = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0,
                                compute='_get_discount')

    def _get_discount(self):
        for re in self:
            if re.discount:
                re.discount_ref = re.discount
