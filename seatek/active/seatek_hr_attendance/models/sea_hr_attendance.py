import calendar
import datetime
import json
from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Attendance(models.Model):
    _name = 'sea.hr.attendance.month'
    _description = "Attendances of Month"
    _sql_constraints = [('model_month_year_company_uniq', 'unique(attendance_id,employee_multi_id,month,year)',
                         'Attendance with this month of company is  already exist!!')]
    _order = 'company_code,department_code,job_code,s_identification_id, year, month asc'

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên",
                                        domain=lambda self: [('employee_current_status', '=', 'working'),
                                                             ('company_id', '=', self.env.user.company_id.id)])
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)

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
    attendance_id = fields.Many2one('sea.hr.attendance', "Attendances", ondelete='cascade')

    month = fields.Integer(string='Tháng')
    year = fields.Integer(string="Năm")

    def compute_month_year_compute(self):
        for rec in self:
            rec.month_year_compute = str(rec.month) + "/" + str(rec.year)

    month_year_compute = fields.Char('Tháng/năm', compute='compute_month_year_compute')

    last_day_of_month = fields.Integer(string='số ngày tối đa của tháng')

    # def _job_id_compute_(self):
    #     for rec in self:
    #         rec.job_id = rec.employee_multi_id.sudo().job_id.id

    # job_id = fields.Many2one('hr.job', string="Chức danh", compute='_job_id_compute_')
    department_id = fields.Many2one('hr.department', string="Phòng Ban/Đơn Vị",
                                    related='employee_multi_id.department_id',
                                    help='Phòng Ban/Đơn Vị vủa nhân sự', store=False)
    job_id = fields.Many2one('hr.job', string="Chức danh", related='employee_multi_id.job_id', store=False)

    day_1 = fields.Many2one('sea.hr.attendance.realtime', string="1",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 1)]")
    day_2 = fields.Many2one('sea.hr.attendance.realtime', string="2",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 2)]")
    day_3 = fields.Many2one('sea.hr.attendance.realtime', string="3",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 3)]")
    day_4 = fields.Many2one('sea.hr.attendance.realtime', string="4",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 4)]")
    day_5 = fields.Many2one('sea.hr.attendance.realtime', string="5",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 5)]")
    day_6 = fields.Many2one('sea.hr.attendance.realtime', string="6",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 6)]")
    day_7 = fields.Many2one('sea.hr.attendance.realtime', string="7",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 7)]")
    day_8 = fields.Many2one('sea.hr.attendance.realtime', string="8",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 8)]")
    day_9 = fields.Many2one('sea.hr.attendance.realtime', string="9",
                            domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                   " ('month', '=', month), ('day', '=', 9)]")
    day_10 = fields.Many2one('sea.hr.attendance.realtime', string="10",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 10)]")
    day_11 = fields.Many2one('sea.hr.attendance.realtime', string="11",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 11)]")
    day_12 = fields.Many2one('sea.hr.attendance.realtime', string="12",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 12)]")
    day_13 = fields.Many2one('sea.hr.attendance.realtime', string="13",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 13)]")
    day_14 = fields.Many2one('sea.hr.attendance.realtime', string="14",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 14)]")
    day_15 = fields.Many2one('sea.hr.attendance.realtime', string="15",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 15)]")
    day_16 = fields.Many2one('sea.hr.attendance.realtime', string="16",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 16)]")
    day_17 = fields.Many2one('sea.hr.attendance.realtime', string="17",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 17)]")
    day_18 = fields.Many2one('sea.hr.attendance.realtime', string="18",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 18)]")
    day_19 = fields.Many2one('sea.hr.attendance.realtime', string="19",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 19)]")
    day_20 = fields.Many2one('sea.hr.attendance.realtime', string="20",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 20)]")
    day_21 = fields.Many2one('sea.hr.attendance.realtime', string="21",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 21)]")
    day_22 = fields.Many2one('sea.hr.attendance.realtime', string="22",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 22)]")
    day_23 = fields.Many2one('sea.hr.attendance.realtime', string="23",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 23)]")
    day_24 = fields.Many2one('sea.hr.attendance.realtime', string="24",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 24)]")
    day_25 = fields.Many2one('sea.hr.attendance.realtime', string="25",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 25)]")
    day_26 = fields.Many2one('sea.hr.attendance.realtime', string="26",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 26)]")
    day_27 = fields.Many2one('sea.hr.attendance.realtime', string="27",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 27)]")
    day_28 = fields.Many2one('sea.hr.attendance.realtime', string="28",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 28)]")
    day_29 = fields.Many2one('sea.hr.attendance.realtime', string="29",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 29)]")
    day_30 = fields.Many2one('sea.hr.attendance.realtime', string="30",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 30)]")
    day_31 = fields.Many2one('sea.hr.attendance.realtime', string="31",
                             domain="[('employee_multi_id', '=', employee_multi_id), ('year', '=', year),"
                                    " ('month', '=', month), ('day', '=', 31)]")

    @api.multi
    def count_soon_late(self):
        red = {'check_in': 0, 'check_in_noon': 0, 'check_out_noon': 0, 'check_out': 0, 'check_in_late': 0,
               'check_in_noon_late': 0, 'check_out_noon_soon': 0, 'check_out_soon': 0, 'day_details': []}
        for rec in self:
            days = [rec.day_1, rec.day_2, rec.day_3, rec.day_4, rec.day_5, rec.day_6, rec.day_7, rec.day_8, rec.day_9,
                    rec.day_10, rec.day_11, rec.day_12, rec.day_13, rec.day_14, rec.day_15, rec.day_16, rec.day_17,
                    rec.day_18, rec.day_19, rec.day_20, rec.day_21, rec.day_22, rec.day_23, rec.day_24, rec.day_25,
                    rec.day_26, rec.day_27, rec.day_28, rec.day_29, rec.day_30, rec.day_31]
            for day in days:
                if day.sudo().shift_details:
                    check_not_attendance = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                        [('employee_multi_id', '=', rec.employee_multi_id.id),
                         ('attendance_config_ids', '=', day.sudo().shift.id)], limit=1)
                    check = True
                    if check_not_attendance:
                        if check_not_attendance.not_attendance:
                            check = False
                    if check:
                        for i in day.sudo().shift_details:
                            check = False
                            '''ngày trong tương lai thi không tính nó luôn luôn là True'''
                            if day.sudo().year <= fields.datetime.now().year:
                                if day.sudo().month < fields.datetime.now().month \
                                        or day.sudo().day <= fields.datetime.now().day \
                                        and day.sudo().month == fields.datetime.now().month:
                                    if i.shift:
                                        if not i.check_in \
                                                or not i.check_out \
                                                or not i.check_in_noon and i.work_break \
                                                or not i.check_out_noon and i.work_break:
                                            if not i.check_in:
                                                red['check_in'] += 1
                                                check = True
                                            if not i.check_in_noon and i.work_break:
                                                red['check_in_noon'] += 1
                                                check = True
                                            if not i.check_out_noon and i.work_break:
                                                red['check_out_noon'] += 1
                                                check = True
                                            if not i.check_out:
                                                red['check_out'] += 1
                                                check = True
                                        else:
                                            if i.check_in_late:
                                                hours, minutes, seconds = map(int, i.check_in_late.split(':'))
                                                if hours * 3600 + minutes * 60 + seconds > 0:
                                                    red['check_in_late'] += 1
                                                    check = True
                                            if i.check_out_noon_soon:
                                                hours2, minutes2, seconds2 = map(int,
                                                                                 i.check_out_noon_soon.split(':'))
                                                if hours2 * 3600 + minutes2 * 60 + seconds2 > 0:
                                                    red['check_out_noon_soon'] += 1
                                                    check = True
                                            if i.check_in_noon_late:
                                                hours1, minutes1, seconds1 = map(int,
                                                                                 i.check_in_noon_late.split(':'))
                                                if hours1 * 3600 + minutes1 * 60 + seconds1 > 0:
                                                    red['check_in_noon_late'] += 1
                                                    check = True
                                            if i.check_out_soon:
                                                hours3, minutes3, seconds3 = map(int, i.check_out_soon.split(':'))
                                                if hours3 * 3600 + minutes3 * 60 + seconds3 > 0:
                                                    red['check_out_soon'] += 1
                                                    check = True
                            if check:
                                red['day_details'].append(i)
        return red

    @api.multi
    def get_day(self, day=None):
        if day == 1:
            return self.day_1
        elif day == 2:
            return self.day_2
        elif day == 3:
            return self.day_3
        elif day == 4:
            return self.day_4
        elif day == 5:
            return self.day_5
        elif day == 6:
            return self.day_6
        elif day == 7:
            return self.day_7
        elif day == 8:
            return self.day_8
        elif day == 9:
            return self.day_9
        elif day == 10:
            return self.day_10
        elif day == 11:
            return self.day_11
        elif day == 12:
            return self.day_12
        elif day == 13:
            return self.day_13
        elif day == 14:
            return self.day_14
        elif day == 15:
            return self.day_15
        elif day == 16:
            return self.day_16
        elif day == 17:
            return self.day_17
        elif day == 18:
            return self.day_18
        elif day == 19:
            return self.day_19
        elif day == 20:
            return self.day_20
        elif day == 21:
            return self.day_21
        elif day == 22:
            return self.day_22
        elif day == 23:
            return self.day_23
        elif day == 24:
            return self.day_24
        elif day == 25:
            return self.day_25
        elif day == 26:
            return self.day_26
        elif day == 27:
            return self.day_27
        elif day == 28:
            return self.day_28
        elif day == 29:
            return self.day_29
        elif day == 30:
            return self.day_30
        elif day == 31:
            return self.day_31

    @api.multi
    def format_time_string(self, time_str):
        if not time_str:
            return ""
        else:
            # Chuyển chuỗi thành đối tượng datetime
            time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
            # Trích xuất giờ, phút và giây từ đối tượng time
            hours, remainder = divmod(time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second, 3600)
            minutes, seconds = divmod(remainder, 60)
            if hours > 0:
                formatted_time = "{:d}h{:02d}p{:02d}s".format(hours, minutes, seconds)
            elif minutes > 0:
                formatted_time = "{:02d}p{:02d}s".format(minutes, seconds)
            else:
                formatted_time = "{:02d}s".format(seconds)

            return formatted_time

    @api.multi
    def test_soon_late(self, day):
        red = 'false'
        if day:
            check_not_attendance = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                [('employee_multi_id', '=', self.employee_multi_id.id),
                 # ('attendance_config_ids', '=', day.sudo().shift.id)
                 ], limit=1)
            check = True
            if check_not_attendance:
                if check_not_attendance.not_attendance:
                    check = False
            if day.sudo().shift_details and check:
                for i in day.sudo().shift_details:
                    '''ngày trong tương lai thi không tính nó luôn luôn là True'''
                    if day.sudo().year <= fields.datetime.now().year:
                        if day.sudo().month < fields.datetime.now().month \
                                or day.sudo().day <= fields.datetime.now().day \
                                and day.sudo().month == fields.datetime.now().month:
                            if i.shift:
                                if not i.check_in \
                                        or not i.check_out \
                                        or not i.check_in_noon and i.work_break \
                                        or not i.check_out_noon and i.work_break:
                                    # print(day.sudo().employee_multi_id.sudo().name.name)
                                    red = ""
                                    if not i.check_in:
                                        red = red + "- Thiếu check in\n"
                                    if not i.check_in_noon and i.work_break:
                                        red = red + "- Thiếu check in noon\n"
                                    if not i.check_out_noon and i.work_break:
                                        red = red + "- Thiếu check out noon\n"
                                    if not i.check_out:
                                        red = red + "- Thiếu check out\n"
                                    # if i.note:
                                    #     red = red + "\n- Ghi chú: " + str(
                                    #         i.note)
                                    # red = red + "\n- Trạng thái: " + (
                                    #     "Chấp nhận\n" if i.explanation_approved else "Không chấp nhận;\n")
                                #     break
                                # else:
                                total_seconds = 0
                                string = ""
                                if i.check_in_late:
                                    hours, minutes, seconds = map(int, i.check_in_late.split(':'))
                                    if hours * 3600 + minutes * 60 + seconds > 0:
                                        total_seconds += hours * 3600 + minutes * 60 + seconds
                                        string = string + "- Check in trễ: " + str(
                                            self.format_time_string(i.check_in_late)) + "\n "
                                if i.check_out_noon_soon:
                                    hours2, minutes2, seconds2 = map(int, i.check_out_noon_soon.split(':'))
                                    if hours2 * 3600 + minutes2 * 60 + seconds2 > 0:
                                        total_seconds += hours2 * 3600 + minutes2 * 60 + seconds2
                                        string = string + "- Check out noon sớm: " + str(
                                            self.format_time_string(i.check_out_noon_soon)) + "\n "

                                if i.check_in_noon_late:
                                    hours1, minutes1, seconds1 = map(int, i.check_in_noon_late.split(':'))
                                    if hours1 * 3600 + minutes1 * 60 + seconds1 > 0:
                                        total_seconds += hours1 * 3600 + minutes1 * 60 + seconds1
                                        string = string + "- Check in noon trễ: " + str(
                                            self.format_time_string(i.check_in_noon_late)) + "\n"

                                if i.check_out_soon:
                                    hours3, minutes3, seconds3 = map(int, i.check_out_soon.split(':'))
                                    if hours3 * 3600 + minutes3 * 60 + seconds3 > 0:
                                        total_seconds += hours3 * 3600 + minutes3 * 60 + seconds3
                                        string = string + "- Check out sớm: " + str(
                                            self.format_time_string(i.check_out_soon)) + "\n"
                                if i.note:
                                    string = string + "- Ghi chú: " + str(
                                        i.note)
                                # string = string + "\n- Trạng thái: " + (
                                #     "Chấp nhận;\n" if i.explanation_approved else "Không chấp nhận\n")
                                if total_seconds > 0:
                                    if red == 'false':
                                        red = string
                                    else:
                                        red += string
                                    # break
        return red

    @api.multi
    def get_soon_late(self, day):
        red = 'false'
        if day:
            if day.sudo().shift_details:
                for i in day.sudo().shift_details:
                    '''ngày trong tương lai thi không tính nó luôn luôn là True'''
                    if day.sudo().year <= fields.datetime.now().year:
                        if day.sudo().month < fields.datetime.now().month \
                                or day.sudo().day <= fields.datetime.now().day \
                                and day.sudo().month == fields.datetime.now().month:
                            if i.shift:
                                if not i.check_in \
                                        or not i.check_out \
                                        or not i.check_in_noon and i.work_break \
                                        or not i.check_out_noon and i.work_break:
                                    # print(day.sudo().employee_multi_id.sudo().name.name)
                                    red = ""
                                    if not i.check_in:
                                        red = red + "Thiếu check in\n "
                                    if not i.check_in_noon and i.work_break:
                                        red = red + "Thiếu check in noon\n"
                                    if not i.check_out_noon and i.work_break:
                                        red = red + "Thiếu check out noon\n"
                                    if not i.check_out:
                                        red = red + "Thiếu check out\n"
                                #     break
                                # else:
                                total_seconds = 0
                                string = ""
                                if i.check_in_late:
                                    hours, minutes, seconds = map(int, i.check_in_late.split(':'))
                                    if hours * 3600 + minutes * 60 + seconds > 0:
                                        total_seconds += hours * 3600 + minutes * 60 + seconds
                                        string = string + "check in trễ: " + str(i.check_in_late) + "\n "
                                if i.check_out_noon_soon:
                                    hours2, minutes2, seconds2 = map(int, i.check_out_noon_soon.split(':'))
                                    if hours2 * 3600 + minutes2 * 60 + seconds2 > 0:
                                        total_seconds += hours2 * 3600 + minutes2 * 60 + seconds2
                                        string = string + "check out noon sớm: " + str(
                                            i.check_out_noon_soon) + "\n "

                                if i.check_in_noon_late:
                                    hours1, minutes1, seconds1 = map(int, i.check_in_noon_late.split(':'))
                                    if hours1 * 3600 + minutes1 * 60 + seconds1 > 0:
                                        total_seconds += hours1 * 3600 + minutes1 * 60 + seconds1
                                        string = string + "check in noon trễ: " + str(i.check_in_noon_late) + "\n"

                                if i.check_out_soon:
                                    hours3, minutes3, seconds3 = map(int, i.check_out_soon.split(':'))
                                    if hours3 * 3600 + minutes3 * 60 + seconds3 > 0:
                                        total_seconds += hours3 * 3600 + minutes3 * 60 + seconds3
                                        string = string + "check out sớm: " + str(
                                            i.check_out_soon) + "\n"
                                if total_seconds > 0:
                                    if red == 'false':
                                        red = string
                                    else:
                                        red += string
                                    # break
        return red

    @api.model
    def compute_soon_or_late(self):
        for rec in self:
            rec.day_1_soon_or_late = rec.test_soon_late(rec.day_1)
            rec.day_2_soon_or_late = rec.test_soon_late(rec.day_2)
            rec.day_3_soon_or_late = rec.test_soon_late(rec.day_3)
            rec.day_4_soon_or_late = rec.test_soon_late(rec.day_4)
            rec.day_5_soon_or_late = rec.test_soon_late(rec.day_5)
            rec.day_6_soon_or_late = rec.test_soon_late(rec.day_6)
            rec.day_7_soon_or_late = rec.test_soon_late(rec.day_7)
            rec.day_8_soon_or_late = rec.test_soon_late(rec.day_8)
            rec.day_9_soon_or_late = rec.test_soon_late(rec.day_9)
            rec.day_10_soon_or_late = rec.test_soon_late(rec.day_10)
            rec.day_11_soon_or_late = rec.test_soon_late(rec.day_11)
            rec.day_12_soon_or_late = rec.test_soon_late(rec.day_12)
            rec.day_13_soon_or_late = rec.test_soon_late(rec.day_13)
            rec.day_14_soon_or_late = rec.test_soon_late(rec.day_14)
            rec.day_15_soon_or_late = rec.test_soon_late(rec.day_15)
            rec.day_16_soon_or_late = rec.test_soon_late(rec.day_16)
            rec.day_17_soon_or_late = rec.test_soon_late(rec.day_17)
            rec.day_18_soon_or_late = rec.test_soon_late(rec.day_18)
            rec.day_19_soon_or_late = rec.test_soon_late(rec.day_19)
            rec.day_20_soon_or_late = rec.test_soon_late(rec.day_20)
            rec.day_21_soon_or_late = rec.test_soon_late(rec.day_21)
            rec.day_22_soon_or_late = rec.test_soon_late(rec.day_22)
            rec.day_23_soon_or_late = rec.test_soon_late(rec.day_23)
            rec.day_24_soon_or_late = rec.test_soon_late(rec.day_24)
            rec.day_25_soon_or_late = rec.test_soon_late(rec.day_25)
            rec.day_26_soon_or_late = rec.test_soon_late(rec.day_26)
            rec.day_27_soon_or_late = rec.test_soon_late(rec.day_27)
            rec.day_28_soon_or_late = rec.test_soon_late(rec.day_28)
            rec.day_29_soon_or_late = rec.test_soon_late(rec.day_29)
            rec.day_30_soon_or_late = rec.test_soon_late(rec.day_30)
            rec.day_31_soon_or_late = rec.test_soon_late(rec.day_31)

    soon_or_late = fields.Boolean('Đi trễ về sớm', compute='compute_soon_or_late')
    day_1_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_2_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_3_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_4_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_5_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_6_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_7_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_8_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_9_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_10_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_11_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_12_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_13_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_14_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_15_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_16_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_17_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_18_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_19_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_20_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_21_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_22_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_23_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_24_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_25_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_26_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_27_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_28_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_29_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_30_soon_or_late = fields.Char('Đi trễ về sớm', store=False)
    day_31_soon_or_late = fields.Char('Đi trễ về sớm', store=False)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id,
                           'Bảng chấm công NS: ' + str(rec.employee_multi_id.sudo().name.sudo().name) + ' ' + str(
                               rec.month_year_compute)))
        return result

    @api.model
    def create(self, vals):
        if 'last_day_of_month' in vals and 'attendance_id' in vals and 'year' in vals and 'month' in vals:
            if 'attendance_id' in vals:
                if vals.get('last_day_of_month') == 0 or vals.get('year') == 0 or vals.get('month') == 0:
                    attendance = self.env['sea.hr.attendance'].sudo().search([('id', '=', vals.get('attendance_id'))])
                    vals['year'] = int(attendance.year)
                    vals['month'] = int(attendance.month)
                    vals['last_day_of_month'] = int(calendar.monthrange(vals.get('year'), vals.get('month'))[1])
        calendar_employee = self.env['sea.hr.calendar.employee'].sudo().search(
            [('employee_multi_id', '=', vals.get('employee_multi_id')),
             ('attendance_id', '=', vals.get('attendance_id')), ('month', '=', vals.get('month')),
             ('year', '=', vals.get('year'))])
        if calendar_employee:
            list_shifts = []
            # print(calendar_employee.employee_multi_id.sudo().name.sudo().name)
            for i in range(vals.get('last_day_of_month') + 1):
                if i > 0:
                    dates = int(date.weekday(date(vals.get('year'), vals.get('month'), i)))
                    # if dates not in [5, 6]:
                    '''tính theo thứ của config shift'''
                    if calendar_employee.get_day(i):
                        day = 'day_' + str(i)
                        if day not in vals:
                            work_number = 0
                            for calendar_e in calendar_employee.get_day(i):
                                if dates == 0 and calendar_e.thu_2 \
                                        or dates == 1 and calendar_e.thu_3 \
                                        or dates == 2 and calendar_e.thu_4 \
                                        or dates == 3 and calendar_e.thu_5 \
                                        or dates == 4 and calendar_e.thu_6 \
                                        or dates == 5 and calendar_e.thu_7 \
                                        or dates == 6 and calendar_e.thu_8:
                                    list_shifts.append(calendar_e.id)
                                    work_number += float(calendar_e.sudo().work_day)

                            '''tính toán cụ thể symbol cho NS có not_attendance = True'''
                            symbol = 1
                            check_not_attendance = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                                [('employee_multi_id', '=', vals.get('employee_multi_id'))], limit=1)

                            if check_not_attendance:
                                if check_not_attendance.not_attendance and work_number:
                                    syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                        [('work_number', '=', work_number), ('default_attendance', '=', True)], limit=1)
                                    if syy:
                                        symbol = syy.id
                            value = {
                                'employee_multi_id': vals.get('employee_multi_id'),
                                'year': int(vals.get('year')),
                                'month': int(vals.get('month')),
                                'day': int(i),
                                'symbol': symbol,
                                # 'shift': [(6, 0, calendar_employee.get_day(i).ids)]
                                'shift': [(6, 0, list_shifts)] if list_shifts else False
                            }
                            day_detail = self.env['sea.hr.attendance.realtime'].sudo().create(value)
                            vals[day] = day_detail.id
        result = super(Attendance, self).create(vals)
        return result

    @api.multi
    def write(self, vals):
        res = super(Attendance, self).write(vals)

        return res


