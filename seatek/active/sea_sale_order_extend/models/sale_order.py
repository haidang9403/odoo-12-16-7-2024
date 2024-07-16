# Update 06/2/2021

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search(self, domains, *args, **kwargs):
        context = self.env.context
        if 'order_by' in context:
            kwargs['order'] = f"{context.get('order_by')}"
        res = super(ResPartner, self).search(domains, *args, **kwargs)
        return res


class SaleOrder(models.Model):
    _inherit = ['sale.order']

    #    customer_partner_id = fields.Many2one('res.partner', string='Customer Partner', readonly=True,
    #                                         states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
    #                                        change_default=True, index=True, track_visibility='always', track_sequence=1,
    #                                       help="You can find a customer by its Name, TIN, Email or Internal Reference.")

    # htkhoa add sea_ship_partner_id#
    # partner_shipping_id = fields.Many2one('res.partner', string='Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]}, help="Delivery address for current sales order.")
    sea_ship_partner_id = fields.Many2one('res.partner', string='Ship', readonly=True,
                                          states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                                  'sale': [('readonly', False)]}, help="Ship for Sale Order",
                                          domain="[('type','=,'ship')]")

    # htkhoa end of sea_ship_partner_id

    total = fields.Monetary(string='Total Amount', readonly=True, track_sequence=5)

    def total_amount(self, tax):
        self.total = float(self.amount_untaxed * (tax / 100) + self.amount_untaxed)

    # from cuong.nguyen
    sea_temp_delivery_address = fields.Char(string='Temporary Delivery Address')
    sea_temp_contact = fields.Char(string='Temporary Contact')
    sea_customer_inquiry_no = fields.Char(string='Customer Inquiry No', store=True, default="")
    sea_customer_inquiry_date = fields.Date(string='Customer InquiryDate', store=True)
    sea_customer_po_no = fields.Char(string='CustomerPO No', store=True, default="", track_visibility='onchange')
    sea_imo_no = fields.Char(string='IMO No', store=True, default="")

    # ThaiPham - 18/Apr/2023
    # Filter Customer
    partner_id = fields.Many2one('res.partner', 'Customer',
                                 domain="[('type', '=', 'contact'), ('parent_id', '=', False), ('customer', '=', True)]",
                                 required=True)
    # ThaiPham - 19/Oct/2023
    partner_shipping_id = fields.Many2one('res.partner', track_visibility='onchange')

    # Default commitment_date
    commitment_date = fields.Datetime('Commitment Date', required=True, default=fields.Datetime.now)

    # ThaiPham - 7/Dec/2023
    sale_transaction_id = fields.Many2one('transaction.type', 'Transaction Type', domain=[('type', '=', 'outgoing')])
    sea_payment_method = fields.Selection(selection=[('cash', 'Tiền Mặt'), ('bank', 'Ngân Hàng'), ('debt', 'Công Nợ'),],
                                          string='Payment Method')

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['sea_payment_method'] = self.sea_payment_method
        return res

    # ThaiPham - 7/Dec/2023
    @api.onchange('sale_transaction_id')
    def _onchange_update_transaction_sale_line(self):
        if self.sale_transaction_id:
            if self.order_line:
                for p in self.order_line:
                    p.update({
                        'sale_line_transaction_id': self.sale_transaction_id
                    })

    partner_vat_id = fields.Many2one('res.partner', string='VAT Address',
                                     states={'draft': [('readonly', False)], 'sent': [('readonly', False)],
                                             'sale': [('readonly', False)]},

                                     domain="",
                                     help="VAT address for current sales order.")

    @api.onchange('partner_id')
    def domain_compute(self):
        for rec in self:
            rec.domain_delivery = False
            rec.domain_vat = False
            rec.domain_invoice = False
            if rec.partner_id:
                domain = []
                domain_vat = []
                domain_invoice = []
                domain.append(rec.partner_id.id)
                domain.extend(self.env['res.partner'].search(
                    [('parent_id', '=', rec.partner_id.id),
                     ('type', '=', 'delivery')]).ids)

                domain_vat.append(rec.partner_id.id)
                domain_vat.extend(
                    # self.env['res.partner'].search(
                    # [('parent_id', '=', rec.partner_id.id),
                    #  ('type', '=', 'vat'), ('contact_type', '=', 'standalone')])
                    rec.partner_id.partner_vat_ids.ids)

                domain_invoice.append(rec.partner_id.id)
                domain_invoice.extend(
                    # self.env['res.partner'].search(
                    # [('parent_id', '=', rec.partner_id.id),
                    #  ('type', '=', 'invoice')])
                    rec.partner_id.partner_invoice_ids.ids)
                rec.domain_delivery = domain
                rec.domain_vat = domain_vat
                rec.domain_invoice = domain_invoice

    domain_delivery = fields.Many2many('res.partner', string='Domain delivery', compute='domain_compute')

    domain_vat = fields.Many2many('res.partner', string='Domain vat', compute='domain_compute')

    domain_invoice = fields.Many2many('res.partner', string='Domain invoice', compute='domain_compute')

    @api.multi
    @api.onchange('partner_id')
    def set_invoice_default(self):
        """
        Update the following fields when the partner is changed:
        - VAT
        """
        if not self.partner_id:
            self.update({
                'partner_invoice_id': False,
            })
            return

        # addr = self.partner_id.address_get(['vat'])
        values = {
            'partner_invoice_id': self.partner_id,
        }
        self.update(values)

    @api.multi
    @api.onchange('partner_invoice_id', 'sea_check_customer_for_invoice')
    def set_vat_default(self):
        """
        Update the following fields when the partner is changed:
        - VAT
        """
        if not self.partner_invoice_id or self.sea_check_customer_for_invoice:
            self.update({
                'partner_vat_id': False,
            })
            return

        # addr = self.partner_id.address_get(['vat'])
        values = {
            'partner_vat_id': self.partner_invoice_id,
        }
        self.update(values)

    @api.model
    def create(self, vals):
        if not vals.get('sea_check_customer_for_invoice'):
            if any(f not in vals for f in ['partner_vat_id']):
                # partner = self.env['res.partner'].browse(vals.get('partner_id'))
                # addr = partner.address_get(['vat'])
                vals['partner_vat_id'] = vals.setdefault('partner_vat_id', vals.get('partner_id'))
        else:
            vals['partner_vat_id'] = False

        result = super(SaleOrder, self).create(vals)
        return result

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['partner_vat_id'] = self.partner_vat_id.id or False
        invoice_vals['buyer_id'] = self.partner_id.id or False
        return invoice_vals

    '''data default when create shipping contact'''
    street_partner = fields.Char(related='partner_id.street')
    street2_partner = fields.Char(related='partner_id.street2')
    state_id_partner = fields.Many2one("res.country.state", string='State', related='partner_id.state_id')
    zip_partner = fields.Char(related='partner_id.zip')
    city_partner = fields.Char(related='partner_id.city')
    country_id_partner = fields.Many2one('res.country', string='Country', related='partner_id.country_id')
    supplier_partner = fields.Boolean(string='Is a Vendor', related='partner_id.supplier')
    customer_partner = fields.Boolean(string='Is a Customer', related='partner_id.customer')
    lang_partner = fields.Selection(string='Language', related='partner_id.lang')
    user_id_partner = fields.Many2one('res.users', string='Salesperson', related='partner_id.user_id')

    # @api.constrains('partner_vat_id')
    # def partner_vat_id_constrains(self):
    #     '''check vat in VAT address'''
    #     for rec in self:
    #         if rec.partner_vat_id and not rec.sea_check_customer_for_invoice and self.company_id.sea_sale_order_take_invoice_enable:
    #             customer = self.env['res.partner'].search([('id', '=', self.partner_vat_id.id)])
    #             if not customer.vat:
    #                 raise UserError(_("VAT address don't have VAT"))


