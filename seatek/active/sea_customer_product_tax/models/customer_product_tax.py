from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomerProductTax(models.Model):
    _name = 'customer.product.tax'
    _description = 'Create a new tax list for Customer when buying products with preferential tax'

    customer_category_id = fields.Many2one('customer.category.tax', 'Customer Category', required=True)
    category_id = fields.Many2one('product.category', string='Product categories', required=True)
    tax_id = fields.Many2one('account.tax', 'Taxes', required=True)
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.user.company_id)

    def checked_enabled(self):
        company_id = self.env.user.company_id
        return company_id.customer_tax_enabled

    def get_company_name_str(self):
        company_id = self.env.user.company_id
        return company_id.name

    @api.multi
    def unlink(self):
        if self.checked_enabled():
            if len(self) > 1:
                raise UserError(_("You need to check each line before delete."))
            check_use = self.env['sale.order.line'].search([('tax_id', '=', self.tax_id.id),
                                                            ('product_id.categ_id', '=', self.category_id.id),
                                                            ('order_partner_id', '=', self.customer_category_id.id)])
            print(check_use)
            if len(check_use) > 0:
                raise UserError(_("You cannot delete this Category because it is used by the system."))
            else:
                return models.Model.unlink(self)
        else:
            raise UserError(
                _("%s\nYou Have Just Readonly Access !") % (self.get_company_name_str()))

    @api.model
    def create(self, values):
        if self.checked_enabled():
            res = super(CustomerProductTax, self).create(values)
            check_exist = self.env['customer.product.tax'].search([('category_id', '=', values['category_id']),
                                                                   ('customer_category_id', '=',
                                                                    values['customer_category_id'])])
            category = check_exist[0].category_id.complete_name
            customer = check_exist[0].customer_category_id.name
            if len(check_exist) > 1:
                raise UserError(
                    _("You cannot Create:\n Category: %s \nCustomer: %s \n IS EXIST") % (str(category), str(customer)))

            return res
        else:
            raise UserError(
                _("%s\nYou Have Just Readonly Access !") % (self.get_company_name_str()))

    @api.multi
    def write(self, values):
        if self.checked_enabled():
            res = super(CustomerProductTax, self).write(values)

            check_exist_true = self.env['customer.product.tax'].search([('tax_id', '=', self.tax_id.id),
                                                                        ('category_id', '=', self.category_id.id),
                                                                        ('customer_category_id', '=',
                                                                         self.customer_category_id.id),
                                                                        ('active', '=', True)])
            if len(check_exist_true) > 1:
                raise UserError(_("You cannot Active this Category because it is exist."))

            if values:
                if 'category_id' in values:
                    check_category = self.env['customer.product.tax'].search(
                        [('category_id', '=', values['category_id']),
                         ('customer_category_id', '=', self.customer_category_id.id)])
                    check_active = self.env['customer.product.tax'].search(
                        [('category_id', '=', values['category_id']),
                         ('customer_category_id', '=', self.customer_category_id.id),
                         ('active', '=', False)])
                    if len(check_category) > 1:
                        raise UserError(_("You cannot Edit, Category and Customer must be unique !"))
                    if len(check_active) > 1:
                        raise UserError(_("You cannot Edit, Category and Customer must be unique !"))

                if 'customer_category_id' in values:
                    check_customer = self.env['customer.product.tax'].search([('category_id', '=', self.category_id.id),
                                                                              (
                                                                                  'customer_category_id', '=',
                                                                                  values['customer_category_id'])])
                    check_active = self.env['customer.product.tax'].search([('category_id', '=', self.category_id.id),
                                                                            (
                                                                                'customer_category_id', '=',
                                                                                values['customer_category_id']),
                                                                            ('active', '=', False)])
                    if len(check_customer) > 1:
                        raise UserError(_("You cannot Edit, Category and Customer must be unique !"))
                    if len(check_active) > 1:
                        raise UserError(_("You cannot Edit, Category and Customer must be unique !"))
            return res
        else:
            raise UserError(
                _("%s\nYou Have Just Readonly Access !") % (self.get_company_name_str()))
