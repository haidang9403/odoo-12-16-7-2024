import calendar
import datetime

from odoo import fields, api, _
from odoo import models
from odoo.exceptions import ValidationError


class HREmployeeReport(models.Model):
    _name = 'hr.employee.report.bdns'
    _description = 'BIẾN ĐỘNG NHÂN SỰ'

    name = fields.Char(string="Name", default='DANH SÁCH BIẾN ĐỘNG NHÂN SỰ')
    from_date = fields.Date(string='Từ Ngày')
    to_date = fields.Date(string='Đến Ngày')
    update_date = fields.Date(string='Ngày Cập Nhật', default=lambda self: fields.Date.today())
    month = fields.Selection([(1, 'Tháng Một'),
                              (2, 'Tháng Hai'),
                              (3, 'Tháng Ba'),
                              (4, 'Tháng Tư'),
                              (5, 'Tháng Năm'),
                              (6, 'Tháng Sáu'),
                              (7, 'Tháng Bảy'),
                              (8, 'Tháng Tám'),
                              (9, 'Tháng Chín'),
                              (10, 'Tháng Mười'),
                              (11, 'Tháng Mười Một'),
                              (12, 'Tháng Mười Hai')], default=datetime.date.today().month)

    @api.model
    def year_selection(self):
        year = 2022
        year_list = []
        while year != 2201:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string="Năm", default=fields.Date.today().strftime("%Y"), required=True)
    total = fields.Integer(string='Tổng')
    bdns_companies = fields.One2many('hr.employee.report.bdns.companies', 'bdns_report_id', string='Nhân Sự')
    user_id = fields.Many2one('res.users', string="User ID")

    def action_remove_biendong_nhansu(self):
        return self.bdns_companies.unlink()

    def action_lay_ds_bdns(self):
        self.bdns_companies.unlink()
        # if not self.from_date:
        #     return
        # from_year=self.from_date.year
        # from_month=self.from_date.month
        # from_day=self.from_date.day
        # to_year=self.to_date.year
        # to_month=self.to_date.month
        # to_day=self.to_date.day
        self.update_date = fields.Date.today()
        for company in self.env.user.company_ids:
            if company.id != 1:

                current_month = fields.Datetime.now().month
                current_year = fields.Datetime.now().year
                '''Lao Dong Tang'''
                tang = self.env.cr.execute(
                    'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status != \'resigned\' and joining_date is not null and EXTRACT(MONTH FROM joining_date) = %s and EXTRACT(YEAR FROM joining_date) = %s',
                    (company.id, current_month, current_year))
                tang = self.env.cr.dictfetchall()
                employee_increase = len(tang)
                '''Lao Dong Giam'''
                giam = self.env.cr.execute(
                    'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status = \'resigned\' and resignation_date is not null and EXTRACT(MONTH FROM resignation_date) = %s and EXTRACT(YEAR FROM resignation_date) = %s',
                    (company.id, current_month, current_year))
                giam = self.env.cr.dictfetchall()
                employee_decrease = len(giam)
                '''Nghi Om Dau'''
                benh = self.env.cr.execute(
                    'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status = \'sick_leave\' and resignation_date is not null and EXTRACT(MONTH FROM resignation_date) <= %s and EXTRACT(YEAR FROM resignation_date) <= %s',
                    (company.id, current_month, current_year))
                benh = self.env.cr.dictfetchall()
                empployee_sick_leave = len(benh)
                '''Nghi Thai San'''
                thai_san = self.env.cr.execute(
                    'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and  company_id = %s and employee_current_status = \'maternity_leave\' and resignation_date is not null and EXTRACT(MONTH FROM resignation_date) <= %s and EXTRACT(YEAR FROM resignation_date) <= %s',
                    (company.id, current_month, current_year))
                thai_san = self.env.cr.dictfetchall()
                empployee_maternity_leave = len(thai_san)
                '''Khanh 13/10/2022'''
                '''Nghi khong luong'''
                khong_luong = self.env.cr.execute(
                    'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and  company_id = %s and employee_current_status = \'leaving\' and resignation_date is not null and EXTRACT(MONTH FROM resignation_date) <= %s and EXTRACT(YEAR FROM resignation_date) <= %s',
                    (company.id, current_month, current_year))
                khong_luong = self.env.cr.dictfetchall()
                empployee_leaving = len(khong_luong)
                '''Tong lao dong'''
                current_employees = self.env.cr.execute(
                    'SELECT name FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status != \'resigned\' order by company_code,department_code,job_code,s_identification_id asc',
                    (company.id,))
                current_employees = self.env.cr.dictfetchall()
                employee_working_total = len(current_employees)
                # employee_working_total += (empployee_maternity_leave + empployee_sick_leave + empployee_leaving)
                employee_current_working_total = employee_working_total - (
                        empployee_maternity_leave + empployee_sick_leave + empployee_leaving)
                employee_previous_month_total = (employee_working_total - employee_increase) + employee_decrease
                bdns_companie = self.env['hr.employee.report.bdns.companies'].sudo().create({
                    'bdns_report_id': self.id,
                    'company_name': company.name,
                    'company_id': company.id,
                    'employee_working_total': employee_working_total,
                    'employee_current_working_total': employee_current_working_total,
                    'nghi_thai_san': empployee_maternity_leave,
                    'nghi_om_dau': empployee_sick_leave,
                    'nghi_khong_luong': empployee_leaving,
                    'employee_increase': employee_increase,
                    'employee_decrease': employee_decrease,
                    'employee_previous_month_total': employee_previous_month_total,
                })
                if bdns_companie:
                    for current_employee in current_employees:
                        self.env['hr.employee.report.bdns.lines'].sudo().create({
                            'bdns_company_id': bdns_companie.id,
                            'employee_id': current_employee['name']})
                ''''''
                # current_employees=self.env['hr.employee'].sudo().search([('company_id','=',company.id),('active','=','true')],order='job_id asc, s_identification_id asc')
                # previous_month_employees=self.env['hr.employee'].sudo().search([('company_id','=',company.id),('active','=','true')])
                # employee_current_working_total=0
                # employee_working_total=0
                # employee_previous_month_total=0
                # empployee_maternity_leave=0
                # empployee_sick_leave=0
                # employee_decrease=0
                # employee_increase=0
                # if current_employees:
                #     for current_employee in current_employees:
                #         if current_employee.employee_current_status !='resigned':
                #             employee_working_total += 1
                #             if current_employee.joining_date:
                #                 if current_employee.joining_date.year==from_year:
                #                     if current_employee.joining_date.month>=from_month and current_employee.joining_date.month<=to_month:
                #                         if current_employee.joining_date.day>=from_day and current_employee.joining_date.day<=to_day:
                #                             employee_increase+=1
                #         if current_employee.employee_current_status=='maternity_leave':
                #             if current_employee.leaving_to_date:
                #                 if current_employee.leaving_to_date>self.from_date:
                #                     empployee_maternity_leave+=1
                #         elif current_employee.employee_current_status=='sick_leave':
                #             if current_employee.leaving_to_date > self.from_date:
                #                 empployee_sick_leave += 1
                #         elif current_employee.employee_current_status=='resigned':
                #             if current_employee.resignation_date:
                #                 if current_employee.resignation_date.year== from_year:
                #                     if current_employee.resignation_date.month>=from_month and current_employee.resignation_date.month<= to_month:
                #                         if current_employee.resignation_date.day>=from_day and current_employee.resignation_date.day<=to_day:
                #                             employee_decrease+=1
                #     employee_working_total+=(empployee_maternity_leave+empployee_sick_leave)
                #     employee_current_working_total=employee_working_total-(empployee_maternity_leave+empployee_sick_leave)
                #     employee_previous_month_total=(employee_working_total-employee_increase)+employee_decrease
                # bdns_companie=self.env['hr.employee.report.bdns.companies'].sudo().create({
                #     'bdns_report_id':self.id,
                #     'company_name':company.name,
                #     'company_id':company.id,
                #     'employee_working_total':employee_working_total,
                #     'employee_current_working_total':employee_current_working_total,
                #     'nghi_thai_san':empployee_maternity_leave,
                #     'nghi_om_dau':empployee_sick_leave,
                #     'employee_increase':employee_increase,
                #     'employee_decrease':employee_decrease,
                #     'employee_previous_month_total':employee_previous_month_total,
                # })
                # if bdns_companie:
                #     for current_employee in current_employees:
                #         if current_employee.employee_current_status !='resigned':
                #             self.env['hr.employee.report.bdns.lines'].sudo().create({
                #                 'bdns_company_id':bdns_companie.id,
                #                 'employee_id': current_employee.id})

    def print_biendong_nhansu(self):
        # if self.update_date and self.from_date and self.to_date:
        return self.env.ref('sea_employee_reports.action_report_biendong_nhansu').report_action(self)

    '''Khánh 10/01/2023'''
    def action_lay_ds_bdns_theo_month(self, user):
        for rec in self:
            rec.bdns_companies.unlink()
            rec.update_date = fields.Date.today() if int(rec.month) == int(datetime.date.today().month) and int(
                rec.year) == int(datetime.date.today().year) else datetime.date(int(rec.year), rec.month, int(
                calendar.monthrange(int(rec.year), rec.month)[1]))
            for company in user.company_ids:
                if company.id != 1:

                    current_month = rec.month
                    current_year = rec.year
                    current_date = fields.Date.today() if int(rec.month) == int(datetime.date.today().month) and int(
                        rec.year) == int(datetime.date.today().year) else datetime.date(int(rec.year), rec.month, int(
                        calendar.monthrange(int(rec.year), rec.month)[1]))
                    '''Lao Dong Tang'''
                    tang = self.env.cr.execute(
                        'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status != \'resigned\' and joining_date is not null and EXTRACT(MONTH FROM joining_date) = %s and EXTRACT(YEAR FROM joining_date) = %s',
                        (company.id, current_month, current_year))
                    tang = self.env.cr.dictfetchall()
                    employee_increase = len(tang)
                    '''Lao Dong Giam'''
                    giam = self.env.cr.execute(
                        'SELECT * FROM hr_employee_multi_company a WHERE a.active = true and company_id = %s and employee_current_status = \'resigned\' and resignation_date is not null and EXTRACT(MONTH FROM resignation_date) = %s and EXTRACT(YEAR FROM resignation_date) = %s',
                        (company.id, current_month, current_year))
                    giam = self.env.cr.dictfetchall()
                    employee_decrease = len(giam)

                    # print("Tăng")
                    # print(tang)
                    # print(len(tang))
                    # print("\n\n")
                    # '''Lao Dong Giam'''
                    # print("Giảm")
                    # print(giam)
                    # print(len(giam))
                    # print("\n\n")

                    '''lao dong nghi'''
                    benh = self.env.cr.execute(
                        'SELECT * FROM hr_employee_multi_company a INNER JOIN sea_employee_history_current_status b \
                        on a.active = True and b.active = True and a.company_id = %s and b.resignation_date <= %s and \
                        b.employee_current_status = \'sick_leave\' and \
                        (b.leaving_to_date >= %s or b.leaving_to_date is null) and b.employee_multi_id = a.id',
                        (company.id, current_date, current_date))
                    benh = self.env.cr.dictfetchall()
                    empployee_sick_leave = len(benh)
                    # print("benh")
                    # print(benh)
                    # print(empployee_sick_leave)
                    # print('\n\n')

                    thai_san = self.env.cr.execute(
                        'SELECT * FROM hr_employee_multi_company a INNER JOIN sea_employee_history_current_status b \
                        on a.active = True and b.active = True and a.company_id = %s and b.resignation_date <= %s and \
                        b.employee_current_status = \'maternity_leave\' and \
                        (b.leaving_to_date >= %s or b.leaving_to_date is null) and b.employee_multi_id = a.id',
                        (company.id, current_date, current_date))
                    thai_san = self.env.cr.dictfetchall()
                    empployee_maternity_leave = len(thai_san)
                    # print("thai san")
                    # print(thai_san)
                    # print(empployee_maternity_leave)
                    # print('\n\n')

                    khong_luong = self.env.cr.execute(
                        'SELECT * FROM hr_employee_multi_company a INNER JOIN sea_employee_history_current_status b \
                        on a.active = True and b.active = True and a.company_id = %s and b.resignation_date <= %s and \
                        b.employee_current_status = \'leaving\' and \
                        (b.leaving_to_date >= %s or b.leaving_to_date is null) and b.employee_multi_id = a.id',
                        (company.id, current_date, current_date))
                    khong_luong = self.env.cr.dictfetchall()
                    empployee_leaving = len(khong_luong)
                    # print("khong luong")
                    # print(khong_luong)
                    # print(empployee_leaving)
                    # print('\n\n')

                    '''Tong lao dong'''
                    current_employees = self.env['hr.employee.multi.company'].sudo().search(
                        ['&',
                         '|', ('joining_date', '<=', current_date), ('joining_date', 'in', [False, None]),
                         '|', ('employee_current_status', '!=', 'resigned'),
                         '&', ('employee_current_status', '=', 'resigned'), ('resignation_date', '>', current_date),
                         ('company_id', '=', company.id)],
                        order='company_code,department_code,job_code,s_identification_id asc')
                    # print("tong lđ")
                    # print(company.short_name)
                    # print(current_employees)
                    # print(len(current_employees))
                    # print("\n\n")

                    # '''lao dong nghi'''
                    # not_working = []
                    # for b in benh:
                    #     not_working.append(b.id)
                    # for ts in thai_san:
                    #     not_working.append(ts.id)
                    # for kl in khong_luong:
                    #     not_working.append(kl.id)
                    #
                    # print("LĐ nghỉ: ", not_working)
                    #
                    # '''LĐ đang làm việc'''
                    # empployee_list_working = self.env['hr.employee.multi.company'].sudo().search(
                    #     ['&',
                    #      '|', ('joining_date', '<=', fields.Date.today()), ('joining_date', 'in', [False, None]),
                    #      '|', ('employee_current_status', '!=', 'resigned'),
                    #      '&', ('employee_current_status', '=', 'resigned'), ('resignation_date', '>', fields.Date.today()),
                    #      ('company_id', '=', company.id), ('id', 'not in', not_working)],
                    #     order='company_code,department_code,job_code,s_identification_id asc')
                    #
                    # print("tong lđ đang làm việc")
                    # print(company.short_name)
                    # print(empployee_list_working)
                    # print(len(empployee_list_working))
                    # print("\n\n")

                    '''Tong lao dong'''
                    employee_working_total = len(current_employees)
                    employee_current_working_total = employee_working_total - (
                            empployee_maternity_leave + empployee_sick_leave + empployee_leaving)
                    employee_previous_month_total = (employee_working_total - employee_increase) + employee_decrease
                    bdns_companie = self.env['hr.employee.report.bdns.companies'].sudo().create({
                        'bdns_report_id': rec.id,
                        'company_name': company.name,
                        'company_id': company.id,
                        'employee_working_total': employee_working_total,
                        'employee_current_working_total': employee_current_working_total,
                        'nghi_thai_san': empployee_maternity_leave,
                        'nghi_om_dau': empployee_sick_leave,
                        'nghi_khong_luong': empployee_leaving,
                        'employee_increase': employee_increase,
                        'employee_decrease': employee_decrease,
                        'employee_previous_month_total': employee_previous_month_total,
                    })
                    if bdns_companie:
                        for current_employee in current_employees:
                            self.env['hr.employee.report.bdns.lines'].sudo().create({
                                'bdns_company_id': bdns_companie.id,
                                'employee_id': current_employee.name.id})

    def print_biendong_nhansu_theo_month(self):
        # if self.update_date and self.from_date and self.to_date:
        return self.env.ref('sea_employee_reports.action_report_biendong_nhansu_theo_month').report_action(self)


