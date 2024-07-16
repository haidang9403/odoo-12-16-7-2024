# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'invoice_line_ids.price_unit', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice', 'global_discount_type', 'global_order_discount')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        totalAmount, totalDiscount = 0.0, 0.0
        amountUntaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        amountTax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
        amountDownpayment = sum(line.price_subtotal for line in self.invoice_line_ids if line.sale_line_ids and line.sale_line_ids[0].is_downpayment)
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
        total = totalAmount - amountDownpayment
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
