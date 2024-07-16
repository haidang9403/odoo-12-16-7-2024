from odoo import models, fields, api


class TransactionType(models.Model):
    _name = "transaction.type"

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    descriptions = fields.Char('Descriptions')
    type = fields.Selection(selection=[('outgoing', 'Customer'),
                                       ('incoming', 'Vendor'),
                                       ('internal', 'Internal'),
                                       ('mrp_operation', 'Manufacturing Operation')],
                            default='internal', string='Type of Operation', required=True)
    account_determination_ids = fields.One2many('account.determination', 'transaction_id',
                                                string='Account Determination')
    create_asset = fields.Boolean('Create Asset')
    src_location_id = fields.Many2one('stock.location', 'Source Location')
    dest_location_id = fields.Many2one('stock.location', 'Destination Location')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True,
                                 readonly=True)


class AccountDetermination(models.Model):
    _name = "account.determination"

    transaction_id = fields.Many2one('transaction.type', 'Transaction References', required=True)
    location_id = fields.Many2one('stock.location', 'Location')
    product_category = fields.Many2one('product.category', 'Product Category')
    account_id = fields.Many2one('account.account', 'Account', required=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id, required=True,
                                 readonly=True)
