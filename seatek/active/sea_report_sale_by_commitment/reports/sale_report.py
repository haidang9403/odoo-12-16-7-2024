# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from odoo import models, fields, api


class AccountingReport(models.TransientModel):
    _name = "sea.sale.order.report"

    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def button_export_xlsx_by_date(self):
        time_tz_7 = datetime.timedelta(hours=7)
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'company_id': self.company_id,
            'start_date': start_date - time_tz_7,
            'end_date': end_date - time_tz_7,
        }
        return self.env.ref(
            'sea_report_sale_by_commitment.action_sale_order_details_by_commitment_date').report_action(self,
                                                                                                                   data=data)