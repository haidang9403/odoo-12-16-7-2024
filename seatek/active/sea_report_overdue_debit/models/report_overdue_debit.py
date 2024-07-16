from datetime import datetime

from odoo import api, fields, models


class ReportOverdueDebit(models.TransientModel):
    _name = "report.overdue.debit"
    _description = "Report Overdue Debit"

    partner_id = fields.Many2one('res.partner', 'Đối tượng', readonly=True)
    ref = fields.Char('Số tham chiếu', readonly=True)
    date_due = fields.Date('Ngày đến hạn')
    origin = fields.Char('Tài liệu gốc')
    debit = fields.Float('Số tiền phải trả', precision=2, scale=2)
    residual_signed = fields.Float('Số tiền còn lại phải trả', precision=2, scale=2)
    date_invoice = fields.Date('Ngày hóa đơn')

    def _get_data(self):
        company_id = self.env.user.company_id.id
        res_partner = self.env['res.partner'].search(
            ['&', ('company_id', '=', company_id), ('customer', '=', True)])
        for partner in res_partner:
            for line in self.env['account.move.line'].sudo(). \
                    search(['&',
                            ('account_id', '=', partner.property_account_receivable_id.id),
                            ('partner_id', '=', partner.id),
                            ('debit', '>', 0), ('credit', '=', 0),
                            ('amount_residual', '>', 0),
                            ('company_id', '=', company_id),
                            ('date_maturity', '<', datetime.now()),
                            ('full_reconcile_id', '=', None)]).sorted('date_maturity'):
                if line.amount_residual > 0:
                    val = {
                        'partner_id': partner.id,
                        'ref': line.ref,
                        'date_due': line.date_maturity,
                        'origin': line.move_id.ref,
                        'debit': line.debit,
                        'residual_signed': line.amount_residual
                    }
                    self.env['report.overdue.debit'].create(val)

    @api.model
    def action_open_report(self):
        self._delete_all_data()
        self._get_data()
        data = self.env.ref('sea_report_overdue_debit.action_report_overdue_debit').read()[0]
        return data

    def _delete_all_data(self):
        all_records = self.env['report.overdue.debit'].search([])
        all_records.unlink()

    def _get_data_invoice(self):
        company_id = self.env.user.company_id.id
        res_partner = self.env['res.partner'].search(
            ['&', ('company_id', '=', company_id), ('customer', '=', True)])
        for partner in res_partner:
            for line in self.env['account.move.line']. \
                    search(['&',
                            ('account_id', '=', partner.property_account_receivable_id.id),
                            ('partner_id', '=', partner.id),
                            ('debit', '>', 0), ('credit', '=', 0),
                            ('amount_residual', '>', 0),
                            ('company_id', '=', company_id),
                            ('date_maturity', '<', datetime.now()),
                            ('full_reconcile_id', '=', None)]).sorted('date_maturity'):
                if line.amount_residual > 0:
                    for invoice in self.env['account.invoice'].search(
                            [('buyer_id', '=', False), ('move_id', '=', line.move_id.id)]):
                        val = {
                            'partner_id': invoice.buyer_id.id,
                            'ref': invoice.reference,
                            'date_invoice': line.date,
                            'date_due': line.date_maturity,
                            'origin': invoice.origin,
                            'debit': line.debit,
                            'residual_signed': line.amount_residual
                        }
                        self.env['report.overdue.debit'].create(val)

    @api.model
    def action_open_report_invoice(self):
        self._delete_all_data()
        self._get_data_invoice()
        data = self.env.ref('sea_report_overdue_debit.action_report_overdue_invoice_debit').read()[0]
        return data
