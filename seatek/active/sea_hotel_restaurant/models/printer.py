from odoo import fields, models


class HotelRestaurantPrinter(models.Model):
    _inherit = 'restaurant.printer'

    title = fields.Char('Title Name')
    product_product_categories_ids = fields.Many2many('product.category', 'printer_product_category_rel', 'printer_id',
                                                      'pro_category_id', string='Printed Product Categories')
