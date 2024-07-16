from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_invoice(self):
        values = super(SaleOrder, self)._prepare_invoice()
        values.update({
            'sea_customer_po_name': self.sea_temp_contact,
            'sea_customer_po_code': self.sea_customer_po_no
        })
        return values

    @api.onchange('sea_temp_contact', 'sea_customer_po_no')
    def _onchange_data(self):
        self.invoice_ids.write({
            'sea_customer_po_name': self.sea_temp_contact,
            'sea_customer_po_code': self.sea_customer_po_no
        })
