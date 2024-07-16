from odoo import fields, models, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    sea_customer_get_invoice = fields.Boolean('Customer Get Invoice', default=True)
    sea_invoice_address = fields.Many2one('res.partner', 'Invoice Address')
    partner_vat_id = fields.Many2one('res.partner', 'VAT Address')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        if ui_order.get('is_get_invoice'):
            res['sea_customer_get_invoice'] = False
            partner_id = self.env['res.partner'].browse(int(ui_order.get('invoice_address')))
            res['partner_vat_id'] = partner_id.id
        else:
            res['partner_vat_id'] = self.env['res.partner'].browse(int(ui_order.get('partner_id'))).id
            res['sea_customer_get_invoice'] = True
        return res

    def _prepare_invoice(self):
        values = super(PosOrder, self)._prepare_invoice()
        domain = [('company_id', '=', self.company_id.id),
                  ('member_ids', '=', self.user_id.id)]
        sale_team = self.env['crm.team'].search(domain, limit=1)
        values.update({
            'sea_check_customer_for_invoice': self.sea_customer_get_invoice,
            'sea_hide_take_invoice_multi_company': 'True',
            'team_id': sale_team,
            'partner_vat_id': self.partner_vat_id
        })
        return values
