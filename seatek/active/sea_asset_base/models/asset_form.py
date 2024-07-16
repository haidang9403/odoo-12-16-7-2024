# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetForm(models.Model):
    _name = 'fixed.asset.card'
    _description = "Asset form fixed asset card"

    so_bb = fields.Char('Số BB', required=True)
    date_bbbg = fields.Datetime('Ngày BBBG')
    create_date = fields.Date('Ngày tạo', default=fields.Date.today())
    department_id_deliver = fields.Many2one('hr.department', string='Đơn Vị Giao')
    department_id_receive = fields.Many2one('hr.department', string='Đơn Vị Nhận')

    employee_multi_id_ks = fields.Many2one('hr.employee.multi.company', string="Đại diện người KS", required=True)
    employee_multi_id_receive = fields.Many2one('hr.employee.multi.company', string="Đại diện người Nhận",
                                                required=True)

    office_location_from = fields.Many2one('sea.office', 'Office Location From', required=True)
    office_location_to = fields.Many2one('sea.office', 'Office Location To', required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('process', 'In Process'), ('done', 'Done'), ('canceled', 'Canceled')], default="draft",
        string="Trạng thái")
    transfer_type = fields.Selection([('internal', 'Internal'), ('Disposal', 'In Process')], string="Loại chuyển",
                                     required=True)

    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

    def compute_depreciation_board(self):
        pass

    def validate(self):
        pass