class HREmployeeReportInherit(models.Model):
    _name = 'hr.employee.report.bdns.lines'
    _description = 'Biến Động Nhân Sự Lines'

    bdns_company_id = fields.Many2one('hr.employee.report.bdns.companies', string='Biến Động Nhân Sự ID',
                                      ondelete='cascade')

    employee_id = fields.Many2one('hr.employee', string='Employee ID')

    def _compute_employee_s_identification_id(self):
        for rec in self:
            if rec.employee_id:
                employees = self.env['hr.employee'].sudo().search([('id', '=', rec.employee_id.id)])
                for employee in employees:
                    rec.employee_s_identification_id = employee.s_identification_id
                    rec.employee_name = employee.name
                    rec.employee_msthue = employee.tax_tncn_code
                    rec.employee_health_insurance_number = employee.health_insurance_number
                    rec.employee_current_status = employee.employee_current_status
                    contract = self.env['hr.contract'].sudo().search([('employee_id', '=', rec.employee_id.id)],
                                                                     order='date_start desc', limit=1)
                    if contract:
                        rec.employee_contract = contract

    employee_s_identification_id = fields.Char(string='Mã NV', compute='_compute_employee_s_identification_id')

    def _compute_employee_name(self):
        pass

    employee_name = fields.Char(string='Họ Và Tên', compute='_compute_employee_name')

    def _compute_msthue(self):
        pass

    employee_msthue = fields.Char(string='Mã Số Thuế', compute='_compute_msthue')

    def _compute_employee_so_nguoi_phuthuoc(self):
        pass

    employee_so_nguoi_phuthuoc = fields.Integer(string='Số Người Phụ Thuộc',
                                                compute='_compute_employee_so_nguoi_phuthuoc')

    def _compute_employee_health_insurance_number(self):
        pass

    employee_health_insurance_number = fields.Char(string='Số BHYT',
                                                   compute='_compute_employee_health_insurance_number')

    def _compute_employee_contract(self):
        pass

    employee_contract = fields.Many2one('hr.contract', string='Contract', compute='_compute_employee_contract')

    def _compute_employee_current_status(self):
        pass

    employee_current_status = fields.Selection([
        ('working', 'Đang làm việc'),
        ('leaving', 'Nghỉ không lương'),
        ('maternity_leave', 'Nghỉ thai sản'),
        ('sick_leave', 'Nghỉ ốm đau'),
        ('resigned', 'Đã nghỉ việc')], compute='_compute_employee_current_status')


