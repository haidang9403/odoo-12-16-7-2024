# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import datetime


class DeliveryInfoReport(models.Model):
    _name = 'delivery.info.report'

    date = fields.Datetime(string='Choose Date', default=fields.Datetime.now())

    def button_export_xlsx_by_date(self):
        date = datetime.datetime(year=self.date.year, month=self.date.month, day=self.date.day)
        start_date = datetime.datetime(year=self.date.year, month=self.date.month, day=self.date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.date.year, month=self.date.month, day=self.date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'start_date': start_date - datetime.timedelta(hours=7),
            'end_date': end_date - datetime.timedelta(hours=7),
            'date': date
        }
        return self.env.ref('sea_report_delivery_info.action_delivery_info_report_by_date').report_action(self,
                                                                                      data=data)
