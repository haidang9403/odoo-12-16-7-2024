from odoo import api, models, fields
from odoo.http import request

class add_company_list(models.Model):
    _inherit = 'res.company'
    _description = "Short Name Companies"

    short_name = fields.Char(string='Short Name', required=False)
    code = fields.Char(string='Code', required=False)
    active=fields.Boolean(string='Active',default=True)

    _order = 'code asc'

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         if record.short_name:
    #             result.append((record.id, record.short_name))
    #         else:
    #             result.append((record.id, record.name))
    #     return result
class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super(IrHttp, self).session_info()
        user = request.env.user
        display_switch_company_menu = user.has_group('base.group_multi_company') and len(user.company_ids) > 1
        result['short_name_company']= {'current_company': (user.company_id.id, user.company_id.short_name), 'allowed_companies': [(comp.id, comp.short_name) for comp in user.company_ids if comp.active==True]} if display_switch_company_menu else False
        return result