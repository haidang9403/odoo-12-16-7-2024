from odoo import models, fields
from datetime import timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sea_customer_received = fields.Char(string='Customer Received',
                                        compute='_get_date_customer_received')
    sea_delivery_name_one = fields.Char(String='one', compute='_get_date_customer_received')
    sea_delivery_name_two = fields.Char(String='two', compute='_get_date_customer_received')
    sea_delivery_name_three = fields.Char(String='three', compute='_get_date_customer_received')
    sea_delivery_name_four = fields.Char(String='four', compute='_get_date_customer_received')

    sea_customer_received_one = fields.Char(String='one', compute='_get_date_customer_received')
    sea_customer_received_two = fields.Char(String='two', compute='_get_date_customer_received')
    sea_customer_received_three = fields.Char(String='three', compute='_get_date_customer_received')
    sea_customer_received_four = fields.Char(String='four', compute='_get_date_customer_received')

    def _get_date_customer_received(self):
        get_name = []
        get_time = []
        for res in self.env['stock.picking'].search([('origin', '=', self.name)]):
            if res.state == 'done' and res.sea_customer_received:
                if res.sea_customer_received:
                    get_date = res.sea_customer_received + timedelta(hours=7)
                    if get_date:
                        get_name.append(str(res.name))
                        get_time.append(str(get_date.strftime("%I:%M %p %d/%m/%y")))
        if get_name:
            i_name = (len(get_name))
            if i_name == 4:
                self.sea_delivery_name_one = get_name[i_name - 1]
                self.sea_delivery_name_two = get_name[i_name - 2]
                self.sea_delivery_name_three = get_name[i_name - 3]
                self.sea_delivery_name_four = get_name[i_name - 4]
            if i_name == 3:
                self.sea_delivery_name_one = get_name[i_name - 1]
                self.sea_delivery_name_two = get_name[i_name - 2]
                self.sea_delivery_name_three = get_name[i_name - 3]
            if i_name == 2:
                self.sea_delivery_name_one = get_name[i_name - 1]
                self.sea_delivery_name_two = get_name[i_name - 2]
            if i_name == 1:
                self.sea_delivery_name_one = get_name[i_name - 1]
        if get_time:
            i_time = len(get_time)
            if i_time == 4:
                self.sea_customer_received_one = ' ' + get_time[i_time - 1]
                self.sea_customer_received_two = ' ' + get_time[i_time - 2]
                self.sea_customer_received_three = ' ' + get_time[i_time - 3]
                self.sea_customer_received_four = ' ' + get_time[i_time - 4]
            if i_time == 3:
                self.sea_customer_received_one = ' ' + get_time[i_time - 1]
                self.sea_customer_received_two = ' ' + get_time[i_time - 2]
                self.sea_customer_received_three = ' ' + get_time[i_time - 3]
            if i_time == 2:
                self.sea_customer_received_one = ' ' + get_time[i_time - 1]
                self.sea_customer_received_two = ' ' + get_time[i_time - 2]
            if i_time == 1:
                self.sea_customer_received_one = ' ' + get_time[i_time - 1]


# Option 2
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     sea_customer_received = fields.Char(string='Customer Received',
#                                         compute='_get_date_customer_received')
#
#     def _get_date_customer_received(self):
#         self.sea_customer_received = ''
#         re = []
#         for res in self.env['stock.picking'].search([('origin', '=', self.name)]):
#             if res.state == 'done' and res.sea_customer_received:
#                 if res.sea_customer_received:
#                     get_date = res.sea_customer_received + timedelta(hours=7)
#                     if get_date:
#                         re.append(str(res.name) + '\n' + ' ' + str(get_date.strftime("%I:%M %p  %d/%m/%y")))
#
#         for r in reversed(re):
#             self.sea_customer_received += ('\n' + r)
