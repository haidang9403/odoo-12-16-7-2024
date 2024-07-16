from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    sea_check_customer_for_invoice = fields.Boolean(string='Customer Don\'t Take Invoice')
    sea_hide_take_invoice_multi_company = fields.Char(
        default=lambda self: self.env.user.company_id.sea_sale_order_take_invoice_enable)