# ThaiPham - 7/Dec/2023
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sale_line_transaction_id = fields.Many2one('transaction.type', 'Transaction', domain=[('type', '=', 'outgoing')])

    product_uom_select = fields.Boolean('Unit select in sale order line', compute='product_uom_select_compute')

    @api.onchange('product_id')
    def product_uom_select_compute(self):
        for rec in self:
            rec.product_uom_select = self.env.user.company_id.product_uom_select

    @api.onchange('product_id')
    def _onchange_default_transaction_sale_line(self):
        self.ensure_one()
        if self.product_id:
            self.sale_line_transaction_id = self.order_id.sale_transaction_id.id
        '''tkk'''
        if self.product_packaging:
            self.update({'product_packaging': False})

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        """ Prepare specific key for moves or other components that will be created from a stock rule
        comming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        self.ensure_one()
        values.update({'sea_transaction_id': self.sale_line_transaction_id.id})
        return values

    '''tkk add packaging_qty and edit product_uom_qty & price_unit based on product_packaging'''
    product_packaging_qty = fields.Integer(string='Packaging Quantity')
    list_price = fields.Float('Package price')
    sale_with_package = fields.Boolean('Sale with Package', related='product_id.sale_with_package', store=False)

    @api.onchange('product_packaging_qty')
    def onchange_product_packaging_qty(self):
        for rec in self:
            if rec.product_packaging:
                vals = {
                    'product_uom_qty': 1 if rec.product_packaging_qty <= 0 else rec.product_packaging.sudo().qty * rec.product_packaging_qty
                }

                if rec.product_packaging_qty <= 0:
                    rec.product_id_change()
                    vals['remarks'] = False
                    vals['list_price'] = rec.product_packaging.sudo().list_price
                if vals:
                    rec.update(vals)
                if rec.product_packaging_qty <= 0:
                    warning_mess = {
                        'title': _('WARNING!'),
                        'message': "The packaged quantity must be greater than 0"
                    }
                    return {'warning': warning_mess}

    @api.onchange('product_packaging')
    def _onchange_product_packaging(self):
        for rec in self:
            vals = {}
            if rec.product_packaging:
                if rec.product_packaging.sudo().qty <= 0 or rec.product_packaging.sudo().list_price <= 0:
                    warning_mess = {
                        'title': _('WARNING!'),
                        'message': "Your packaging selected have price or quantity smaller than or equal 0"
                    }
                    return {'warning': warning_mess}
                if not rec.product_packaging_qty:
                    vals['product_packaging_qty'] = 1
                if rec.list_price != rec.product_packaging.sudo().list_price:
                    vals['list_price'] = rec.product_packaging.sudo().list_price
            else:
                if rec.product_packaging_qty or rec.list_price:
                    vals['product_packaging_qty'] = False
                    vals['list_price'] = False
                    rec.product_id_change()
            if vals:
                return rec.update(vals)

    @api.onchange('list_price')
    def _onchange_list_price(self):
        for rec in self:
            if rec.product_packaging:
                if rec.product_packaging_qty <= 0:
                    # warning_mess = {
                    #     'title': _('WARNING!'),
                    #     'message': "Packaging Quantity is 0"
                    # }
                    # return {'warning': warning_mess}
                    pass
                else:
                    return rec.update({'price_unit': rec.list_price / rec.product_packaging.sudo().qty})
            elif rec.list_price > 0:
                rec.product_id_change()
                warning_mess = {
                    'title': _('WARNING!'),
                    'message': "Not packaging selected"
                }
                return {'warning': warning_mess}

    @api.onchange('product_packaging', 'product_packaging_qty')
    def _onchange_list_price_product_packaging_qty(self):
        if self.product_packaging and self.product_packaging_qty > 0:
            self.update({'remarks': str(self.product_packaging_qty) + " " + self.product_packaging.sudo().name})

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        if not self.product_uom or not self.product_id:
            self.price_unit = 0.0
            return
        if self.order_id.pricelist_id and self.order_id.partner_id:
            product = self.product_id.with_context(
                lang=self.order_id.partner_id.lang,
                partner=self.order_id.partner_id,
                quantity=self.product_uom_qty,
                date=self.order_id.date_order,
                pricelist=self.order_id.pricelist_id.id,
                uom=self.product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            self.price_unit = (
                    self.list_price / self.product_packaging.sudo().qty) \
                if self.product_packaging and self.product_packaging_qty > 0 else self.env[
                'account.tax']._fix_tax_included_price_company(
                self._get_display_price(product),
                product.taxes_id,
                self.tax_id, self.company_id)


# ThaiPham - 7/Dec/2023
class StockRule(models.Model):
    _inherit = "stock.rule"

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, values, group_id):
        datas = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name,
                                                              origin, values, group_id)
        if values.get('sea_transaction_id'):
            datas.update({'sea_transaction_id': values['sea_transaction_id']})
        return datas
