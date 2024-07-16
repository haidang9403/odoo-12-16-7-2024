from odoo import models, fields, _, api
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_consolidation_id = fields.Many2one('invoice.consolidation', 'Invoice Consolidation')
    get_choose_to_invoice_consolidation = fields.Char('Invoice',
                                                      compute='_get_sea_view_choose_to_invoice_consolidation')
    sea_view_choose_to_invoice_consolidation = fields.Char('Invoice', related='get_choose_to_invoice_consolidation',
                                                           readonly=True, copy=False)
    sea_consolidation_state = fields.Selection([
        ('not', 'Not'),
        ('merged', 'Merged'),
        ('split', 'Split')
    ], string='Merged Status', copy=False, index=True, required=True, default='not', readonly=True,
        track_visibility='onchange')
    sea_bill_pos = fields.Char('Bill Pos')
    sea_customer_po_name = fields.Char('Customer Name')
    sea_customer_po_code = fields.Char('PO Code')

    # @api.one
    # @api.depends('pos_order_id')
    # def _get_bill_pos_order(self):
    #     print('###########################################')
    #     for re in self:
    #         if re.pos_order_id:
    #             re.sea_bill_pos = re.pos_order_id.pos_reference

    def _get_sea_view_choose_to_invoice_consolidation(self):
        for r in self:
            if r.sea_check_customer_for_invoice:
                r.get_choose_to_invoice_consolidation = 'No INV'
            else:
                r.get_choose_to_invoice_consolidation = 'Invoice'

    def push_invoice_to_issue(self):
        self = self.sorted('date_invoice')
        for r in reversed(self):
            if r.sea_view_choose_to_invoice_consolidation != 'No INV'\
                    or r.sea_view_choose_to_invoice_consolidation == 'No INV' and r.team_id.name == 'TMĐT':
                if r.sea_consolidation_state == 'not' and r.number:
                    adj_status = r.state
                    original_consolidation = r.origin
                    bill_pos = ''
                    if r.pos_order_id:
                        bill_pos = r.pos_order_id.pos_reference
                    if r.type == 'out_refund':
                        if r.reconciled:
                            obj_search = r.env['account.invoice'].search([('number', '=', r.origin)])
                            check_cancel = r.env['account.invoice'].search([('origin', '=', obj_search.origin)])
                            if len(check_cancel) > 1:
                                for i in r.invoice_line_ids:
                                    if i.quantity == 0:
                                        adj_status = 'adjustment'
                                    else:
                                        adj_status = 'cancelled'
                            else:
                                if r.amount_total_signed == 0:
                                    adj_status = 'adjustment'
                                else:
                                    adj_status = 'cancel'
                        else:
                            if r.pos_order_id:
                                pos_order = self.env['pos.order'].search([('name', '=', r.origin)])
                                pos_order_return = self.env['pos.order'].search(
                                    [('name', '=', pos_order.return_order_id.name)])
                                if pos_order:
                                    original_consolidation = pos_order.return_order_id.name
                                    if abs(pos_order.amount_total) == abs(pos_order_return.amount_total):
                                        adj_status = 'cancel'
                                    else:
                                        adj_status = 'adjustment'
                            else:
                                credit_type = r.env['account.invoice'].search([('origin', '=', r.origin)])
                                if len(credit_type) > 1:
                                    check_status = []
                                    for i in credit_type:
                                        check_status.append(i.amount_total)
                                    if len(set(check_status)) > 1:
                                        adj_status = 'adjustment'
                                    else:
                                        adj_status = 'cancel'
                                else:
                                    if credit_type:
                                        for line in credit_type.invoice_line_ids:
                                            if line.product_id.name == "Chiết khấu thương mại":
                                                adj_status = 'open'
                                            else:
                                                adj_status = 'adjustment'
                    else:
                        check_replace = r.env['account.invoice'].search([('reference', '=', r.reference)])
                        if check_replace:
                            index = r.reference.rfind('/')
                            re_number = r.reference[0:index]
                            if re_number == r.number:
                                adj_status = 'open'
                            else:
                                if r.pos_order_id:
                                    adj_status = 'open'
                                else:
                                    adj_status = 'replacement'

                    order = self.env['sale.order'].search([('name', '=', self.origin)])
                    channel_id = ''
                    if order:
                        channel_id = order.sea_sale_channel_id.id

                    invoice_id = self.env['invoice.consolidation'].create({
                        'partner_id': r.get_customer_name(),
                        'address': r.get_customer_address(),
                        'vat_number': r.get_customer_vat(),
                        'email': r.get_email_invoice(),
                        'origin': r.number,
                        'currency_id': r.currency_id.id,
                        'amount_untaxed': r.amount_untaxed_signed,
                        'amount_tax': r.amount_tax_signed,
                        'amount_total': r.amount_total_signed,
                        'state': adj_status,
                        'original': original_consolidation,
                        'bill_pos': bill_pos,
                        'customer_po_name': r.sea_customer_po_name,
                        'customer_po_code': r.sea_customer_po_code,
                        'team_id': r.team_id.id,
                        'sale_channel_id': channel_id
                    })
                    self.invoice_consolidation_id = invoice_id

                    product_id_with_price = []
                    product_id_no_price = []
                    product_id_drink_with_price = []
                    product_id_drink_no_price = []
                    product_id_adjustment_invoice_info = []

                    product_drinks = self.env['product.product'].search([('name', '=', 'Thức uống')])
                    # adjustment_invoice_info = self.env['product.product'].search([('name', '=', 'Điều chỉnh thông tin')])
                    for line in r.invoice_line_ids:
                        if line.product_id.sea_pos_check_drinks and line.price_total != 0:
                            product_id_drink_with_price.append(line.product_id.id)
                        if line.product_id.sea_pos_check_drinks and line.price_total == 0:
                            product_id_drink_no_price.append(line.product_id.id)
                        if not line.product_id.sea_pos_check_drinks and line.price_total != 0:
                            product_id_with_price.append(line.product_id.id)
                        if not line.product_id.sea_pos_check_drinks and line.price_total == 0 and line.quantity != 0:
                            product_id_no_price.append(line.product_id.id)
                        if line.product_id.name == 'Điều chỉnh thông tin' and line.quantity == 0:
                            product_id_adjustment_invoice_info.append(line.product_id.id)

                    if product_id_adjustment_invoice_info:
                        for obj in self.env['product.product'].browse(list(set(product_id_adjustment_invoice_info))):
                            tax_id = 0
                            for line in r.invoice_line_ids:
                                tax_id = line.invoice_line_tax_ids.id
                            self.env['invoice.line.consolidation'].create({
                                'invoice_id': invoice_id.id,
                                'product_id': obj.id,
                                'description': line.name,
                                'quantity': 0,
                                'tax_id': tax_id,
                            })
                    if product_id_with_price:
                        for obj in self.env['product.product'].browse(list(set(product_id_with_price))):
                            quantity_with_price = 0
                            price_subtotal_with_price = 0
                            price_total_with_price = 0
                            uom_id = 0
                            tax_id = 0
                            check_adjustment_with_price = 0
                            for line in r.invoice_line_ids:
                                if line.product_id.id == obj.id and line.price_total != 0:
                                    quantity_with_price += line.quantity
                                    price_subtotal_with_price += line.price_subtotal
                                    price_total_with_price += line.price_total
                                    if obj.sea_unit_of_measure.id:
                                        uom_id = obj.sea_unit_of_measure.id
                                    else:
                                        raise UserError(
                                            _('%s, has not set units yet.!') % (obj.display_name))
                                    tax_id = line.invoice_line_tax_ids.id
                                    check_adjustment_with_price += line.price_subtotal_signed
                            price_unit_with_price = price_total_with_price / quantity_with_price
                            price_tax_with_price = price_total_with_price - price_subtotal_with_price

                            # if not r.reconciled and r.type == 'out_refund':
                            if adj_status == 'adjustment':
                                if obj.name == 'Chiết khấu thương mại':
                                    item_name = obj.name
                                else:
                                    item_name = 'Điều chỉnh giảm số lượng, '
                                    if price_tax_with_price == 0:
                                        item_name += 'Thành tiền mặt hàng ' + obj.name
                                    else:
                                        item_name += 'Tiền thuế, Thành tiền mặt hàng ' + obj.name
                                self.env['invoice.line.consolidation'].create({
                                    'invoice_id': invoice_id.id,
                                    'product_id': obj.id,
                                    'description': item_name,
                                    'quantity': -quantity_with_price,
                                    'uom_id': uom_id,
                                    'price_unit': price_unit_with_price,
                                    'tax_id': tax_id,
                                    'price_subtotal': -price_subtotal_with_price,
                                    'price_tax': -price_tax_with_price,
                                    'price_total': -price_total_with_price,
                                })
                            # elif r.reconciled and r.type == 'out_refund':
                            elif adj_status == 'cancel' or adj_status == 'cancelled':
                                self.env['invoice.line.consolidation'].create({
                                    'invoice_id': invoice_id.id,
                                    'product_id': obj.id,
                                    'description': obj.name,
                                    'quantity': -quantity_with_price,
                                    'uom_id': uom_id,
                                    'price_unit': price_unit_with_price,
                                    'tax_id': tax_id,
                                    'price_subtotal': -price_subtotal_with_price,
                                    'price_tax': -price_tax_with_price,
                                    'price_total': -price_total_with_price,
                                })
                            else:
                                if obj.name == 'Chiết khấu thương mại':
                                    quantity_dis = -quantity_with_price
                                    price_subtotal_dis = -price_subtotal_with_price
                                    price_tax_dis = -price_tax_with_price
                                    price_total_dis = -price_total_with_price
                                else:
                                    quantity_dis = quantity_with_price
                                    price_subtotal_dis = price_subtotal_with_price
                                    price_tax_dis = price_tax_with_price
                                    price_total_dis = price_total_with_price
                                self.env['invoice.line.consolidation'].create({
                                    'invoice_id': invoice_id.id,
                                    'product_id': obj.id,
                                    'description': obj.name,
                                    'quantity': quantity_dis,
                                    'uom_id': uom_id,
                                    'price_unit': price_unit_with_price,
                                    'tax_id': tax_id,
                                    'price_subtotal': price_subtotal_dis,
                                    'price_tax': price_tax_dis,
                                    'price_total': price_total_dis,
                                })

                    if product_id_drink_with_price:
                        for obj in self.env['product.product'].browse(product_drinks.id):
                            quantity_drink_with_price = 0
                            price_subtotal_drink_with_price = 0
                            price_total_drink_with_price = 0
                            uom_id = 0
                            tax_id = 0
                            check_adjustment_drink_with_price = 0
                            for line in r.invoice_line_ids:
                                if line.product_id.sea_pos_check_drinks and line.price_total != 0:
                                    quantity_drink_with_price += line.quantity
                                    price_subtotal_drink_with_price += line.price_subtotal
                                    price_total_drink_with_price += line.price_total
                                    if obj.sea_unit_of_measure.id:
                                        uom_id = obj.sea_unit_of_measure.id
                                    else:
                                        raise UserError(
                                            _('%s, has not set units yet.!') % (obj.display_name))
                                    tax_id = line.invoice_line_tax_ids.id
                                    check_adjustment_drink_with_price += line.price_subtotal_signed
                            price_unit_drink_with_price = price_total_drink_with_price / quantity_drink_with_price
                            price_tax_drink_with_price = price_total_drink_with_price - price_subtotal_drink_with_price
                            # if not r.reconciled and r.type == 'out_refund':
                            if adj_status == 'adjustment':
                                item_name = 'Điều chỉnh giảm '
                                if price_tax_drink_with_price == 0:
                                    item_name += 'thành tiền mặt hàng ' + obj.name
                                else:
                                    item_name += 'tiền thuế, thành tiền mặt hàng ' + obj.name
                                self.env['invoice.line.consolidation'].create({
                                    'invoice_id': invoice_id.id,
                                    'product_id': obj.id,
                                    'description': item_name,
                                    'quantity': -quantity_drink_with_price,
                                    'uom_id': uom_id,
                                    'price_unit': price_unit_drink_with_price,
                                    'tax_id': tax_id,
                                    'price_subtotal': -price_subtotal_drink_with_price,
                                    'price_tax': -price_tax_drink_with_price,
                                    'price_total': -price_total_drink_with_price,
                                })
                            else:
                                self.env['invoice.line.consolidation'].create({
                                    'invoice_id': invoice_id.id,
                                    'product_id': obj.id,
                                    'description': obj.name,
                                    'quantity': quantity_drink_with_price,
                                    'uom_id': uom_id,
                                    'price_unit': price_unit_drink_with_price,
                                    'tax_id': tax_id,
                                    'price_subtotal': price_subtotal_drink_with_price,
                                    'price_tax': price_tax_drink_with_price,
                                    'price_total': price_total_drink_with_price,
                                })

                    if product_id_no_price:
                        list_product = list(set(product_id_no_price))
                        for obj in self.env['product.product'].browse(list_product):
                            quantity_no_price = 0
                            price_subtotal_no_price = 0
                            price_total_no_price = 0
                            uom_id = 0
                            tax_id = 0
                            for line in r.invoice_line_ids:
                                if obj.id == line.product_id.id and line.price_total == 0:
                                    quantity_no_price += line.quantity
                                    price_subtotal_no_price += line.price_subtotal
                                    price_total_no_price += line.price_total
                                    if obj.sea_unit_of_measure.id:
                                        uom_id = obj.sea_unit_of_measure.id
                                    else:
                                        raise UserError(
                                            _('%s, has not set units yet.!') % (obj.display_name))
                                    tax_id = line.invoice_line_tax_ids.id
                            price_unit_no_price = price_total_no_price / quantity_no_price
                            price_tax_no_price = price_total_no_price - price_subtotal_no_price
                            self.env['invoice.line.consolidation'].create({
                                'invoice_id': invoice_id.id,
                                'product_id': obj.id,
                                'description': obj.name,
                                'quantity': quantity_no_price,
                                'uom_id': uom_id,
                                'price_unit': price_unit_no_price,
                                'tax_id': tax_id,
                                'price_subtotal': price_subtotal_no_price,
                                'price_tax': price_tax_no_price,
                                'price_total': price_total_no_price,
                            })

                    if product_id_drink_no_price:
                        for obj in self.env['product.product'].browse(product_drinks.id):
                            quantity_drink_no_price = 0
                            price_subtotal_drink_no_price = 0
                            price_total_drink_no_price = 0
                            uom_id = 0
                            tax_id = 0
                            for line in r.invoice_line_ids:
                                if line.product_id.sea_pos_check_drinks and line.price_total == 0:
                                    quantity_drink_no_price += line.quantity
                                    price_subtotal_drink_no_price += line.price_subtotal
                                    price_total_drink_no_price += line.price_total
                                    if obj.sea_unit_of_measure.id:
                                        uom_id = obj.sea_unit_of_measure.id
                                    else:
                                        raise UserError(
                                            _('%s, has not set units yet.!') % (obj.display_name))
                                    tax_id = line.invoice_line_tax_ids.id
                            price_unit_drink_no_price = price_total_drink_no_price / quantity_drink_no_price
                            price_tax_drink_no_price = price_total_drink_no_price - price_subtotal_drink_no_price
                            self.env['invoice.line.consolidation'].create({
                                'invoice_id': invoice_id.id,
                                'product_id': obj.id,
                                'description': obj.name,
                                'quantity': quantity_drink_no_price,
                                'uom_id': uom_id,
                                'price_unit': price_unit_drink_no_price,
                                'tax_id': tax_id,
                                'price_subtotal': price_subtotal_drink_no_price,
                                'price_tax': price_tax_drink_no_price,
                                'price_total': price_total_drink_no_price,
                            })

                else:
                    raise UserError(_('Invoice has been merged or Unconfirmed Invoice'))
            else:
                raise UserError(_('Check Invoice.? Customer don\'t take Invoice'))
        self.update({
            'sea_consolidation_state': 'merged',
        })

    def _get_customer(self):
        list_cus = []
        list_cus_dont_take_inv = []
        list_cus_to_inv = []
        for r in self:
            list_cus.append(r.partner_vat_id.id)
            if r.sea_view_choose_to_invoice_consolidation == 'No INV' and r.team_id.name != 'TMĐT':
                list_cus_dont_take_inv.append(r.partner_vat_id.id)
            else:
                list_cus_to_inv.append(r.partner_vat_id.id)
        if len(list_cus) == len(list_cus_dont_take_inv):
            domain = [
                ('name', '=', 'Khách lẻ (Người mua không lấy hóa đơn)'),
                ('company_ids', '=', r.company_id.id)
            ]
            for obj in self.env['res.partner'].search(domain):
                return obj
            # if r.company_id.id == 2:
            #     for obj in self.env['res.partner'].search([('name', '=', 'Khách lẻ (Người mua không lấy hóa đơn)'),
            #                                                ('company_ids', '=', r.company_id.id)]):
            #         return obj
            # elif r.company_id.id == 14:
            #     for obj in self.env['res.partner'].search([('name', '=', 'Khách lẻ (Người mua không lấy hóa đơn)'),
            #                                                ('company_ids', '=', r.company_id.id)]):
            #         return obj
        else:
            if len(list_cus) == len(list_cus_to_inv) and len(set(list_cus_to_inv)) == 1:
                list_cus_to_inv_set = list(set(list_cus_to_inv))
                for obj in self.env['res.partner'].search([('id', 'in', list_cus_to_inv_set)]):
                    return obj
            else:
                raise UserError(
                    _('Customers are not the same or Exist Customers take Invoice and don\'t take Invoice'))

    def get_customer_name(self):
        if self._get_customer().parent_id:
            return self._get_customer().parent_id.id
        else:
            return self._get_customer().id

    def get_customer_vat(self):
        if self._get_customer().parent_id:
            return self._get_customer().parent_id.vat
        else:
            return self._get_customer().vat

    def get_email_invoice(self):
        if self._get_customer().parent_id:
            return self._get_customer().parent_id.sea_email_invoice
        else:
            return self._get_customer().sea_email_invoice

    def get_customer_address(self):
        address = ''
        if self._get_customer().parent_id:
            if self._get_customer().parent_id.street:
                address = address + str(self._get_customer().parent_id.street)
            if self._get_customer().parent_id.state_id:
                address = address + ', ' + str(self._get_customer().parent_id.state_id.name)
            if self._get_customer().parent_id.country_id:
                address = address + ', ' + str(self._get_customer().parent_id.country_id.name)
        else:
            for cus in self._get_customer():
                if cus.type == 'invoice':
                    if cus.street:
                        address = address + str(self._get_customer().street)
                    if cus.state_id:
                        address = address + ', ' + str(self._get_customer().state_id.name)
                    if cus.country_id:
                        address = address + ', ' + str(self._get_customer().country_id.name)
                else:
                    if cus.street:
                        address = address + str(self._get_customer().street)
                    if cus.state_id:
                        address = address + ', ' + str(self._get_customer().state_id.name)
                    if cus.country_id:
                        address = address + ', ' + str(self._get_customer().country_id.name)
        return address

    def invoice_consolidation(self):
        if len(self) == 1:
            if self.sea_view_choose_to_invoice_consolidation == 'Invoice':
                raise UserError(_('Only for multiple invoices or retail customer don''t take invoice'))
        self = self.sorted('date_invoice')
        amount_untaxed = 0
        amount_tax = 0
        amount_total = 0
        temp_status = []
        get_status = ''
        origin = ''
        original = ''
        bill_pos = ''
        count_inv = 0

        invoice_line = []
        for r in self:
            count_inv += 1
            if r.sea_consolidation_state == 'not' and r.number:
                origin += '\n' + r.number
                original += '\n' + r.origin
                if r.pos_order_id:
                    bill_pos += '\n' + r.pos_order_id.pos_reference
                amount_untaxed += r.amount_untaxed_invoice_signed
                amount_tax += r.amount_tax_signed
                amount_total += r.amount_total_signed
                for line in r.invoice_line_ids:
                    invoice_line.append(line)
            else:
                raise UserError(_('Invoice has been merged or Unconfirmed Invoice'))

            if r.type == 'out_refund':
                if r.reconciled:
                    obj_search = r.env['account.invoice'].search([('number', '=', r.origin)])
                    check_cancel = r.env['account.invoice'].search([('origin', '=', obj_search.origin)])
                    if len(check_cancel) > 1:
                        for i in invoice_line:
                            if i.quantity == 0:
                                temp_status.append('adjustment')
                                get_status = 'adjustment'
                            else:
                                temp_status.append('cancelled')
                                get_status = 'cancelled'
                    else:
                        if r.amount_total_signed == 0:
                            temp_status.append('adjustment')
                            get_status = 'adjustment'
                        else:
                            temp_status.append('cancel')
                            get_status = 'cancel'
                else:
                    credit_type = r.env['account.invoice'].search([('origin', '=', r.origin)])
                    if len(credit_type) > 1:
                        check_status = []
                        for i in credit_type:
                            check_status.append(i.amount_total)
                        if len(set(check_status)) > 1:
                            temp_status.append('adjustment')
                            get_status = 'adjustment'
                        else:
                            temp_status.append('cancel')
                            get_status = 'cancel'
                    else:
                        if r.pos_order_id.return_order_id:
                            if r.amount_total == r.pos_order_id.return_order_id.amount_total:
                                res = self.env['invoice.consolidation'].search([])
                                for i in res:
                                    if i:
                                        if str(r.pos_order_id.return_order_id.name) == str(i.original)[1:]:
                                            temp_status.append('cancel')
                                            get_status = 'cancel'
                                        elif str(r.pos_order_id.return_order_id.name) in str(i.original)[1:] and \
                                                len(str(i.original)[1:]) > len(
                                            str(r.pos_order_id.return_order_id.name)):
                                            temp_status.append('adjustment')
                                            get_status = 'adjustment'
                            else:
                                temp_status.append('adjustment')
                                get_status = 'adjustment'
                        else:
                            temp_status.append('adjustment')
                            get_status = 'adjustment'
            else:
                check_replace = r.env['account.invoice'].search([('reference', '=', r.reference)])
                if check_replace:
                    if r.company_id in [2, 14]:
                        index = r.reference[0:15]
                    else:
                        index = r.reference[0:16]
                    if index == r.number or r.reference == r.origin:
                        temp_status.append('open')
                        get_status = 'open'
                    else:
                        temp_status.append('replacement')
                        get_status = 'replacement'
            if r.pos_order_id:
                if r.pos_order_id.return_order_id:
                    original = r.pos_order_id.return_order_id.name

        # Get Status after Invoice Merge
        if len(temp_status) > 1:
            if amount_total == 0:
                status = 'cancelled'
            else:
                status = 'open'
        else:
            if amount_total == 0:
                status = 'cancelled'
            elif amount_total < 0:
                if count_inv == 1:
                    pos_order = self.env['pos.order'].search([('name', '=', self.origin)])
                    pos_order_return = self.env['pos.order'].search([('name', '=', pos_order.return_order_id.name)])
                    if abs(pos_order.amount_total) == abs(pos_order_return.amount_total):
                        status = 'cancel'
                    else:
                        status = 'adjustment'
                else:
                    raise UserError(_('Error Consolidation Invoice. Amount total not be less than 0.!'))
            else:
                status = get_status

        # Create Invoice Header After Merge
        invoice_id = self.env['invoice.consolidation'].create({
            'partner_id': self.get_customer_name(),
            'address': self.get_customer_address(),
            'vat_number': self.get_customer_vat(),
            'email': self.get_email_invoice(),
            'currency_id': r.currency_id.id,
            'origin': origin,
            'amount_untaxed': amount_untaxed,
            'amount_tax': amount_tax,
            'amount_total': amount_total,
            'state': status,
            'original': original,
            'bill_pos': bill_pos,
            'customer_po_name': r.sea_customer_po_name,
            'customer_po_code': r.sea_customer_po_code,
        })
        for inv_id in self:
            inv_id.invoice_consolidation_id = invoice_id

        product_id_with_price = []
        product_id_no_price = []
        product_id_drink_with_price = []
        product_id_drink_no_price = []
        product_id_adjustment_invoice_info = []

        product_drinks = self.env['product.product'].search([('name', '=', 'Thức uống')])
        for line in invoice_line:
            if line.product_id.sea_pos_check_drinks and line.price_total != 0:
                product_id_drink_with_price.append(line.product_id.id)
            if line.product_id.sea_pos_check_drinks and line.price_total == 0:
                product_id_drink_no_price.append(line.product_id.id)
            if not line.product_id.sea_pos_check_drinks and line.price_total != 0:
                product_id_with_price.append(line.product_id.id)
            if not line.product_id.sea_pos_check_drinks and line.price_total == 0 and line.quantity != 0:
                product_id_no_price.append(line.product_id.id)
            if line.product_id.name == 'Điều chỉnh thông tin' and line.quantity == 0:
                product_id_adjustment_invoice_info.append(line.product_id.id)

        if product_id_adjustment_invoice_info:
            for obj in self.env['product.product'].browse(list(set(product_id_adjustment_invoice_info))):
                tax_id = 0
                for line in r.invoice_line_ids:
                    tax_id = line.invoice_line_tax_ids.id
                self.env['invoice.line.consolidation'].create({
                    'invoice_id': invoice_id.id,
                    'product_id': obj.id,
                    'description': line.name,
                    'quantity': 0,
                    'tax_id': tax_id,
                })

        if product_id_with_price:
            for obj in self.env['product.product'].browse(list(set(product_id_with_price))):
                quantity_with_price = 0
                price_subtotal_with_price = 0
                price_total_with_price = 0
                uom_id = 0
                tax_id = 0

                for line in invoice_line:
                    if line.product_id.id == obj.id and line.price_total != 0:
                        quantity_with_price += line.quantity
                        price_subtotal_with_price += line.price_subtotal
                        price_total_with_price += line.price_total
                        # if line.price_subtotal_signed < 0:
                        #     quantity_with_price += -line.quantity
                        #     price_subtotal_with_price += -line.price_subtotal
                        #     price_total_with_price += -line.price_total
                        # else:
                        #     quantity_with_price += line.quantity
                        #     price_subtotal_with_price += line.price_subtotal
                        #     price_total_with_price += line.price_total
                        if obj.sea_unit_of_measure.id:
                            uom_id = obj.sea_unit_of_measure.id
                        else:
                            raise UserError(
                                _('%s, has not set units yet.!') % (obj.display_name))
                        tax_id = line.invoice_line_tax_ids.id
                price_unit_with_price = price_total_with_price / quantity_with_price
                price_tax_with_price = price_total_with_price - price_subtotal_with_price

                if status == 'adjustment':
                    # Decrease adjustment for issued invoice
                    item_name = 'Điều chỉnh giảm số lượng, '
                    if price_tax_with_price == 0:
                        item_name += 'Thành tiền mặt hàng ' + obj.name
                    else:
                        item_name += 'Tiền thuế, Thành tiền mặt hàng ' + obj.name
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': item_name,
                        'quantity': -quantity_with_price,
                        'uom_id': uom_id,
                        'price_unit': price_unit_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': -price_subtotal_with_price,
                        'price_tax': -price_tax_with_price,
                        'price_total': -price_total_with_price,
                    })
                elif status == 'cancelled':
                    # Merge Invoices of type out_invoice and out_refund to amount_total == 0
                    # Do not Issue Invoice
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': obj.name,
                        'quantity': 0,
                        'uom_id': uom_id,
                        'price_unit': price_unit_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': 0,
                        'price_tax': 0,
                        'price_total': 0,
                    })
                elif status == 'cancel':
                    # Cancel issued invoice
                    # Choose only 1 invoice to cancel
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': obj.name,
                        'quantity': -quantity_with_price,
                        'uom_id': uom_id,
                        'price_unit': price_unit_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': -price_subtotal_with_price,
                        'price_tax': -price_tax_with_price,
                        'price_total': -price_total_with_price,
                    })
                else:
                    # Can merge Invoices of type out_invoice and out_refund
                    # Status == open to Issue Invoice
                    qty_invoice = 0
                    qty_refund = 0
                    price_subtotal = 0
                    price_total_invoice = 0
                    price_total_refund = 0
                    for inv in self:
                        for line in inv.invoice_line_ids:
                            if line.product_id.id == obj.id and line.price_total != 0:
                                if inv.type == 'out_invoice':
                                    qty_invoice += line.quantity
                                    price_total_invoice += line.price_total
                                if inv.type == 'out_refund':
                                    qty_refund += line.quantity
                                    price_total_refund += line.price_total
                                price_subtotal += line.price_subtotal_signed

                    amount_tax = (price_total_invoice - price_total_refund) - price_subtotal
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': obj.name,
                        'quantity': qty_invoice - qty_refund,
                        'uom_id': uom_id,
                        'price_unit': price_unit_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': price_subtotal,
                        'price_tax': amount_tax,
                        'price_total': price_total_invoice - price_total_refund,
                    })

        if product_id_drink_with_price:
            for obj in self.env['product.product'].browse(product_drinks.id):
                quantity_drink_with_price = 0
                price_subtotal_drink_with_price = 0
                price_total_drink_with_price = 0
                uom_id = 0
                tax_id = 0
                for line in invoice_line:
                    if line.product_id.sea_pos_check_drinks and line.price_total != 0:
                        # if line.price_subtotal_signed < 0:
                        #     quantity_drink_with_price += -line.quantity
                        #     price_subtotal_drink_with_price += -line.price_subtotal
                        #     price_total_drink_with_price += -line.price_total
                        # else:
                        #     quantity_drink_with_price += line.quantity
                        #     price_subtotal_drink_with_price += line.price_subtotal
                        #     price_total_drink_with_price += line.price_total
                        quantity_drink_with_price += line.quantity
                        price_subtotal_drink_with_price += line.price_subtotal
                        price_total_drink_with_price += line.price_total
                        if obj.sea_unit_of_measure.id:
                            uom_id = obj.sea_unit_of_measure.id
                        else:
                            raise UserError(
                                _('%s, has not set units yet.!') % (obj.display_name))
                        tax_id = line.invoice_line_tax_ids.id
                price_unit_drink_with_price = price_total_drink_with_price / quantity_drink_with_price
                price_tax_drink_with_price = price_total_drink_with_price - price_subtotal_drink_with_price
                if status == 'adjustment':
                    item_name = 'Điều chỉnh giảm '
                    if price_tax_drink_with_price == 0:
                        item_name += 'thành tiền mặt hàng ' + obj.name
                    else:
                        item_name += 'tiền thuế, thành tiền mặt hàng ' + obj.name
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': item_name,
                        'quantity': -quantity_drink_with_price,
                        'uom_id': uom_id,
                        'price_unit': price_unit_drink_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': -price_subtotal_drink_with_price,
                        'price_tax': -price_tax_drink_with_price,
                        'price_total': -price_total_drink_with_price,
                    })
                else:
                    self.env['invoice.line.consolidation'].create({
                        'invoice_id': invoice_id.id,
                        'product_id': obj.id,
                        'description': obj.name,
                        'quantity': quantity_drink_with_price,
                        'uom_id': uom_id,
                        'price_unit': price_unit_drink_with_price,
                        'tax_id': tax_id,
                        'price_subtotal': price_subtotal_drink_with_price,
                        'price_tax': price_tax_drink_with_price,
                        'price_total': price_total_drink_with_price,
                    })
                # self.env['invoice.line.consolidation'].create({
                #     'invoice_id': invoice_id.id,
                #     'product_id': obj.id,
                #     'description': obj.name,
                #     'quantity': quantity_drink_with_price,
                #     'uom_id': uom_id,
                #     'price_unit': price_unit_drink_with_price,
                #     'tax_id': tax_id,
                #     'price_subtotal': price_subtotal_drink_with_price,
                #     'price_tax': price_tax_drink_with_price,
                #     'price_total': price_total_drink_with_price,
                # })

        if product_id_no_price:
            list_product = list(set(product_id_no_price))
            for obj in self.env['product.product'].browse(list_product):
                quantity_no_price = 0
                price_subtotal_no_price = 0
                price_total_no_price = 0
                uom_id = 0
                tax_id = 0
                price_unit_no_price_line = 0
                for line in invoice_line:
                    if obj.id == line.product_id.id and line.price_total == 0:
                        quantity_no_price += line.quantity
                        price_subtotal_no_price += line.price_subtotal
                        price_total_no_price += line.price_total
                        price_unit_no_price_line = line.price_subtotal
                        if obj.sea_unit_of_measure.id:
                            uom_id = obj.sea_unit_of_measure.id
                        else:
                            raise UserError(
                                _('%s, has not set units yet.!') % (obj.display_name))
                        tax_id = line.invoice_line_tax_ids.id
                if quantity_no_price != 0:
                    price_unit_no_price = price_total_no_price / quantity_no_price
                else:
                    price_unit_no_price = price_unit_no_price_line
                price_tax_no_price = price_total_no_price - price_subtotal_no_price
                self.env['invoice.line.consolidation'].create({
                    'invoice_id': invoice_id.id,
                    'product_id': obj.id,
                    'description': obj.name,
                    'quantity': quantity_no_price,
                    'uom_id': uom_id,
                    'price_unit': price_unit_no_price,
                    'tax_id': tax_id,
                    'price_subtotal': price_subtotal_no_price,
                    'price_tax': price_tax_no_price,
                    'price_total': price_total_no_price,
                })

        if product_id_drink_no_price:
            for obj in self.env['product.product'].browse(product_drinks.id):
                quantity_drink_no_price = 0
                price_subtotal_drink_no_price = 0
                price_total_drink_no_price = 0
                uom_id = 0
                tax_id = 0
                for line in invoice_line:
                    if line.product_id.sea_pos_check_drinks and line.price_total == 0:
                        quantity_drink_no_price += line.quantity
                        price_subtotal_drink_no_price += line.price_subtotal
                        price_total_drink_no_price += line.price_total
                        if obj.sea_unit_of_measure.id:
                            uom_id = obj.sea_unit_of_measure.id
                        else:
                            raise UserError(
                                _('%s, has not set units yet.!') % (obj.display_name))
                        tax_id = line.invoice_line_tax_ids.id
                price_unit_drink_no_price = price_total_drink_no_price / quantity_drink_no_price
                price_tax_drink_no_price = price_total_drink_no_price - price_subtotal_drink_no_price
                self.env['invoice.line.consolidation'].create({
                    'invoice_id': invoice_id.id,
                    'product_id': obj.id,
                    'description': obj.name,
                    'quantity': quantity_drink_no_price,
                    'uom_id': uom_id,
                    'price_unit': price_unit_drink_no_price,
                    'tax_id': tax_id,
                    'price_subtotal': price_subtotal_drink_no_price,
                    'price_tax': price_tax_drink_no_price,
                    'price_total': price_total_drink_no_price,
                })
        self.update({
            'sea_consolidation_state': 'merged',
        })


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def create(self, values):
        product_id = self.env['product.product'].browse(values['product_id'])
        if product_id.name == 'Điều chỉnh thông tin':
            values['quantity'] = 0
        return super(AccountInvoiceLine, self).create(values)
