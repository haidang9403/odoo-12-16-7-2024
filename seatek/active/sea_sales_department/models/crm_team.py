from odoo import models, fields


class CRMTeam(models.Model):
    _inherit = "crm.team"

    def _get_sales_department_team(self):
        res = []
        for item in self.env.user.sea_user_department_ids:
            if self.env.user.company_id == item.company_id:
                res.append(item.id)
        if res:
            return res

    sales_department_id = fields.Many2one('sales.department', 'Sales Department',
                                          domain=lambda self: [('id', 'in', self._get_sales_department_team())])
