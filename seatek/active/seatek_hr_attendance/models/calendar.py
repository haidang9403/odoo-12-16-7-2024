import calendar
import datetime
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CalendarEmployee(models.Model):
    _name = 'sea.hr.calendar'
    _description = "Calendar for Month"
    _sql_constraints = [('model_month_year_company_uniq', 'unique(employee_multi_id,month,year,day,shifts)',
                         'Attendance with this month of company is  already exist!!')]
    _order = 'company_code,department_code,job_code,s_identification_id, year, month, day asc'

    @api.depends('employee_multi_id')
    def domain_employee_compute(self):
        for rec in self:
            if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_manager'):
                employee = self.env['hr.employee.multi.company'].sudo().search(
                    [('employee_current_status', '=', 'working'),
                     ('company_id', '=', self.env.user.company_id.id)])
                if employee:
                    rec.domain_employee = employee.ids
            else:
                if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                    employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)],
                        limit=1)
                    if employee_multi_id:
                        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                        if employee:
                            list_employee = [employee_multi_id.id]
                            department_list = self.env['hr.department'].sudo().search(
                                [('manager_ids', '=', employee.id)])
                            if department_list:
                                employee_department = self.env['hr.employee.multi.company'].sudo().search(
                                    [('department_id', 'in', department_list.ids)])
                                if employee_department:
                                    for i in employee_department:
                                        list_employee.append(i.id)
                            rec.domain_employee = list_employee

    domain_employee = fields.Many2many('hr.employee.multi.company', string='Domain', compute='domain_employee_compute')
    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên", required=True,
                                        domain="[('id', 'in', domain_employee)]")

    department_id = fields.Many2one('hr.department', string='Department', related='employee_multi_id.department_id',
                                    store=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_multi_id.job_id', store=True)
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)

    user_ids = fields.Many2many('res.users', string='Dành cho QLTT')

    '''dkh add for sorting'''

    def _compute_job_code_compute(self):
        for rec in self:
            rec.sudo().write({'job_code': rec.employee_multi_id.sudo().job_id.sudo().sequence})
            rec.sudo().write({'department_code': rec.employee_multi_id.sudo().department_id.sudo().sort_name})
            rec.sudo().write({'company_code': rec.company_id.sudo().code})

    job_code_compute = fields.Char(compute='_compute_job_code_compute')
    job_code = fields.Char(string='Job Code')
    department_code = fields.Char(string='Department Code')
    company_code = fields.Char(string='Company Code')

    company_id = fields.Many2one('res.company', string="Công ty", related='employee_multi_id.company_id', store=True)

    month = fields.Integer(string='Tháng')
    year = fields.Integer(string="Năm")
    day = fields.Integer(string="Ngày")
    calendar_employee = fields.Many2one('sea.hr.calendar.employee', string='')

    @api.onchange('employee_multi_id')
    def onchange_employee_multi_id(self):
        for rec in self:
            rec.domain_compute()

    def domain_compute(self):
        '''company'''
        for rec in self:
            # '''trừ ra những ca thuộc phòng ban khác của employee'''
            # department = self.env['sea.hr.attendance.shift'].sudo().search([])
            # id_shift = []
            # if department:
            #     for i in department:
            #         if i.department_id:
            #             if i.department_id.id != rec.employee_multi_id.sudo().department_id.id:
            #                 id_shift.append(i.id)
            #
            # shifts = rec.env['sea.hr.attendance.shift'].sudo().search(
            #     [('company_id', '=', rec.company_id.id), ('id', 'not in', id_shift)])
            shifts = rec.env['sea.hr.attendance.shift'].sudo().search(
                [('company_id', '=', rec.company_id.id)])

            rec.domain_day = shifts.ids

    domain_day = fields.Many2many('sea.hr.attendance.shift', string='Domain', compute='domain_compute')
    shifts = fields.Many2one('sea.hr.attendance.shift', string="Ca làm viêc", required=True,
                             domain="[('id', 'in', domain_day)]")

    date_from = fields.Datetime('Start Date', required=True)
    # , default=fields.Datetime.now())
    date_to = fields.Datetime('End Date', required=True)

    # , default=fields.Datetime.now())

    @api.constrains('shifts')
    def check_shifts(self):
        for rec in self:
            if rec.shifts:
                '''tính date_from - day_to'''
                if rec.shifts.sudo().type_of_shift == 'full_time_shift':
                    if rec.shifts.for_full_time_shift == 'check_in_day':
                        rec.date_to = rec.date_to + datetime.timedelta(days=1)
                    elif rec.shifts.for_full_time_shift == 'check_out_day':
                        rec.date_from = rec.date_from - datetime.timedelta(days=1)

                hour_start = rec.shifts.hour_start
                hour_end = rec.shifts.hour_end
                # Lấy phần nguyên là giờ
                hours_s = int(hour_start)
                hours_e = int(hour_end)
                # Lấy phần thập phân là phút, chuyển đổi về phút và lấy phần nguyên
                minutes_s = int((hour_start - hours_s) * 60)
                minutes_e = int((hour_end - hours_e) * 60)
                # Lấy phần thập phân của phút, chuyển đổi về giây và lấy phần nguyên
                seconds_s = int(((hour_start - hours_s) * 60 - minutes_s) * 60)
                seconds_e = int(((hour_end - hours_e) * 60 - minutes_e) * 60)

                if hours_s < 7:
                    hours = 7 - hours_s
                    hours_s = 24 - hours
                    rec.date_from = rec.date_from - datetime.timedelta(days=1)
                else:
                    hours_s -= 7
                if hours_e < 7:
                    hour = 7 - hours_e
                    hours_e = 24 - hour
                    rec.date_to = rec.date_to - datetime.timedelta(days=1)
                else:
                    hours_e -= 7

                rec.date_from = rec.date_from.replace(hour=hours_s, minute=minutes_s, second=seconds_s)
                rec.date_to = rec.date_to.replace(hour=hours_e, minute=minutes_e, second=seconds_e)

                # '''check thứ của ca và thứ của ngày chấm công'''
                # date_from = datetime.datetime.strptime(str(rec.date_from), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                #     hours=7)
                # date_to = datetime.datetime.strptime(str(rec.date_to), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                #     hours=7)
                # rec.day = date_from.day
                # rec.month = date_from.month
                # rec.year = date_from.year
                # if rec.shifts.sudo().for_full_time_shift == 'check_out_day' and \
                #         rec.shifts.sudo().type_of_shift == 'full_time_shift':
                #     rec.day = date_to.day
                #     rec.month = date_to.month
                #     rec.year = date_to.year
                #
                # date_ = int(date.weekday(date(int(rec.year), int(rec.month), int(rec.day))))
                # if rec.shifts.sudo().thu_2 and date_ == 0 \
                #         or rec.shifts.sudo().thu_3 and date_ == 1 \
                #         or rec.shifts.sudo().thu_4 and date_ == 2 \
                #         or rec.shifts.sudo().thu_5 and date_ == 3 \
                #         or rec.shifts.sudo().thu_6 and date_ == 4 \
                #         or rec.shifts.sudo().thu_7 and date_ == 5 \
                #         or rec.shifts.sudo().thu_8 and date_ == 6:
                #     pass
                # else:
                #     print('không trùng nè')
                #     thu = ''
                #     if date_ == 0:
                #         thu = 'Thứ hai'
                #     elif date_ == 1:
                #         thu = 'Thứ ba'
                #     elif date_ == 2:
                #         thu = 'thứ tư'
                #     elif date_ == 3:
                #         thu = 'thứ năm'
                #     elif date_ == 4:
                #         thu = 'thứ sáu'
                #     elif date_ == 5:
                #         thu = 'thứ bảy'
                #     elif date_ == 6:
                #         thu = 'chủ nhật'
                #     raise ValidationError("Ca " + str(rec.shifts.sudo().name) + ' không thuộc ' + str(thu))
                #
                '''check ca trùng nhau'''
                shifts = self.env['sea.hr.calendar'].sudo().search(
                    [('id', '!=', rec.id), ('employee_multi_id', '=', rec.employee_multi_id.id), ('day', '=', rec.day),
                     ('month', '=', rec.month), ('year', '=', rec.year)])
                if shifts:
                    list_attendance = [attendance.shifts for attendance in shifts]
                    list_0 = rec.shifts.duplicate_shifts(rec.shifts)
                    error = False
                    for i in range(len(list_attendance)):
                        '''Trùng thứ chấm công của nhau không được trùng'''
                        if rec.shifts.sudo().thu_2 and list_attendance[i].thu_2 \
                                or rec.shifts.sudo().thu_3 and list_attendance[i].thu_3 \
                                or rec.shifts.sudo().thu_4 and list_attendance[i].thu_4 \
                                or rec.shifts.sudo().thu_5 and list_attendance[i].thu_5 \
                                or rec.shifts.sudo().thu_6 and list_attendance[i].thu_6 \
                                or rec.shifts.sudo().thu_7 and list_attendance[i].thu_7 \
                                or rec.shifts.sudo().thu_8 and list_attendance[i].thu_8:

                            if list_attendance[i].first_in_late_out or rec.shifts.first_in_late_out:
                                raise ValidationError("Lỗi cài đặt trùng ca")
                            else:
                                list_s = list_attendance[i].duplicate_shifts(list_attendance[i])
                                error = set(list_0).intersection(set(list_s))
                                if error:
                                    break
                    if error:
                        raise ValidationError("Lỗi cài đặt trùng ca")

    @api.onchange('shifts')
    def onchange_shifts(self):
        for rec in self:
            if rec.shifts:
                '''check thứ của ca và thứ của ngày chấm công'''
                date_from = datetime.datetime.strptime(str(rec.date_from), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                    hours=7)
                date_to = datetime.datetime.strptime(str(rec.date_to), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
                    hours=7)
                rec.day = date_from.day
                rec.month = date_from.month
                rec.year = date_from.year
                if rec.shifts.sudo().for_full_time_shift == 'check_out_day' and \
                        rec.shifts.sudo().type_of_shift == 'full_time_shift':
                    rec.day = date_to.day
                    rec.month = date_to.month
                    rec.year = date_to.year

                date_ = int(date.weekday(date(int(rec.year), int(rec.month), int(rec.day))))
                if rec.shifts.sudo().thu_2 and date_ == 0 \
                        or rec.shifts.sudo().thu_3 and date_ == 1 \
                        or rec.shifts.sudo().thu_4 and date_ == 2 \
                        or rec.shifts.sudo().thu_5 and date_ == 3 \
                        or rec.shifts.sudo().thu_6 and date_ == 4 \
                        or rec.shifts.sudo().thu_7 and date_ == 5 \
                        or rec.shifts.sudo().thu_8 and date_ == 6:
                    pass
                else:
                    # print('không trùng nè')
                    thu = ''
                    if date_ == 0:
                        thu = 'Thứ hai'
                    elif date_ == 1:
                        thu = 'Thứ ba'
                    elif date_ == 2:
                        thu = 'thứ tư'
                    elif date_ == 3:
                        thu = 'thứ năm'
                    elif date_ == 4:
                        thu = 'thứ sáu'
                    elif date_ == 5:
                        thu = 'thứ bảy'
                    elif date_ == 6:
                        thu = 'chủ nhật'
                    raise ValidationError(str(rec.shifts.sudo().name) + ' không thuộc ' + str(thu))

    def shifts_name_compute(self):
        for rec in self:
            rec.shifts_name = str(rec.shifts.sudo().name) + " - " + str(rec.employee_multi_id.sudo().name.name)

    shifts_name = fields.Char('Ca làm việc - NS', compute='shifts_name_compute')

    @api.model
    def calendar_employee(self):

        # print('ll', self.user_ids)
        list_not_delete = []
        employee_current = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        list_create = []
        if employee_current:
            employees = self.env['hr.employee.multi.company'].sudo().search(
                [('name', '=', employee_current.id)])
            for i in employees:
                list_create.append(i.id)

            department_list = self.env['hr.department'].sudo().search([('manager_ids', '=', employee_current.id)])
            if department_list:
                employee_department = self.env['hr.employee.multi.company'].sudo().search(
                    [('department_id', 'in', department_list.ids)])
                if employee_department:
                    for i in employee_department:
                        list_create.append(i.id)
            # print(list_create)

            calendar_create = self.env['sea.hr.calendar.employee'].sudo().search(
                [('employee_multi_id', 'in', list_create)])
            '''xóa LLV cũ của những employee này để cập nhật lại LLV mới'''
            calendar_delete = self.env['sea.hr.calendar'].sudo().search(
                [('employee_multi_id', 'in', list_create)])
            calendar_delete.sudo().unlink()
            ''''''
            if calendar_create:
                for calendar in calendar_create:
                    for i in range(calendar.last_day_of_month):
                        day = i + 1
                        shifts = calendar.get_day(day)
                        for shift in shifts:
                            date_str = str(calendar.year) + '-' + str(calendar.month) + '-' + str(
                                day) + ' ' + '00:00:00'
                            date_format = "%Y-%m-%d %H:%M:%S"
                            datetime_calendar = datetime.datetime.strptime(date_str, date_format)
                            calendar_exit = self.env['sea.hr.calendar'].sudo().search(
                                [('employee_multi_id', '=', calendar.employee_multi_id.id), ('day', '=', day),
                                 ('month', '=', calendar.month), ('year', '=', calendar.year),
                                 ('shifts', '=', shift.id)])
                            if not calendar_exit:
                                value = {
                                    'employee_multi_id': calendar.employee_multi_id.id,
                                    'day': day,
                                    'month': calendar.month,
                                    'year': calendar.year,
                                    'shifts': shift.id,
                                    'date_from': datetime_calendar,
                                    'date_to': datetime_calendar,
                                    'calendar_employee': calendar.id
                                }
                                id_e = self.env['sea.hr.calendar'].sudo().create(value)
                                list_not_delete.append(id_e)
                            else:
                                list_not_delete.append(calendar_exit)

        '''cập nhật lại user_ids '''
        upgrade_list = self.env['sea.hr.calendar'].sudo().search([('user_ids', 'in', self.env.user.id)])
        for not_delete in upgrade_list:
            if not_delete.employee_multi_id:
                li = []
                if not_delete.employee_multi_id.sudo().user_id:
                    li.append(not_delete.employee_multi_id.sudo().user_id.id)
                for i in not_delete.employee_multi_id.department_id.sudo().manager_ids:
                    if i.sudo().user_id:
                        li.append(i.sudo().user_id.id)
                not_delete.write({'user_ids': [(6, 0, li)]})
        ''''''

        get_date_current = fields.Datetime.now().date()
        calendar_all = self.env['sea.hr.calendar'].sudo().search(
            [('id', 'not in', [i.id for i in list_not_delete]), ('create_date', '<', get_date_current)])
        # print('len', len(calendar_all))
        if calendar_all:
            calendar_all.sudo().unlink()
            # print('Done')
        search_view = self.env.ref('seatek_hr_attendance.sea_hr_calendar_view_search')
        return {
            'name': 'Calendar',
            'type': 'ir.actions.act_window',
            'res_model': 'sea.hr.calendar',
            'view_mode': 'calendar,tree,form',
            'domain': [('company_id', 'in', self.env.user.company_ids.ids), ('user_ids', 'in', self.env.user.id)],
            # 'domain': [],
            'context': {

            },
            'search_view_id': search_view.id,

        }

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (rec.id, str(rec.employee_multi_id.sudo().name.name) + ' - ' + str(rec.day) + '/' + str(
                    rec.month) + '/' + str(rec.year)))
        return result

    @api.model
    def create(self, vals):
        # if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
        #     employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
        #         [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)],
        #         limit=1)
        #     if employee_multi_id:
        #         employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
        #         if employee:
        #             department_list = self.env['hr.department'].sudo().search(
        #                 [('manager_ids', '=', employee.id)])
        #             if not department_list:
        #                 raise Warning("You are not allowed to create records.")
        #                 return False
        if 'employee_multi_id' in vals:
            employee = self.env['hr.employee.multi.company'].sudo().search(
                [('id', '=', vals.get('employee_multi_id'))])
            if employee:
                li = []
                if employee.sudo().user_id:
                    li.append(employee.sudo().user_id.id)
                for i in employee.department_id.sudo().manager_ids:
                    if i.sudo().user_id:
                        li.append(i.sudo().user_id.id)
                vals['user_ids'] = [(6, 0, li)]
        rec = super(CalendarEmployee, self).create(vals)
        upgrade = self.env['sea.hr.calendar.employee'].sudo().search(
            [('employee_multi_id', '=', rec.employee_multi_id.id), ('month', '=', rec.month),
             ('year', '=', rec.year)])
        if upgrade:
            if rec.shifts:
                upgrade.write({'day_' + str(rec.day): [(4, rec.shifts.id)]})
        return rec

    @api.multi
    def write(self, vals):
        if 'shifts' in vals:
            shift = self.shifts
            upgrade = self.env['sea.hr.calendar.employee'].sudo().search(
                [('employee_multi_id', '=', self.employee_multi_id.id), ('month', '=', self.month),
                 ('year', '=', self.year)])
            if upgrade:
                if shift:
                    upgrade.write({'day_' + str(self.day): [(3, shift.id)]})

                upgrade.write({'day_' + str(self.day): [(4, vals.get('shifts'))]})
        rec = super(CalendarEmployee, self).write(vals)
        return rec


