import datetime
from datetime import timedelta
from odoo import models, fields, api


class ExportInventoryAsset(models.TransientModel):
    _name = "export.inventory.asset"

    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())
    department_id = fields.Many2one('hr.department', 'Department',domain="[('company_id','=',company_id)]")
    location_id = fields.Many2one('sea.office', 'Location')
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id.id)
    type = fields.Selection([
        ('by_commitment', 'Commitment date'),
        ('by_invoice', 'Invoice date'),
    ], string='Type', required=1, default='by_commitment')

    @api.onchange('department_id')
    def _onchange_clear_department_id(self):
        if self.department_id:
            self.location_id = {}

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def export_xlsx(self):
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'company_id': self.company_id.ids,
        }
        if self.department_id:
            data.update({'department_id':self.department_id.sudo().id})
        if self.location_id:
            data.update({'location_id': self.location_id.id})
        return self.env.ref('sea_asset_base.action_export_inventory_asset').report_action(self, data=data)
