import datetime
from datetime import timedelta
from odoo import models, fields, api


class AssetReport(models.TransientModel):
    _name = "asset.report"

    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now() - timedelta(days=1))
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id.id)
    department_id=fields.Many2one('hr.department',string='Department',domain="[('company_id','=',company_id)]")
    asset_type = fields.Selection([('tscd', 'TSCD'), ('ccdc', 'CCDC'), ('ccdccpb', 'CCDCCPB')], 'Asset Type')
    category_id = fields.Many2one('account.asset.category', string='Category')
    sea_office_id = fields.Many2one('sea.office', 'Location')
    latest_inventory_status = fields.Selection([
        ('good', 'Good'),
        ('damaged_waiting_for_repair', 'Damaged waiting for repair'),
        ('damaged_waiting_for_liquidation', 'Damaged waiting for liquidation'),
        ('self_destruct', 'Self destruct')],
        'Latest Inventory Status')
    latest_asset_transfer_date_from = fields.Datetime('Latest Asset Transfer Date From')
    latest_asset_transfer_date_to = fields.Datetime('Latest Asset Transfer Date To')
    asset_receive_date_from = fields.Datetime('Asset Receive Date From')
    asset_receive_date_to = fields.Datetime('Asset Receive Date To')
    type = fields.Selection([
        ('by_commitment', 'Commitment date'),
        ('by_invoice', 'Invoice date'),
    ], string='Type', required=1, default='by_commitment')

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

        department_id=False
        asset_type=False
        category_id=False
        sea_office_id=False
        latest_inventory_status=False
        latest_asset_transfer_date_from=False
        latest_asset_transfer_date_to=False
        asset_receive_date_from=False
        asset_receive_date_to=False
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'company_id': self.company_id.id
        }
        if self.department_id:
            data.update({'department_id':self.department_id.id})
        if self.asset_type:
            data.update({'asset_type': self.asset_type})
        if self.category_id:
            data.update({'category_id': self.category_id.id})
        if self.sea_office_id:
            data.update({'sea_office_id': self.sea_office_id.id})
        if self.latest_inventory_status:
            data.update({'latest_inventory_status': self.latest_inventory_status})
        if self.latest_asset_transfer_date_from:
            data.update({'latest_asset_transfer_date_from': self.latest_asset_transfer_date_from})
        if self.latest_asset_transfer_date_to:
            data.update({'latest_asset_transfer_date_to': self.latest_asset_transfer_date_to})
        if self.asset_receive_date_from:
            data.update({'asset_receive_date_from': self.asset_receive_date_from})
        if self.asset_receive_date_to:
            data.update({'asset_receive_date_to': self.asset_receive_date_to})
        # data = {
        #     'start_date': start_date,
        #     'end_date': end_date,
        #     'company_id': self.company_id.id,
        #     'department_id': department_id,
        #     'asset_type': asset_type,
        #     'category_id': category_id,
        #     'sea_office_id': sea_office_id,
        #     'latest_inventory_status': latest_inventory_status,
        #     'latest_asset_transfer_date_from': latest_asset_transfer_date_from,
        #     'latest_asset_transfer_date_to': latest_asset_transfer_date_to,
        #     'asset_receive_date_from': asset_receive_date_from,
        #     'asset_receive_date_to': asset_receive_date_to,
        # }
        return self.env.ref('sea_asset_base.action_asset_report_xls').report_action(self, data=data)
