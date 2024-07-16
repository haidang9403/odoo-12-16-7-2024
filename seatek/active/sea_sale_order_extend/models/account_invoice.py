# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    partner_vat_id = fields.Many2one(
        'res.partner',
        string='VAT Address',
        states={'draft': [('readonly', False)]},
        domain="[('is_company', '=', True)]",
        help="VAT address for current invoice.")
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        domain="[('customer', '=', True)]",
        states={'draft': [('readonly', False)]},
        help="Buyer for current invoice.")

    @api.onchange('partner_id', 'company_id', 'sea_check_customer_for_invoice')
    def _onchange_vat_address(self):
        # addr = self.partner_id.address_get(['vat'])
        if not self.sea_check_customer_for_invoice:
            self.partner_vat_id = self.partner_id
        else:
            self.partner_vat_id = False
        self.buyer_id = self.partner_id
        # inv_type = self.type or self.env.context.get('type', 'out_invoice')
        # if inv_type == 'out_invoice':
        #     company = self.company_id or self.env.user.company_id
        #     self.comment = company.with_context(lang=self.partner_id.lang or self.env.lang).sale_note or (
        #                 self._origin.company_id == company and self.comment)

    @api.model
    def create(self, vals):
        if vals.get('origin'):
            sale = self.env['sale.order'].search([('name', '=', vals.get('origin'))])
            if sale:
                if sale.partner_id:
                    if sale.partner_invoice_id:
                        if sale.partner_id.id != sale.partner_invoice_id.id \
                                and sale.partner_invoice_id.id not in sale.partner_id.partner_invoice_ids.ids:
                            sale.partner_id.write({
                                'partner_invoice_ids': [(4, sale.partner_invoice_id.id)]
                            })
                    if sale.partner_vat_id:
                        if sale.partner_id.id != sale.partner_vat_id.id \
                                and sale.partner_vat_id.id not in sale.partner_id.partner_vat_ids.ids:
                            sale.partner_id.write({
                                'partner_vat_ids': [(4, sale.partner_vat_id.id)]
                            })

        return super(AccountInvoice, self).create(vals)
