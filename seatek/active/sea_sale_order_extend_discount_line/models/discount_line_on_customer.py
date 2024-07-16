from odoo import models, fields, api, _
from odoo.exceptions import UserError


class DiscountLineOnCustomer(models.Model):
    _name = 'discount.line.on.customer'

    partner_id = fields.Many2one('res.partner', 'Customer')
    product_id = fields.Many2one('product.product', 'Product')
    category_id = fields.Many2one('product.category', 'Product category')
    sale_channel_id = fields.Many2one('sale.channel', 'Sale Channel')
    discount = fields.Float('Discount')
    discount_type = fields.Selection([('percent', 'Percent'), ('fixed', 'Fixed')], string='Discount Type',
                                     required=True, default='percent')
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)

    @api.model
    def create(self, vals):
        res = super(DiscountLineOnCustomer, self).create(vals)
        domain = []
        if vals.get('partner_id'):
            domain.append(('partner_id', '=', vals.get('partner_id')))
        if vals.get('product_id'):
            domain.append(('product_id', '=', vals.get('product_id')))
        else:
            if vals.get('category_id'):
                domain.append(('category_id', '=', vals.get('category_id')))
            else:
                if vals.get('sale_channel_id'):
                    domain.append(('sale_channel_id', '=', vals.get('sale_channel_id')))
        if len(self.env['discount.line.on.customer'].search(domain)) > 1:
            raise UserError(_('Document already exists...!'))
        if vals.get('discount') == 0:
            raise UserError(_('Discount value has not been assigned...!'))
        return res

    @api.multi
    def write(self, vals):
        res = super(DiscountLineOnCustomer, self).write(vals)
        domain = []
        if vals.get('partner_id'):
            domain.append(('partner_id', '=', vals.get('partner_id')))
        if vals.get('product_id'):
            domain.append(('product_id', '=', vals.get('product_id')))
        else:
            if vals.get('category_id'):
                domain.append(('category_id', '=', vals.get('category_id')))
            else:
                if vals.get('sale_channel_id'):
                    domain.append(('sale_channel_id', '=', vals.get('sale_channel_id')))
        check_exist = self.env['discount.line.on.customer'].search(domain)
        if len(check_exist) > 1:
            raise UserError(_('Document already exists...!'))
        if vals.get('discount') == 0:
            raise UserError(_('Discount value has not been assigned...!'))
        return res
