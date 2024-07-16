# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    advance_file_id = fields.Many2one('account.payment.res.file', domain="[('company_id', '=', company_id)]",
                                      string="Document Code")

    def _get_counterpart_move_line_vals(self, invoice=False):
        values = super(AccountPayment, self)._get_counterpart_move_line_vals(invoice)
        if self.advance_file_id:
            values['advance_file_id'] = self.advance_file_id.id
        return values

class AccountPaymentResFile(models.Model):
    _name = 'account.payment.res.file'
    _description = "Respective File Of Account Payment"

    active = fields.Boolean(string='Active', default=True)
    name = fields.Char(default='Advance Payment Request')
    description = fields.Char(string="Description")
    code = fields.Char(required=True, string="Code", unique=True)
    partner_id = fields.Many2one('res.partner', string="Applicant")
    account_payments = fields.One2many('account.payment', 'advance_file_id', string="Account payment")
    company_id = fields.Many2one(
        'res.company',
        string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    @api.onchange('code')
    def onchange_code(self):
        for rec in self:
            rec.name = rec.code

    @api.model
    def create(self, vals):
        vals['name'] = vals.get('code')
        # if not vals.get('partner_id') and vals.get('account_payments'):
        #     account_payment = self.env['account.payment'].sudo().search(
        #         [('id', 'in', vals['account_payments'][0][2])], limit=1).sudo()
        #     vals['partner_id'] = account_payment.partner_id.id if account_payment else False
        category = super(AccountPaymentResFile, self).create(vals)
        return category

    @api.multi
    def write(self, value):
        if value.get('code'):
            raise UserError(_('Bạn không được phép chỉnh sửa CODE.'))
        # for rec in self:
            # if not value.get('partner_id') and not rec.partner_id:
            #     account_payment = self.env['account.payment'].sudo().search(
            #         [('id', 'in', value['account_payments'][0][2] if value.get(
            #             'account_payments') else rec.account_payments.ids)], limit=1).sudo()
            #     value['partner_id'] = account_payment.partner_id.id if account_payment else False
        return super(AccountPaymentResFile, self).write(value)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, str(rec.code) + ' | ' + str(rec.description)))
        return result