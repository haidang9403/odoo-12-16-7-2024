from odoo import api, fields, models
import datetime
from datetime import timedelta


class SeaDeliveryLogReport(models.Model):
    _name = 'delivery.packing.log.report'

    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())
    warehouse_id = fields.Many2one(
        'stock.warehouse', 'Warehouse', required=True)

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def button_export_xlsx_by_date(self):
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        warehouse_id = self.warehouse_id.id
        data = {
            'start_date': start_date - timedelta(hours=7),
            'end_date': end_date - timedelta(hours=7),
            'warehouse_id': warehouse_id
        }
        return self.env.ref('sea_report_delivery_packing_log.action_sea_delivery_log_report').report_action(self,
                                                                                                    data=data)
