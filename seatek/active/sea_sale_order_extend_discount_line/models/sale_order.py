from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_customer_compute_discount_line(self):
        if self.partner_id and self.order_line:
            for line in self.order_line:
                disc_product = self.env['discount.line.on.customer'].search(
                    [('partner_id', '=', self.partner_id.id),
                     ('product_id', '=', line.product_id.id)])
                if disc_product:
                    if len(disc_product) == 1:
                        line.update({
                            'discount_type': disc_product.discount_type,
                            'discount': disc_product.discount,
                        })
                    else:
                        amount_list = []
                        for disc in disc_product:
                            if line.price_unit:
                                if disc.discount_type == 'percent':
                                    amount_list.append(line.price_unit - ((line.price_unit * disc.discount) / 100))
                                if disc.discount_type == 'fixed':
                                    amount_list.append(line.price_unit - disc.discount)
                        if amount_list:
                            for d in disc_product:
                                min_disc = min(amount_list)
                                if d.discount_type == 'percent':
                                    if line.price_unit - ((line.price_unit * d.discount) / 100) == min_disc:
                                        line.update({
                                            'discount_type': d.discount_type,
                                            'discount': d.discount,
                                        })
                                if d.discount_type == 'fixed':
                                    if line.price_unit - d.discount == min_disc:
                                        line.update({
                                            'discount_type': d.discount_type,
                                            'discount': d.discount,
                                        })
                else:
                    cate_ids = []
                    for p in line.product_id.categ_id:
                        cate_ids.append(p.id)
                        if p.parent_id:
                            cate_ids.append(p.parent_id.id)
                    disc_product_category = self.env['discount.line.on.customer'].search(
                        [('partner_id', '=', self.partner_id.id),
                         ('category_id', 'in', cate_ids)])
                    if disc_product_category:
                        if len(disc_product_category) == 1:
                            line.update({
                                'discount_type': disc_product_category.discount_type,
                                'discount': disc_product_category.discount,
                            })
                    else:
                        channel_ids = []
                        for channel in self.partner_id.sea_partner_sale_channel_id:
                            if channel:
                                channel_ids.append(channel.id)
                                if channel.parent_id:
                                    channel_ids.append(channel.parent_id.id)
                        disc_channel = self.env['discount.line.on.customer'].search(
                            [('partner_id', '=', self.partner_id.id),
                             ('sale_channel_id', 'in', channel_ids)])
                        if disc_channel:
                            if len(disc_channel) == 1:
                                line.update({
                                    'discount_type': disc_channel.discount_type,
                                    'discount': disc_channel.discount,
                                })
                        else:
                            line.update({
                                'discount': 0,
                            })


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'sale_line_transaction_id', 'price_unit')
    def _onchange_compute_discount_line(self):
        self.ensure_one()
        if self.product_id:
            if self.sale_line_transaction_id and self.sale_line_transaction_id.free_of_charge:
                self.discount_type = 'percent'
                self.discount = 100
            else:
                if self.order_id.partner_id:
                    disc_product = self.env['discount.line.on.customer'].search(
                        [('partner_id', '=', self.order_id.partner_id.id),
                         ('product_id', '=', self.product_id.id)])
                    if disc_product:
                        if len(disc_product) == 1:
                            self.discount_type = disc_product.discount_type
                            self.discount = disc_product.discount
                        else:
                            amount_list = []
                            for disc in disc_product:
                                if self.price_unit:
                                    if disc.discount_type == 'percent':
                                        amount_list.append(self.price_unit - ((self.price_unit * disc.discount)/100))
                                    if disc.discount_type == 'fixed':
                                        amount_list.append(self.price_unit - disc.discount)
                            if amount_list:
                                for line in disc_product:
                                    min_disc = min(amount_list)
                                    if line.discount_type == 'percent':
                                        if self.price_unit - ((self.price_unit * line.discount)/100) == min_disc:
                                            self.discount_type = line.discount_type
                                            self.discount = line.discount
                                    if line.discount_type == 'fixed':
                                        if self.price_unit - line.discount == min_disc:
                                            self.discount_type = line.discount_type
                                            self.discount = line.discount
                    else:
                        cate_ids = []
                        for p in self.product_id.categ_id:
                            cate_ids.append(p.id)
                            if p.parent_id:
                                cate_ids.append(p.parent_id.id)
                        disc_product_category = self.env['discount.line.on.customer'].search(
                            [('partner_id', '=', self.order_id.partner_id.id),
                             ('category_id', 'in', cate_ids)])
                        if disc_product_category:
                            if len(disc_product_category) == 1:
                                self.discount_type = disc_product_category.discount_type
                                self.discount = disc_product_category.discount
                        else:
                            channel_ids = []
                            for channel in self.order_id.partner_id.sea_partner_sale_channel_id:
                                if channel:
                                    channel_ids.append(channel.id)
                                    if channel.parent_id:
                                        channel_ids.append(channel.parent_id.id)
                            disc_channel = self.env['discount.line.on.customer'].search(
                                [('partner_id', '=', self.order_id.partner_id.id),
                                 ('sale_channel_id', 'in', channel_ids)])
                            if disc_channel:
                                if len(disc_channel) == 1:
                                    self.discount_type = disc_channel.discount_type
                                    self.discount = disc_channel.discount
                            else:
                                self.discount = 0