class CalendarDateFromTo(models.Model):
    _name = 'shift.employee.date.from.to'
    _description = "Employee calendar for a period of time"

    company_id = fields.Many2one('res.company', string="Công Ty", required=True,
                                 default=lambda self: self.env.user.company_id)
    shifts = fields.Many2many('sea.hr.attendance.shift', string="Shifts", domain="[('company_id', '=', company_id)]")

    @api.onchange('shifts')
    def _onchange_shifts_(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc tính'''
        for rec in self:
            list_attendance = [attendance for attendance in rec.shifts]
            while True:
                if len(list_attendance) == 0:
                    break
                attendance_0 = list_attendance[0]
                list_attendance.pop(0)
                error = False
                for i in range(len(list_attendance)):
                    '''Trùng thứ chấm công của nhau không được trùng'''
                    if attendance_0.thu_2 and list_attendance[i].thu_2 \
                            or attendance_0.thu_3 and list_attendance[i].thu_3 \
                            or attendance_0.thu_4 and list_attendance[i].thu_4 \
                            or attendance_0.thu_5 and list_attendance[i].thu_5 \
                            or attendance_0.thu_6 and list_attendance[i].thu_6 \
                            or attendance_0.thu_7 and list_attendance[i].thu_7 \
                            or attendance_0.thu_8 and list_attendance[i].thu_8:

                        if attendance_0.first_in_late_out or list_attendance[i].first_in_late_out:
                            error = True
                            break
                        else:
                            list_0 = attendance_0.duplicate_shifts(attendance_0)
                            list_s = list_attendance[i].duplicate_shifts(list_attendance[i])
                            error = set(list_0).intersection(set(list_s))
                            if error:
                                break

                if error:
                    rec.shifts = [(3, list_attendance[i].id)]
                    return {'warning': {
                        'title': 'Lỗi thêm ca làm việc',
                        'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                    }}

    type = fields.Selection(
        [(1, 'Chọn thứ'), (2, 'Chọn ngày'), (3, 'Chọn khoảng thời gian')],
        required=True, string="Type")
    date_even_uneven = fields.Selection(
        [(2, 'Chẵn'), (1, 'lẻ')], string="Chọn ngày Chẵn/Lẻ")

    thu_2 = fields.Boolean('Thứ 2', default=False)
    thu_3 = fields.Boolean('Thứ 3', default=False)
    thu_4 = fields.Boolean('Thứ 4', default=False)
    thu_5 = fields.Boolean('Thứ 5', default=False)
    thu_6 = fields.Boolean('Thứ 6', default=False)
    thu_7 = fields.Boolean('Thứ 7', default=False)
    thu_8 = fields.Boolean('Chủ nhật', default=False)

    day_1 = fields.Boolean('Ngày 1', default=False)
    day_2 = fields.Boolean('Ngày 2', default=False)
    day_3 = fields.Boolean('Ngày 3', default=False)
    day_4 = fields.Boolean('Ngày 4', default=False)
    day_5 = fields.Boolean('Ngày 5', default=False)
    day_6 = fields.Boolean('Ngày 6', default=False)
    day_7 = fields.Boolean('Ngày 7', default=False)
    day_8 = fields.Boolean('Ngày 8', default=False)
    day_9 = fields.Boolean('Ngày 9', default=False)
    day_10 = fields.Boolean('Ngày 10', default=False)
    day_11 = fields.Boolean('Ngày 11', default=False)
    day_12 = fields.Boolean('Ngày 12', default=False)
    day_13 = fields.Boolean('Ngày 13', default=False)
    day_14 = fields.Boolean('Ngày 14', default=False)
    day_15 = fields.Boolean('Ngày 15', default=False)
    day_16 = fields.Boolean('Ngày 16', default=False)
    day_17 = fields.Boolean('Ngày 17', default=False)
    day_18 = fields.Boolean('Ngày 18', default=False)
    day_19 = fields.Boolean('Ngày 19', default=False)
    day_20 = fields.Boolean('Ngày 20', default=False)
    day_21 = fields.Boolean('Ngày 21', default=False)
    day_22 = fields.Boolean('Ngày 22', default=False)
    day_23 = fields.Boolean('Ngày 23', default=False)
    day_24 = fields.Boolean('Ngày 24', default=False)
    day_25 = fields.Boolean('Ngày 25', default=False)
    day_26 = fields.Boolean('Ngày 26', default=False)
    day_27 = fields.Boolean('Ngày 27', default=False)
    day_28 = fields.Boolean('Ngày 28', default=False)
    day_29 = fields.Boolean('Ngày 29', default=False)
    day_30 = fields.Boolean('Ngày 30', default=False)
    day_31 = fields.Boolean('Ngày 31', default=False)

    def get_day(self, day=0):
        for rec in self:
            if day == 1:
                return rec.day_1
            elif day == 2:
                return rec.day_2
            elif day == 3:
                return rec.day_3
            elif day == 4:
                return rec.day_4
            elif day == 5:
                return rec.day_5
            elif day == 6:
                return rec.day_6
            elif day == 7:
                return rec.day_7
            elif day == 8:
                return rec.day_8
            elif day == 9:
                return rec.day_9
            elif day == 10:
                return rec.day_10
            elif day == 11:
                return rec.day_11
            elif day == 12:
                return rec.day_12
            elif day == 13:
                return rec.day_13
            elif day == 14:
                return rec.day_14
            elif day == 15:
                return rec.day_15
            elif day == 16:
                return rec.day_16
            elif day == 17:
                return rec.day_17
            elif day == 18:
                return rec.day_18
            elif day == 19:
                return rec.day_19
            elif day == 20:
                return rec.day_20
            elif day == 22:
                return rec.day_22
            elif day == 21:
                return rec.day_21
            elif day == 23:
                return rec.day_23
            elif day == 24:
                return rec.day_24
            elif day == 25:
                return rec.day_25
            elif day == 26:
                return rec.day_26
            elif day == 27:
                return rec.day_27
            elif day == 28:
                return rec.day_28
            elif day == 29:
                return rec.day_29
            elif day == 30:
                return rec.day_30
            elif day == 31:
                return rec.day_31
            else:
                return False

    def get_thu(self, thu=False):
        for rec in self:
            if thu == 0:
                return rec.thu_2
            elif thu == 1:
                return rec.thu_3
            elif thu == 2:
                return rec.thu_4
            elif thu == 3:
                return rec.thu_5
            elif thu == 4:
                return rec.thu_6
            elif thu == 5:
                return rec.thu_7
            elif thu == 6:
                return rec.thu_8
            else:
                return False

    date_from = fields.Integer('Start Date', default=lambda self: fields.datetime.now().day)
    date_to = fields.Integer('End Date', default=lambda self: fields.datetime.now().day)

    @api.constrains('date_from', 'date_to', 'type')
    def onchange_date_from_to(self):
        for rec in self:
            if rec.type == 3:
                if rec.date_from > rec.date_to:
                    raise ValidationError("Ngày từ phải nhỏ hơn hoặc bằng ngày đến")
                elif rec.date_from <= 0 or rec.date_from >= 31:
                    raise ValidationError("Ngày từ phải lớn hơn 0 và nho hơn 32")
                if rec.date_to <= 0 or rec.date_to >= 32:
                    raise ValidationError("Ngày đến phải lớn hơn 0 và nhở hơn 32")

    @api.onchange('date_even_uneven')
    def onchange_type(self):
        for rec in self:
            if not rec.date_even_uneven:
                rec.clear_data_uneven()
                rec.clear_data_even()
            elif rec.date_even_uneven == 1:
                rec.day_1 = True
                rec.day_3 = True
                rec.day_5 = True
                rec.day_7 = True
                rec.day_9 = True
                rec.day_11 = True
                rec.day_13 = True
                rec.day_15 = True
                rec.day_17 = True
                rec.day_19 = True
                rec.day_21 = True
                rec.day_23 = True
                rec.day_25 = True
                rec.day_27 = True
                rec.day_29 = True
                rec.day_31 = True
                rec.clear_data_even()
            elif rec.date_even_uneven == 2:
                rec.day_30 = True
                rec.day_28 = True
                rec.day_26 = True
                rec.day_24 = True
                rec.day_22 = True
                rec.day_20 = True
                rec.day_18 = True
                rec.day_16 = True
                rec.day_14 = True
                rec.day_12 = True
                rec.day_10 = True
                rec.day_8 = True
                rec.day_6 = True
                rec.day_4 = True
                rec.day_2 = True
                rec.clear_data_uneven()

    def clear_data_thu(self):
        for rec in self:
            rec.thu_2 = False
            rec.thu_3 = False
            rec.thu_4 = False
            rec.thu_5 = False
            rec.thu_6 = False
            rec.thu_7 = False
            rec.thu_8 = False

    def clear_data_ngay(self):
        for rec in self:
            rec.day_1 = False
            rec.day_2 = False
            rec.day_3 = False
            rec.day_4 = False
            rec.day_5 = False
            rec.day_6 = False
            rec.day_7 = False
            rec.day_8 = False
            rec.day_9 = False
            rec.day_10 = False
            rec.day_11 = False
            rec.day_12 = False
            rec.day_13 = False
            rec.day_14 = False
            rec.day_15 = False
            rec.day_16 = False
            rec.day_17 = False
            rec.day_18 = False
            rec.day_19 = False
            rec.day_20 = False
            rec.day_21 = False
            rec.day_22 = False
            rec.day_23 = False
            rec.day_24 = False
            rec.day_25 = False
            rec.day_26 = False
            rec.day_27 = False
            rec.day_28 = False
            rec.day_29 = False
            rec.day_30 = False
            rec.day_31 = False

    def clear_data_uneven(self):
        for rec in self:
            rec.day_1 = False
            rec.day_3 = False
            rec.day_5 = False
            rec.day_7 = False
            rec.day_9 = False
            rec.day_11 = False
            rec.day_13 = False
            rec.day_15 = False
            rec.day_17 = False
            rec.day_19 = False
            rec.day_21 = False
            rec.day_23 = False
            rec.day_25 = False
            rec.day_27 = False
            rec.day_29 = False
            rec.day_31 = False

    def clear_data_even(self):
        for rec in self:
            rec.day_30 = False
            rec.day_28 = False
            rec.day_26 = False
            rec.day_24 = False
            rec.day_22 = False
            rec.day_20 = False
            rec.day_18 = False
            rec.day_16 = False
            rec.day_14 = False
            rec.day_12 = False
            rec.day_10 = False
            rec.day_8 = False
            rec.day_6 = False
            rec.day_4 = False
            rec.day_2 = False

    def clear_data_ktg(self):
        for rec in self:
            rec.date_from = None
            rec.date_to = None

    @api.constrains('type')
    def constraint_type(self):
        for rec in self:
            if rec.type == 1:
                rec.clear_data_ngay()
                rec.clear_data_ktg()
            elif rec.type == 2:
                rec.clear_data_thu()
                rec.clear_data_ktg()
            elif rec.type == 3:
                rec.clear_data_thu()
                rec.clear_data_ngay()

    @api.depends('employee_multi_ids')
    def domain_employee_compute(self):
        for rec in self:
            if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_manager'):
                employee = self.env['hr.employee.multi.company'].sudo().search(
                    [('employee_current_status', '=', 'working'),
                     ('company_id', '=', self.env.user.company_id.id)])
                if employee:
                    rec.domain_employee = employee.ids
            else:
                if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                    employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)],
                        limit=1)
                    if employee_multi_id:
                        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                        if employee:
                            list_employee = [employee_multi_id.id]
                            department_list = self.env['hr.department'].sudo().search(
                                [('manager_ids', '=', employee.id)])
                            if department_list:
                                employee_department = self.env['hr.employee.multi.company'].sudo().search(
                                    [('department_id', 'in', department_list.ids)])
                                if employee_department:
                                    for i in employee_department:
                                        list_employee.append(i.id)
                            rec.domain_employee = list_employee

    domain_employee = fields.Many2many('hr.employee.multi.company', string='Domain', compute='domain_employee_compute')
    employee_multi_ids = fields.Many2many('hr.employee.multi.company', 'employee_multi_calendar_from_to_rel',
                                          'calendar_id', 'emp_mul_id', string='Employees',
                                          domain="[('id', 'in', domain_employee)]", required=True)

    attendance_id_apply_list = fields.Many2many('sea.hr.attendance', 'atendance_shift_from_to_unapply_rel',
                                                'attendance_id', 'shift_from_to_id',
                                                domain="[('company_id', '=', company_id), "
                                                       "('mark_as_todo', '=', False)]",
                                                string='Attendance Apply')
    attendance_id_apply = fields.Many2one('sea.hr.attendance', string='Attendance Apply',
                                          domain="[('company_id', '=', company_id), "
                                                 "('id', 'not in', attendance_id_apply_list)"
                                                 ", ('mark_as_todo', '=', False)]")

    def apply_shift_current_month(self):
        for rec in self:
            shifts = self.env['shift.employee.date.from.to'].sudo().search(
                [('id', '!=', rec.id), ('company_id', '=', rec.company_id.id)])
            if shifts:
                for shift in shifts:
                    shift.write({'attendance_id_apply': None})
            if rec.attendance_id_apply:
                self.write({'attendance_id_apply_list': [(4, rec.attendance_id_apply.id)]})

                if rec.attendance_id_apply.sudo().attendance_of_month:
                    '''điều kiện apply chỉ cho hiện tại'''
                    # if int(rec.attendance_id_apply.sudo().year) > fields.datetime.now().year \
                    #         or int(rec.attendance_id_apply.sudo().year) == fields.datetime.now().year and \
                    #         int(rec.attendance_id_apply.sudo().month) >= fields.datetime.now().month:

                    list_day = []
                    if rec.type:
                        if rec.type == 1:
                            for i in range(int(calendar.monthrange(int(rec.attendance_id_apply.sudo().year),
                                                                   int(rec.attendance_id_apply.sudo().month))[1])):
                                if rec.get_thu(int(date.weekday(date(int(rec.attendance_id_apply.sudo().year),
                                                                     int(rec.attendance_id_apply.sudo().month),
                                                                     int(i + 1))))):
                                    list_day.append(i + 1)

                        elif rec.type == 2:
                            for i in range(int(calendar.monthrange(int(rec.attendance_id_apply.sudo().year),
                                                                   int(rec.attendance_id_apply.sudo().month))[1])):
                                if rec.get_day(i + 1):
                                    list_day.append(i + 1)
                        elif rec.type == 3:
                            start = int(rec.date_from)
                            end = int(rec.date_to)
                            for day_f in range(start, end + 1):
                                list_day.append(day_f)

                    if list_day is not None:
                        for i in list_day:
                            '''điều kiện apply chỉ cho hiện tại'''
                            # if int(rec.attendance_id_apply.sudo().month) == fields.datetime.now().month \
                            #         and int(rec.attendance_id_apply.sudo().year) == fields.datetime.now().year \
                            #         and i <= fields.datetime.now().day:
                            #     continue
                            # else:
                            shift = []
                            for j in rec.shifts:
                                date_ = int(date.weekday(date(int(rec.attendance_id_apply.sudo().year),
                                                              int(rec.attendance_id_apply.sudo().month),
                                                              int(i))))
                                if j.sudo().thu_2 and date_ == 0 \
                                        or j.sudo().thu_3 and date_ == 1 \
                                        or j.sudo().thu_4 and date_ == 2 \
                                        or j.sudo().thu_5 and date_ == 3 \
                                        or j.sudo().thu_6 and date_ == 4 \
                                        or j.sudo().thu_7 and date_ == 5 \
                                        or j.sudo().thu_8 and date_ == 6:
                                    shift.append(j.id)
                            if shift is not None:
                                    list_employee = []
                                    list_upgrade = []
                                    if rec.attendance_id_apply.sudo().calendar_of_month_compute:
                                        for m in rec.attendance_id_apply.sudo().calendar_of_month_compute:
                                            list_employee.append(m.employee_multi_id.id)
                                    if rec.employee_multi_ids:
                                        list_upgrade = set(list_employee).intersection(
                                            set(rec.employee_multi_ids.ids))
                                    if list_upgrade is not None:
                                        calendar_update = self.env['sea.hr.calendar.employee'].sudo().search(
                                            [('month', '=', rec.attendance_id_apply.sudo().month),
                                             ('year', '=', rec.attendance_id_apply.sudo().year),
                                             ('attendance_id', '=', rec.attendance_id_apply.id),
                                             ('employee_multi_id', 'in', list(list_upgrade))])
                                        if calendar_update:
                                            for update in calendar_update:
                                                update.write({'day_' + str(i): [(6, 0, shift)]})

                                        realtime_update = self.env['sea.hr.attendance.realtime'].sudo().search(
                                            [('day', '=', i), ('month', '=', rec.attendance_id_apply.sudo().month),
                                             ('year', '=', rec.attendance_id_apply.sudo().year),
                                             ('employee_multi_id', 'in', list(list_upgrade))])
                                        if realtime_update:
                                            for update in realtime_update:
                                                update.write({'shift': [(6, 0, shift)]})
                    '''tự động tính lại bảng chấm công cho tháng đó'''
                    # rec.attendance_id_apply.upgrade_attendance()

    user_id_create = fields.Many2one('res.users', string="By", default=lambda self: self.env.user.id)
