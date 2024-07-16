from odoo import models


class AgedPartnerBalanceWizard(models.TransientModel):
    """Aged partner balance report wizard."""

    _inherit = 'aged.partner.balance.wizard'
