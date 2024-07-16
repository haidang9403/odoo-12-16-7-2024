# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields

class Res_District(models.Model):
    _name = 'res.district'
    _description = 'List district of city'
    _order = 'name'

    name = fields.Char(string='District Name', required=True)
    madvhc = fields.Char(string='Mã ĐVHC', required=False)
    city_id = fields.Many2one('res.country.state', string='City ID', required=True)

    @api.model
    def get_import_templates(self):
        return [{
            'label': ('Import Template for District'),
            'template': '/seatek_employees_optional/static/xls/res_district.xls'
        }]
class Res_Id_Issue_Place(models.Model):
    _name = 'res.id.issue.place'
    _description = "List Id Issue Place"
    _order = 'name'

    name = fields.Char(string='Id Issue Place', require=True)

class Res_Country(models.Model):
    _inherit = 'res.country.state'

class Employees_Optional(models.Model):
    _inherit = 'hr.employee'

    health_insurance_number = fields.Text(string="Health Insurance Number")
    permanent_country_id = fields.Many2one('res.country', string="Country Name")
    permanent_city_id = fields.Many2one('res.country.state', string="City Name", domain= "[('country_id', '=', permanent_country_id)]")
    permanent_district_id = fields.Many2one('res.district', string="District Name", domain="[('city_id', '=', permanent_city_id)]")
    temporary_country_id = fields.Many2one('res.country', string="Country Name")
    temporary_city_id = fields.Many2one('res.country.state', string="City Name", domain="[('country_id', '=', temporary_country_id)]")
    temporary_district_id = fields.Many2one('res.district', string="District Name", domain="[('city_id', '=', temporary_city_id)]")
    id_issue_place = fields.Many2one('res.id.issue.place', string="ID Issue Place")

class Country(models.Model):
    _inherit = ['res.country']
    _description = 'List country'

    @api.model
    def get_import_templates(self):
        return [{
            'label': ('Import Template for Country'),
            'template': '/seatek_employees_optional/static/xls/res_country.xls'
        }]