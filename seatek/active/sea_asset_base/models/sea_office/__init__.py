from odoo import models, fields


class SeaOffice(models.Model):
    _name = "sea.office"

    office_code = fields.Char('Office Code')
    name = fields.Char('Name')
    address = fields.Char('Address')
    active = fields.Boolean(default=True, help="Set active to false to hide the tax without removing it.")

