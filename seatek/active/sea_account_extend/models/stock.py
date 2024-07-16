import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sea_transaction_id = fields.Many2one('transaction.type', 'Transaction Type')

    # asset_code_id = fields.Many2one('account.asset.asset', 'Asset Code')

    @api.onchange('sea_transaction_id')
    def _onchange_transaction_stock_move(self):
        if self.sea_transaction_id.id:
            if self.move_ids_without_package:
                for s in self.move_ids_without_package:
                    s.update({
                        'sea_transaction_id': self.sea_transaction_id
                    })
                    analytic_account = self.env['account.determination'].search(
                        [('transaction_id', '=', self.sea_transaction_id.id)])
                    # print(analytic_account)
                    if analytic_account:
                        for acc in analytic_account:
                            if acc.location_id == self.location_dest_id:
                                s.update({
                                    'analytic_account_id': acc.analytic_account_id,
                                    'analytic_tag_ids': acc.analytic_tag_ids
                                })
                            elif not acc.location_id:
                                s.update({
                                    'analytic_account_id': acc.analytic_account_id,
                                    'analytic_tag_ids': acc.analytic_tag_ids
                                })
                    else:
                        s.update({
                            'analytic_account_id': {},
                            'analytic_tag_ids': {}
                        })

            list_src_location_ids = []
            if self.sea_transaction_id.src_location_id:
                self.location_id = self.sea_transaction_id.src_location_id.id
                list_src_location_ids = [self.sea_transaction_id.src_location_id.id]
                for src_location in self.sea_transaction_id.src_location_id.child_ids:
                    list_src_location_ids.append(src_location.id)
                    if src_location.child_ids:
                        for src in src_location.child_ids:
                            list_src_location_ids.append(src.id)
                # return {'domain': {'location_id': [('id', 'in', list_src_location_ids)]}}

            list_dest_location_ids = []
            if self.sea_transaction_id.dest_location_id:
                self.location_dest_id = self.sea_transaction_id.dest_location_id.id
                list_dest_location_ids = [self.sea_transaction_id.dest_location_id.id]
                for dest_location in self.sea_transaction_id.dest_location_id.child_ids:
                    list_dest_location_ids.append(dest_location.id)
                    if dest_location.child_ids:
                        for dest in dest_location.child_ids:
                            list_dest_location_ids.append(dest.id)
            if list_src_location_ids and list_dest_location_ids:
                return {'domain': {'location_id': [('id', 'in', list_src_location_ids)],
                                   'location_dest_id': [('id', 'in', list_dest_location_ids)]}}
        else:
            self.location_id = self.picking_type_id.default_location_src_id.id
            self.location_dest_id = self.picking_type_id.default_location_dest_id.id
            list_src_location_ids = [self.picking_type_id.default_location_src_id.id]
            list_dest_location_ids = [self.picking_type_id.default_location_dest_id.id]
            for src_location in self.picking_type_id.default_location_src_id.child_ids:
                list_src_location_ids.append(src_location.id)
                if src_location.child_ids:
                    for src in src_location.child_ids:
                        list_src_location_ids.append(src.id)
            # if self.picking_type_id.default_location_src_id.location_id:
            #     for src in self.picking_type_id.default_location_src_id.location_id.child_ids:
            #         list_src_location_ids.append(src.id)
            for dest_location in self.picking_type_id.default_location_dest_id.child_ids:
                list_dest_location_ids.append(dest_location.id)
                if dest_location.child_ids:
                    for dest in dest_location.child_ids:
                        list_dest_location_ids.append(dest.id)
            # if self.picking_type_id.default_location_dest_id.location_id:
            #     for dest in self.picking_type_id.default_location_dest_id.location_id.child_ids:
            #         list_dest_location_ids.append(dest.id)
            return {'domain': {'sea_transaction_id': [('type', '=', self.picking_type_id.code)],
                               'location_id': [('id', 'in', list_src_location_ids)],
                               'location_dest_id': [('id', 'in', list_dest_location_ids)]}}

    @api.onchange('picking_type_id')
    def _add_domain_transaction(self):
        if self.picking_type_id:
            self.sea_transaction_id = {}
            list_src_location_ids = [self.picking_type_id.default_location_src_id.id]
            list_dest_location_ids = [self.picking_type_id.default_location_dest_id.id]
            for src_location in self.picking_type_id.default_location_src_id.child_ids:
                list_src_location_ids.append(src_location.id)
                if src_location.child_ids:
                    for src in src_location.child_ids:
                        list_src_location_ids.append(src.id)
            # if self.picking_type_id.default_location_src_id.location_id:
            #     for src in self.picking_type_id.default_location_src_id.location_id.child_ids:
            #         list_src_location_ids.append(src.id)

            for dest_location in self.picking_type_id.default_location_dest_id.child_ids:
                list_dest_location_ids.append(dest_location.id)
                if dest_location.child_ids:
                    for dest in dest_location.child_ids:
                        list_dest_location_ids.append(dest.id)
            # if self.picking_type_id.default_location_dest_id.location_id:
            #     for dest in self.picking_type_id.default_location_dest_id.location_id.child_ids:
            #         list_dest_location_ids.append(dest.id)
            return {'domain': {'sea_transaction_id': [('type', '=', self.picking_type_id.code)],
                               'location_id': [('id', 'in', list_src_location_ids)],
                               'location_dest_id': [('id', 'in', list_dest_location_ids)]}}