class SeaHrAttendance(models.Model):
    _name = 'sea.hr.attendance'
    _description = "Attendances"
    _sql_constraints = [('model_month_year_company_uniq', 'unique(company_id,month,year)',
                         'Attendance with this month of company is  already exist!!')]
    _order = 'company_code, year, month asc'

    mark_as_todo = fields.Boolean(string='Mark as todo', default=False)
    company_id = fields.Many2one('res.company', string='Công Ty', required=True,
                                 default=lambda self: self.env.user.company_id.id)
    '''dkh add for sorting'''

    def _compute_company_code_compute(self):
        for rec in self:
            rec.sudo().write({'company_code': rec.company_id.sudo().code})

    job_code_compute = fields.Char(compute='_compute_company_code_compute')
    company_code = fields.Char(string='Company Code')

    date = fields.Date(string="Ngày tạo", default=fields.Date.today())

    month = fields.Selection(
        [(1, "Tháng 1"), (2, "Tháng 2"), (3, "Tháng 3"), (4, "Tháng 4"), (5, "Tháng 5"), (6, "Tháng 6"),
         (7, "Tháng 7"), (8, "Tháng 8"), (9, "Tháng 9"), (10, "Tháng 10"), (11, "Tháng 11"),
         (12, "Tháng 12")],
        string='Tháng', default=lambda self: fields.datetime.now().month, required=True)

    @api.model
    def year_selection(self):
        year = 2000
        year_list = []
        while year != 2201:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    year = fields.Selection(year_selection, string="Năm", default=fields.Date.today().strftime("%Y"), required=True)
    attendance_of_month = fields.One2many('sea.hr.attendance.month', 'attendance_id', string="Ngày trong tháng")

    '''add domain'''
    department_all = fields.Char(string='Tất cả Department của Company', compute='department_all_compute')
    department_id = fields.Many2one('hr.department', string='Tìm theo phòng ban')
    employee_id = fields.Char(string='Tìm theo tên nhân sự hoặc mã SeaCode')
    ''''''

    def department_all_compute(self):
        for rec in self:
            departments = self.env['hr.department'].sudo().search([('company_id', '=', rec.company_id.id)])
            list_department = []
            for department in departments:
                list_department.append({'id': department.id,
                                        'name': department.name,
                                        'sort_name': department.sort_name
                                        })
            rec.department_all = json.dumps(list_department, ensure_ascii=False)

    # @api.onchange('department_code', 'employee_id')
    # def onchange_department_code_or_employee(self):
    #     for rec in self:
    #         if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
    #                 'seatek_hr_attendance.hr_attendance_manager'):
    #             if rec.department_code or rec.employee_id:
    #                 hr_employee = False
    #                 if rec.employee_id:
    #                     hr_employee = self.env['hr.employee'].sudo().search(
    #                         ['|', ('s_identification_id', 'ilike', rec.employee_id),
    #                          ('name', 'ilike', rec.employee_id), ('company_id', '=', rec.company_id.id)])
    #
    #                 else:
    #                     rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #                         lambda record: record.department_code == rec.department_code)
    #
    #                 if hr_employee:
    #                     if rec.department_code:
    #                         rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #                             lambda
    #                                 record: record.department_code == rec.department_code and record.s_identification_id in [
    #                                 i.s_identification_id for i in
    #                                 hr_employee])
    #                     else:
    #                         rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #                             lambda record: record.s_identification_id in [i.s_identification_id for i in
    #                                                                           hr_employee])
    #             else:
    #                 rec.attendance_of_month_compute = rec.attendance_of_month
    #         else:
    #             if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
    #                 employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
    #                     [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
    #                 if employee_multi_id:
    #                     employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
    #                     if employee:
    #                         department_list = self.env['hr.department'].sudo().search(
    #                             [('manager_ids', '=', employee.id)])
    #                         list_employee = [employee_multi_id.id]
    #                         if department_list:
    #                             employee_department = self.env['hr.employee.multi.company'].sudo().search(
    #                                 [('department_id', 'in', department_list.ids)])
    #                             if employee_department:
    #                                 for i in employee_department:
    #                                     list_employee.append(i.id)
    #                         rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #                             lambda record: record.employee_multi_id.id in list_employee)

    def compute_attendance_of_month_compute(self):
        for rec in self:
            rec.attendance_of_month_compute = None
            attendance_of_month = rec.attendance_of_month

            if rec.department_id or rec.employee_id:
                hr_employee = False
                if rec.employee_id:
                    hr_employee = self.env['hr.employee'].sudo().search(
                        ['|', ('s_identification_id', 'ilike', rec.employee_id),
                         ('name', 'ilike', rec.employee_id), ('company_id', '=', rec.company_id.id)])

                else:
                    attendance_of_month = attendance_of_month.filtered(
                        lambda record: record.employee_multi_id.sudo().department_id.id == rec.department_id.id)

                if hr_employee:
                    if rec.department_id:
                        attendance_of_month = attendance_of_month.filtered(
                            lambda
                                record: record.employee_multi_id.sudo().department_id.id == rec.department_id.id and record.s_identification_id in [
                                i.s_identification_id for i in
                                hr_employee])
                    else:
                        attendance_of_month = attendance_of_month.filtered(
                            lambda record: record.s_identification_id in [i.s_identification_id for i in
                                                                          hr_employee])

            if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_manager'):
                # if rec.department_id or rec.employee_id:
                #     hr_employee = False
                #     if rec.employee_id:
                #         hr_employee = self.env['hr.employee'].sudo().search(
                #             ['|', ('s_identification_id', 'ilike', rec.employee_id),
                #              ('name', 'ilike', rec.employee_id), ('company_id', '=', rec.company_id.id)])
                #
                #     else:
                #         rec.attendance_of_month_compute = attendance_of_month.filtered(
                #             lambda record: record.employee_multi_id.sudo().department_id.id == rec.department_id.id)
                #
                #     if hr_employee:
                #         if rec.department_id:
                #             rec.attendance_of_month_compute = attendance_of_month.filtered(
                #                 lambda
                #                     record: record.employee_multi_id.sudo().department_id.id == rec.department_id.id and record.s_identification_id in [
                #                     i.s_identification_id for i in
                #                     hr_employee])
                #         else:
                #             rec.attendance_of_month_compute = attendance_of_month.filtered(
                #                 lambda record: record.s_identification_id in [i.s_identification_id for i in
                #                                                               hr_employee])
                # else:
                rec.attendance_of_month_compute = attendance_of_month
            else:
                if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                    employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                        [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
                    if employee_multi_id:
                        employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                        list_employee = [employee_multi_id.id]
                        if employee:
                            department_list = self.env['hr.department'].sudo().search(
                                [('manager_ids', '=', employee.id)])
                            if department_list:
                                employee_department = self.env['hr.employee.multi.company'].sudo().search(
                                    [('department_id', 'in', department_list.ids)])
                                if employee_department:
                                    for i in employee_department:
                                        list_employee.append(i.id)
                        rec.attendance_of_month_compute = attendance_of_month.filtered(
                            lambda record: record.employee_multi_id.id in list_employee)

    attendance_of_month_compute = fields.One2many('sea.hr.attendance.month', 'attendance_id',
                                                  compute='compute_attendance_of_month_compute',
                                                  string="Ngày trong tháng")

    check_managers = fields.Boolean(string='Check Managers', compute='check_managers_compute')

    def check_managers_compute(self):
        for rec in self:
            rec.check_managers = False
            employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
            if employee_multi_id:
                employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                if employee:
                    department_list = self.env['hr.department'].sudo().search(
                        [('manager_ids', '=', employee.id)])
                    if department_list:
                        rec.check_managers = True

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append(
                (rec.id, str(rec.company_id.sudo().short_name) + ' Tháng ' + str(rec.month) + '/' + str(rec.year)))
        return result

    @api.multi
    def write(self, vals):
        # print("value:", vals)
        return super(SeaHrAttendance, self).write(vals)

    @api.model
    def create(self, vals):
        result = super(SeaHrAttendance, self).create(vals)
        employees = self.env['hr.employee.multi.company'].sudo().search(
            [('company_id', '=', vals.get('company_id')), ('employee_current_status', '=', "working")])
        last_day_of_month = int(calendar.monthrange(int(result.year), int(result.month))[1])
        for employee in employees:
            value = {
                'employee_multi_id': employee.id,
                'attendance_id': result.id,
                'last_day_of_month': int(last_day_of_month),
                'year': int(result.year),
                'month': int(result.month)
            }

            '''tạo lịch làm việc'''
            self.env['sea.hr.calendar.employee'].sudo().create({
                'employee_multi_id': employee.id,
                'attendance_id': result.id,
                'last_day_of_month': int(last_day_of_month),
                'year': int(result.year),
                'month': int(result.month)
            })
            ''''tạo cho tháng'''
            self.env['sea.hr.attendance.month'].sudo().create(value)

        return result

    @api.multi
    def action_confirm(self):
        for rec in self:
            rec.mark_as_todo = True
            realtime_list = self.env['sea.hr.attendance.realtime'].sudo().search(
                [('company_id', '=',
                  rec.sudo().company_id.id),
                 ('month', '=', rec.month),
                 ('year', '=', rec.year)], limit=1)
            for realtime in realtime_list:
                realtime.mark_as_todo = True
        return True

    def print_attendance(self):
        return self.env.ref('seatek_hr_attendance.action_report_attendance').report_action(self)

    def print_attendance_violation(self):
        domain = [('check_late_soon', '=', True), ('month', '=', self.month),
                  ('year', '=', self.year)]
        if self.department_id:
            domain.append(('department_id', '=', self.department_id.id))

        if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_manager'):
            if self.env['sea.hr.attendance.details'].sudo().search(domain):
                return self.env.ref('seatek_hr_attendance.action_report_attendance_violation').report_action(self)
            else:
                raise ValidationError("Không có vi phạm nào cả")
        else:
            employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
            if employee_multi_id:
                employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                list_employee = [employee_multi_id.id]
                if employee:
                    department_list = self.env['hr.department'].sudo().search(
                        [('manager_ids', '=', employee.id)])
                    if department_list:
                        employee_department = self.env['hr.employee.multi.company'].sudo().search(
                            [('department_id', 'in', department_list.ids)])
                        if employee_department:
                            for i in employee_department:
                                list_employee.append(i.id)
                domain.append(('employee_multi_id', 'in', list_employee))
                if self.env['sea.hr.attendance.details'].sudo().search(domain):
                    return self.env.ref('seatek_hr_attendance.action_report_attendance_violation').report_action(self)
                else:
                    raise ValidationError("Không có vi phạm nào cả")
            else:
                raise ValidationError(
                    "Không tìm thấy bất kỳ thông tin nhân sự của bạn liên kết đến tài khoản hiện tại đang sử dụng")

    def print_attendance_calendar(self):
        pass

    def upgrade_attendance(self):
        for rec in self:
            for employee in rec.attendance_of_month_compute:
                # print(employee.employee_multi_id.sudo().name.name)
                if employee.last_day_of_month and employee.employee_multi_id:
                    calendar_employee = self.env['sea.hr.calendar.employee'].sudo().search(
                        [('employee_multi_id', '=', employee.employee_multi_id.id),
                         ('attendance_id', '=', rec.id), ('month', '=', rec.month),
                         ('year', '=', rec.year)])
                    for i in range(employee.last_day_of_month):
                        day = i + 1

                        upgrade_day = employee.get_day(day)

                        '''reset data table details'''
                        emp_delete = self.env['sea.hr.attendance.details'].sudo().search(
                            [('employee_multi_id', '=', employee.employee_multi_id.id),
                             ('attendance_realtime_id', '=', upgrade_day.id)])
                        if emp_delete:
                            emp_delete.sudo().unlink()
                        ''''''
                        realtime = self.env['attendance.realtime'].sudo().search(
                            [('day', '=', day), ('month', '=', employee.month),
                             ('year', '=', employee.year),
                             ('s_identification_id', '=', employee.employee_multi_id.sudo().s_identification_id)],
                            order="datetime asc")
                        if realtime:
                            stt = 0
                            for real in sorted(realtime, key=lambda re: re.datetime):
                                ot = False
                                stt += 1
                                month = real.month
                                year = real.year
                                time_employee_reality = datetime.datetime(year=real.datetime.year,
                                                                          month=real.datetime.month,
                                                                          day=real.datetime.day,
                                                                          hour=real.datetime.hour,
                                                                          minute=real.datetime.minute,
                                                                          second=real.datetime.second) \
                                                        + datetime.timedelta(hours=7)
                                day = time_employee_reality.day
                                time_employee = datetime.timedelta(hours=time_employee_reality.hour,
                                                                   minutes=time_employee_reality.minute,
                                                                   seconds=time_employee_reality.second)
                                shift_employee = self.env['sea.hr.calendar.employee'].sudo().search(
                                    [('employee_multi_id', '=', employee.employee_multi_id.id), ('month', '=', month),
                                     ('year', '=', year)])

                                if shift_employee:
                                    if shift_employee.get_day(day):
                                        if upgrade_day:
                                            for u_s in upgrade_day.shift:
                                                if u_s.id not in shift_employee.get_day(day).ids:
                                                    '''xóa ca đó khỏi sea_hr_attendance_realtime'''
                                                    upgrade_day.shift = [(3, u_s.id)]
                                                    # '''xóa luôn bảng details'''
                                                    # details = self.env['sea.hr.attendance.details'].sudo().search(
                                                    #     [('employee_multi_id', '=', employee.employee_multi_id.id),
                                                    #      ('attendance_realtime_id', '=', upgrade_day.id)])
                                                    # if details:
                                                    #     details.sudo().unlink()
                                                # else:
                                                #     '''nếu không có thay đổi ca làm việc đó thì data không đổi'''

                                        ''' xác định ca làm việc theo ngày giờ chấm công và chấm cho ca nào'''
                                        day_check, id_attendance_shift, check_in, check_late_or_soon, time_late_or_soon \
                                            = real.get_shift(employee.employee_multi_id, shift_employee.get_day(day),
                                                             time_employee, day,
                                                             month, year)

                                        if id_attendance_shift:
                                            if id_attendance_shift.sudo().first_in_late_out and 1 < stt < len(realtime):
                                                pass
                                            else:
                                                if time_late_or_soon and check_in:
                                                    # # print(time_late_or_soon, time_employee)
                                                    # '''tính toán số giờ sớm muộn
                                                    #     cần tách tính giờ trễ sớm
                                                    #     qua hàm create và write của shift_details'''
                                                    # check_in_late_or_soon_hour = '00:00:00'
                                                    # if time_employee > time_late_or_soon and check_in in ['check_in',
                                                    #                                                       'check_in_noon']:
                                                    #     check_in_l_s = time_employee - time_late_or_soon
                                                    #     check_in_l_s = datetime.datetime.strptime(str(check_in_l_s),
                                                    #                                               "%H:%M:%S")
                                                    #     check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                                                    #     # print('trễ', check_in_late_or_soon_hour)
                                                    #
                                                    # elif time_employee < time_late_or_soon and check_in in [
                                                    #     'check_out_noon', 'check_out']:
                                                    #     check_in_l_s = time_late_or_soon - time_employee
                                                    #     check_in_l_s = datetime.datetime.strptime(str(check_in_l_s),
                                                    #                                               "%H:%M:%S")
                                                    #     check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                                                    #     # print('sớm', check_in_late_or_soon_hour)

                                                    '''tổng hợp chi tiết'''

                                                    employee_attendance_realtime = self.env[
                                                        'sea.hr.attendance.realtime'].sudo().search(
                                                        [('employee_multi_id', '=', employee.employee_multi_id.id),
                                                         ('day', '=', day_check),
                                                         ('month', '=', month), ('year', '=', year)], limit=1)
                                                    if employee_attendance_realtime:
                                                        realtime_id = employee_attendance_realtime
                                                        '''cập nhật'''
                                                        '''shift'''
                                                        if id_attendance_shift.id not in employee_attendance_realtime.shift.ids:
                                                            # print('thêm mới ca cho tổng hợp')
                                                            employee_attendance_realtime.write(
                                                                {'shift': [(4, id_attendance_shift.id)]})

                                                        '''shift_details'''
                                                        if id_attendance_shift.id not in [i.sudo().shift.id for i in
                                                                                          employee_attendance_realtime.shift_details]:
                                                            # print('thêm chi tiết')
                                                            # work_number = 0.5 if id_attendance_shift.work_break else 1
                                                            # work_number = work_number * id_attendance_shift.work_day
                                                            # syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                                            #     [('work_number', '=', work_number)], limit=1)
                                                            employee_attendance_realtime.write(
                                                                {'shift_details': [(0, 0, {
                                                                    'employee_multi_id': employee.employee_multi_id.id,
                                                                    'company_id': employee.employee_multi_id.sudo().company_id.id,
                                                                    'attendance_realtime_id': realtime_id.id,
                                                                    'shift': id_attendance_shift.id,
                                                                    'location_check_id': real.location_check_id.id if real.location_check_id else None,
                                                                    # 'symbol': None if not syy else syy.id,
                                                                    check_in: real.datetime,
                                                                    # check_late_or_soon: check_in_late_or_soon_hour,
                                                                })]})
                                                            # print('1', check_in, real.datetime)
                                                        else:
                                                            '''check in lấy lần sớm nhất"
                                                            "còn check out thì lấy lần cuối'''
                                                            for shift_detail in employee_attendance_realtime.shift_details:
                                                                if shift_detail.sudo().shift.id == id_attendance_shift.id:
                                                                    write = False \
                                                                        if not shift_detail.sudo().shift.first_in_late_out \
                                                                        else True
                                                                    if not write:
                                                                        hour_check_in = datetime.timedelta(
                                                                            hours=shift_detail.check_in.hour,
                                                                            minutes=shift_detail.check_in.minute,
                                                                            seconds=shift_detail.check_in.second) \
                                                                                        + datetime.timedelta(
                                                                            hours=7) \
                                                                            if shift_detail.check_in \
                                                                            else False
                                                                        hour_check_out = datetime.timedelta(
                                                                            hours=shift_detail.check_out.hour,
                                                                            minutes=shift_detail.check_out.minute,
                                                                            seconds=shift_detail.check_out.second) \
                                                                                         + datetime.timedelta(
                                                                            hours=7) \
                                                                            if shift_detail.check_out else False

                                                                        hour_check_in_noon = datetime.timedelta(
                                                                            hours=shift_detail.check_in_noon.hour,
                                                                            minutes=shift_detail.check_in_noon.minute,
                                                                            seconds=shift_detail.check_in_noon.second) + datetime.timedelta(
                                                                            hours=7) \
                                                                            if shift_detail.check_in_noon else False
                                                                        hour_check_out_noon = datetime.timedelta(
                                                                            hours=shift_detail.check_out_noon.hour,
                                                                            minutes=shift_detail.check_out_noon.minute,
                                                                            seconds=shift_detail.check_out_noon.second) + datetime.timedelta(
                                                                            hours=7) \
                                                                            if shift_detail.check_out_noon else False
                                                                        if check_in == 'check_in':
                                                                            if not shift_detail.check_in \
                                                                                    or hour_check_in > time_employee \
                                                                                    and shift_detail.check_in.day >= \
                                                                                    real.datetime.day:
                                                                                write = True
                                                                        elif check_in == 'check_out_noon':
                                                                            if not shift_detail.check_out_noon \
                                                                                    or hour_check_out_noon < \
                                                                                    time_employee \
                                                                                    and shift_detail.check_out_noon.day \
                                                                                    <= real.datetime.day:
                                                                                write = True
                                                                        elif check_in == 'check_in_noon':
                                                                            if not shift_detail.check_in_noon \
                                                                                    or hour_check_in_noon > \
                                                                                    time_employee and \
                                                                                    shift_detail.check_in_noon.day \
                                                                                    >= real.datetime.day:
                                                                                write = True
                                                                        elif check_in == 'check_out':
                                                                            if not shift_detail.check_out \
                                                                                    or hour_check_out < time_employee \
                                                                                    and shift_detail.check_out.day <= \
                                                                                    real.datetime.day:
                                                                                write = True

                                                                    if write:
                                                                        '''???_test lại thử_???'''
                                                                        # sy = shift_detail.symbol.sudo().work_number
                                                                        # if shift_detail.work_break:
                                                                        #     if check_in in ['check_in', 'check_out_noon']:
                                                                        #         if shift_detail.check_out \
                                                                        #                 or shift_detail.check_in_noon:
                                                                        #             sy = 1
                                                                        #     elif shift_detail.check_in \
                                                                        #             or shift_detail.check_out_noon:
                                                                        #         sy = 1
                                                                        #     else:
                                                                        #         sy = 0.5
                                                                        # else:
                                                                        #     sy = 1
                                                                        # work_number = sy * id_attendance_shift.work_day
                                                                        # syy = self.env[
                                                                        #     'sea.hr.timesheet.symbol'].sudo().search(
                                                                        #     [('work_number', '=', work_number)], limit=1)
                                                                        employee_attendance_realtime.write(
                                                                            {'shift_details': [(1, shift_detail.id, {
                                                                                check_in: real.datetime,
                                                                                'location_check_id':
                                                                                    real.location_check_id.id
                                                                                    if real.location_check_id
                                                                                    else None,
                                                                            })]})
                                                                        # print('2', check_in, real.datetime)
                                                                        break
                                                    else:
                                                        '''tạo mới'''
                                                        value = {
                                                            'employee_multi_id': employee.employee_multi_id.id,
                                                            'day': int(day_check),
                                                            'month': int(month),
                                                            'year': int(year),
                                                            'shift': [(6, 0, [id_attendance_shift.id])],
                                                        }
                                                        realtime_id = self.env[
                                                            'sea.hr.attendance.realtime'].sudo().create(
                                                            value)

                                                        '''chi tiết chấm công'''
                                                        # work_number = 0.5 if id_attendance_shift.work_break else 1
                                                        # work_number = work_number * id_attendance_shift.work_day
                                                        # syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                                        #     [('work_number', '=', work_number)], limit=1)
                                                        attendance_details = self.env[
                                                            'sea.hr.attendance.details'].sudo().create({
                                                            'employee_multi_id': employee.employee_multi_id.id,
                                                            'company_id': employee.employee_multi_id.sudo().company_id.id,
                                                            'attendance_realtime_id': realtime_id.id,
                                                            'shift': id_attendance_shift.id,
                                                            'location_check_id': real.location_check_id.id
                                                            if real.location_check_id
                                                            else None,
                                                            # 'symbol': None if not syy else syy.id,
                                                            check_in: real.datetime,
                                                            # check_late_or_soon: check_in_late_or_soon_hour,
                                                        })
                                                        # print('3', check_in, real.datetime)

                                                    '''kiểm tra NS này đã được tạo bảng chấm công chưa'''
                                                    attendance_month = self.env[
                                                        'sea.hr.attendance.month'].sudo().search(
                                                        [('employee_multi_id', '=', employee.employee_multi_id.id),
                                                         ('month', '=', month),
                                                         ('year', '=', year)])
                                                    day_of_month = 'day_' + str(day_check)
                                                    if attendance_month:
                                                        '''cập nhật lại'''
                                                        attendance_month.write({day_of_month: realtime_id.id})
                                                    else:
                                                        '''tạo lại cho NS bảng chấm công mới'''
                                                        attendance_id = self.env['sea.hr.attendance'].sudo().search(
                                                            [('company_id', '=',
                                                              employee.employee_multi_id.sudo().company_id.id),
                                                             ('month', '=', month),
                                                             ('year', '=', year)], limit=1)
                                                        if attendance_id:
                                                            values = {
                                                                'employee_multi_id': employee.employee_multi_id.id,
                                                                'attendance_id': attendance_id.id,
                                                                'last_day_of_month': int(
                                                                    calendar.monthrange(year, month)[1]),
                                                                'year': int(year),
                                                                'month': int(month),
                                                                day_of_month: realtime_id.id,
                                                            }
                                                            self.env['sea.hr.attendance.month'].sudo().create(values)
                                        else:
                                            ot = True
                                    else:
                                        ot = True
                                else:
                                    ot = True
                                if ot:
                                    # print("OT")
                                    '''OT -- cứ lấy check in check out cho mỗi lần chấm công'''
                                    syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                        [('symbol', '=', 'OT'), ('default_attendance', '=', True)], limit=1)
                                    '''đảm bảo rằng nếu có ca first in late out thì chỉ có ca đó trong ngày'''
                                    if syy:
                                        # print("OT", syy)
                                        employee_realtime = self.env['sea.hr.attendance.realtime'].sudo().search(
                                            [('employee_multi_id', '=', employee.employee_multi_id.id),
                                             ('day', '=', day),
                                             ('month', '=', month), ('year', '=', year)], limit=1)
                                        if not employee_realtime:
                                            # print("OT not employee_realtime")
                                            '''tạo mới attendance.realtime'''
                                            value = {
                                                'employee_multi_id': employee.employee_multi_id.id,
                                                'day': int(day),
                                                'month': int(month),
                                                'year': int(year),
                                                'shift': None,
                                                'symbol': syy.id,
                                            }
                                            realtime_id = self.env['sea.hr.attendance.realtime'].sudo().create(value)
                                            '''chi tiết chấm công'''
                                            self.env['sea.hr.attendance.details'].sudo().create({
                                                'employee_multi_id': employee.employee_multi_id.id,
                                                'company_id': employee.sudo().company_id.id,
                                                'attendance_realtime_id': realtime_id.id,
                                                'location_check_id': real.location_check_id.id if real.location_check_id else None,
                                                'shift': None,
                                                'check_in': real.datetime,
                                                'symbol': syy.id,
                                            })

                                        else:
                                            realtime_id = employee_realtime
                                            if not employee_realtime.shift_details:
                                                # print("OT not shift_details")
                                                '''tạo mới shift_details'''
                                                employee_realtime.write({'shift_details': [(0, 0, {
                                                    'employee_multi_id': employee.employee_multi_id.id,
                                                    'company_id': employee.sudo().company_id.id,
                                                    'attendance_realtime_id': realtime_id.id,
                                                    'shift': None,
                                                    'location_check_id': real.location_check_id.id if real.location_check_id else None,
                                                    'symbol': syy.id,
                                                    'check_in': real.datetime,
                                                })]})
                                            else:
                                                check_create = True
                                                for shift_detail in sorted(employee_realtime.shift_details,
                                                                           key=lambda detail: detail.check_in):
                                                    # print("checkin: ", shift_detail.check_in)
                                                    '''so sánh thời gian của check in'''
                                                    check_in_temp = datetime.datetime(year=shift_detail.check_in.year,
                                                                                      month=shift_detail.check_in.month,
                                                                                      day=shift_detail.check_in.day,
                                                                                      hour=shift_detail.check_in.hour,
                                                                                      minute=shift_detail.check_in.minute,
                                                                                      second=shift_detail.check_in.second) \
                                                                    + datetime.timedelta(
                                                        hours=7) if shift_detail.check_in else False
                                                    check_out_temp = datetime.datetime(year=shift_detail.check_out.year,
                                                                                       month=shift_detail.check_out.month,
                                                                                       day=shift_detail.check_out.day,
                                                                                       hour=shift_detail.check_out.hour,
                                                                                       minute=shift_detail.check_out.minute,
                                                                                       second=shift_detail.check_out.second) \
                                                                     + datetime.timedelta(
                                                        hours=7) if shift_detail.check_out else False
                                                    hour_check_in = datetime.timedelta(hours=check_in_temp.hour,
                                                                                       minutes=check_in_temp.minute,
                                                                                       seconds=check_in_temp.second) if check_in_temp else False
                                                    hour_check_out = datetime.timedelta(hours=check_out_temp.hour,
                                                                                        minutes=check_out_temp.minute,
                                                                                        seconds=check_out_temp.second) if check_out_temp else False
                                                    if not shift_detail.check_in or hour_check_in > time_employee:
                                                        if shift_detail.check_out:
                                                            check_create = True
                                                            shift_detail.write(
                                                                {'check_in': real.datetime.replace(hour=0, minute=0,
                                                                                                   second=0) + time_employee - timedelta(
                                                                    hours=7), 'check_out': shift_detail.check_in})
                                                            time_employee = hour_check_out
                                                        else:
                                                            shift_detail.write(
                                                                {'check_in': real.datetime.replace(hour=0, minute=0,
                                                                                                   second=0) + time_employee - timedelta(
                                                                    hours=7), 'check_out': shift_detail.check_in})
                                                            check_create = False
                                                            break
                                                    else:
                                                        if not shift_detail.check_out or hour_check_out > time_employee:
                                                            if shift_detail.check_out:
                                                                check_create = True
                                                                shift_detail.write(
                                                                    {'check_out': real.datetime.replace(hour=0,
                                                                                                        minute=0,
                                                                                                        second=0) + time_employee - timedelta(
                                                                        hours=7)})
                                                                time_employee = hour_check_out
                                                            else:
                                                                shift_detail.write({
                                                                    'check_out': real.datetime.replace(hour=0, minute=0,
                                                                                                       second=0) + time_employee - timedelta(
                                                                        hours=7)
                                                                })
                                                                check_create = False
                                                                break
                                                            # print("hhhhh1: ", time_employee, shift_detail.check_out)
                                                if check_create:
                                                    # print("OT create new shift_details")
                                                    '''tạo mới shift_details'''
                                                    employee_realtime.write({'shift_details': [(0, 0, {
                                                        'employee_multi_id': employee.employee_multi_id.id,
                                                        'company_id': employee.employee_multi_id.sudo().company_id.id,
                                                        'attendance_realtime_id': realtime_id.id,
                                                        'shift': None,
                                                        'location_check_id': real.location_check_id.id if real.location_check_id else None,
                                                        'symbol': syy.id,
                                                        'check_in': real.datetime.replace(hour=0, minute=0,
                                                                                          second=0) + time_employee - timedelta(
                                                            hours=7),
                                                    })]})
                                        '''kiểm tra NS này đã được tạo bảng chấm công chưa'''
                                        attendance_month = self.env['sea.hr.attendance.month'].sudo().search(
                                            [('employee_multi_id', '=', employee.employee_multi_id.id),
                                             ('month', '=', month),
                                             ('year', '=', year)])
                                        day_of_month = 'day_' + str(day)
                                        if attendance_month:
                                            '''cập nhật lại'''
                                            attendance_month.write({day_of_month: realtime_id.id})
                                        else:
                                            values = {
                                                'employee_multi_id': employee.employee_multi_id.id,
                                                'attendance_id': rec.id,
                                                'last_day_of_month': int(calendar.monthrange(year, month)[1]),
                                                'year': int(year),
                                                'month': int(month),
                                                day_of_month: realtime_id.id,
                                            }
                                            self.env['sea.hr.attendance.month'].sudo().create(values)

                        elif calendar_employee:
                            list_shifts = []
                            dates = int(date.weekday(
                                date(int(rec.year), int(rec.month), day)))
                            '''tính theo thứ của config shift'''
                            if calendar_employee.get_day(day):
                                work_number = 0
                                for calendar_e in calendar_employee.get_day(day):
                                    if dates == 0 and calendar_e.thu_2 \
                                            or dates == 1 and calendar_e.thu_3 \
                                            or dates == 2 and calendar_e.thu_4 \
                                            or dates == 3 and calendar_e.thu_5 \
                                            or dates == 4 and calendar_e.thu_6 \
                                            or dates == 5 and calendar_e.thu_7 \
                                            or dates == 6 and calendar_e.thu_8:
                                        list_shifts.append(calendar_e.id)
                                        work_number += float(calendar_e.sudo().work_day)
                                if work_number > 0:
                                    check_not_attendance = self.env[
                                        'sea.hr.attendance.shift.employee'].sudo().search(
                                        [('employee_multi_id', '=',
                                          employee.employee_multi_id.id)], limit=1)
                                    if check_not_attendance:
                                        day_detail = self.env[
                                            'sea.hr.attendance.realtime'].sudo().search(
                                            [('employee_multi_id', '=',
                                              employee.employee_multi_id.id),
                                             ('day', '=', day),
                                             ('month', '=', rec.month),
                                             ('year', '=', rec.year)], limit=1)
                                        if not day_detail:
                                            '''tạo mới'''
                                            value = {
                                                'employee_multi_id': employee.employee_multi_id.id,
                                                'day': int(day),
                                                'month': int(rec.month),
                                                'year': int(rec.year),
                                                'shift': [(6, 0, list_shifts)],
                                            }
                                            day_detail = self.env['sea.hr.attendance.realtime'].sudo().create(value)
                                        '''???'''
                                        x = self.env['sea.hr.attendance.month'].sudo().search(
                                            [('employee_multi_id', '=', employee.employee_multi_id.id),
                                             ('attendance_id', '=', rec.id)])
                                        if x:
                                            x.sudo().write({'day_' + str(day): day_detail.id})
                                        if not day_detail.symbol_sign:
                                            if not check_not_attendance.not_attendance:
                                                day_detail.write({'symbol': 1})
                                            else:
                                                '''set default for employee not attendance'''
                                                '''tính toán cụ thể symbol cho NS có not_attendance = True'''
                                                syy = self.env[
                                                    'sea.hr.timesheet.symbol'].sudo().search(
                                                    [('work_number', '=',
                                                      work_number), ('default_attendance', '=', True)], limit=1)
                                                day_detail.write({'symbol': syy.id if syy else 1})

                                    ''''''

    def upgrade_calendar_for_shift(self):
        shifts = self.env['shift.employee.date.from.to'].sudo().search([('company_id', '=', self.company_id.id)])
        list_employee = []
        list_shift = []
        if self.calendar_of_month_compute:
            for i in self.calendar_of_month_compute:
                list_employee.append(i.employee_multi_id.id)
        if shifts:
            for shift in shifts:
                shift.write({'attendance_id_apply': self.id})
                if shift.employee_multi_ids:
                    if set(list_employee).intersection(set(shift.employee_multi_ids.ids)):
                        list_shift.append(shift.id)
        tree_view = self.env.ref('seatek_hr_attendance.shift_employee_date_from_to_tree_apply')
        return {
            'name': 'Shift of employees',
            'type': 'ir.actions.act_window',
            'res_model': 'shift.employee.date.from.to',
            'view_mode': 'tree',
            'views': [(tree_view.id, 'tree')],
            'target': 'new',
            'res_id': self.id,
            'domain': [('company_id', '=', self.company_id.id), ('id', 'in', list_shift)],
            # áp dụng cho apply duy nhất một lần
            # ('attendance_id_apply_list', 'not in', self.id)],
            'context': {}
        }

    def add_note_attendance_details(self):
        employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
            [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
        tree_view = self.env.ref('seatek_hr_attendance.sea_hr_attendance_details_edit_note_view_tree')
        if employee_multi_id:
            if self.env['sea.hr.attendance.details'].sudo().search([('check_late_soon', '=', True),
                                                                    ('month', '=', self.month),
                                                                    ('year', '=', self.year),
                                                                    ('employee_multi_id', '=', employee_multi_id.id)]):
                domain = [('check_late_soon', '=', True), ('month', '=', self.month), ('year', '=', self.year),
                          ('employee_multi_id', '=', employee_multi_id.id)]
                return {
                    'name': 'Attendances Details Violation',
                    'type': 'ir.actions.act_window',
                    'res_model': 'sea.hr.attendance.details',
                    'view_mode': 'tree',
                    'views': [(tree_view.id, 'tree')],
                    'target': 'new',
                    # 'res_id': self.id,
                    'domain': domain,
                    'context': {}
                }
            else:
                raise ValidationError("Bạn không có vi phạm nào cả")
        else:
            raise ValidationError(
                "Không tìm thấy bất kỳ thông tin nhân sự của bạn liên kết đến tài khoản hiện tại đang sử dụng")

    def approved_attendance_details(self):
        employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
            [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
        domain = [('check_late_soon', '=', True), ('month', '=', self.month), ('year', '=', self.year),
                  ('company_id', '=', self.env.user.company_id.id)]
        tree_view = self.env.ref('seatek_hr_attendance.sea_employee_details_approved_view_tree')
        if employee_multi_id:
            employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
            list_employee = [employee_multi_id.id]
            if employee:
                department_list = self.env['hr.department'].sudo().search(
                    [('manager_ids', '=', employee.id)])
                if department_list:
                    employee_department = self.env['hr.employee.multi.company'].sudo().search(
                        [('department_id', 'in', department_list.ids),
                         ('company_id', '=', self.env.user.company_id.id)])
                    if employee_department:
                        for i in employee_department:
                            list_employee.append(i.id)

            if self.env['sea.hr.attendance.details'].sudo().search([('check_late_soon', '=', True),
                                                                    ('month', '=', self.month),
                                                                    ('year', '=', self.year),
                                                                    ('employee_multi_id', 'in', list_employee),
                                                                    ('company_id', '=', self.env.user.company_id.id)]):
                domain.append(('employee_multi_id', 'in', list_employee))
                return {
                    'name': 'Attendances Details Violation',
                    'type': 'ir.actions.act_window',
                    'res_model': 'sea.hr.attendance.details',
                    'view_mode': 'tree',
                    'views': [(tree_view.id, 'tree')],
                    'domain': domain,
                    'context': {}
                }
            else:
                raise ValidationError("Không có vi phạm nào cả")
        else:
            raise ValidationError(
                "Không tìm thấy bất kỳ thông tin nhân sự của bạn liên kết đến tài khoản hiện tại đang sử dụng")
