# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_uom_select = fields.Boolean('Unit select in sale order line')

