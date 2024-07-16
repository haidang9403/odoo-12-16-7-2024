from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError, UserError


class SeatekInventoryReport(models.Model):
    _name = "inventory.period.report.month"
    _description = "Inventory Period Report Month"
