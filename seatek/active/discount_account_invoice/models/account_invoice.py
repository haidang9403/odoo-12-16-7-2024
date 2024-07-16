# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'invoice_line_ids.price_unit', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'global_discount_type', 'global_order_discount')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        totalAmount, totalDiscount = 0.0, 0.0
        amountUntaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        amountTax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
        lineTotalDiscount = sum((line.quantity*(line.price_unit) - line.price_subtotal) if line.discount_type == 'percent' else line.discount for line in self.invoice_line_ids)
        totalDiscount = lineTotalDiscount
        IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
        discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
        if not discTax:
            discTax = 'untax'
        totalGlobalDiscount = 0
        if discTax == 'taxed':
            totalAmount = amountUntaxed + amountTax
        else:
            totalAmount = amountUntaxed
        total = totalAmount
        if self.global_discount_type == 'fixed':
            totalGlobalDiscount = self.global_order_discount or 0.0
        else:
            totalGlobalDiscount = total * (self.global_order_discount or 0.0) / 100
        totalAmount -= totalGlobalDiscount
        totalDiscount += totalGlobalDiscount
        if discTax != 'taxed':
            totalAmount = totalAmount + amountTax
        self.total_discount = totalDiscount
        self.amount_untaxed = amountUntaxed
        self.amount_tax = amountTax
        self.amount_total = totalAmount
        self.total_global_discount = totalGlobalDiscount
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id
            amount_total_company_signed = currency_id._convert(self.amount_total, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
            amount_untaxed_signed = currency_id._convert(self.amount_untaxed, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        round_curr = self.currency_id.round
        for line in self.invoice_line_ids:
            if not line.account_id or line.display_type:
                continue
            quantity = 1.0
            if line.discount_type == 'fixed':
                price_unit = line.price_unit * line.quantity - (line.discount or 0.0)
            else:
                quantity = line.quantity
                price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, quantity, line.product_id, self.partner_id)['taxes']
            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)
                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]['base'] = round_curr(val['base'])
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += round_curr(val['base'])
        return tax_grouped

    total_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    total_global_discount = fields.Monetary(string='Total Global Discount', store=True, readonly=True, compute='_compute_amount')
    global_discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], string="Discount Type", default="percent")
    global_order_discount = fields.Float(string='Global Discount', store=True)

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        inv_obj = self[0]
        if inv_obj.total_global_discount > 0.0:
            if self.type in ['out_invoice', 'in_refund']:
                sign = 1
                account = self.env.user.company_id.discount_account_invoice
                for i, j, line in move_lines:
                    if line.get('debit') and not line.get('product_id'):
                        line['debit'] -= inv_obj.total_global_discount
                        break
            else:
                sign = -1
                account = self.env.user.company_id.discount_account_bill
                for i, j, line in move_lines:
                    if line.get('credit') and not line.get('product_id'):
                        line['credit'] -= inv_obj.total_global_discount
                        break
            if not account:
                raise UserError(_("Global Discount!\nPlease first set account for global discount in account setting"))
            amount_currency = 0.0
            currency = inv_obj.currency_id
            company_currency = inv_obj.company_id.currency_id
            diff_currency = currency != company_currency
            if diff_currency:
                date = self._get_currency_rate_date() or fields.Date.context_today(self)
                amount_currency = currency._convert(
                    inv_obj.total_global_discount, company_currency, inv_obj.company_id, date)
            else:
                currency = False
            global_line =  {
                'type': 'dest',
                'name': account.name,
                'price': sign * (inv_obj.total_global_discount),
                'account_id': account.id,
                'date_maturity': inv_obj.date_due,
                'amount_currency': diff_currency and amount_currency,
                'currency_id': currency and currency.id,
                'invoice_id': inv_obj.id
            }
            part = self.env['res.partner']._find_accounting_partner(inv_obj.partner_id)
            global_line = [(0, 0, self.line_get_convert(global_line, part.id))]
            move_lines += global_line
        return move_lines

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        values = super()._prepare_refund(
            invoice, date_invoice=date_invoice, date=date, description=description, journal_id=journal_id)
        values.update({
            'global_discount_type' : invoice.global_discount_type,
            'global_order_discount' : invoice.global_order_discount,
        })
        return values



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)
    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], string="Discount Type", default="percent")

    @api.one
    @api.depends('price_unit', 'discount', 'discount_type', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        quantity = 1.0
        if self.discount_type == 'fixed':
            price = self.price_unit * self.quantity - self.discount or 0.0
        else:
            quantity = self.quantity
            price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(
                price, currency, quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            currency = self.invoice_id.currency_id
            date = self.invoice_id._get_currency_rate_date()
            price_subtotal_signed = currency._convert(
                price_subtotal_signed, self.invoice_id.company_id.currency_id,
                self.company_id or self.env.user.company_id,  date or fields.Date.today())
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign
