import logging
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class SaleOrder(models.Model):
    _inherit = "sale.order"

    '''Phụ thu'''
    surcharge_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percent', 'Percent')
    ], string="Surcharge Type", default="percent")
    surcharge = fields.Float('Discount', default=0)

    state = fields.Selection(
        selection_add=[('sale_folio', 'Sale Folio')])

    pos_hotel_restaurant_id = fields.Many2one("sea.pos.hotel.restaurant", "Point of Sale")

    order_type = fields.Selection([
        ('hotel_order', 'Is Hotel Order'),
        ('restaurant_order', 'Is Restaurant Order')], string='Order Type')

    folio_id = fields.Many2one("sea.folio", "Folio",
                               domain="[('customer_id', '=', partner_id),('state', '=', 'inprogress')]")
    state_folio = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
        ('inprogress', 'In Progress'),
    ], related='folio_id.state')

    table_id = fields.Many2one("sea.restaurant.table", "Table Restaurant",
                               domain="[('company_id', '=', company_id), ('status', '=', 'available'),"
                                      "('pos_hotel_restaurant_id', '=', pos_hotel_restaurant_id)]")
    room_id = fields.Many2one("sea.hotel.room", "Room", domain="[('company_id', '=', company_id), ('status', '=', "
                                                               "'available'), ('pos_hotel_restaurant_id', '=', "
                                                               "pos_hotel_restaurant_id)]")
    status_room = fields.Selection([("available", "Available"), ("occupied", "Occupied"),
                                    ("maintained", "Maintained"), ("cleaned", "Cleaned")], String="State Room",
                                   related='room_id.status')
    check_in = fields.Datetime(string='Check In',
                               default=datetime(datetime.now().year, datetime.now().month, datetime.now().day, 12, 0,
                                                0))
    check_out = fields.Datetime(string='Check Out',
                                default=datetime(datetime.now().year, datetime.now().month, datetime.now().day, 14,
                                                 0, 0)
                                )
    ''' Lấy data khách hàng default từ POS khi tạo đơn hàng '''
    partner_id_hr = fields.Many2one('res.partner', string='Partner Hotel Restaurant',
                                    domain="[('property_account_receivable_id', 'not in', [None, False])]",
                                    default=lambda self: self.env['sea.pos.hotel.restaurant'].browse(
                                        self._context.get('active_id')).customer_default_id.id)
    ''' Trường hợp folio '''

    '''cần xem lại'''

    @api.onchange('partner_id_hr')
    def onchange_partner_id_hr(self):
        self.partner_id = self.partner_id_hr
        self.onchange_partner_id()

    '''cần xem lại'''

    @api.constrains('partner_id_hr')
    def constraint_partner_id_hr(self):
        if self.partner_id_hr:
            listprice_id_old = self.pricelist_id.id
            self.partner_id = self.partner_id_hr
            self.onchange_partner_id()
            if self.pricelist_id.id != listprice_id_old:
                self.pricelist_id = listprice_id_old
            check_folio_partner_old = self.env['sea.folio'].sudo().search(
                [('id', '=', self.folio_id.id)], limit=1)
            check_folio_partner_new = self.env['sea.folio'].sudo().search(
                [('customer_id', '=', self.partner_id_hr.id), ('state', '=', 'inprogress'),
                 ('branch_id', '=', self.pos_hotel_restaurant_id.hotel_restaurant_branch_id.id)], limit=1)
            if check_folio_partner_new.id != check_folio_partner_old.id:
                if check_folio_partner_new and len(check_folio_partner_old) < 1:
                    self.folio_id = check_folio_partner_new.id

                elif len(check_folio_partner_new) < 1 and check_folio_partner_old:
                    if len(check_folio_partner_old.order_ids) > 1:
                        res = self.env['sea.folio'].sudo().create({
                            'customer_id': self.partner_id_hr.id,
                            'sale_person_id': self.env.user.partner_id.id,
                            'branch_id': self.pos_hotel_restaurant_id.hotel_restaurant_branch_id.id,
                            'company_id': self.company_id.id,
                            'state': 'inprogress'
                        })

                        self.folio_id = res.id
                    if len(check_folio_partner_old.order_ids) == 1:
                        update_folio = self.env['sea.folio'].sudo().search(
                            [('id', '=', self.folio_id.id)])
                        update_folio.write({'customer_id': self.partner_id_hr.id,
                                            'folio_name': self.partner_id_hr.name})
                elif check_folio_partner_new and check_folio_partner_old:
                    if len(check_folio_partner_old.order_ids) > 1:
                        for order in check_folio_partner_new:
                            self.folio_id = order.id

                    if len(check_folio_partner_old.order_ids) == 1:
                        for order in check_folio_partner_new:
                            self.folio_id = order.id

    '''"Các trường này dùng để tính thành tiền tổng đơn dựa trên SL đã phục vụ.
     Hiện do thống nhất sẽ tính trên SL đặt nên những trường này chưa cần xài"'''

    # done_untaxed = fields.Monetary(string='Untaxed Amount', currency_field='currency_id', store=True, readonly=True,
    #                                track_visibility='onchange', track_sequence=5)
    # done_taxes = fields.Monetary(string='Taxes', currency_field='currency_id', store=True, readonly=True)
    # done_discount = fields.Monetary(string='Discount', currency_field='currency_id',
    #                                 store=True, readonly=True, track_visibility='always')
    # done_total = fields.Monetary(string='Total', currency_field='currency_id', store=True,
    #                              readonly=True, track_visibility='always', track_sequence=6)
    # currency_id = fields.Many2one('res.currency', string="Currency",
    #                               default=lambda self: self.env.user.company_id.currency_id)

    # @api.multi
    # def set_default_is_hotel_guest(self):
    #     if self.folio_id_restaurant or self.folio_id_hotel:
    #         self.is_hotel_guest = True
    #
    # @api.multi
    # def check_invoice_can_be_pay(self):
    #     pay_ok = True
    #     if not self.invoice_ids:
    #         pay_ok = False
    #     else:
    #         for invoice in self.invoice_ids:
    #             if invoice.state != 'open':
    #                 pay_ok = False
    #                 break
    #     self.can_be_pay = pay_ok
    #
    # is_hotel_guest = fields.Boolean("Is Hotel Guest?", default=False, compute='set_default_is_hotel_guest')
    #
    # can_be_pay = fields.Boolean(default=False, compute='check_invoice_can_be_pay')

    '''lấy price list default của POS đó dùng riêng cho hotel & restaurant'''

    @api.constrains('pricelist_id')
    def constrains_pricelist_id(self):
        for rec in self:
            if rec.order_type and rec.pos_hotel_restaurant_id:
                if rec.order_type in ['hotel_order',
                                      'restaurant_order'] and rec.pos_hotel_restaurant_id.sudo().available_pricelist_id:
                    if rec.pricelist_id.id != rec.pos_hotel_restaurant_id.sudo().available_pricelist_id.id:
                        rec.pricelist_id = rec.pos_hotel_restaurant_id.sudo().available_pricelist_id.id

    @api.onchange('room_id')
    def onchange_room_id(self):
        order_lines = []
        if self.order_line:
            self.order_line = None
        if self.room_id.product_default:
            for product in self.room_id.product_default:
                order_lines.append((0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': product.list_price,
                    # 'checkin_date': self.get_checkin_date(),
                    # 'checkout_date': self.get_checkout_date(),
                    'product_uom': product.sudo().product_tmpl_id.sudo().uom_id.sudo().id,
                    'room_id': self.room_id

                }))
        if self.room_id.default_amenities:
            for product_amenities in self.room_id.default_amenities:
                # print('test product_amenities', product_amenities)
                order_lines.append((0, 0, {
                    'product_id': product_amenities.product_id,
                    'product_uom_qty': product_amenities.quantity,
                    'price_unit': product_amenities.product_id.list_price,
                    'product_uom': product.sudo().product_tmpl_id.sudo().uom_id.sudo().id,
                    'room_id': self.room_id
                }))
        self.order_line = order_lines

    @api.multi
    def get_checkin_date(self):
        if "checkin" in self._context:
            return self._context["checkin"]
        else:
            now = datetime.now()
            checkin_date = datetime(now.year, now.month, now.day, 5, 0, 0)
            return checkin_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    @api.multi
    def get_checkout_date(self):
        if "checkout" in self._context:
            return self._context["checkout"]
        else:
            now = datetime.now()
            checkin_date = datetime(now.year, now.month, now.day, 5, 0, 0)
            checkout_date = checkin_date + timedelta(days=1)
            return checkout_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    @api.multi
    def check_folio_customer(self, partner_id):
        folio_check = self.env['sea.folio'].search([('customer_id', '=', partner_id), ('state', '=', 'inprogress')],
                                                   limit=1)
        if folio_check:
            return folio_check.id
        else:
            return False

    @api.model
    def create(self, vals):
        # print("create order: ", vals)
        if 'order_type' in vals:
            if vals.get('order_type') in ['restaurant_order', 'hotel_order']:
                if 'sea_check_customer_for_invoice' not in vals:
                    vals['sea_check_customer_for_invoice'] = None
                # print("Sale order create start: ", vals)
                '''nếu là Language -- English thì name là New -- VN thì name sẽ là Mới'''
                if 'name' in vals:
                    if self.env.user.lang == 'vi_VN' and vals.get('name') == 'New':
                        vals['name'] = 'Mới'
                '''gán check in check out default'''
                if 'check_in' not in vals and 'check_out' not in vals and 'room_id' in vals:
                    vals['check_in'] = self.get_checkin_date()
                    vals['check_out'] = self.get_checkout_date()

                get_branch_id = self.env['sea.pos.hotel.restaurant'].search(
                    [('id', '=', vals.get('pos_hotel_restaurant_id'))])
                if get_branch_id.pos_type == 'hotel':
                    folio_id = self.check_folio_customer(vals.get('partner_id'))
                    if folio_id:
                        vals["folio_id"] = folio_id
                    else:
                        # if vals.get('folio_sequence', _('New')) == _('New'):
                        #     if 'company_id' in vals:
                        #         vals['folio_sequence'] = self.env['ir.sequence'].with_context(
                        #             force_company=vals['company_id']).next_by_code(
                        #             'seatek.folio') or _('New')
                        #     else:
                        #         vals['folio_sequence'] = self.env['ir.sequence'].next_by_code('seatek.folio') or _('New')
                        # customer_id = self.env["res.partner"].sudo().search([("id", "=", vals["partner_id"])])
                        # vals["folio_name"] = customer_id.display_name
                        # if customer_id.phone:
                        #     vals["folio_name"] += " | " + customer_id.phone
                        res = self.env['sea.folio'].sudo().create({'customer_id': vals.get('partner_id'),
                                                                   'sale_person_id': self.env.user.partner_id.id,
                                                                   'branch_id': get_branch_id.hotel_restaurant_branch_id.id,
                                                                   'company_id': vals.get('company_id'),
                                                                   'state': 'inprogress'
                                                                   })
                        vals["folio_id"] = res.id
                rec = super(SaleOrder, self).create(vals)
                # if 'room_id' in vals and rec.order_type == 'hotel_order':
                #     room = self.env['sea.hotel.room'].sudo().search([('id', '=', vals.get('room_id'))])
                #     if room:
                #         if room.product_default:
                #             self.env['sale.order.line'].sudo().create({'product_id': room.product_default.id,
                #                                                        'room_id': vals.get('room_id'),
                #                                                        'order_id': rec.id,
                #                                                        'checkin_date': self._get_checkin_date(),
                #                                                        'checkout_date': self._get_checkout_date()
                #                                                        })
                #         if room.default_amenities:
                #             for default_amenitie in room.default_amenities:
                #                 self.env['sale.order.line'].sudo().create({'product_id': default_amenitie.product_id.id,
                #                                                            'product_uom_qty': default_amenitie.quantity,
                #                                                            'room_id': vals.get('room_id'),
                #                                                            'order_id': rec.id,
                #                                                            })
                # if rec.room_id:
                #     if rec.room_id.status != 'occupied':
                #         rec.room_id.status = 'occupied'
                # else:
                #     if rec.table_id:
                #         if rec.table_id.status != 'occupied':
                #             rec.table_id.status = 'occupied'
                # if 'room_id' in vals and rec.order_type == 'hotel_order':
                #     room = self.env['sea.hotel.room'].sudo().search([('id', '=', vals.get('room_id'))])
                #     ''' tự động cộng số lượng sale.order.line khi thêm sản phẩm giống sản phẩm default '''
                #     if room:
                #         get_order_line = vals.get('order_line')
                #         if get_order_line:
                #             if room.product_default:
                #                 count = 0
                #                 product_uom_qty = 1
                #                 for product in get_order_line:
                #                     get_sale_order_line = self.env['sale.order.line'].search(
                #                         [('order_id', '=', rec.id), ('product_id', '=', product[2].get('product_id'))])
                #                     if room.product_default.id == int(product[2].get('product_id')):
                #                         count = int(product[2].get('product_id'))
                #                         get_sale_order_line.sudo().write({
                #                             'product_uom_qty': product_uom_qty + int(product[2].get('product_uom_qty')),
                #                             'checkin_date': self.get_checkin_date(),
                #                             'checkout_date': self.get_checkout_date()
                #                         })
                #                 if count == 0:
                #                     self.env['sale.order.line'].sudo().create({'product_id': room.product_default.id,
                #                                                                'room_id': vals.get('room_id'),
                #                                                                'order_id': rec.id,
                #                                                                'checkin_date': self.get_checkin_date(),
                #                                                                'checkout_date': self.get_checkout_date()
                #                                                                })
                #             if room.default_amenities:
                #                 for default_amenitie in room.default_amenities:
                #                     count_amenitie = 0
                #                     get_sale_order = self.env['sale.order.line'].search(
                #                         [('order_id', '=', rec.id), ('product_id', '=', default_amenitie.product_id.id)])
                #                     for product in get_order_line:
                #                         if default_amenitie.product_id.id == int(product[2].get('product_id')):
                #                             count_amenitie = count_amenitie + 1
                #                             get_sale_order.write({
                #                                 'product_uom_qty': int(
                #                                     product[2].get('product_uom_qty')) + default_amenitie.quantity,
                #                             })
                #                     if count_amenitie < 1:
                #                         self.env['sale.order.line'].sudo().create(
                #                             {'product_id': default_amenitie.product_id.id,
                #                              'product_uom_qty': default_amenitie.quantity,
                #                              'room_id': vals.get('room_id'),
                #                              'order_id': rec.id,
                #                              })
                #         else:
                #             if room.product_default:
                #                 self.env['sale.order.line'].sudo().create({'product_id': room.product_default.id,
                #                                                            'room_id': vals.get('room_id'),
                #                                                            'order_id': rec.id,
                #                                                            'checkin_date': self.get_checkin_date(),
                #                                                            'checkout_date': self.get_checkout_date()
                #                                                            })
                #             if room.default_amenities:
                #                 for default_amenitie in room.default_amenities:
                #                     self.env['sale.order.line'].sudo().create({'product_id': default_amenitie.product_id.id,
                #                                                                'product_uom_qty': default_amenitie.quantity,
                #                                                                'room_id': vals.get('room_id'),
                #                                                                'order_id': rec.id,
                #                                                                })
                #
                #                     ''' tự động cộng số lượng sale.order.line khi thêm sản phẩm giống sản phẩm default '''
                # print("Sale order create end: ", vals)
            else:
                rec = super(SaleOrder, self).create(vals)
        else:
            rec = super(SaleOrder, self).create(vals)
        return rec

    @api.multi
    def write(self, vals):
        # print("write order: ", vals)
        if self.order_type:
            if self.order_type in ['hotel_order', 'restaurant_order']:
                reserved_old = {}
                line_ids = []
                if 'order_line' in vals:
                    for line_values in vals['order_line']:
                        if line_values[0] != 0:
                            line_ids.append(int(line_values[1]))
                        if line_values[0] == 1:  # Kiểm tra action là update
                            reserved_old[str(line_values[1])] = self.env['sale.order.line'].browse(
                                line_values[1]).qty_reserved
                    rec = super(SaleOrder, self).write(vals)
                    for line_values in vals['order_line']:
                        if line_values[0] == 1 or line_values[0] == 0:
                            if line_values[0] == 1 and self.env['sale.order.line'].browse(
                                    line_values[1]).qty_reserved >= reserved_old.get(
                                str(line_values[1])) or line_values[0] == 0:
                                print("validate")
                                '''validate'''
                                picking_ids = self.env['stock.picking'].sudo().search(
                                    [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id),
                                     ('origin', '=', self.name)])
                                line_id = 0
                                pro_id = 0
                                if line_values[0] == 1:
                                    line_id = line_values[1]
                                    pro_id = self.env['sale.order.line'].browse(line_values[1]).product_id.id
                                else:
                                    if line_ids and self.order_line:
                                        for line in self.order_line:
                                            if line.id not in line_ids:
                                                line_id = line.id
                                                pro_id = line.product_id.id
                                                break
                                if line_id != 0 and pro_id != 0:
                                    if picking_ids:
                                        for picking in picking_ids:
                                            check = self.env['stock.move'].sudo().search(
                                                [('picking_id', '=', picking.id),
                                                 ('sale_line_id', '=', line_id),
                                                 ('product_id', '=', pro_id)])
                                            for i in check:
                                                if i.quantity_done > 0:
                                                    picking.validate_for_hotel_restaurant()
                                                    break
                            elif line_values[0] == 1 and self.env['sale.order.line'].browse(
                                    line_values[1]).qty_reserved < reserved_old.get(
                                str(line_values[1])):
                                print("return")
                                '''return'''
                                picking_ids_return = self.env['stock.picking'].sudo().search(
                                    [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id),
                                     ('origin', '!=', self.name)])
                                if picking_ids_return:
                                    upgrade = False
                                    for picking_return in picking_ids_return:
                                        check_s = self.env['stock.move'].sudo().search(
                                            [('picking_id', '=', picking_return.id),
                                             ('sale_line_id', '=', line_values[1]),
                                             ('product_id', '=',
                                              self.env['sale.order.line'].browse(line_values[1]).product_id.id)])
                                        for i in check_s:
                                            if i.quantity_done > 0:
                                                picking_return.validate_return_for_hotel_restaurant()
                                                upgrade = True
                                                break

                                    '''chú ý CHÚ Ý'''
                                    if upgrade:
                                        uom_qty = self.env['sale.order.line'].browse(line_values[1]).product_uom_qty
                                        self.env['sale.order.line'].browse(line_values[1]).write(
                                            {'product_uom_qty': uom_qty - (
                                                    reserved_old.get(str(line_values[1])) - self.env[
                                                'sale.order.line'].browse(line_values[1]).qty_reserved)})
                                        self.env['sale.order.line'].browse(line_values[1]).write(
                                            {'product_uom_qty': uom_qty})
                    # if line_ids:
                    #     '''thực hiện DONE nếu qty_reseved > 0 Không có RETURN'''
                    #     if self.order_line:
                    #         pro_ids = []
                    #         for line in self.order_line:
                    #             if line.id not in line_ids:
                    #                 if line.qty_reserved > 0:
                    #                     qty_done = line.qty_reserved
                    #                     pro_ids.append(line.product_id.id)
                    #                     stock_pickings = self.env['stock.picking'].sudo().search(
                    #                         [('sale_id', '=', line.order_id.id), ('state', 'not in', ['done', 'cancel'])])
                    #                     if stock_pickings:
                    #                         for stock_picking in stock_pickings:
                    #                             if qty_done == 0:
                    #                                 break
                    #                             stock_moves = self.env['stock.move'].sudo().search(
                    #                                 [('picking_id', '=', stock_picking.id), ('sale_line_id', '=', line.id),
                    #                                  ('product_id', '=', line.product_id.id)])
                    #                             if stock_moves:
                    #                                 for stock_move in stock_moves:
                    #                                     if qty_done == 0:
                    #                                         break
                    #                                     stock_move_lines = self.env['stock.move.line'].sudo().search(
                    #                                         [('move_id', '=', stock_move.id),
                    #                                          ('picking_id', '=', stock_picking.id),
                    #                                          ('product_id', '=', line.product_id.id)])
                    #
                    #                                     if not stock_move_lines:
                    #                                         '''tạo STOCK MOVE LINE
                    #                                         nếu không có picking_type_id.default_location_dest_id
                    #                                         thì sẽ lấy id=9'''
                    #                                         if stock_picking.picking_type_id and stock_picking.location_id:
                    #                                             location_id = stock_picking.location_id
                    #                                             if stock_picking.picking_type_id.sudo().default_location_dest_id:
                    #                                                 location_dest_id = \
                    #                                                     stock_picking.picking_type_id.sudo().default_location_dest_id.id
                    #                                             else:
                    #                                                 location_dest_id = 9
                    #
                    #                                             self.env['stock.move.line'].sudo().create(
                    #                                                 [{
                    #                                                     'picking_id': stock_picking.id,
                    #                                                     'product_id': line.product_id.id,
                    #                                                     'location_id': location_id.id,
                    #                                                     'location_dest_id': location_dest_id,
                    #                                                     'remarks': '',
                    #                                                     'qty_done': qty_done,
                    #                                                     'product_uom_id': stock_move.product_uom.id,
                    #                                                     'state': 'confirmed',
                    #                                                     'move_id': stock_move.id,
                    #                                                 }]
                    #                                             )
                    #                                     if stock_move_lines:
                    #                                         for stock_move_line in stock_move_lines:
                    #                                             if qty_done <= 0:
                    #                                                 break
                    #                                             else:
                    #                                                 qty_tang = stock_move_line.product_uom_qty - stock_move_line.qty_done
                    #                                                 if qty_done >= qty_tang:
                    #                                                     stock_move_line.qty_done += qty_tang
                    #                                                     qty_done -= qty_tang
                    #                                                 else:
                    #                                                     stock_move_line.qty_done += qty_done
                    #                                                     qty_done = 0
                    #                             '''product có lệnh sx và không có tồn kho'''
                    #                             for stock_move_sx in stock_picking.move_lines.sudo():
                    #                                 if stock_move_sx.quantity_done > 0 \
                    #                                         and stock_move_sx.created_production_id \
                    #                                         and stock_move_sx.sudo().product_id.id == line.product_id.id:
                    #                                     production_id = stock_move_sx.sudo().created_production_id
                    #                                     mrp_product_produce = self.env[
                    #                                         'mrp.product.produce'].sudo().with_context(
                    #                                         active_id=production_id.id).sudo().create(
                    #                                         {'production_id': production_id.id,
                    #                                          'product_id': line.product_id.id,
                    #                                          'product_qty': stock_move_sx.quantity_done})
                    #                                     mrp_product_produce._onchange_product_qty()
                    #                                     mrp_product_produce.do_produce()
                    #                                     production_id.post_inventory()
                    #                                     stock_move_update = self.env['stock.move'].sudo().search(
                    #                                         [('raw_material_production_id', '=', production_id.id),
                    #                                          ('state', 'not in', ['done', 'cancel'])])
                    #                                     for i in stock_move_update:
                    #                                         move_line = self.env['stock.move.line'].sudo().search(
                    #                                             [('move_id', '=', i.id),
                    #                                              ('state', 'not in', ['done', 'cancel'])])
                    #                                         for line_ in move_line:
                    #                                             if line_.product_uom_qty < 0:
                    #                                                 line_.product_uom_qty = 0
                    #
                    #         '''validate'''
                    #         picking_ids = self.env['stock.picking'].sudo().search(
                    #             [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id),
                    #              ('origin', '=', self.name)])
                    #         if picking_ids:
                    #             for picking in picking_ids:
                    #                 check = self.env['stock.move'].sudo().search(
                    #                     [('picking_id', '=', picking.id),
                    #                      ('product_id', 'in', pro_ids)])
                    #                 for i in check:
                    #                     if i.quantity_done > 0:
                    #                         picking.validate_for_hotel_restaurant()
                    #                         break
                    return rec

                '''active = False nếu folio chỉ chứa sale order này
                nếu các sale order khác là done or cancel thì sẽ done'''
                if 'folio_id' in vals:
                    for rec in self:
                        if rec.folio_id:
                            active = False
                            if rec.folio_id.sudo().order_ids:
                                list_sale_order = rec.folio_id.sudo().order_ids.filtered(
                                    lambda record: record.id != rec.id)
                                state = True
                                if list_sale_order:
                                    for i in list_sale_order:
                                        if i.state == 'done' or i.state == 'cancel':
                                            continue
                                        else:
                                            state = False
                                            break
                                    if state:
                                        rec.folio_id.sudo().state = 'done'
                                else:
                                    active = True
                            else:
                                active = True
                            if active:
                                rec.folio_id.sudo().active = False

        return super(SaleOrder, self).write(vals)

    @api.multi
    def confirm_order(self):
        # update all food item in restaurant served
        if self.order_type == "restaurant_order" and self.table_id:
            if self.table_id.status != 'occupied':
                self.table_id.write({"status": "occupied"})

        # update status of rooms is available for sale
        if self.order_type == "hotel_order" and self.room_id:
            if self.room_id.status != 'occupied':
                self.room_id.write({"status": "occupied"})
                # for line in self.order_line:
                #     if line.room_id:
                #         if line.room_id.status != 'occupied':
                #             line.room_id.write({"status": "occupied"})

        # ''' product_uom_qty = qty_reserved '''
        # for rec in self:
        #     get_sale_line = self.env['sale.order.line'].sudo().search(
        #         [('order_id', '=', rec.id)])
        #     if get_sale_line:
        #         for sale in get_sale_line:
        #             sale.qty_reserved = sale.product_uom_qty
        # confirm and unlock sale order
        self.action_confirm()
        self.action_unlock()
        '''thực hiện DONE nếu qty_reseved > 0 Không có RETURN'''
        for rec in self:
            if rec.order_line:
                pro_ids = []
                for line in rec.order_line:
                    if line.qty_reserved > 0:
                        qty_done = line.qty_reserved
                        '''code old'''
                        # pro_ids.append(line.product_id.id)
                        # stock_pickings = self.env['stock.picking'].sudo().search(
                        #     [('sale_id', '=', line.order_id.id), ('state', 'not in', ['done', 'cancel'])])
                        # if stock_pickings:
                        #     for stock_picking in stock_pickings:
                        #         if qty_done == 0:
                        #             break
                        #         stock_moves = self.env['stock.move'].sudo().search(
                        #             [('picking_id', '=', stock_picking.id), ('sale_line_id', '=', line.id),
                        #              ('product_id', '=', line.product_id.id)])
                        #         if stock_moves:
                        #             for stock_move in stock_moves:
                        #                 if qty_done == 0:
                        #                     break
                        #                 stock_move_lines = self.env['stock.move.line'].sudo().search(
                        #                     [('move_id', '=', stock_move.id),
                        #                      ('picking_id', '=', stock_picking.id),
                        #                      ('product_id', '=', line.product_id.id)])
                        #
                        #                 if not stock_move_lines:
                        #                     '''tạo STOCK MOVE LINE'''
                        #                     '''nếu không có picking_type_id.default_location_dest_id thì sẽ lấy id=9'''
                        #                     if stock_picking.picking_type_id and stock_picking.location_id:
                        #                         location_id = stock_picking.location_id
                        #                         if stock_picking.picking_type_id.sudo().default_location_dest_id:
                        #                             location_dest_id = \
                        #                                 stock_picking.picking_type_id.sudo().default_location_dest_id.id
                        #                         else:
                        #                             location_dest_id = 9
                        #
                        #                         self.env['stock.move.line'].sudo().create(
                        #                             [{
                        #                                 'picking_id': stock_picking.id,
                        #                                 'product_id': line.product_id.id,
                        #                                 'location_id': location_id.id,
                        #                                 'location_dest_id': location_dest_id,
                        #                                 'remarks': '',
                        #                                 'qty_done': qty_done,
                        #                                 'product_uom_id': stock_move.product_uom.id,
                        #                                 'state': 'confirmed',
                        #                                 'move_id': stock_move.id,
                        #                             }]
                        #                         )
                        #
                        #                 if stock_move_lines:
                        #                     length = 0
                        #                     for stock_move_line in stock_move_lines:
                        #                         length += 1
                        #                         if qty_done <= 0:
                        #                             break
                        #                         else:
                        #                             if length == len(stock_move_lines):
                        #                                 qty_tang = qty_done
                        #                             else:
                        #                                 qty_tang = (
                        #                                         stock_move_line.product_uom_qty - stock_move_line.qty_done) \
                        #                                     if stock_move_line.product_uom_qty > 0 else qty_done
                        #                             if qty_done >= qty_tang:
                        #                                 stock_move_line.qty_done += qty_tang
                        #                                 qty_done -= qty_tang
                        #                             else:
                        #                                 stock_move_line.qty_done += qty_done
                        #                                 qty_done = 0
                        #         '''product có lệnh sx và không có tồn kho'''
                        #         for stock_move_sx in stock_picking.move_lines.sudo():
                        #             if stock_move_sx.quantity_done > 0 \
                        #                     and stock_move_sx.created_production_id \
                        #                     and stock_move_sx.sudo().product_id.id == line.product_id.id:
                        #                 production_id = stock_move_sx.sudo().created_production_id
                        #                 mrp_product_produce = self.env[
                        #                     'mrp.product.produce'].sudo().with_context(
                        #                     active_id=production_id.id).sudo().create(
                        #                     {'production_id': production_id.id,
                        #                      'product_id': line.product_id.id,
                        #                      'product_qty': stock_move_sx.quantity_done})
                        #                 mrp_product_produce._onchange_product_qty()
                        #                 mrp_product_produce.do_produce()
                        #                 production_id.post_inventory()
                        #                 stock_move_update = self.env['stock.move'].sudo().search(
                        #                     [('raw_material_production_id', '=', production_id.id),
                        #                      ('state', 'not in', ['done', 'cancel'])])
                        #                 for i in stock_move_update:
                        #                     move_line = self.env['stock.move.line'].sudo().search(
                        #                         [('move_id', '=', i.id), ('state', 'not in', ['done', 'cancel'])])
                        #                     for line_ in move_line:
                        #                         if line_.product_uom_qty < 0:
                        #                             line_.product_uom_qty = 0
                        stock_pickings = self.env['stock.picking'].sudo().search(
                            [('sale_id', '=', rec.id), ('state', 'not in', ['done', 'cancel'])])
                        if stock_pickings:
                            product_list = [{'product_id': line.product_id.id,
                                             'qty': qty_done}]
                            '''thao tác với SP kit'''
                            check_kit = False
                            mrp_bom = self.env['mrp.bom'].sudo().search(
                                ['|', ('product_id', '=', line.product_id.sudo().id), '&',
                                 ('product_id', '=', False),
                                 ('product_tmpl_id', '=', line.product_id.sudo().product_tmpl_id.id)], limit=1)
                            if mrp_bom:
                                if mrp_bom.type == 'phantom':
                                    '''start'''
                                    '''lấy công thức trên một đơn vị'''
                                    if mrp_bom.sudo().bom_line_ids:
                                        product_list = []
                                        for i in mrp_bom.sudo().bom_line_ids:
                                            check_kit = True
                                            pro_ids.append(i.product_id.id)
                                            product_list.append({'product_id': i.product_id.id,
                                                                 'qty': (
                                                                                i.product_qty / mrp_bom.sudo().product_qty) * qty_done})
                            if not check_kit:
                                pro_ids.append(line.product_id.id)

                            ''''''
                            for product_id in product_list:
                                for stock_picking in stock_pickings:
                                    if product_id['qty'] == 0:
                                        break
                                    stock_moves = self.env['stock.move'].sudo().search(
                                        [('picking_id', '=', stock_picking.id), ('sale_line_id', '=', line.id),
                                         ('product_id', '=', product_id['product_id'])])
                                    production_id = False
                                    if stock_moves:
                                        for stock_move in stock_moves:
                                            if product_id['qty'] == 0:
                                                break
                                            '''lấy cho lệnh SX'''
                                            if stock_move.created_production_id and not production_id:
                                                production_id = stock_move.sudo().created_production_id
                                            ''''''
                                            stock_move_lines = self.env['stock.move.line'].sudo().search(
                                                [('move_id', '=', stock_move.id), ('picking_id', '=', stock_picking.id),
                                                 ('product_id', '=', product_id['product_id'])])
                                            if not stock_move_lines:
                                                '''tạo STOCK MOVE LINE'''
                                                '''nếu không có picking_type_id.default_location_dest_id thì sẽ lấy id=9'''
                                                if stock_picking.picking_type_id and stock_picking.location_id:
                                                    location_id = stock_picking.location_id
                                                    if stock_picking.picking_type_id.sudo().default_location_dest_id:
                                                        location_dest_id = \
                                                            stock_picking.picking_type_id.sudo().default_location_dest_id.id
                                                    else:
                                                        location_dest_id = 9
                                                    stock_move_lines = self.env['stock.move.line'].sudo().create(
                                                        [{
                                                            'picking_id': stock_picking.id,
                                                            'product_id': product_id['product_id'],
                                                            'location_id': location_id.id,
                                                            'location_dest_id': location_dest_id,
                                                            'remarks': '',
                                                            'qty_done': 0.0,
                                                            'product_uom_id': stock_move.product_uom.id,
                                                            'state': 'confirmed',
                                                            'move_id': stock_move.id,
                                                        }]
                                                    )
                                            if stock_move_lines:
                                                length = 0
                                                for stock_move_line in stock_move_lines:
                                                    length += 1
                                                    if product_id['qty'] <= 0:
                                                        break
                                                    else:
                                                        '''nếu stock_move_line.product_uom_qty = 0 thì vẫn tiếp tục done'''
                                                        if length == len(stock_move_lines):
                                                            qty_tang = product_id['qty']
                                                        else:
                                                            qty_tang = (
                                                                    stock_move_line.product_uom_qty - stock_move_line.qty_done) \
                                                                if stock_move_lines.product_uom_qty > 0 else product_id[
                                                                'qty']
                                                        if product_id['qty'] >= qty_tang:
                                                            stock_move_line.qty_done += qty_tang
                                                            sx = True
                                                            product_id['qty'] -= qty_tang
                                                        else:
                                                            stock_move_line.qty_done += product_id['qty']
                                                            sx = True
                                                            product_id['qty'] = 0
                                                        ''' Bắt đầu cho SX và not tồn kho '''
                                                        if sx and production_id:
                                                            '''chú ý CHÚ Ý'''
                                                            update_quantity_wizard = self.env[
                                                                'change.production.qty'].create({
                                                                'mo_id': production_id.id,
                                                                'product_qty': stock_move_line.qty_done + production_id.product_qty,
                                                            })
                                                            update_quantity_wizard.change_prod_qty()

                                                            mrp_product_produce = self.env[
                                                                'mrp.product.produce'].sudo().with_context(
                                                                active_id=production_id.id).sudo().create(
                                                                {'production_id': production_id.id,
                                                                 'product_id': product_id['product_id'],
                                                                 'product_qty': stock_move_line.qty_done})
                                                            mrp_product_produce._onchange_product_qty()
                                                            mrp_product_produce.do_produce()
                                                            production_id.post_inventory()

                                                            '''chú ý CHÚ Ý'''
                                                            stock_move_update = self.env['stock.move'].sudo().search(
                                                                [('raw_material_production_id', '=', production_id.id),
                                                                 ('state', 'not in', ['done', 'cancel'])])
                                                            for i in stock_move_update:
                                                                move_line = self.env['stock.move.line'].sudo().search(
                                                                    [('move_id', '=', i.id),
                                                                     ('state', 'not in', ['done', 'cancel'])])
                                                                for line_ in move_line:
                                                                    if line_.product_uom_qty < 0:
                                                                        line_.product_uom_qty = 0

                '''validate'''
                picking_ids = self.env['stock.picking'].sudo().search(
                    [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', rec.id),
                     ('origin', '=', rec.name)])
                if picking_ids:
                    for picking in picking_ids:
                        check = self.env['stock.move'].sudo().search(
                            [('picking_id', '=', picking.id),
                             ('product_id', 'in', pro_ids)])
                        for i in check:
                            if i.quantity_done > 0:
                                picking.validate_for_hotel_restaurant()
                                break
        return True

    @api.multi
    def unlock_sale_order(self):
        self.action_unlock()
        if self.table_id:
            self.table_id.status = 'occupied'
            if self.folio_id:
                self.folio_id.state = 'inprogress'
        elif self.room_id:
            self.room_id.status = 'occupied'
            if self.folio_id:
                self.folio_id.state = 'inprogress'

    @api.multi
    def cancel_stock_picking(self):
        picking_ids = self.env['stock.picking'].sudo().search(
            [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
        for picking in picking_ids:
            picking.action_cancel()

    @api.multi
    def done_or_cancel_mrp_production(self):
        mrp_ids = self.env['mrp.production'].sudo().search(
            [('origin', '=', self.name), ('state', 'not in', ['done', 'cancel'])])
        for mrp in mrp_ids:
            if mrp.finished_move_line_ids:
                '''cập nhật lại SL SX bằng với SX thực tế'''
                qty = 0.0
                for i in mrp.finished_move_line_ids:
                    if i.qty_done:
                        qty += i.qty_done
                update_quantity_wizard = self.env['change.production.qty'].sudo().create({
                    'mo_id': mrp.id,
                    'product_qty': qty,
                })
                update_quantity_wizard.change_prod_qty()
                mrp.button_mark_done()
            else:
                mrp.action_cancel()

    @api.multi
    def done_or_move_folio(self):
        for rec in self:
            if rec.folio_id:
                check_done_folio = rec.folio_id.sudo().order_ids.filtered(
                    lambda record: record.state not in ['done', 'cancel'])
                if not check_done_folio:
                    rec.folio_id.state = 'done'
                else:
                    '''xóa SO khỏi folio nếu có'''
                    rec.folio_id = False

    @api.multi
    def change_partner(self):
        picking_ids = self.env['stock.picking'].sudo().search(
            [('sale_id', '=', self.id)])
        for picking in picking_ids:
            if picking.sudo().partner_id:
                if picking.sudo().partner_id.id != self.partner_id.id:
                    picking.sudo().partner_id = self.partner_id.id
            else:
                picking.sudo().partner_id = self.partner_id.id

    @api.multi
    def lock_restaurant_order(self, state_folio=False):
        # print('lock_restaurant_order: ', state_folio)
        if self.state != 'sale_folio' and self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
            pro_ids = []
            for line in self.order_line:
                ''' product_uom_qty = qty_reserved '''
                if line.qty_reserved != line.product_uom_qty:
                    line.write({
                        'qty_reserved': line.product_uom_qty
                    })
                    pro_ids.append(line.product_id.id)
            '''validate'''
            picking_ids = self.env['stock.picking'].sudo().search(
                [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
            if picking_ids:
                for picking in picking_ids:
                    check = self.env['stock.move'].sudo().search(
                        [('picking_id', '=', picking.id),
                         ('product_id', 'in', pro_ids)])
                    for i in check:
                        if i.quantity_done > 0:
                            picking.validate_for_hotel_restaurant()
                            break
        check = True
        if self.order_type == "restaurant_order" and self.order_line:
            for line in self.order_line:
                if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
                    '''cập nhật lại product_uom_qty = qty_delivered'''
                    line.product_uom_qty = line.qty_delivered
                    if line.qty_reserved != line.qty_delivered:
                        check = False
                else:
                    line.product_uom_qty = line.qty_reserved

            if self.table_id:
                self.table_id.status = 'available'
        self.action_done()
        if self.order_type == "restaurant_order" and not check and self.order_line:
            for line in self.order_line:
                if line.qty_reserved != line.qty_delivered \
                        and line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
                    '''cập nhật lại qty_reserved = qty_delivered'''
                    line.qty_reserved = line.qty_delivered

        if state_folio:
            if 'state_folio' in state_folio:
                if not state_folio.get('state_folio'):
                    self.done_or_move_folio()
        else:
            self.done_or_move_folio()
        self.change_partner()
        self.done_or_cancel_mrp_production()
        self.cancel_stock_picking()

    @api.multi
    def lock_hotel_order(self, state_folio=False):
        # print('lock_hotel_order: ', state_folio)
        if self.state != 'sale_folio' and self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
            pro_ids = []
            for line in self.order_line:
                ''' product_uom_qty = qty_reserved '''
                line.write({
                    'qty_reserved': line.product_uom_qty
                })
                pro_ids.append(line.product_id.id)
            '''validate'''
            picking_ids = self.env['stock.picking'].sudo().search(
                [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
            if picking_ids:
                for picking in picking_ids:
                    check = self.env['stock.move'].sudo().search(
                        [('picking_id', '=', picking.id),
                         ('product_id', 'in', pro_ids)])
                    for i in check:
                        if i.quantity_done > 0:
                            picking.validate_for_hotel_restaurant()
                            break
        check = True
        if self.order_type == "hotel_order" and self.order_line:
            for line in self.order_line:
                if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
                    '''cập nhật lại product_uom_qty = qty_delivered'''
                    line.product_uom_qty = line.qty_delivered
                    if line.qty_reserved != line.qty_delivered:
                        check = False
                else:
                    line.product_uom_qty = line.qty_reserved
            if self.room_id:
                self.room_id.status = 'cleaned'
        self.action_done()
        if self.order_type == "hotel_order" and self.order_line and not check:
            for line in self.order_line:
                if line.qty_reserved != line.qty_delivered \
                        and line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
                    '''cập nhật lại qty_reserved = qty_delivered'''
                    line.qty_reserved = line.qty_delivered

        if state_folio:
            if 'state_folio' in state_folio:
                if not state_folio.get('state_folio'):
                    self.done_or_move_folio()
        else:
            self.done_or_move_folio()
        self.change_partner()
        self.done_or_cancel_mrp_production()
        self.cancel_stock_picking()

    @api.multi
    def lock_to_folio_restaurant_order(self):
        # if self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
        #     pro_ids = []
        #     for line in self.order_line:
        #         ''' product_uom_qty = qty_reserved '''
        #         line.write({
        #             'qty_reserved': line.product_uom_qty
        #         })
        #         pro_ids.append(line.product_id.id)
        #     '''validate'''
        #     picking_ids = self.env['stock.picking'].sudo().search(
        #         [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
        #     if picking_ids:
        #         for picking in picking_ids:
        #             check = self.env['stock.move'].sudo().search(
        #                 [('picking_id', '=', picking.id),
        #                  ('product_id', 'in', pro_ids)])
        #             for i in check:
        #                 if i.quantity_done > 0:
        #                     picking.validate_for_hotel_restaurant()
        #                     break
        # check = True
        # if self.order_type == "restaurant_order":
        #     if self.order_line:
        #         for line in self.order_line:
        #             # check_service = self.env['product.product'].sudo().search(
        #             #     [('id', '=', line.product_id.id)])
        #             if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
        #                 '''cập nhật lại product_uom_qty = qty_delivered'''
        #                 line.product_uom_qty = line.qty_delivered
        #                 if line.qty_reserved != line.qty_delivered:
        #                     check = False
        #             else:
        #                 line.product_uom_qty = line.qty_reserved
        #
        #     if self.table_id:
        #         self.table_id.status = 'available'
        # self.action_done()
        # if not check and self.order_type == "restaurant_order" and self.order_line:
        #     for line in self.order_line:
        #         if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
        #             '''cập nhật lại qty_reserved = qty_delivered'''
        #             line.qty_reserved = line.qty_delivered
        # self.cancel_stock_picking()
        if self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
            pro_ids = []
            for line in self.order_line:
                ''' product_uom_qty = qty_reserved '''
                line.write({
                    'qty_reserved': line.product_uom_qty
                })
                pro_ids.append(line.product_id.id)
            '''validate'''
            picking_ids = self.env['stock.picking'].sudo().search(
                [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
            if picking_ids:
                for picking in picking_ids:
                    check = self.env['stock.move'].sudo().search(
                        [('picking_id', '=', picking.id),
                         ('product_id', 'in', pro_ids)])
                    for i in check:
                        if i.quantity_done > 0:
                            picking.validate_for_hotel_restaurant()
                            break

        if self.table_id:
            self.table_id.status = 'available'
        self.state = 'sale_folio'

    @api.multi
    def lock_to_folio_hotel_order(self):
        # if self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
        #     pro_ids = []
        #     for line in self.order_line:
        #         ''' product_uom_qty = qty_reserved '''
        #         line.write({
        #             'qty_reserved': line.product_uom_qty
        #         })
        #         pro_ids.append(line.product_id.id)
        #     '''validate'''
        #     picking_ids = self.env['stock.picking'].sudo().search(
        #         [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id),
        #          ('origin', '=', self.name)])
        #     if picking_ids:
        #         for picking in picking_ids:
        #             check = self.env['stock.move'].sudo().search(
        #                 [('picking_id', '=', picking.id),
        #                  ('product_id', 'in', pro_ids)])
        #             for i in check:
        #                 if i.quantity_done > 0:
        #                     picking.validate_for_hotel_restaurant()
        #                     break
        # check = True
        # if self.order_type == "hotel_order":
        #     if self.order_line:
        #         for line in self.order_line:
        #             # check_service = self.env['product.product'].sudo().search(
        #             #     [('id', '=', line.product_id.id)])
        #             if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
        #                 '''cập nhật lại product_uom_qty = qty_delivered'''
        #                 line.product_uom_qty = line.qty_delivered
        #                 if line.qty_reserved != line.qty_delivered:
        #                     check = False
        #             else:
        #                 line.product_uom_qty = line.qty_reserved
        #     if self.room_id:
        #         self.room_id.status = 'cleaned'
        # self.action_done()
        # if self.order_type == "hotel_order" and not check and self.order_line:
        #     for line in self.order_line:
        #         if line.product_id.sudo().product_tmpl_id.sudo().type != 'service':
        #             '''cập nhật lại qty_reserved = qty_delivered'''
        #             line.qty_reserved = line.qty_delivered
        # self.cancel_stock_picking()
        if self.order_line and self.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().done_invisible:
            pro_ids = []
            for line in self.order_line:
                ''' product_uom_qty = qty_reserved '''
                line.write({
                    'qty_reserved': line.product_uom_qty
                })
                pro_ids.append(line.product_id.id)
            '''validate'''
            picking_ids = self.env['stock.picking'].sudo().search(
                [('state', 'not in', ['done', 'cancel']), ('sale_id', '=', self.id)])
            if picking_ids:
                for picking in picking_ids:
                    check = self.env['stock.move'].sudo().search(
                        [('picking_id', '=', picking.id),
                         ('product_id', 'in', pro_ids)])
                    for i in check:
                        if i.quantity_done > 0:
                            picking.validate_for_hotel_restaurant()
                            break

        if self.room_id:
            self.room_id.status = 'cleaned'
        self.state = 'sale_folio'

    @api.multi
    def cleaned_room(self):
        if self.room_id:
            self.room_id.status = 'available'

    @api.multi
    def action_open_folio_view(self):
        # if self.folio_id_hotel:
        #     folio = self.folio_id_hotel
        # elif self.folio_id_restaurant:
        #     folio = self.folio_id_restaurant
        if self.folio_id:
            return {
                'name': _(self.folio_id.folio_name),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sea.folio',
                'view_id': self.env.ref('sea_hotel_restaurant.view_hotel_folio_form').id,
                'type': 'ir.actions.act_window',
                'res_id': self.folio_id.id,
                'target': 'current',
            }
        else:
            return True

    @api.multi
    def pool_table(self):
        context = dict(self._context)
        context.update({'order_id_parent': self.table_id.id,
                        'company_id': self.company_id.id,
                        'pos_hotel_restaurant': self.pos_hotel_restaurant_id.id})
        view = self.env.ref('sea_hotel_restaurant.view_table_virtual_form')
        return {
            'name': 'Chọn bàn để gộp',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'table.virtual',
            'view_id': view.id,
            'context': context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def move_table(self):
        context = dict(self._context)
        context.update({'move_order_id_parent': self.table_id.id,
                        'company_id': self.company_id.id,
                        'pos_hotel_restaurant': self.pos_hotel_restaurant_id.id})
        view = self.env.ref('sea_hotel_restaurant.view_move_table_virtual_form')
        return {
            'name': 'Chọn bàn để chuyển',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'table.virtual.many2one',
            'view_id': view.id,
            'context': context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def move_room(self):
        context = dict(self._context)
        context.update({'room_id_parent': self.room_id.id,
                        'company_id': self.company_id.id,
                        'pos_hotel_restaurant': self.pos_hotel_restaurant_id.id})
        view = self.env.ref('sea_hotel_restaurant.view_move_room_virtual_form')
        return {
            'name': 'Chọn phòng để chuyển',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'table.virtual.many2one',
            'view_id': view.id,
            'context': context,
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def invoice_create_and_validate_hotel_restaurant(self, payment_id=False):
        '''tạo invoice'''
        '''kiểm tra trước khi tạo'''
        validate = True
        if self.invoice_ids.sudo().filtered(
                lambda record: record.state in ['open']):
            list_invoice = self.invoice_ids.sudo().filtered(
                lambda record: record.state in ['open']).ids
            validate = False
        else:
            list_invoice = self.env['sale.order'].browse([self.id]).action_invoice_create()

        '''Thay đổi:
            + journal_id lấy invoice_journal_id trong POS, branch(branch giành cho folio hoặc khi POS không có)
            nếu đúng thì account_id, origin, partner_id, partner_shipping_id,user_id đều không cần đổi
            + account_id lấy trong res_partner (property_account_recievable_id) (không lấy partner có trường này null)
            + origin lấy từ SO (lấy tất cả các tên của SO. Cách nhau bằng ",")
            + partner_id và partner_shipping_id (lấy từ SO đẩy qua invoice)
            + user_id (từ salesperson trong SO, và salesperson trong folio)
        '''
        for rec in self:
            '''lấy journal_id'''
            journal_ids = []
            if payment_id:
                if 'account_payment_id' in payment_id:
                    journals = payment_id.get('account_payment_id').split(',')
                    for j in journals:
                        value = j.split(':')
                        if value and len(value) == 2:
                            journal_ids.append({'id': value[0], 'value': value[1]})

            '''nếu không có thì chỉ validate => phương thức Ghi Nợ'''
            # if len(journal_ids) == 0:
            #     if rec.pos_hotel_restaurant_id:
            #         if rec.pos_hotel_restaurant_id.sudo().payment_journal_ids:
            #             for i in rec.pos_hotel_restaurant_id.sudo().payment_journal_ids:
            #                 journal_ids.append({'id': i.id, 'value': False})
            #                 break
            #         else:
            #             if rec.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().payment_journal_ids:
            #                 for j in rec.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().payment_journal_ids:
            #                     journal_ids.append({'id': j.id, 'value': False})
            #                     break
            print("journal_id: ", journal_ids)

            for invoice in self.env['account.invoice'].sudo().search([('id', 'in', list_invoice)]):
                if rec.pos_hotel_restaurant_id:
                    if rec.pos_hotel_restaurant_id.sudo().invoice_journal_id:
                        if rec.pos_hotel_restaurant_id.sudo().invoice_journal_id.id != invoice.journal_id.id:
                            invoice.journal_id = rec.pos_hotel_restaurant_id.sudo().invoice_journal_id.id
                    else:
                        if rec.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().invoice_journal_id.id != invoice.journal_id.id:
                            invoice.journal_id = rec.pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().invoice_journal_id.id

                '''validate'''
                if validate:
                    self.env['account.invoice'].browse([invoice.id]).action_invoice_open()

                '''Register Payment'''
                '''account.payment 
                create: {
                    'partner_id': 8912, 'amount': 1100000, 'journal_id': 34, 
                    'currency_id': 23, 'payment_date': '2023-07-22', 'communication': 'INV/2023/230949/89', 
                    data default
                    'payment_type': 'inbound', 'partner_type': 'customer', 
                    'payment_difference_handling': 'open', 'writeoff_label': 'Write-Off', 
                    'payment_method_id': 1}'''
                if journal_ids and len(journal_ids) > 0:
                    for journal in journal_ids:
                        account_payment = {
                            'invoice_ids': [[6, False, [invoice.id]]],
                            'journal_id': journal['id'],
                            'amount': journal['value'] if journal['value'] else invoice.amount_total,
                            'currency_id': invoice.currency_id.id,
                            'partner_id': invoice.partner_id.id,
                            'payment_date': datetime.now().strftime("%Y-%m-%d"),
                            'communication': invoice.reference,
                            'payment_type': 'inbound',
                            'partner_type': 'customer',
                            'payment_difference_handling': 'open',
                            'writeoff_label': 'Write-Off',
                            'payment_method_id': 1
                        }
                        res = self.env['account.payment'].sudo().create(account_payment)
                        self.env['account.payment'].browse([res.id]).action_validate_invoice_payment()

    @api.multi
    def get_payments(self):
        value = []
        for rec in self:
            if rec.invoice_ids.sudo().filtered(
                    lambda record: record.state in ['open']):
                value.append(0)
            else:
                for invoice in rec.invoice_ids.sudo().filtered(
                        lambda record: record.state in ['paid']):
                    for move in invoice.sudo().payment_move_line_ids:
                        value.append(move.sudo().journal_id.sudo().id)
        return value

    @api.multi
    @api.constrains('surcharge_type', 'surcharge')
    def get_surcharge(self):
        for rec in self:
            if rec.surcharge_type and rec.surcharge:
                default_code = rec.sudo().pos_hotel_restaurant_id.sudo().hotel_restaurant_branch_id.sudo().default_code_surcharge
                if default_code:
                    pro = self.env["product.product"].sudo().search([('default_code', '=', default_code)])
                if pro:
                    line = rec.sudo().order_line.filtered(
                        lambda record: record.product_id.id == pro.id)
                    if line:
                        if rec.surcharge > 0:
                            if rec.surcharge_type == 'fixed':
                                price_unit = rec.surcharge
                            else:
                                price_unit = rec.amount_total * (rec.surcharge / 100)
                            line[0].sudo().write(
                                {'discount': 0, 'price_unit': price_unit, 'product_uom_qty': 1, 'qty_reserved': 1})
                    elif rec.surcharge_type and rec.surcharge:
                        if rec.surcharge > 0:
                            if rec.surcharge_type == 'fixed':
                                price_unit = rec.surcharge
                            else:
                                price_unit = rec.amount_total * (rec.surcharge / 100)
                            self.env['sale.order.line'].sudo().create({'product_id': pro.id,
                                                                       'product_uom_qty': 1,
                                                                       'order_id': rec.id,
                                                                       'qty_reserved': 1,
                                                                       'discount': 0,
                                                                       'price_unit': price_unit
                                                                       })

    @api.multi
    def edit_line(self, vals):
        self.write({'order_line': vals})
        return True

    @api.multi
    def action_cancel_hotel_restaurant(self):
        try:
            for rec in self:
                res = rec.action_cancel()
                if res:
                    if rec.room_id:
                        rec.room_id.status = 'available'
                    elif rec.table_id:
                        rec.table_id.status = 'available'
                    '''xử lí folio'''
                    if rec.folio_id:
                        if not rec.folio_id.sudo().order_ids.filtered(
                                lambda record: record.state not in ['cancel']):
                            rec.folio_id.state = 'cancel'
                        else:
                            '''xóa SO khỏi folio nếu có'''
                            rec.folio_id = False

                    '''cần cancel luôn cả lệnh SX'''
                    '''lấy DS mrp.production theo origin'''
                    mrp_productions = self.env['mrp.production'].sudo().search(
                        [('origin', '=', rec.name),
                         ('state', 'not in', ['done', 'cancel'])])
                    if mrp_productions:
                        for mrp_pro in mrp_productions:
                            mrp_pro.sudo().action_cancel()
                    return res
        except Exception as e:
            # Ghi log vào tệp tin odoo.log khi có ngoại lệ
            logging.exception("\n\nException Hotel & Restaurant: %s\n\n", str(e))
        return False


class TableVirtual(models.TransientModel):
    _name = 'table.virtual'
    _description = 'Table Virtual To Test'

    table_id_pool = fields.Many2many('sea.restaurant.table', required=True, string='Table Will Merge')
    order_id_parent = fields.Many2one('sea.restaurant.table', required=True, string="Table ID Origin",
                                      default=lambda self: self._context.get('order_id_parent'))
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self._context.get('company_id'))
    pos_hotel_restaurant_id = fields.Many2one('sea.pos.hotel.restaurant', string='Point of Sale', require=True,
                                              default=lambda self: self._context.get('pos_hotel_restaurant'))

    @api.model
    def create(self, vals):
        # print('vals table.virtual', vals)
        record = super(TableVirtual, self).create(vals)
        order_id_parent = self.env["sale.order"].sudo().search(
            [('table_id', '=', record.order_id_parent.id), ('state', 'in', ['sale'])], limit=1)
        '''Kiem tra xem neu nhu gop ban co partner_id khac nhau thi bao loi'''
        reference_partner_id = order_id_parent.partner_id.id
        for table_id_children in vals.get('table_id_pool')[0][2]:
            if table_id_children:
                check_partner_id = self.env["sale.order"].sudo().search([
                    ('table_id', '=', table_id_children),
                    ('state', 'in', ['sale'])
                ], limit=1)
                if reference_partner_id == False or check_partner_id.partner_id.id == False:
                    raise UserError(_('Empty Tables Cannot Be Combined'))

        ''' Lay children '''
        for table_id_children in vals.get('table_id_pool')[0][2]:
            if table_id_children:
                order_id_children = self.env["sale.order"].sudo().search(
                    [('table_id', '=', table_id_children), ('state', 'in', ['sale'])], limit=1)
                order_id_children_line = self.env["sale.order.line"].sudo().search(
                    [('order_id', '=', order_id_children.id)])
                for order_line in order_id_children_line:
                    change_origin_stock_move = self.env["stock.move"].sudo().search(
                        [('sale_line_id', '=', order_line.id)])
                    origin_old_to_get_rpm_production = False
                    change_sale_id_picking = self.env["stock.picking"].sudo().search(
                        [('sale_id', '=', order_id_children.id)])
                    for picking_change in change_sale_id_picking:
                        picking_change.write({'sale_id': order_id_parent.id,
                                              'origin': order_id_parent.name
                                              })
                    for stock_move in change_origin_stock_move:
                        origin_old_to_get_rpm_production = stock_move.origin
                        stock_move.write({'origin': order_id_parent.name})

                    if origin_old_to_get_rpm_production != False:

                        change_origin_mrp_production = self.env["mrp.production"].sudo().search(
                            [('origin', '=', origin_old_to_get_rpm_production)])

                        if change_origin_mrp_production:
                            for mrp_production in change_origin_mrp_production:
                                mrp_production.write({'origin': order_id_parent.name})

                    order_line.write({'order_id': order_id_parent.id})
                order_id_parent.write(
                    {'amount_untaxed': order_id_parent.amount_untaxed + order_id_children.amount_untaxed,
                     'amount_tax': order_id_parent.amount_tax + order_id_children.amount_tax,
                     'amount_total': (order_id_parent.amount_untaxed + order_id_children.amount_untaxed)
                                     + (order_id_parent.amount_tax + order_id_children.amount_tax)
                     })

                vals["order_id_children"] = order_id_children.id
                order_id_children.write({'state': 'cancel'})
                return_availeble_table = self.env["sea.restaurant.table"].sudo().search(
                    [('id', '=', table_id_children)])
                return_availeble_table.write({'status': 'available'})
        return record


class TableVirtualMany2one(models.TransientModel):
    _name = 'table.virtual.many2one'
    _description = 'Table Virtual Many2one To Test'

    table_id_pool = fields.Many2one('sea.restaurant.table', string='Table Will Merge')
    order_id_parent = fields.Many2one('sea.restaurant.table', string="Table ID Origin", readonly=True,
                                      default=lambda self: self._context.get('move_order_id_parent'))
    order_line = fields.Many2many('sale.order.line', string='List Of Dishes', domain="[]")
    room_id = fields.Many2one('sea.hotel.room', string='Room Will Merge')
    room_id_parent = fields.Many2one('sea.hotel.room', string="Room ID Origin", readonly=True,
                                     default=lambda self: self._context.get('room_id_parent'))
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self._context.get('company_id'))
    pos_hotel_restaurant_id = fields.Many2one('sea.pos.hotel.restaurant', string='Point of Sale', require=True,
                                              default=lambda self: self._context.get('pos_hotel_restaurant'))

    @api.model
    def create(self, vals):
        record = super(TableVirtualMany2one, self).create(vals)
        if record.room_id:
            order_id_parent = self.env["sale.order"].sudo().search(
                [('room_id', '=', record.room_id_parent.id), ('state', 'in', ['sale'])], limit=1)
            order_id_parent.write({'room_id': record.room_id.id})
            room = self.env['sea.hotel.room'].sudo().search([('id', '=', record.room_id.id)])
            if room:
                if room.product_default:
                    self.env['sale.order.line'].sudo().create({'product_id': room.product_default.id,
                                                               'room_id': vals.get('room_id'),
                                                               'order_id': order_id_parent.id,
                                                               # 'checkin_date': order_id_parent.get_checkin_date(),
                                                               # 'checkout_date': order_id_parent.get_checkout_date()
                                                               })
                if room.default_amenities:
                    for default_amenitie in room.default_amenities:
                        self.env['sale.order.line'].sudo().create({'product_id': default_amenitie.product_id.id,
                                                                   'product_uom_qty': default_amenitie.quantity,
                                                                   'room_id': vals.get('room_id'),
                                                                   'order_id': order_id_parent.id,
                                                                   })

            return_occupied_room = self.env["sea.hotel.room"].sudo().search(
                [('id', '=', record.room_id.id)])
            return_occupied_room.write({'status': 'occupied'})
            return_availeble_room = self.env["sea.hotel.room"].sudo().search(
                [('id', '=', record.room_id_parent.id)])
            return_availeble_room.write({'status': 'available'})

        elif record.order_id_parent:
            order_id_parent = self.env["sale.order"].sudo().search(
                [('table_id', '=', record.order_id_parent.id), ('state', 'in', ['sale'])], limit=1)
            order_id_parent.write({'table_id': vals.get('table_id_pool')})
            return_occupied_table = self.env["sea.restaurant.table"].sudo().search(
                [('id', '=', record.table_id_pool.id)])
            return_occupied_table.write({'status': 'occupied'})
            return_availeble_table = self.env["sea.restaurant.table"].sudo().search(
                [('id', '=', record.order_id_parent.id)])
            return_availeble_table.write({'status': 'available'})

        return record


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create(self, vals):
        if 'company_ids' not in vals and 'company_id' in vals:
            vals['company_ids'] = [[6, False, [vals.get('company_id')]]]

        return super(ResPartner, self).create(vals)
