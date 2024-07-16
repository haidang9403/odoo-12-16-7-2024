# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from functools import partial

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total', 'global_order_discount', 'global_discount_type')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            total_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                if line.discount_type == 'fixed':
                    total_discount += line.discount
                else:
                    total_discount += line.product_uom_qty * \
                        (line.price_unit - line.price_reduce)
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    quantity = 1.0
                    if line.discount_type == 'fixed':
                        price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
                    else:
                        quantity = line.product_uom_qty
                        price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id,
                                                    quantity, product=line.product_id, partner=line.order_id.partner_id)
                    amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                else:
                    amount_tax += line.price_tax

            IrConfigPrmtrSudo = self.env['ir.config_parameter'].sudo()
            discTax = IrConfigPrmtrSudo.get_param('account.global_discount_tax')
            total_amount = amount_untaxed
            if discTax == 'taxed':
                total_amount = amount_untaxed + amount_tax
            if order.global_discount_type == 'fixed':
                global_discount = order.global_order_discount or 0.0
            else:
                global_discount = total_amount * (order.global_order_discount or 0.0) / 100
            total_amount -= global_discount
            total_discount += global_discount
            if discTax != 'taxed':
                total_amount = total_amount + amount_tax
            order.update({
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed),
                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': total_amount,
                'total_global_discount': global_discount,
                'total_discount': total_discount,
            })

    total_global_discount = fields.Monetary(
        string='Total Global Discount', store=True, readonly=True, compute='_amount_all')
    total_discount = fields.Monetary(
        string='Discount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    global_discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], string="Discount Type",
        default="percent",
        help="If global discount type 'Fixed' has been applied then no partial invoice will be generated for this order.")
    global_order_discount = fields.Float(
        string='Global Discount', store=True,  track_visibility='always')

    @api.one
    def _compute_amount_undiscounted(self):
        total = 0.0
        for line in self.order_line:
            if line.discount_type == 'fixed':
                total += line.price_subtotal + (line.discount or 0.0)
            else:
                total += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0) * line.product_uom_qty  # why is there a discount in a field named amount_undiscounted ??
        self.amount_undiscounted = total

    def _amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
            res = {}
            for line in order.order_line:
                if line.discount_type == 'fixed' and line.product_uom_qty:
                    price_reduce = line.price_unit * line.product_uom_qty - line.discount
                    price_reduce /= line.product_uom_qty
                else:
                    price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
                for tax in line.tax_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {'amount': 0.0, 'base': 0.0})
                    for t in taxes:
                        if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
                            res[group]['amount'] += t['amount']
                            res[group]['base'] += t['base']
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            order.amount_by_group = [(
                l[0].name, l[1]['amount'], l[1]['base'],
                fmt(l[1]['amount']), fmt(l[1]['base']),
                len(res),
            ) for l in res]

    @api.multi
    def _prepare_invoice(self):
        invoiceVals = super(SaleOrder, self)._prepare_invoice()
        self.ensure_one()
        if self.global_order_discount:
            if self.global_discount_type == 'fixed':
                lines = self.order_line.filtered(
                    lambda l: not l.is_downpayment and l.product_uom_qty != l.qty_to_invoice)
                if lines:
                    raise UserError(
                        _("This action is going to make partial invoice for the less quantity delivered of this order. It will not be allowed because 'Fixed' type global discount has been applied."))
            invoiceVals.update({
                'global_discount_type' : self.global_discount_type,
                'global_order_discount' : self.global_order_discount
                })
        return invoiceVals

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)
    line_amount_subtotal = fields.Monetary(compute='_get_price_reduce', string='Line Subtotal', readonly=True, store=True)
    line_amount_total = fields.Monetary(compute='_get_price_reduce', string='Line Total', readonly=True, store=True)
    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
        ], default='percent',
        string="Discount Type",)

    @api.depends('product_uom_qty','discount_type', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        for line in self:
            quantity = 1.0
            if line.discount_type == 'fixed':
                price = line.price_unit * line.product_uom_qty - (line.discount or 0.0)
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                quantity = line.product_uom_qty
            taxes = line.tax_id.compute_all(
                price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    @api.depends('price_unit', 'discount_type', 'discount', 'product_uom_qty', 'tax_id')
    def _get_price_reduce(self):
        for line in self:
            if line.discount_type == 'fixed' and line.product_uom_qty:
                price_reduce = line.price_unit * line.product_uom_qty - line.discount
                line.price_reduce = price_reduce/line.product_uom_qty
            else:
                line.price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
            price = line.price_unit
            quantity = line.product_uom_qty
            taxes = line.tax_id.compute_all(
                price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
            line.line_amount_subtotal = taxes['total_excluded']
            line.line_amount_total = taxes['total_included']

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        discount = self.discount
        if self.discount_type == 'fixed' and self.product_uom_qty:
            discount = (discount * self.qty_to_invoice) / self.product_uom_qty
        res.update({
            'discount_type': self.discount_type,
            'discount': discount,
        })
        return res

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        if not (self.product_id and self.product_uom and
                self.order_id.partner_id and self.order_id.pricelist_id and
                self.order_id.pricelist_id.discount_policy == 'without_discount' and
                self.env.user.has_group('sale.group_discount_per_so_line')):
            return

        self.discount = 0.0
        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id,
            quantity=self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id,
            fiscal_position=self.env.context.get('fiscal_position')
        )

        product_context = dict(self.env.context, partner_id=self.order_id.partner_id.id, date=self.order_id.date_order, uom=self.product_uom.id)

        price, rule_id = self.order_id.pricelist_id.with_context(product_context).get_product_price_rule(self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
        new_list_price, currency = self.with_context(product_context)._get_real_price_currency(product, rule_id, self.product_uom_qty, self.product_uom, self.order_id.pricelist_id.id)

        if new_list_price != 0:
            if self.order_id.pricelist_id.currency_id != currency:
                # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                new_list_price = currency._convert(
                    new_list_price, self.order_id.pricelist_id.currency_id,
                    self.order_id.company_id or self.env.user.company_id, self.order_id.date_order or fields.Date.today())
            rule = self.order_id.pricelist_id.with_context(
                product_context)._get_pricelist_item([
                    (self.product_id, self.product_uom_qty or 1.0, self.order_id.partner_id)
                ])
            if rule and rule.compute_price == 'fixed':
                discount = (new_list_price - price) * (self.product_uom_qty or 1.0)
                discount_type = 'fixed'
            else:
                discount = (new_list_price - price) / new_list_price * 100
                discount_type = 'percent'

            if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                self.discount = discount
                self.discount_type = discount_type


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def _get_pricelist_item(self, products_qty_partner, date=False, uom_id=False):
        if not date:
            date = self._context.get('date') or fields.Date.today()
        date = fields.Date.to_date(date)  # boundary conditions differ if we have a datetime
        if not uom_id and self._context.get('uom'):
            uom_id = self._context['uom']
        if uom_id:
            # rebrowse with uom if given
            products = [item[0].with_context(uom=uom_id) for item in products_qty_partner]
            products_qty_partner = [
                (products[index], data_struct[1], data_struct[2])
                for index, data_struct in enumerate(products_qty_partner)
            ]
        else:
            products = [item[0] for item in products_qty_partner]

        if not products:
            return {}

        categ_ids = {}
        for p in products:
            categ = p.categ_id
            while categ:
                categ_ids[categ.id] = True
                categ = categ.parent_id
        categ_ids = list(categ_ids)

        is_product_template = products[0]._name == "product.template"
        if is_product_template:
            prod_tmpl_ids = [tmpl.id for tmpl in products]
            # all variants of all products
            prod_ids = [
                p.id for p in list(
                    chain.from_iterable(
                        [t.product_variant_ids for t in products]))
            ]
        else:
            prod_ids = [product.id for product in products]
            prod_tmpl_ids = [product.product_tmpl_id.id for product in products]

        # Load all rules
        self._cr.execute(
            'SELECT item.id '
            'FROM product_pricelist_item AS item '
            'LEFT JOIN product_category AS categ '
            'ON item.categ_id = categ.id '
            'WHERE (item.product_tmpl_id IS NULL OR item.product_tmpl_id = any(%s))'
            'AND (item.product_id IS NULL OR item.product_id = any(%s))'
            'AND (item.categ_id IS NULL OR item.categ_id = any(%s)) '
            'AND (item.pricelist_id = %s) '
            'AND (item.date_start IS NULL OR item.date_start<=%s) '
            'AND (item.date_end IS NULL OR item.date_end>=%s)'
            'ORDER BY item.applied_on, item.min_quantity desc, categ.complete_name desc, item.id desc',
            (prod_tmpl_ids, prod_ids, categ_ids, self.id, date, date))
        # NOTE: if you change `order by` on that query, make sure it matches
        # _order from model to avoid inconstencies and undeterministic issues.

        item_ids = [x[0] for x in self._cr.fetchall()]
        items = self.env['product.pricelist.item'].browse(item_ids)
        return items[0] if items else False
