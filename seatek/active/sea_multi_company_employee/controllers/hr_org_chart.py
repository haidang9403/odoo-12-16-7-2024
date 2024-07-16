# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.http import request
from odoo.addons.hr_org_chart.controllers.hr_org_chart import HrOrgChartController


class HrOrgChartController(HrOrgChartController):
    _managers_level = 2  # FP request

    def _prepare_employee_data(self, employee):
        # job = employee.sudo().employee_multi_company.job_id
        job = request.env['hr.employee.multi.company'].sudo().search(
            [('name', '=', employee.id), ('company_id', '=', request.env.user.company_id.id)], limit=1).job_id
        return dict(
            id=employee.id,
            name=employee.name,
            link='/mail/view?model=hr.employee&res_id=%s' % employee.id,
            job_id=job.id,
            job_name=job.name or '',
            direct_sub_count=len(employee.child_ids),
            indirect_sub_count=employee.child_all_count,
        )
