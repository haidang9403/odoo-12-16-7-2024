from datetime import datetime

from odoo import models, fields, api


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    mark_as_todo = fields.Boolean(string='Lock', default=False)
    total_debit = fields.Monetary(string='Total debit', compute='compute_debit', currency_field='currency_id')
    debit_overdue = fields.Monetary(string='Debit overdue', compute='compute_debit', currency_field='currency_id')

    check_debit_overdue = fields.Boolean(string='Check Debit overdue', default=False)
    # date_overdue_oldest = fields.Date(string='Date overdue oldest',
    #                                   compute='compute_date_overdue_oldest', default=datetime.today().date())
    days_past_due = fields.Integer(string='Days past due', compute='compute_days_past_due')

    policy_id = fields.Many2one('credit.policy', "Credit policy")

    def compute_days_past_due(self):
        for rec in self:
            oldest_date = False
            for line in self.env['account.move.line'].sudo(). \
                    search([('account_id', '=', rec.property_account_receivable_id.id),
                            ('partner_id', '=', rec.id),
                            ('debit', '>', 0), ('credit', '=', 0),
                            ('amount_residual', '>', 0),
                            ('company_id', '=', self.env.user.company_id.id),
                            ('date_maturity', '<', datetime.now()),
                            ('full_reconcile_id', '=', None)]):
                if line.date_maturity:
                    if oldest_date:
                        if oldest_date > line.date_maturity:
                            oldest_date = line.date_maturity
                    else:
                        oldest_date = line.date_maturity
            if oldest_date:
                rec.days_past_due = (
                        datetime.now().date() - oldest_date).days
            else:
                rec.days_past_due = oldest_date

    def compute_debit(self):
        for partner in self:
            total_debit_overdue = 0
            total_debit_not_yet_due = 0
            for line in self.env['account.move.line'].sudo(). \
                    search([
                ('account_id', '=', partner.property_account_receivable_id.id),
                ('partner_id', '=', partner.id),
                ('debit', '>', 0), ('credit', '=', 0),
                ('amount_residual', '>', 0),
                ('company_id', '=', self.env.user.company_id.id),
                ('full_reconcile_id', '=', None)]):
                if line.date_maturity < datetime.today().date():
                    total_debit_overdue += line.amount_residual
                else:
                    total_debit_not_yet_due += line.amount_residual

            partner.debit_overdue = total_debit_overdue
            partner.total_debit = total_debit_overdue + total_debit_not_yet_due
            if partner.debit_overdue > 0:
                partner.check_debit_overdue = True
            else:
                partner.check_debit_overdue = False

    @api.multi
    def view_all_debit(self):
        action = self.env.ref('sea_report_overdue_debit.action_account_move_line_total_debit').read()[0]
        action['domain'] = [('account_id', '=', self.property_account_receivable_id.id),
                            ('partner_id', '=', self.id),
                            ('debit', '>', 0), ('credit', '=', 0),
                            ('amount_residual', '>', 0),
                            ('company_id', '=', self.env.user.company_id.id),
                            ('full_reconcile_id', '=', None)]
        action['target'] = 'current'
        return action

    @api.multi
    def view_debit_overdue(self):
        action = self.env.ref('sea_report_overdue_debit.action_account_move_line_debit_due').read()[0]
        action['domain'] = [
            ('account_id', '=', self.property_account_receivable_id.id),
            ('partner_id', '=', self.id),
            ('debit', '>', 0), ('credit', '=', 0),
            ('amount_residual', '>', 0),
            ('company_id', '=', self.env.user.company_id.id),
            ('date_maturity', '<', datetime.now()),
            ('full_reconcile_id', '=', None)]
        action['target'] = 'current'
        return action

    @api.multi
    def view_oldest_debit(self):
        account_move_line = {}
        oldest_date = datetime.today().date()
        domain = [
            ('account_id', '=', self.property_account_receivable_id.id),
            ('partner_id', '=', self.id),
            ('debit', '>', 0), ('credit', '=', 0),
            ('amount_residual', '>', 0),
            ('company_id', '=', self.env.user.company_id.id),
            ('date_maturity', '<', datetime.now()),
            ('full_reconcile_id', '=', None)]

        for line in self.env['account.move.line'].sudo().search(domain):
            if line.date_maturity < oldest_date:
                oldest_date = line.date_maturity
                account_move_line = line
            if line.date_maturity == oldest_date:
                account_move_line += line
        action = self.env.ref('sea_report_overdue_debit.action_account_move_line_debit_oldest').read()[0]
        action['domain'] = [('id', 'in', account_move_line.mapped('id'))]
        action['target'] = 'current'
        return action

    @api.multi
    def check_data(self):
        self.env.cr.execute(""" 
            SELECT rp.id
            FROM res_partner AS rp
            JOIN account_move_line AS aml ON aml.partner_id = rp.id and rp.company_id = aml.company_id
            WHERE 
                rp.company_id = %s AND
                rp.customer = True AND
                aml.debit > 0 AND
                aml.credit = 0 AND
                aml.amount_residual > 0 AND
                aml.date_maturity < %s AND
                aml.full_reconcile_id IS NULL
            group by rp.id
            """, (self.env.user.company_id.id, datetime.now().date().strftime('%Y-%m-%d')))

        partners = self.env.cr.dictfetchall()
        res_partner = self.env['res.partner'].search(
            [('id', 'in', [res['id'] for res in partners])])
        # print("start: ", datetime.now())
        for partner in res_partner:
            self.env.cr.execute("""
                        SELECT *
                        FROM account_move_line
                        WHERE
                            account_id = %s AND
                            partner_id = %s AND
                            debit > 0 AND
                            credit = 0 AND
                            amount_residual > 0 AND
                            company_id = %s AND
                            date_maturity < %s AND
                            full_reconcile_id IS NULL;
                            """, (
                partner.property_account_receivable_id.id, partner.id, self.env.user.company_id.id,
                datetime.now().date().strftime('%Y-%m-%d')))

            # if self.env['account.move.line'].sudo(). \
            #         search([('account_id', '=', partner.property_account_receivable_id.id),
            #                 ('partner_id', '=', partner.id),
            #                 ('debit', '>', 0), ('credit', '=', 0),
            #                 ('amount_residual', '>', 0),
            #                 ('company_id', '=', self.env.user.company_id.id),
            #                 ('date_maturity', '<', datetime.now()),
            #                 ('full_reconcile_id', '=', None)]):
            if self.env.cr.dictfetchall():
                if not partner.check_debit_overdue:
                    partner.check_debit_overdue = True
            elif partner.check_debit_overdue:
                partner.check_debit_overdue = False
        # print("end: ", datetime.now())

    @api.model
    def action_open_report(self):
        self.check_data()
        data = self.env.ref('sea_report_overdue_debit.action_report_overdue_debit').read()[0]
        return data

    @api.multi
    def action_un_confirm(self):
        for rec in self:
            rec.mark_as_todo = False

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.mark_as_todo = True