class HRCompanyReport(models.Model):
    _name = 'hr.employee.report.bdns.companies'
    _description = 'Biến Động Nhân Sự Công Ty'

    bdns_report_id = fields.Many2one('hr.employee.report.bdns', string='Biến Động Nhân Sự ID')
    company_name = fields.Char(string='Công Ty')
    company_id = fields.Many2one('res.company', string='Công Ty ID')
    employee_working_total = fields.Integer(string='Tổng Lao Động')
    employee_current_working_total = fields.Integer(string='Tổng Lao Động Làm Việc')
    employee_increase = fields.Integer(string='Tăng')
    employee_decrease = fields.Integer(string='Giảm')

    nghi_thai_san = fields.Integer(string='Nghỉ Thai Sản')
    nghi_om_dau = fields.Integer(string='Nghỉ Ốm Đau')
    # Khanh 13/10/2022
    nghi_khong_luong = fields.Integer(string='Nghỉ Không Lương')
    employee_resign_total = fields.Integer(string='Tổng Nghỉ Việc')
    employee_previous_month_total = fields.Integer(string='Tổng Lao Động Tháng Trước')
    bdns_employees = fields.One2many('hr.employee.report.bdns.lines', 'bdns_company_id', string='Nhân Sự')


class EmployeeReportBDNS(models.TransientModel):
    _name = 'hr.employee.report.temp.bdns'

    month = fields.Selection([(1, 'Tháng Một'),
                              (2, 'Tháng Hai'),
                              (3, 'Tháng Ba'),
                              (4, 'Tháng Tư'),
                              (5, 'Tháng Năm'),
                              (6, 'Tháng Sáu'),
                              (7, 'Tháng Bảy'),
                              (8, 'Tháng Tám'),
                              (9, 'Tháng Chín'),
                              (10, 'Tháng Mười'),
                              (11, 'Tháng Mười Một'),
                              (12, 'Tháng Mười Hai')], default=datetime.date.today().month, required=True,
                             string='Tháng')

    @api.model
    def year_selection(self):
        year = 2022
        year_list = []
        while year != 2201:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string="Năm", default=fields.Date.today().strftime("%Y"), required=True)

    def action_lay_ds_bdns(self):
        self.ensure_one()
        rec = self.env['hr.employee.report.bdns'].sudo().search(
            [('month', '=', self.month), ('year', '=', self.year), ('create_uid', '=', self.env.user.id)])
        if rec:
            res_id = rec
            res_id.action_lay_ds_bdns_theo_month(self.env.user)
        else:
            res_id = self.env['hr.employee.report.bdns'].sudo().create({'month': self.month, 'year': self.year})
            res_id.action_lay_ds_bdns_theo_month(self.env.user)
        return {
            'name': _('DANH SÁCH BIẾN ĐỘNG NHÂN SỰ'),
            'res_model': 'hr.employee.report.bdns',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': res_id.id if res_id else False,
            'view_id': self.env.ref(
                'sea_employee_reports.employee_report_biendong_nhansu_theo_month_action_form_view').id,
            'type': 'ir.actions.act_window',
            'context': {
                'create': 0, 'delete': 0, 'edit': 0}
        }

    @api.model
    def create(self, vals):
        current_month = datetime.date.today().month
        current_year = fields.Date.today().strftime("%Y")
        if vals['year'] < current_year or vals['year'] == current_year and vals['month'] <= current_month:
            return super(EmployeeReportBDNS, self).create(vals)
        else:
            raise ValidationError("Bạn không thể chọn tháng năm lớn hơn hiện tại")
            return True