class StockLocation(models.Model):
    _inherit = "stock.location"

    usage = fields.Selection(selection_add=[('cost_center', 'Cost Center')])

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')

    @api.constrains('warehouse_id')
    def change_warehouse_children(self):
        for rec in self:
            for location in self.env['stock.location'].sudo().search([('location_id', '=', rec.id)]):
                if rec.warehouse_id:
                    if location.warehouse_id:
                        if location.warehouse_id.id != rec.warehouse_id.id:
                            location.write({'warehouse_id': rec.warehouse_id.id})
                    else:
                        location.write({'warehouse_id': rec.warehouse_id.id})
                elif location.warehouse_id:
                    location.write({'warehouse_id': False})

    @api.multi
    def get_parent(self):
        stock_locations = []
        for rec in self:
            if rec.location_id:
                stock_locations.append(rec.location_id)
                stock_locations.extend(rec.location_id.get_parent())
        return stock_locations

    @api.multi
    def get_children(self):
        stock_locations = []
        for rec in self:
            if self.env['stock.location'].sudo().search([('location_id', '=', rec.id)]):
                stock_locations.extend(
                    [loca for loca in self.env['stock.location'].sudo().search([('location_id', '=', rec.id)])])
                for location in self.env['stock.location'].sudo().search([('location_id', '=', rec.id)]):
                    stock_locations.extend(location.get_children())
        return stock_locations

    @api.constrains('location_id')
    def constrains_location_id(self):
        for rec in self:
            list_location = [location.id for location in (rec.get_parent() + rec.get_children() + [rec])]
            warehouse = self.env['stock.warehouse'].sudo().search([('view_location_id', 'in', list_location)], limit=1)
            if warehouse:
                list_children = warehouse.view_location_id.get_children()
                for i in list_children:
                    if not i.warehouse_id:
                        rec.write({'warehouse_id': rec.location_id.sudo().warehouse_id.id})
                    elif i.warehouse_id.id != warehouse.id:
                        rec.write({'warehouse_id': rec.location_id.sudo().warehouse_id.id})
            else:
                for i in (rec.get_parent() + rec.get_children() + [rec]):
                    if i.warehouse_id:
                        rec.write({'warehouse_id': False})


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def create(self, vals):
        res = super(Warehouse, self).create(vals)
        if res.view_location_id:
            res.view_location_id.sudo().write({'warehouse_id': res.id})
        return res


