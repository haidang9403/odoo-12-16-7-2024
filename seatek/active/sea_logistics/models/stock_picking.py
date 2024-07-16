from datetime import timedelta
from odoo import models, fields, api, _
from lxml import etree
import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def _get_info_logistic(self):

        for item in self:
            date = datetime.datetime.now()
            item.date_now = datetime.datetime(year=date.year, month=date.month,
                                              day=date.day,
                                              hour=0, minute=0, second=0) - timedelta(hours=7)
            if item.sale_id:
                if item.sale_id.partner_shipping_id:
                    item.sales_person = item.sale_id.user_id
                    item.logistic_delivery = item.sale_id.partner_shipping_id.name
                    address = ''
                    if item.sale_id.partner_shipping_id.street:
                        address += item.sale_id.partner_shipping_id.street
                    if item.sale_id.partner_shipping_id.street2:
                        address += ', '
                        address += item.sale_id.partner_shipping_id.street2
                    if item.sale_id.partner_shipping_id.city:
                        address += ', '
                        address += item.sale_id.partner_shipping_id.city
                    if item.sale_id.partner_shipping_id.state_id:
                        address += ', '
                        address += item.sale_id.partner_shipping_id.state_id.name
                    item.logistic_delivery_address = address
                if item.sale_id.note:
                    item.logistic_note = item.sale_id.note
            elif item.consignment_process_id:
                item.sales_person = item.consignment_process_id.create_uid
                if item.consignment_process_id.consignment_delivery_address:
                    item.logistic_delivery = item.consignment_process_id.consignment_delivery_address.name
                    address = ''
                    if item.consignment_process_id.consignment_delivery_address.street:
                        address += item.consignment_process_id.consignment_delivery_address.street
                    if item.consignment_process_id.consignment_delivery_address.street2:
                        address += ', '
                        address += item.consignment_process_id.consignment_delivery_address.street2
                    if item.consignment_process_id.consignment_delivery_address.city:
                        address += ', '
                        address += item.consignment_process_id.consignment_delivery_address.city
                    if item.consignment_process_id.consignment_delivery_address.state_id:
                        address += ', '
                        address += item.consignment_process_id.consignment_delivery_address.state_id.name
                    item.logistic_delivery_address = address
                if item.consignment_process_id.delivery_address_note:
                    item.logistic_note = item.consignment_process_id.delivery_address_note
            elif item.stock_request_ids:
                for req in item.stock_request_ids:
                    item.sales_person = req.order_id.create_uid
                    if req.order_id.note:
                        item.logistic_note = req.order_id.note

    logistic_delivery = fields.Char('Delivery To', compute='_get_info_logistic')
    logistic_delivery_address = fields.Char('Delivery Address', compute='_get_info_logistic')
    logistic_destination_location = fields.Char('Destination Location', compute='_get_info_logistic')
    logistic_note = fields.Char('Note', compute='_get_info_logistic')
    date_now = fields.Datetime('Current Date', compute='_get_info_logistic')
    sales_person = fields.Many2one('res.users', 'Sales Person', compute='_get_info_logistic')

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(StockPicking, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_id == self.env.ref('sea_logistics.action_picking_tree_logistic_all_tree').id:
            doc = etree.XML(res['arch'])
            readonly = 'false'
            if not self.env.user.has_group('sea_logistics.group_logistic_user'):
                readonly = 'true'
            for node in doc.xpath("//field[@name='sea_customer_received']"):
                node.set('modifiers', '{"readonly": ' + readonly + '}')
            res['arch'] = etree.tostring(doc, encoding='unicode')
        return res

    @api.one
    @api.constrains('sea_customer_received')
    def _check_values(self):
        current = datetime.datetime.now()
        if self.sea_customer_received:
            if self.sea_customer_received > current:
                raise Warning(_('Input date is not greater than current date.!'))

    def received_done(self):
        self.sea_customer_received = datetime.datetime.now()
