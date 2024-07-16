# -*- coding: utf-8 -*-
from odoo import models, fields, api
class PosConfig(models.Model):
    _inherit = "pos.config"

    default_cash_journal_id = fields.Many2one(
        'account.journal', string='Cash Control Journal',
        domain=[('type', '=', 'cash')],
        help="Cash Control Journal",
        )

    @api.multi
    def _compute_cash_all(self):
        # Your code goes here
        for session in self:
            session.cash_journal_id = session.cash_register_id = session.cash_control = False
            if session.config_id.cash_control:
                for statement in session.statement_ids:
                    if statement.journal_id.type == 'cash':
                        session.cash_control = True
                        session.cash_journal_id = statement.journal_id.id
                        session.cash_register_id = statement.id
                if not session.cash_control and session.state != 'closed':
                    raise UserError(_("Cash control can only be applied to cash journals."))

        return super(PosConfig, self)._compute_cash_all()
