from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    env['account.tax.group'].set_tax_group_is_vat_vietnam()
