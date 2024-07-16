# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields

class Res_CiTy(models.Model):
    _name = 'res.city'
    _description = 'List Cities of Vietnamese'
    _order = 'name'

    name = fields.Char(string='City Name', required=True)
    madvhc = fields.Char(string= 'Mã ĐVHC', required=False)
    mabuuchinh = fields.Char(string='Mã Bưu Chính', required=False)
    phone_code = fields.Integer(string='Country Calling Code')
    country_code = fields.Many2one('res.country', string='Country Code', required=True)

class Res_District(models.Model):
    _name = 'res.district'
    _description = 'List district of city'
    _order = 'name'

    name = fields.Char(string = 'District Name', required=True)
    madvhc = fields.Char(string='Mã ĐVHC', required=False)
    city_madvhc = fields.Char(string ='City MaDVHC', required = True)
    city_id = fields.Many2one('res.city', string='City MaDVHC', required=True)

