# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sea_pos_region_name = fields.Selection([
        ('mien_bac', 'Miền Bắc'),
        ('mien_trung', 'Miền Trung'),
        ('mien_nam', 'Miền Nam')
    ], 'Pos Region Name')
