from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    total_debit = fields.Monetary(string='Total debit', compute='compute_debit', currency_field='currency_id')
    debit_overdue = fields.Monetary(string='Debit overdue', compute='compute_debit', currency_field='currency_id')
    re_available_debit = fields.Monetary(string='Remaining available debit ', compute='compute_debit',
                                         currency_field='currency_id')
    re_available_overdue_debit = fields.Monetary(string='Remaining avalable overdue debit', compute='compute_debit',
                                                 currency_field='currency_id')

    # date_overdue_oldest = fields.Date(string='Date overdue oldest', default=datetime.today().date(), readonly=True,
    #                                   compute='compute_date_overdue_oldest')
    days_past_due = fields.Integer(string='Days past due', compute='compute_debit')
    state = fields.Selection(
        selection_add=[('validate', 'Validating')])
    user_validate = fields.Many2one('res.users', string="User Validating")
    policy_id = fields.Many2one('credit.policy', "Credit policy", related='partner_id.policy_id')

    @api.multi
    def view_all_f(self):
        return True

    @api.multi
    def action_confirm(self):
        for rec in self:
            check = False
            policy = rec.policy_id.sudo()
            if policy and rec.state == 'draft':
                if policy.check_longest_overdue_debt \
                        or policy.check_total_debt \
                        or policy.check_overdue_debt_limit:
                    if policy.check_total_debt:
                        if (rec.total_debit + rec.amount_total) >= policy.total_debt:
                            check = True
                    if not check and policy.overdue_debt_limit and policy.check_overdue_debt_limit:
                        if rec.debit_overdue >= policy.overdue_debt_limit:
                            check = True
                    if not check and policy.check_longest_overdue_debt and policy.longest_overdue_debt:
                        # if (datetime.now().date() - rec.date_overdue_oldest).days >= policy.longest_overdue_debt:
                        if rec.days_past_due >= policy.longest_overdue_debt:
                            check = True
            if check:
                rec.write({'state': 'validate'})
                return check
            else:
                if rec.state == 'validate':
                    rec.write({'user_validate': self.env.user.id})
                return super(SaleOrder, self).action_confirm()

    @api.multi
    def view_all_debit(self):
        for rec in self:
            return rec.partner_id.view_all_debit()

    @api.multi
    def view_debit_overdue(self):
        for rec in self:
            return rec.partner_id.view_debit_overdue()

    @api.multi
    def view_oldest_debit(self):
        for rec in self:
            return rec.partner_id.view_oldest_debit()

    @api.multi
    def compute_debit(self):
        for rec in self:
            if rec.partner_id:
                rec.total_debit = rec.partner_id.total_debit
                rec.debit_overdue = rec.partner_id.debit_overdue
                rec.days_past_due = rec.partner_id.days_past_due
                if rec.policy_id:
                    rec.re_available_debit = rec.policy_id.total_debt - rec.partner_id.total_debit
                    rec.re_available_overdue_debit = rec.policy_id.overdue_debt_limit - rec.partner_id.debit_overdue
            else:
                rec.debit_overdue = 0
                rec.total_debit = 0
                rec.days_past_due = 0
                rec.re_available_debit = 0
                rec.re_available_overdue_debit = 0

    @api.onchange('partner_id')
    def onchange_partner_id_view_debit_overdue(self):
        self.compute_debit()
