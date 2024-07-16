from odoo import api, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def create_from_ui(self, partner):
        if partner.get('group_ids'):
            partner['group_ids'] = [(6, 0, partner.get('group_ids'))]
        return super(ResPartner, self).create_from_ui(partner)
