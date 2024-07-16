from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_sales_department_user(self):
        res = []
        for item in self.env.user.sea_user_department_ids:
            if self.env.user.company_id == item.company_id:
                res.append(item.id)
        if res:
            return res

    sales_department_id = fields.Many2one('sales.department', 'Sales Department',
                                          domain=lambda self: [('id', 'in', self._get_sales_department_user())])

    @api.onchange('team_id')
    def _onchange_sales_department(self):
        if self.team_id.sales_department_id:
            self.sales_department_id = self.team_id.sales_department_id.id
