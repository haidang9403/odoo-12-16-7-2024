from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    transaction_id = fields.Many2one('transaction.type', 'Transaction Type')
    date = fields.Date(required=True, states={'posted': [('readonly', False)]}, default=fields.Date.context_today)

    @api.onchange('transaction_id')
    def _onchange_transaction_stock_move(self):
        if self.line_ids:
            if self.line_ids:
                for line in self.line_ids:
                    line.update({
                        'transaction_item_id': self.transaction_id
                    })


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    transaction_item_id = fields.Many2one('transaction.type', 'Transaction')
    asset_code_id = fields.Many2one('account.asset.asset', 'Asset Code',
                                    domain=lambda self: [('company_id', '=', self.env.user.company_id.id)])
    advance_file_id = fields.Many2one('account.payment.res.file', domain="[('company_id', '=', company_id)]",
                                      string="Document Code")

class AccountMoveUpdateDate(models.TransientModel):
    _name = 'account.move.update.date'
    _description = 'Account Move Update Date'

    date = fields.Date('Date', required=True, default=fields.Date.context_today)

    def update_date(self):
        ids = self.env.context['active_ids']
        move_ids = self.env['account.move'].browse(ids)
        for move in move_ids:
            if move:
                move.update({'date': self.date})

class AccountReconciliation(models.AbstractModel):
    _inherit = 'account.reconciliation.widget'

    @api.model
    def _prepare_move_lines(self, move_lines, target_currency=False, target_date=False, recs_count=0):
        values=super(AccountReconciliation, self)._prepare_move_lines(move_lines,target_currency,target_date,recs_count)
        for value in values:
            line=move_lines.browse(value.get('id'))
            if line.advance_file_id:
                description=""
                if line.advance_file_id.description:
                    description=line.advance_file_id.description
                value.update({'advance_file_id':str(line.advance_file_id.code) +'|'+description})

        return values