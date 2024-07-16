# -*- coding: utf-8 -*-
from odoo import models, fields


class AssetType(models.Model):
    _name = 'account.asset.type'
    _description = "Asset Type"

    name=fields.Char(string='Name')
    description=fields.Char(string='Description')
    active=fields.Boolean(string='Active',default=True)
    type_template = fields.Selection([('tscd', 'TSCD'), ('ccdc', 'CCDC'), ('ccdccpb', 'CCDCCPB')], required=True,string='Type Template')

