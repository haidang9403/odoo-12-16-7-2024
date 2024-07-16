from odoo import models, fields, api

class HrDirectoryReportTemp(models.TransientModel):
    _name = "hr.directory.report.temp"

    company_ids = fields.Many2many('res.company', string='Companies', required=True)
    is_all_company = fields.Boolean('All Company', default=False)

    @api.onchange('is_all_company')
    def onchange_is_all_company(self):
        if self.is_all_company == True:
            self.company_ids = self.env['res.company'].sudo().search([(1, '=', 1)])

    @api.onchange('company_ids')
    def on_change_company_ids(self):
        if self.company_ids != self.env['res.company'].sudo().search([(1, '=', 1)]):
            self.is_all_company = False
        else:
            self.is_all_company = True

    def action_print_directory(self):
        ids = []
        for id in self.company_ids:
            ids.append(id.id)
        data = {'company_ids': ids}
        return self.env.ref('sea_hr_directory.report_directory').report_action(self, data=data)