class HRCompanyReport(models.Model):
    _inherit = 'hr.employee'

    @api.multi
    def print_lao_dong_nu_report(self):
        employees = self.env['hr.employee'].sudo().search([('active', '=', True), ('gender', '=', 'female')])
        list_employee_ids = []
        for employee in employees:
            multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                [('name', '=', employee.id), ('employee_current_status', '!=', 'resigned')])
            if multi_companies:
                list_employee_ids.append(employee.id)
        brs_employees = self.env['hr.employee'].sudo().browse(list_employee_ids)
        return self.env.ref('sea_employee_reports.action_report_lao_dong_nu').report_action(brs_employees)

    @api.multi
    def print_quoc_te_thieu_nhi_report(self):
        employees = self.env['hr.employee'].sudo().search([('active', '=', True)])
        return self.env.ref('sea_employee_reports.action_report_quoc_te_thieu_nhi').report_action(employees)

    @api.multi
    def print_tai_ky_report(self):
        employees = self.env['hr.employee.multi.company'].sudo().search(
            [('active', '=', True)])
        return self.env.ref('sea_employee_reports.action_report_tai_ky').report_action(employees)


class EmployeeReportBirthday(models.TransientModel):
    _name = 'hr.employee.report.birthday'

    month = fields.Selection([(1, 'Tháng 1'),
                              (2, 'Tháng 2'),
                              (3, 'Tháng 3'),
                              (4, 'Tháng 4'),
                              (5, 'Tháng 5'),
                              (6, 'Tháng 6'),
                              (7, 'Tháng 7'),
                              (8, 'Tháng 8'),
                              (9, 'Tháng 9'),
                              (10, 'Tháng 10'),
                              (11, 'Tháng 11'),
                              (12, 'Tháng 12')], default=lambda self: fields.Datetime.now().month + 1)

    # def print_birthday(self):
    #     resigned = 'resigned'
    #     employees = self.env.cr.execute(
    #         'SELECT a.id  FROM hr_employee a, hr_department b, hr_job c  WHERE  a.department_id=b.id and a.job_id=c.id and birthday is not null and EXTRACT(MONTH FROM birthday) = %s and a.active=True order by EXTRACT(DAY FROM birthday), b.sort_name, c.sequence',
    #         (self.month,))
    #     employees = self.env.cr.dictfetchall()
    #     ids = []
    #     for employee in employees:
    #         ids.append(employee['id'])
    #     empls = self.env['hr.employee'].browse(ids)
    #     return self.env.ref('sea_employee_reports.action_report_birthday').report_action(empls)

    def print_birthday(self):
        resigned = 'resigned'
        employees = self.env.cr.execute(
            'SELECT a.id  FROM hr_employee a  WHERE birthday is not null and EXTRACT(MONTH FROM birthday) = %s and a.active=True order by EXTRACT(DAY FROM birthday)',
            (self.month,))
        employees = self.env.cr.dictfetchall()
        ids = []
        for employee in employees:
            ids.append(employee['id'])
        empls = self.env['hr.employee'].browse(ids)
        return self.env.ref('sea_employee_reports.action_report_birthday').report_action(empls)


