# -*- coding: utf-8 -*-
from doc._extensions.pyjsparser.parser import true
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    enable_shipping_cost = fields.Boolean(string='Shipping Cost')
    shipping_cost = fields.Float(string='Default Cost')
    shipping_product_id = fields.Many2one('product.product', string='Shipping Product',
                                          domain="[('available_in_pos', '=', 1), ('sale_ok', '=', 1), ('type', '=', 'service')]")

    hide_taxes_receipt = fields.Boolean(string='Hide taxes in Receipt')
    display_taxes_percent_orderline = fields.Boolean(string='Display taxes percent in Orderline')

    # sea_pos_code = fields.Char(string="Point of Sale Code", default=159, required=true)

    # Add fields Digets for Discount POS
    sea_digits_of_discount = fields.Integer('Digits of Discount', default=2, required=True)

    @api.onchange('sea_digits_of_discount')
    def _onchange_sea_digits_of_discount(self):
        if 0 < self.sea_digits_of_discount < 5:
            self.sea_digits_of_discount == self.sea_digits_of_discount
        else:
            raise UserError('Number cannot be less than 0 and greater than 4.')

    @api.model
    def conver_p2div_tag(self, html_val):
        return html_val.replace('<p', '<div').replace('</p>', '</div>')

    @api.model
    def create(self, vals):
        if 'receipt_header' in vals:
            vals['receipt_header'] = self.conver_p2div_tag(vals['receipt_header'])
        if 'receipt_footer' in vals:
            vals['receipt_footer'] = self.conver_p2div_tag(vals['receipt_footer'])
        return super(PosConfig, self).create(vals)

    def write(self, vals):
        if 'receipt_header' in vals:
            vals['receipt_header'] = self.conver_p2div_tag(vals['receipt_header'])
        if 'receipt_footer' in vals:
            vals['receipt_footer'] = self.conver_p2div_tag(vals['receipt_footer'])
        return super(PosConfig, self).write(vals)
