from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sea_email_invoice = fields.Char('Email send Invoice')