class EmployeeReportManagerLeave(models.Model):
    _name = 'hr.employee.report.manager.leave'

    name = fields.Char(string="Name", default='DANH SÁCH NHÂN SỰ CÓ QLTT / CẤP TRÊN QLTT NGHỈ VIỆC')
    update_date = fields.Date(string='Ngày Cập Nhật', default=lambda self: fields.Date.today())
    employee_data_lines = fields.One2many('hr.employee.report.manager.leave.lines', 'report_ml_id')
    user_id = fields.Many2one('res.users', string="User ID")

    def action_remove_data_lines(self):
        return self.employee_data_lines.unlink()

    def get_report_manager_leave_data(self):
        self.sudo().employee_data_lines.unlink()
        self.update_date = fields.Date.today()
        sql = '''
                SELECT 
                    HREM.name as name,
                    EMP.id as id,
                    EMP.s_identification_id as SC_nhan_su,
                    COMPANY.name as cong_ty,
                    CASE
                        WHEN MUMANAGER.resignation_date is not null and MUMANAGER.employee_current_status = 'resigned' and MUMANAGER.resignation_date <= NOW()
                        THEN MUMANAGER.s_identification_id
                        ELSE NULL
                    END as SC_QLTT_da_nghi_viec_can_cap_nhat,
                    CASE
                        WHEN MUMANAGER.resignation_date is not null and MUMANAGER.employee_current_status = 'resigned' and MUMANAGER.resignation_date <= NOW()
                        THEN MANAGER.name
                        ELSE NULL
                    END as QLTT_da_nghi_viec_can_cap_nhat,
                    CASE
                        WHEN MUSMANAGER.resignation_date is not null and MUSMANAGER.employee_current_status = 'resigned' and MUSMANAGER.resignation_date <= NOW()
                        THEN MUSMANAGER.s_identification_id
                        ELSE NULL
                    END as SC_cap_tren_QLTT_da_nghi_viec_can_cap_nhat,
                    CASE
                        WHEN MUSMANAGER.resignation_date is not null and MUSMANAGER.employee_current_status = 'resigned' and MUSMANAGER.resignation_date <= NOW()
                        THEN SMANAGER.name
                        ELSE NULL
                    END as cap_tren_QLTT_da_nghi_viec_can_cap_nhat
                FROM hr_employee_multi_company AS EMP
                LEFT JOIN res_company AS COMPANY ON EMP.company_id = COMPANY.id
                LEFT JOIN hr_employee AS MANAGER ON  EMP.parent_id = MANAGER.id
                LEFT JOIN hr_employee AS SMANAGER ON EMP.super_manager_company = SMANAGER.id
                LEFT JOIN hr_employee AS HREM ON EMP.name = HREM.id
                LEFT JOIN hr_employee_multi_company AS MUMANAGER ON MUMANAGER.name = MANAGER.id AND MUMANAGER.company_id = EMP.company_id
                LEFT JOIN hr_employee_multi_company AS MUSMANAGER ON MUSMANAGER.name = SMANAGER.id AND MUSMANAGER.company_id = EMP.company_id
                WHERE 
                    EMP.employee_current_status = 'working'
                    AND EMP.active is TRUE
                    AND
                    (
                        (MUMANAGER.resignation_date is not null and MUMANAGER.employee_current_status = 'resigned' and MUMANAGER.resignation_date <= NOW())
                        OR
                        (MUSMANAGER.resignation_date is not null and MUSMANAGER.employee_current_status = 'resigned' and MUSMANAGER.resignation_date <= NOW())
                    )
        '''
        report_data = self.env.cr.execute(sql)
        report_data = self.env.cr.dictfetchall()

        for data in report_data:
            # employee = self.env['hr.employee.multi.company'].sudo().search([('id', '=', data.get('id'))], limit=1)
            self.env['hr.employee.report.manager.leave.lines'].sudo().create({
                'report_ml_id': self.id,
                # 'employee_id': employee.id,
                # 'employee_id': data.get('id'),
                'company_name': data.get('cong_ty'),
                'employee_scid': data.get('sc_nhan_su'),
                'employee_name': data.get('name'),
                'manager_name': data.get('qltt_da_nghi_viec_can_cap_nhat'),
                'manager_scid': data.get('sc_qltt_da_nghi_viec_can_cap_nhat'),
                'upper_manager_name': data.get('cap_tren_qltt_da_nghi_viec_can_cap_nhat'),
                'upper_manager_scid': data.get('sc_cap_tren_qltt_da_nghi_viec_can_cap_nhat'),
            })

    def call_view_action(self, user_id):
        action_values = self.env.ref('sea_employee_reports.employee_report_manager_leave_action_view').sudo().read()[0]
        res_id = self.env['hr.employee.report.manager.leave'].search([('user_id', '=', user_id)], limit=1)
        if not res_id:
            res_id = self.env['hr.employee.report.manager.leave'].create({'user_id': user_id})
        res_id.action_remove_data_lines()
        res_id.get_report_manager_leave_data()
        action_values.update({'res_id': res_id.id})
        return action_values

    def print_manager_leave(self):
        return self.env.ref('sea_employee_reports.action_report_manager_leave').report_action(self)


class EmployeeReportManagerLeaveLines(models.Model):
    _name = 'hr.employee.report.manager.leave.lines'

    report_ml_id = fields.Many2one('hr.employee.report.manager.leave')
    company_name = fields.Char(String="Tên công ty")
    employee_name = fields.Char(String="Tên nhân sự")
    employee_scid = fields.Char(String="Mã SC nhân sự")
    manager_name = fields.Char(String="Tên QLTT đã nghỉ việc")
    manager_scid = fields.Char(String="Mã SC QLTT đã nghỉ việc")
    upper_manager_name = fields.Char(String="Tên cấp trên QLTT đã nghỉ việc")
    upper_manager_scid = fields.Char(String="Mã SC cấp trên QLTT đã nghỉ việc")
    # employee_id = fields.Many2one('hr.employee.multi.company', string='Employee')