class StockMove(models.Model):
    _inherit = "stock.move"

    sea_transaction_id = fields.Many2one('transaction.type', 'Transaction')
    asset_code_id = fields.Many2one('account.asset.asset', 'Asset Code')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')
    account_id = fields.Many2one('account.account', string='Account')

    @api.onchange('product_id')
    def _onchange_transaction_get_account(self):
        self.ensure_one()
        if self.product_id:
            self.sea_transaction_id = self.picking_id.sea_transaction_id.id

            analytic_account = self.env['account.determination'].search(
                [('transaction_id', '=', self.sea_transaction_id.id)])
            if analytic_account:
                for acc in analytic_account:
                    if acc.location_id == self.location_dest_id:
                        self.analytic_account_id = acc.analytic_account_id
                        self.analytic_tag_ids = acc.analytic_tag_ids
                    elif not acc.location_id:
                        self.analytic_account_id = acc.analytic_account_id
                        self.analytic_tag_ids = acc.analytic_tag_ids

    @api.onchange('move_line_ids', 'sea_transaction_id')
    def _add_domain_dest_location(self):
        if self.move_line_ids and self.sea_transaction_id:
            for line in self.move_line_ids:
                if self.sea_transaction_id.dest_location_id:
                    if not self.to_refund:
                        line.location_dest_id = self.sea_transaction_id.dest_location_id.id

    @api.model
    def _prepare_account_move_line(self, qty, cost,
                                   credit_account_id, debit_account_id):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id)
        for line in res:
            line[2]['asset_code_id'] = self.asset_code_id.id
            line[2]['transaction_item_id'] = self.sea_transaction_id.id
        return res

    # def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id,
    #                                    credit_account_id):
    #     # This method returns a dictionary to provide an easy extension hook to modify the valuation lines
    #     # (see purchase for an example)
    #     self.ensure_one()
    #     if self._context.get('forced_ref'):
    #         ref = self._context['forced_ref']
    #     else:
    #         ref = self.picking_id.name
    #
    #     analytic_account = {}
    #     analytic_tag = {}
    #     if self.analytic_account_id:
    #         analytic_account = self.analytic_account_id.id
    #     if self.analytic_tag_ids:
    #         for tag in self.analytic_tag_ids:
    #             analytic_tag = tag.id
    #
    #     debit_line_vals = {
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'quantity': qty,
    #         'product_uom_id': self.product_id.uom_id.id,
    #         'ref': ref,
    #         'partner_id': partner_id,
    #         'debit': debit_value if debit_value > 0 else 0,
    #         'credit': -debit_value if debit_value < 0 else 0,
    #         'account_id': debit_account_id,
    #         'analytic_account_id': analytic_account,
    #         'analytic_tag_ids': [(4, analytic_tag)],
    #     }
    #
    #     credit_line_vals = {
    #         'name': self.name,
    #         'product_id': self.product_id.id,
    #         'quantity': qty,
    #         'product_uom_id': self.product_id.uom_id.id,
    #         'ref': ref,
    #         'partner_id': partner_id,
    #         'credit': credit_value if credit_value > 0 else 0,
    #         'debit': -credit_value if credit_value < 0 else 0,
    #         'account_id': credit_account_id,
    #     }
    #
    #     rslt = {'credit_line_vals': credit_line_vals, 'debit_line_vals': debit_line_vals}
    #     if credit_value != debit_value:
    #         # for supplier returns of product in average costing method, in anglo saxon mode
    #         diff_amount = debit_value - credit_value
    #         price_diff_account = self.product_id.property_account_creditor_price_difference
    #         if not price_diff_account:
    #             price_diff_account = self.product_id.categ_id.property_account_creditor_price_difference_categ
    #         if not price_diff_account:
    #             raise UserError(_(
    #                 'Configuration error. Please configure the price difference account on the product or its category to process this operation.'))
    #
    #         rslt['price_diff_line_vals'] = {
    #             'name': self.name,
    #             'product_id': self.product_id.id,
    #             'quantity': qty,
    #             'product_uom_id': self.product_id.uom_id.id,
    #             'ref': ref,
    #             'partner_id': partner_id,
    #             'credit': diff_amount > 0 and diff_amount or 0,
    #             'debit': diff_amount < 0 and -diff_amount or 0,
    #             'account_id': price_diff_account.id,
    #         }
    #     return rslt
    # @api.model
    # def create(self, values):
    #     rec = super(StockMove, self).create(values)
    #     if values:
    #         print('Values', values)
    #     return rec


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    sea_transaction_id = fields.Many2one('transaction.type', 'Transaction')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')

    @api.onchange('qty_done')
    def _onchange_transaction_analytic(self):
        if self.qty_done:
            for line in self:
                if self.move_id.sea_transaction_id:
                    line.sea_transaction_id = self.move_id.sea_transaction_id

    @api.model
    def create(self, values):
        if values['move_id']:
            move = self.env['stock.move'].browse(values['move_id'])
            if move.sea_transaction_id and move.sea_transaction_id.dest_location_id:
                if not move.to_refund:
                    values['location_dest_id'] = move.sea_transaction_id.dest_location_id.id
        return super(StockMoveLine, self).create(values)
