import datetime
from datetime import timedelta
from odoo import models, fields, api

class AssetInventoryReport(models.TransientModel):
    _name = "asset.inventory.report"

    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id.id)
    department_id = fields.Many2one('hr.department', 'Department',domain="[('company_id','=',company_id)]")
    location_id = fields.Many2one('sea.office', 'Location')

    def export_xlsx(self):
        data={}
        if self.department_id:
            data.update({'department_id':self.department_id.id})
        if self.location_id:
            data.update({'location_id': self.location_id.id})
        assets=self.env['account.asset.asset'].sudo().search([('sea_office_id','=',self.location_id.id)])
        data.update({'assets':assets})
        return self.env.ref('sea_asset_base.asset_inventory_report').report_action(self, data=data)
