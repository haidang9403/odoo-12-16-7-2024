# -*- coding: utf-8 -*-
from odoo import fields, models


class SeaContact(models.Model):
    _inherit = 'res.partner'
    # Ma Kinh Doanh from PhiMa
    sea_business_code = fields.Char(string='Business Code', copy=False)
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
         ("ship", "Ship"),
         ], string='Address Type',
        default='contact',
        help="Used by Sales and Purchase Apps to select the relevant address depending on the context.")
    vat = fields.Char(track_visibility='onchange')
    sea_customer_type_id = fields.Many2one('customer.category.tax', track_visibility='onchange')
    sea_email_invoice = fields.Char(track_visibility='onchange')
    sea_payment_method = fields.Selection(
        selection=[('cash', 'Tiền Mặt'), ('bank', 'Ngân Hàng'), ('debt', 'Công Nợ'), ],
        string='Payment Method')
