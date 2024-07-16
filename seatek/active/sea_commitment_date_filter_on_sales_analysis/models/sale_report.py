# -*- coding: utf-8 -*-
from odoo import models, fields


class SaleReport(models.Model):
    _inherit = "sale.report"

    commitment_date = fields.Datetime('Commitment Date', readonly=True)
    sea_sale_channel_id = fields.Many2one('sale.channel', 'Sales Channel', readonly=True)
    sea_sale_department = fields.Selection([
        ('si', 'Sỉ'),
        ('le', 'Lẻ'),
    ], string='Sales Department', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['commitment_date'] = ", s.commitment_date AS commitment_date"
        fields['region_name'] = ", s.region_name AS region_name"
        fields['warehouse_id'] = ", s.warehouse_id AS warehouse_id"
        fields['sea_sale_channel_id'] = ", s.sea_sale_channel_id AS sea_sale_channel_id"
        fields['sea_sale_department'] = ", s.sea_sale_department AS sea_sale_department"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
