from odoo import models, fields, api, _


class SeaTimeKeeper(models.Model):
    _name = 'sea.timekeeper'
    _description = "Timekeeper Information"
    _sql_constraints = [('serial_number_uniq', 'unique(serial_number)',
                         'serial number is  already exist!!')]

    name = fields.Char(string='Name', required=1)
    serial_number = fields.Char(string="Serial Number", required=1)

    sea_office_id = fields.Many2one('sea.office', string='Office', required=1)


class SeaNetworkDomain(models.Model):
    _name = 'sea.network.domain'
    _description = "Network Domain Information"
    _sql_constraints = [('domain_uniq', 'unique(domain)',
                         'Domain is  already exist!!')]

    name = fields.Char(string='Name', required=1)
    domain = fields.Char(string="Domain", required=1)

    sea_office_id = fields.Many2one('sea.office', string='Office', required=1)


class SeaGPSLocation(models.Model):
    _name = 'sea.gps.location'
    _description = "GPS Location Information"
    _sql_constraints = [('gps_uniq', 'unique(gps)',
                         'GPS is  already exist!!')]

    name = fields.Char(string='Name', required=1)
    gps = fields.Char(string="GPS", required=1)

    sea_office_id = fields.Many2one('sea.office', string='Office', required=1)


# class SeaOffice(models.Model):
#     _inherit = 'sea.office'
#
#     timekeeper_id = fields.One2many('sea.timekeeper', 'sea_office_id', string="TimeKeeper")
#     network_domain_id = fields.One2many('sea.network.domain', 'sea_office_id', string="Network Domain")
#     gps_location_id = fields.One2many('sea.gps.location', 'sea_office_id', string="GPS Location")
