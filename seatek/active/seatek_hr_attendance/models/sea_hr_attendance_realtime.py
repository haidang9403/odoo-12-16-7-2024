import calendar
import datetime
from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttendanceRealtime(models.Model):
    _name = 'attendance.realtime'
    _description = "Attendance Realtime"
    _order = 'datetime desc'

    s_identification_id = fields.Char(string='Mã nhân sự', required=True)
    datetime = fields.Datetime(track_visibility='onchange', string="Ngày giờ chấm công", required=True,
                               default=lambda self: fields.datetime.now())
    category = fields.Selection([('login', 'Đăng nhập'), ('logout', 'Đăng xuất'), ('overtime', 'Tăng ca')],
                                string="Loại chấm công")
    serial_number = fields.Char(string="Serial Number")
    gps_location = fields.Char(string="GPS Location")
    network_domain = fields.Char(string="Network Domain")
    location_check_id = fields.Many2one('sea.office', 'Location Check')

    type_attendance = fields.Selection([
        ('timekeeper', 'Máy chấm công'),
        ('telephone', 'Điện thoại')],
        string='Type of attendance')
    verify_mode = fields.Selection([('fingerprint', 'Fingerprint'), ('password', 'Password'), ('card', 'Card')])
    day = fields.Integer(string="Ngày", required=True)
    month = fields.Integer(string="Tháng", required=True)
    year = fields.Integer(string="Năm", required=True)

    @api.multi
    def get_shift(self, employee_multi, list_shift, time_employee, day, month, year):
        '''rút gọn lại'''
        # print('khánh nè')
        id_attendance_shift = False
        check_in = None
        check_late_or_soon = None
        time_late_or_soon = None
        day_check = day
        for shift_company in list_shift:
            id_attendance_shift = shift_company
            if shift_company.type_of_shift == 'full_time_shift':
                if id_attendance_shift.for_full_time_shift == 'check_in_day' \
                        and check_in == 'check_out':
                    day_check = day - 1
                elif id_attendance_shift.for_full_time_shift == 'check_out_day' \
                        and check_in == 'check_in':
                    day_check = day + 1
            if shift_company.first_in_late_out:
                '''case ca first_in_late_out = True'''
                '''đảm bảo rằng nếu có ca first in late out thì chỉ có ca đó trong ngày'''
                id_attendance_shift = shift_company
                employee_realtime = self.env['sea.hr.attendance.realtime'].sudo().search(
                    [('employee_multi_id', '=', employee_multi.id), ('day', '=', day_check),
                     ('month', '=', month), ('year', '=', year)], limit=1)
                # print(employee_realtime)
                if not employee_realtime:
                    if not shift_company.login_logout \
                            or shift_company.login_logout and self.category == 'login':
                        check_in = 'check_in'
                        check_late_or_soon = 'check_in_late'
                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start)
                        break
                else:
                    if id_attendance_shift.id not in [i.sudo().shift.id for i in
                                                      employee_realtime.shift_details]:
                        if not shift_company.login_logout \
                                or shift_company.login_logout and self.category == 'login':
                            check_in = 'check_in'
                            check_late_or_soon = 'check_in_late'
                            time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start)
                            break
                    else:
                        for i in employee_realtime.shift_details:
                            if i.sudo().shift.id == id_attendance_shift.id:
                                '''so sánh thời gian của check in'''
                                check_in_temp = datetime.datetime(year=i.check_in.year,
                                                                  month=i.check_in.month,
                                                                  day=i.check_in.day,
                                                                  hour=i.check_in.hour,
                                                                  minute=i.check_in.minute,
                                                                  second=i.check_in.second) \
                                                + datetime.timedelta(hours=7) if i.check_in else False

                                check_out_temp = datetime.datetime(year=i.check_out.year,
                                                                   month=i.check_out.month,
                                                                   day=i.check_out.day,
                                                                   hour=i.check_out.hour,
                                                                   minute=i.check_out.minute,
                                                                   second=i.check_out.second) \
                                                 + datetime.timedelta(hours=7) if i.check_out else False

                                hour_check_in = datetime.timedelta(hours=check_in_temp.hour,
                                                                   minutes=check_in_temp.minute,
                                                                   seconds=check_in_temp.second) if check_in_temp else False
                                hour_check_out = datetime.timedelta(hours=check_out_temp.hour,
                                                                    minutes=check_out_temp.minute,
                                                                    seconds=check_out_temp.second) if check_out_temp else False

                                if not i.check_in or hour_check_in > time_employee:
                                    if not shift_company.login_logout \
                                            or shift_company.login_logout and self.category == 'login':
                                        check_in = 'check_in'
                                        check_late_or_soon = 'check_in_late'
                                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start)
                                else:
                                    if not i.check_out or hour_check_out < time_employee:
                                        if not shift_company.login_logout \
                                                or shift_company.login_logout and self.category == 'logout':
                                            check_in = 'check_out'
                                            check_late_or_soon = 'check_out_soon'
                                            time_late_or_soon = datetime.timedelta(hours=shift_company.hour_end)
                                break

                        if check_in and check_late_or_soon:
                            break

            else:
                '''case shift first_in_late_out = False'''
                if shift_company.hour_start > 0 and datetime.timedelta(
                        hours=shift_company.hour_start_start) <= time_employee < datetime.timedelta(
                    hours=shift_company.hour_start_end):
                    if not shift_company.login_logout \
                            or shift_company.login_logout and self.category == 'login':
                        id_attendance_shift = shift_company
                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start)
                        check_in = 'check_in'
                        check_late_or_soon = 'check_in_late'
                        break
                elif shift_company.hour_end_noon > 0 and datetime.timedelta(
                        hours=shift_company.hour_end_noon_start) <= time_employee <= datetime.timedelta(
                    hours=shift_company.hour_end_noon_end):
                    if not shift_company.login_logout \
                            or shift_company.login_logout and self.category == 'login':
                        id_attendance_shift = shift_company
                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_end_noon)
                        check_in = 'check_in_noon'
                        check_late_or_soon = 'check_in_noon_late'
                        break
                elif shift_company.hour_end > 0 and datetime.timedelta(
                        hours=shift_company.hour_end_start) <= time_employee < datetime.timedelta(
                    hours=shift_company.hour_end_end):
                    if not shift_company.login_logout \
                            or shift_company.login_logout and self.category == 'logout':
                        id_attendance_shift = shift_company
                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_end)
                        check_in = 'check_out'
                        check_late_or_soon = 'check_out_soon'
                        break
                elif shift_company.hour_start_noon > 0 and datetime.timedelta(
                        hours=shift_company.hour_start_noon_start) <= \
                        time_employee < datetime.timedelta(hours=shift_company.hour_start_noon_end):
                    if not shift_company.login_logout \
                            or shift_company.login_logout and self.category == 'logout':
                        id_attendance_shift = shift_company
                        time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start_noon)
                        check_in = 'check_out_noon'
                        check_late_or_soon = 'check_out_noon_soon'
                        break
        return day_check, id_attendance_shift, check_in, check_late_or_soon, time_late_or_soon

    @api.model
    def check_duplicate_data(self, vals):
        # print("khkh: ", vals)
        if 's_identification_id' in vals:
            employee_id = self.env['hr.employee'].sudo().search(
                [('barcode', '=', vals.get('s_identification_id'))], limit=1)
            if employee_id:
                employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('employee_current_status', '!=', 'resigned'), ('name', '=', employee_id.id)], limit=1)
                if employee_multi_id:
                    vals['s_identification_id'] = employee_multi_id.s_identification_id
                else:
                    return False
            else:
                return False
            duplicate_employee = self.env['attendance.realtime'].sudo().search(
                [('s_identification_id', '=', vals.get('s_identification_id')),
                 ('datetime', '=', vals.get('datetime'))])
            if duplicate_employee:
                return False
        return self.env['attendance.realtime'].sudo().create(vals)

    @api.model
    def create(self, vals):
        if 'serial_number' in vals:
            timekeeper = self.env['sea.timekeeper'].sudo().search([('serial_number', '=', vals.get('serial_number'))],
                                                                  limit=1)
            if timekeeper:
                vals['location_check_id'] = timekeeper.sea_office_id.id
        elif 'gps_location' in vals:
            gps = self.env['sea.gps.location'].sudo().search([('gps', '=', vals.get('gps_location'))],
                                                             limit=1)
            if gps:
                vals['location_check_id'] = gps.sea_office_id.id
        elif 'network_domain' in vals:
            domain = self.env['sea.network.domain'].sudo().search([('domain', '=', vals.get('network_domain'))],
                                                                  limit=1)
            if domain:
                vals['location_check_id'] = domain.sea_office_id.id

        datetime_x = datetime.datetime.strptime(str(vals.get('datetime')), '%Y-%m-%d %H:%M:%S') + datetime.timedelta(
            hours=7)
        vals['day'] = datetime_x.day
        vals['month'] = datetime_x.month
        vals['year'] = datetime_x.year
        rec = super(AttendanceRealtime, self).create(vals)
        day = datetime_x.day
        month = datetime_x.month
        year = datetime_x.year
        employee_multi = self.env['hr.employee.multi.company'].sudo().search(
            [('employee_current_status', '!=', 'resigned'),
             ('s_identification_id', '=', rec.s_identification_id.upper())])
        ot = False
        if employee_multi:
            for employee in employee_multi:
                attendance_id = self.env['sea.hr.attendance'].sudo().search(
                    [('company_id', '=', employee.sudo().company_id.id), ('month', '=', month),
                     ('year', '=', year)], limit=1)
                if attendance_id:
                    time_employee = datetime.timedelta(hours=datetime_x.hour, minutes=datetime_x.minute,
                                                       seconds=datetime_x.second)
                    '''lấy ca từ lịch làm việc đảm bảo ca làm việc chỉ lấy từ lịch làm việc'''
                    shift_employee = self.env['sea.hr.calendar.employee'].sudo().search(
                        [('employee_multi_id', '=', employee.id), ('month', '=', rec.month),
                         ('year', '=', rec.year)])
                    if shift_employee:
                        if shift_employee.get_day(day):
                            ''' xác định ca làm việc theo ngày giờ chấm công và chấm cho ca nào'''
                            day_check, id_attendance_shift, check_in, check_late_or_soon, time_late_or_soon \
                                = rec.get_shift(employee, shift_employee.get_day(day), time_employee, day, month, year)
                            # '''case nhiều ca trong ngày'''
                            # for shift_company in shifts:
                            #     if shift_company.first_in_late_out:
                            #         '''case ca first_in_late_out = True'''
                            #         print('first_in_late_out')
                            #         id_attendance_shift = shift_company
                            #
                            #     else:
                            #         if shift_company.hour_start > 0 and datetime.timedelta(
                            #                 hours=shift_company.hour_start_start) <= time_employee < datetime.timedelta(
                            #                 hours=shift_company.hour_start_end):
                            #             if not shift_company.login_logout \
                            #                     or shift_company.login_logout and rec.category == 'login':
                            #                 id_attendance_shift = shift_company
                            #                 time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start)
                            #                 check_in = 'check_in'
                            #                 check_late_or_soon = 'check_in_late'
                            #                 break
                            #         elif shift_company.hour_end_noon > 0 and datetime.timedelta(
                            #                 hours=shift_company.hour_end_noon_start) <= time_employee <= datetime.timedelta(
                            #                 hours=shift_company.hour_end_noon_end):
                            #             if not shift_company.login_logout \
                            #                     or shift_company.login_logout and rec.category == 'login':
                            #                 id_attendance_shift = shift_company
                            #                 time_late_or_soon = datetime.timedelta(hours=shift_company.hour_end_noon)
                            #                 check_in = 'check_in_noon'
                            #                 check_late_or_soon = 'check_in_noon_late'
                            #                 break
                            #         elif shift_company.hour_end > 0 and datetime.timedelta(
                            #                 hours=shift_company.hour_end_start) <= time_employee < datetime.timedelta(
                            #                 hours=shift_company.hour_end_end):
                            #             if not shift_company.login_logout \
                            #                     or shift_company.login_logout and rec.category == 'logout':
                            #                 id_attendance_shift = shift_company
                            #                 time_late_or_soon = datetime.timedelta(hours=shift_company.hour_end)
                            #                 check_in = 'check_out'
                            #                 check_late_or_soon = 'check_out_soon'
                            #                 break
                            #         elif shift_company.hour_start_noon > 0 and datetime.timedelta(
                            #                 hours=shift_company.hour_start_noon_start) <= \
                            #                 time_employee < datetime.timedelta(hours=shift_company.hour_start_noon_end):
                            #             if not shift_company.login_logout \
                            #                     or shift_company.login_logout and rec.category == 'logout':
                            #                 id_attendance_shift = shift_company
                            #                 time_late_or_soon = datetime.timedelta(hours=shift_company.hour_start_noon)
                            #                 check_in = 'check_out_noon'
                            #                 check_late_or_soon = 'check_out_noon_soon'
                            #                 break

                            # print('check_in', check_in)
                            # print('check_late_or_soon', check_late_or_soon)
                            if id_attendance_shift:
                                # '''tính lại day'''
                                # day_check = day
                                # if id_attendance_shift.type_of_shift == 'full_time_shift':
                                #     if id_attendance_shift.for_full_time_shift == 'check_in_day' \
                                #             and check_in == 'check_out':
                                #         day_check -= 1
                                #     elif id_attendance_shift.for_full_time_shift == 'check_out_day' \
                                #             and check_in == 'check_in':
                                #         day_check += 1
                                # ''''''
                                if time_late_or_soon and check_in:
                                    # # print(time_late_or_soon, time_employee)
                                    # '''tính toán số giờ sớm muộn'''
                                    # '''cần tách tính giờ trễ sớm qua hàm create và write của shift_details'''
                                    # check_in_late_or_soon_hour = '00:00:00'
                                    # if time_employee > time_late_or_soon and check_in in ['check_in', 'check_in_noon']:
                                    #     check_in_l_s = time_employee - time_late_or_soon
                                    #     check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                                    #     check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                                    #     # print('trễ', check_in_late_or_soon_hour)
                                    #
                                    # elif time_employee < time_late_or_soon and check_in in ['check_out_noon', 'check_out']:
                                    #     check_in_l_s = time_late_or_soon - time_employee
                                    #     check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                                    #     check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                                    #     # print('sớm', check_in_late_or_soon_hour)
                                    '''tổng hợp chi tiết'''
                                    employee_realtime = self.env['sea.hr.attendance.realtime'].sudo().search(
                                        [('employee_multi_id', '=', employee.id), ('day', '=', day_check),
                                         ('month', '=', month), ('year', '=', year)], limit=1)
                                    if employee_realtime:
                                        realtime_id = employee_realtime
                                        '''cập nhật'''
                                        '''shift'''
                                        if id_attendance_shift.id not in employee_realtime.shift.ids:
                                            # print('thêm mới ca cho tổng hợp')
                                            employee_realtime.write({'shift': [(4, id_attendance_shift.id)]})

                                        '''shift_details'''
                                        if id_attendance_shift.id not in [i.sudo().shift.id for i in
                                                                          employee_realtime.shift_details]:
                                            # print('thêm chi tiết')
                                            # work_number = 0.5 if id_attendance_shift.work_break else 1
                                            # work_number = work_number * id_attendance_shift.work_day
                                            # syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                            #     [('work_number', '=', work_number)], limit=1)
                                            employee_realtime.write({'shift_details': [(0, 0, {
                                                'employee_multi_id': employee.id,
                                                'company_id': employee.sudo().company_id.id,
                                                'attendance_realtime_id': realtime_id.id,
                                                'shift': id_attendance_shift.id,
                                                'location_check_id': vals.get('location_check_id'),
                                                # 'symbol': None if not syy else syy.id,
                                                check_in: rec.datetime,
                                                # check_late_or_soon: check_in_late_or_soon_hour,
                                            })]})
                                        else:
                                            '''check in lấy lần sớm nhất"
                                            "còn check out thì lấy lần cuối'''
                                            for i in employee_realtime.shift_details:
                                                if i.sudo().shift.id == id_attendance_shift.id:
                                                    '''???nếu thời gian được đưa lên lộn xộn vậy cần tính lại
                                                    VD: check_in lúc đầu là 15H sau đó thì check_in là 8h30
                                                    thì cái 15H phải so sánh với check out và tính tiếp tục???'''
                                                    write = False if not i.sudo().shift.first_in_late_out else True
                                                    if not write:
                                                        hour_check_in = datetime.timedelta(hours=i.check_in.hour,
                                                                                           minutes=i.check_in.minute,
                                                                                           seconds=i.check_in.second) \
                                                                        + datetime.timedelta(
                                                            hours=7) if i.check_in else False
                                                        hour_check_out = datetime.timedelta(hours=i.check_out.hour,
                                                                                            minutes=i.check_out.minute,
                                                                                            seconds=i.check_out.second) \
                                                                         + datetime.timedelta(
                                                            hours=7) if i.check_out else False

                                                        hour_check_in_noon = datetime.timedelta(
                                                            hours=i.check_in_noon.hour,
                                                            minutes=i.check_in_noon.minute,
                                                            seconds=i.check_in_noon.second) \
                                                                             + datetime.timedelta(
                                                            hours=7) if i.check_in_noon else False
                                                        hour_check_out_noon = datetime.timedelta(
                                                            hours=i.check_out_noon.hour,
                                                            minutes=i.check_out_noon.minute,
                                                            seconds=i.check_out_noon.second) \
                                                                              + datetime.timedelta(
                                                            hours=7) if i.check_out_noon else False
                                                        write = False
                                                        # if check_in in ['check_out_noon', 'check_out'] \
                                                        #         or i.check_in in [None, False] and check_in == 'check_in' \
                                                        #         or i.check_in_noon in [None,
                                                        #                                False] and check_in == 'check_in_noon':
                                                        # print('cập nhật chi tiết')
                                                        if check_in == 'check_in':
                                                            if not i.check_in or hour_check_in > time_employee and i.check_in.day >= day:
                                                                write = True
                                                        elif check_in == 'check_in_noon':
                                                            if not i.check_in_noon or hour_check_in_noon > time_employee and i.check_in.day >= day:
                                                                write = True
                                                        elif check_in == 'check_out':
                                                            if not i.check_out or hour_check_out < time_employee and i.check_in.day <= day:
                                                                write = True
                                                        elif check_in == 'check_out_noon':
                                                            if not i.check_out_noon or hour_check_out_noon < time_employee and i.check_in.day <= day:
                                                                write = True
                                                    if write:
                                                        '''???_test lại thử_???'''
                                                        # sy = i.symbol.sudo().work_number
                                                        # if i.work_break:
                                                        #     if check_in in ['check_in', 'check_out_noon']:
                                                        #         if i.check_out \
                                                        #                 or i.check_in_noon:
                                                        #             sy = 1
                                                        #     elif i.check_in \
                                                        #             or i.check_out_noon:
                                                        #         sy = 1
                                                        #     else:
                                                        #         sy = 0.5
                                                        # else:
                                                        #     sy = 1

                                                        # if i.symbol.sudo().work_number == 0:
                                                        #     if i.sudo().work_break:
                                                        #         sy = 0.5
                                                        #     else:
                                                        #         sy = 1
                                                        # else:
                                                        #     if i.symbol.sudo().work_number == 0.5:
                                                        #         if i.work_break:
                                                        #             if check_in in ['check_in', 'check_out_noon']:
                                                        #                 if i.check_out \
                                                        #                         or i.check_in_noon:
                                                        #                     sy = 1
                                                        #             elif i.check_in \
                                                        #                     or i.check_out_noon:
                                                        #                 sy = 1
                                                        # work_number = sy * id_attendance_shift.work_day
                                                        # syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                                        #     [('work_number', '=', work_number)], limit=1)
                                                        employee_realtime.write(
                                                            {'shift_details': [(1, i.id, {
                                                                'location_check_id': vals.get('location_check_id'),
                                                                check_in: rec.datetime,
                                                                # 'symbol': None if not syy else syy.id,
                                                                # check_late_or_soon: check_in_late_or_soon_hour,
                                                            })]})
                                                        break
                                    else:
                                        '''tạo mới'''
                                        value = {
                                            'employee_multi_id': employee.id,
                                            'day': int(day_check),
                                            'month': int(month),
                                            'year': int(year),
                                            'shift': [(6, 0, [id_attendance_shift.id])],
                                        }
                                        realtime_id = self.env['sea.hr.attendance.realtime'].sudo().create(value)

                                        '''chi tiết chấm công'''
                                        # work_number = 0.5 if id_attendance_shift.work_break else 1
                                        # work_number = work_number * id_attendance_shift.work_day
                                        # syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                                        #     [('work_number', '=', work_number)], limit=1)
                                        attendance_details = self.env['sea.hr.attendance.details'].sudo().create({
                                            'employee_multi_id': employee.id,
                                            'company_id': employee.sudo().company_id.id,
                                            'attendance_realtime_id': realtime_id.id,
                                            # 'symbol': None if not syy else syy.id,
                                            'location_check_id': vals.get('location_check_id'),
                                            'shift': id_attendance_shift.id,
                                            check_in: rec.datetime,
                                            # check_late_or_soon: check_in_late_or_soon_hour,
                                        })

                                    '''kiểm tra NS này đã được tạo bảng chấm công chưa'''
                                    attendance_month = self.env['sea.hr.attendance.month'].sudo().search(
                                        [('employee_multi_id', '=', employee.id), ('month', '=', month),
                                         ('year', '=', year)])
                                    day_of_month = 'day_' + str(day_check)
                                    if attendance_month:
                                        '''cập nhật lại'''
                                        attendance_month.write({day_of_month: realtime_id.id})
                                        # print('cập nhật cho bảng chấm công tháng', day_of_month, realtime_id)
                                    else:
                                        '''tạo lại cho NS bảng chấm công mới'''
                                        values = {
                                            'employee_multi_id': employee.id,
                                            'attendance_id': attendance_id.id,
                                            'last_day_of_month': int(calendar.monthrange(year, month)[1]),
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
                                [('employee_multi_id', '=', employee.id), ('day', '=', day),
                                 ('month', '=', month), ('year', '=', year)], limit=1)
                            if not employee_realtime:
                                # print("OT not employee_realtime")
                                '''tạo mới attendance.realtime'''
                                value = {
                                    'employee_multi_id': employee.id,
                                    'day': int(day),
                                    'month': int(month),
                                    'year': int(year),
                                    'shift': None,
                                    'symbol': syy.id,
                                }
                                realtime_id = self.env['sea.hr.attendance.realtime'].sudo().create(value)
                                '''chi tiết chấm công'''
                                self.env['sea.hr.attendance.details'].sudo().create({
                                    'employee_multi_id': employee.id,
                                    'company_id': employee.sudo().company_id.id,
                                    'attendance_realtime_id': realtime_id.id,
                                    'location_check_id': vals.get('location_check_id'),
                                    'shift': None,
                                    'check_in': rec.datetime,
                                    'symbol': syy.id,
                                })

                            else:
                                realtime_id = employee_realtime
                                if not employee_realtime.shift_details:
                                    # print("OT not shift_details")
                                    '''tạo mới shift_details'''
                                    employee_realtime.write({'shift_details': [(0, 0, {
                                        'employee_multi_id': employee.id,
                                        'company_id': employee.sudo().company_id.id,
                                        'attendance_realtime_id': realtime_id.id,
                                        'shift': None,
                                        'location_check_id': vals.get('location_check_id'),
                                        'symbol': syy.id,
                                        'check_in': rec.datetime,
                                    })]})
                                else:
                                    check_create = True
                                    for i in sorted(employee_realtime.shift_details, key=lambda x: x.check_in):
                                        # print("checkin: ", i.check_in)
                                        '''so sánh thời gian của check in'''
                                        check_in_temp = datetime.datetime(year=i.check_in.year,
                                                                          month=i.check_in.month,
                                                                          day=i.check_in.day,
                                                                          hour=i.check_in.hour,
                                                                          minute=i.check_in.minute,
                                                                          second=i.check_in.second) \
                                                        + datetime.timedelta(hours=7) if i.check_in else False
                                        check_out_temp = datetime.datetime(year=i.check_out.year,
                                                                           month=i.check_out.month,
                                                                           day=i.check_out.day,
                                                                           hour=i.check_out.hour,
                                                                           minute=i.check_out.minute,
                                                                           second=i.check_out.second) \
                                                         + datetime.timedelta(hours=7) if i.check_out else False
                                        hour_check_in = datetime.timedelta(hours=check_in_temp.hour,
                                                                           minutes=check_in_temp.minute,
                                                                           seconds=check_in_temp.second) if check_in_temp else False
                                        hour_check_out = datetime.timedelta(hours=check_out_temp.hour,
                                                                            minutes=check_out_temp.minute,
                                                                            seconds=check_out_temp.second) if check_out_temp else False
                                        if not i.check_in or hour_check_in > time_employee:
                                            # print("gggggg: ", time_employee, i.check_in, i.check_out)
                                            if i.check_out:
                                                check_create = True
                                                i.write({'check_in': rec.datetime.replace(hour=0, minute=0,
                                                                                          second=0) + time_employee - timedelta(
                                                    hours=7), 'check_out': i.check_in})
                                                time_employee = hour_check_out
                                            else:
                                                i.write({'check_in': rec.datetime.replace(hour=0, minute=0,
                                                                                          second=0) + time_employee - timedelta(
                                                    hours=7), 'check_out': i.check_in})
                                                check_create = False
                                                break
                                            # print("gggggg1: ", time_employee, i.check_in, i.check_out)
                                        else:
                                            if not i.check_out or hour_check_out > time_employee:
                                                # print("hhhhh: ", time_employee, i.check_out)
                                                if i.check_out:
                                                    check_create = True
                                                    i.write({'check_out': rec.datetime.replace(hour=0, minute=0,
                                                                                               second=0) + time_employee - timedelta(
                                                        hours=7)})
                                                    time_employee = hour_check_out
                                                else:
                                                    i.write({
                                                        'check_out': rec.datetime.replace(hour=0, minute=0,
                                                                                          second=0) + time_employee - timedelta(
                                                            hours=7)
                                                    })
                                                    check_create = False
                                                    break
                                                # print("hhhhh1: ", time_employee, i.check_out)
                                    if check_create:
                                        # print("OT create new shift_details")
                                        '''tạo mới shift_details'''
                                        employee_realtime.write({'shift_details': [(0, 0, {
                                            'employee_multi_id': employee.id,
                                            'company_id': employee.sudo().company_id.id,
                                            'attendance_realtime_id': realtime_id.id,
                                            'shift': None,
                                            'location_check_id': vals.get('location_check_id'),
                                            'symbol': syy.id,
                                            'check_in': rec.datetime.replace(hour=0, minute=0,
                                                                             second=0) + time_employee - timedelta(
                                                hours=7),
                                        })]})
                            '''kiểm tra NS này đã được tạo bảng chấm công chưa'''
                            attendance_month = self.env['sea.hr.attendance.month'].sudo().search(
                                [('employee_multi_id', '=', employee.id), ('month', '=', month),
                                 ('year', '=', year)])
                            day_of_month = 'day_' + str(day)
                            if attendance_month:
                                '''cập nhật lại'''
                                attendance_month.write({day_of_month: realtime_id.id})
                            else:
                                values = {
                                    'employee_multi_id': employee.id,
                                    'attendance_id': attendance_id.id,
                                    'last_day_of_month': int(calendar.monthrange(year, month)[1]),
                                    'year': int(year),
                                    'month': int(month),
                                    day_of_month: realtime_id.id,
                                }
                                self.env['sea.hr.attendance.month'].sudo().create(values)
        return rec


class AttendanceDetails(models.Model):
    _name = 'sea.hr.attendance.details'
    _description = "Attendance Details"

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên")
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)
    company_id = fields.Many2one('res.company', string="Công Ty", required=True,
                                 default=lambda self: self.env.user.company_id)

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

            rec.domain_shift = shifts.ids

    domain_shift = fields.Many2many('sea.hr.attendance.shift', string='Domain', compute='domain_compute')

    shift = fields.Many2one('sea.hr.attendance.shift', string="Ca làm việc", domain="[('id', 'in', domain_shift)]")
    work_break = fields.Boolean(string="Nghỉ giữa ca", store=False, related='shift.work_break')

    attendance_realtime_id = fields.Many2one('sea.hr.attendance.realtime', string="Attendance realtime")

    '''Tính theo thực tế'''
    symbol = fields.Many2one('sea.hr.timesheet.symbol', string='Ký hiệu', default=1)
    # so_cong = fields.Float('Số công thực tế', default=0)

    check_in = fields.Datetime(track_visibility='onchange', string="Datetime check in")
    check_in_late = fields.Char(string="Check In Late")

    check_in_noon = fields.Datetime(track_visibility='onchange', string="Datetime noon check in")
    check_in_noon_late = fields.Char(string="Check In noon Late")

    check_out_noon = fields.Datetime(track_visibility='onchange', string="Datetime noon check out")
    check_out_noon_soon = fields.Char(string="Check Out noon Soon")

    check_out = fields.Datetime(track_visibility='onchange', string="Datetime check out")
    check_out_soon = fields.Char(string="Check Out Soon")

    check_late_soon = fields.Boolean('Check', default=False)

    location_check_id = fields.Many2one('sea.office', 'Location Check')

    note = fields.Text(string="Note")
    explanation_approved = fields.Boolean(string="Explanation Approved", default=True)
    month = fields.Integer(string='Tháng', related='attendance_realtime_id.month', store=True)
    year = fields.Integer(string="Năm", related='attendance_realtime_id.year', store=True)
    day = fields.Integer(string="Ngày", related='attendance_realtime_id.day', store=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_multi_id.department_id',
                                    store=True)
    job_id = fields.Many2one('hr.job', string='Job Position', related='employee_multi_id.job_id')

    @api.constrains('check_out', 'check_in', 'check_in_noon', 'check_out_noon')
    def overtime_(self):
        for rec in self:
            overtime = 0.0
            if rec.shift:
                if rec.check_in:
                    time_employee_temp = datetime.datetime(year=rec.check_in.year,
                                                           month=rec.check_in.month,
                                                           day=rec.check_in.day,
                                                           hour=rec.check_in.hour,
                                                           minute=rec.check_in.minute,
                                                           second=rec.check_in.second) \
                                         + datetime.timedelta(hours=7)
                    time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                       seconds=time_employee_temp.second)
                    if time_employee and datetime.timedelta(hours=rec.shift.sudo().hour_start) and datetime.timedelta(
                            hours=rec.shift.sudo().hour_start) > time_employee:
                        overtime += (datetime.timedelta(
                            hours=rec.shift.sudo().hour_start) - time_employee).total_seconds() / 3600

                if rec.check_out:
                    time_employee_temp = datetime.datetime(year=rec.check_out.year,
                                                           month=rec.check_out.month,
                                                           day=rec.check_out.day,
                                                           hour=rec.check_out.hour,
                                                           minute=rec.check_out.minute,
                                                           second=rec.check_out.second) \
                                         + datetime.timedelta(hours=7)
                    time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                       seconds=time_employee_temp.second)
                    if time_employee and datetime.timedelta(hours=rec.shift.sudo().hour_end) and datetime.timedelta(
                            hours=rec.shift.sudo().hour_end) < time_employee:
                        overtime += (time_employee - datetime.timedelta(
                            hours=rec.shift.sudo().hour_end)).total_seconds() / 3600

                if rec.check_in_noon:
                    time_employee_temp = datetime.datetime(year=rec.check_in_noon.year,
                                                           month=rec.check_in_noon.month,
                                                           day=rec.check_in_noon.day,
                                                           hour=rec.check_in_noon.hour,
                                                           minute=rec.check_in_noon.minute,
                                                           second=rec.check_in_noon.second) \
                                         + datetime.timedelta(hours=7)
                    time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                       seconds=time_employee_temp.second)
                    if time_employee and datetime.timedelta(
                            hours=rec.shift.sudo().hour_start_noon) and datetime.timedelta(
                        hours=rec.shift.sudo().hour_start_noon) > time_employee:
                        overtime += (datetime.timedelta(
                            hours=rec.shift.sudo().hour_start_noon) - time_employee).total_seconds() / 3600

                if rec.check_out_noon:
                    time_employee_temp = datetime.datetime(year=rec.check_out_noon.year,
                                                           month=rec.check_out_noon.month,
                                                           day=rec.check_out_noon.day,
                                                           hour=rec.check_out_noon.hour,
                                                           minute=rec.check_out_noon.minute,
                                                           second=rec.check_out_noon.second) \
                                         + datetime.timedelta(hours=7)
                    time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                       seconds=time_employee_temp.second)
                    if time_employee and datetime.timedelta(
                            hours=rec.shift.sudo().hour_end_noon) and datetime.timedelta(
                        hours=rec.shift.sudo().hour_end_noon) < time_employee:
                        overtime += (time_employee - datetime.timedelta(
                            hours=rec.shift.sudo().hour_end_noon)).total_seconds() / 3600
            else:
                if rec.check_in and rec.check_out:
                    result_datetime = rec.check_out - rec.check_in
                    overtime += result_datetime.total_seconds() / 3600
            rec.overtime = overtime

    overtime = fields.Float(string="Overtime", default=-1)
    overtime_sign = fields.Float(string="Overtime Sign", default=-1)
    overtime_sign_offline = fields.Float(string="Overtime Sign Offline", default=-1)
    overtime_hr = fields.Float(string="Overtime HR", default=-1)
    check_overtime = fields.Boolean(string="Check Overtime", compute='check_overtime_compute')

    def check_overtime_compute(self):
        for rec in self:
            rec.check_overtime = False
            if rec.overtime:
                if rec.overtime > 0:
                    rec.check_overtime = True
            if rec.overtime_hr:
                if rec.overtime_hr > 0:
                    rec.check_overtime = True
            if rec.overtime_sign:
                if rec.overtime_sign > 0:
                    rec.check_overtime = True
            if rec.overtime_sign_offline:
                if rec.overtime_sign_offline > 0:
                    rec.check_overtime = True

    @api.constrains('overtime_hr', 'overtime', 'overtime_sign', 'overtime_sign_offline')
    def constrains_overtime_hr(self):
        for rec in self:
            overtime = 0
            if rec.attendance_realtime_id:
                if rec.attendance_realtime_id.sudo().shift_details:
                    for i in rec.attendance_realtime_id.sudo().shift_details:
                        m = 0
                        check = True
                        if i.overtime_hr:
                            if i.overtime_hr > 0:
                                m = i.overtime_hr
                                check = False
                        if check:
                            check1 = False
                            if i.overtime_sign:
                                if i.overtime_sign > 0:
                                    check1 = True
                                    if m > i.overtime_sign:
                                        m = i.overtime_sign
                            if i.overtime_sign_offline:
                                if i.overtime_sign_offline > 0:
                                    check1 = True
                                    if m > i.overtime_sign_offline:
                                        m = i.overtime_sign_offline
                            if check1 and i.overtime:
                                if m > i.overtime > 0:
                                    m = i.overtime
                        overtime += m
            rec.attendance_realtime_id.sudo().write({'overtime': overtime})

    @api.constrains('symbol')
    def constraint_symbol(self):
        for rec in self:
            if not rec.attendance_realtime_id.sudo().symbol_sign:
                work_number = 0
                check_ot = False
                if rec.symbol:
                    if rec.shift:
                        check_ot = False
                        work_number += float(rec.symbol.sudo().work_number)
                    else:
                        check_ot = True
                if rec.attendance_realtime_id:
                    attendances = self.env[
                        'sea.hr.attendance.details'].sudo().search(
                        [('attendance_realtime_id', '=', rec.attendance_realtime_id.id), ('id', '!=', rec.id)])
                    if attendances:
                        check_ot = True
                        for attendance in attendances:
                            if attendance.symbol and rec.shift:
                                check_ot = False
                                work_number += float(attendance.symbol.sudo().work_number)

                if check_ot:
                    domain = [('symbol', '=', 'OT'), ('default_attendance', '=', True)]
                else:
                    domain = [('work_number', '=', work_number), ('default_attendance', '=', True)]
                syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                    domain, limit=1)
                if syy:
                    symbol = syy.id
                    rec.attendance_realtime_id.sudo().write({'symbol': symbol})

    @api.constrains('check_in')
    def constraint_check_in(self):
        for rec in self:
            if rec.check_in and rec.shift:
                time_late_or_soon = datetime.timedelta(hours=rec.shift.sudo().hour_start)

                time_employee_temp = datetime.datetime(year=rec.check_in.year,
                                                       month=rec.check_in.month,
                                                       day=rec.check_in.day,
                                                       hour=rec.check_in.hour,
                                                       minute=rec.check_in.minute,
                                                       second=rec.check_in.second) \
                                     + datetime.timedelta(hours=7)
                time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                   seconds=time_employee_temp.second)
                if time_employee and time_late_or_soon and time_late_or_soon < time_employee:
                    check_in_l_s = time_employee - time_late_or_soon
                    check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                    check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                    rec.check_in_late = check_in_late_or_soon_hour
                else:
                    rec.check_in_late = None
            else:
                rec.check_in_late = None

    @api.constrains('check_in_noon')
    def constraint_check_in_noon(self):
        for rec in self:
            if rec.check_in_noon and rec.shift:
                time_late_or_soon = datetime.timedelta(hours=rec.shift.sudo().hour_start_noon)

                time_employee_temp = datetime.datetime(year=rec.check_in_noon.year,
                                                       month=rec.check_in_noon.month,
                                                       day=rec.check_in_noon.day,
                                                       hour=rec.check_in_noon.hour,
                                                       minute=rec.check_in_noon.minute,
                                                       second=rec.check_in_noon.second) \
                                     + datetime.timedelta(hours=7)
                time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                   seconds=time_employee_temp.second)
                if time_employee and time_late_or_soon and time_late_or_soon < time_employee:
                    check_in_l_s = time_employee - time_late_or_soon
                    check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                    check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                    rec.check_in_noon_late = check_in_late_or_soon_hour
                else:
                    rec.check_in_noon_late = None
            else:
                rec.check_in_noon_late = None

    @api.constrains('check_out')
    def constraint_check_out(self):
        for rec in self:
            if rec.check_out and rec.shift:
                time_late_or_soon = datetime.timedelta(hours=rec.shift.sudo().hour_end)

                time_employee_temp = datetime.datetime(year=rec.check_out.year,
                                                       month=rec.check_out.month,
                                                       day=rec.check_out.day,
                                                       hour=rec.check_out.hour,
                                                       minute=rec.check_out.minute,
                                                       second=rec.check_out.second) \
                                     + datetime.timedelta(hours=7)
                time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                   seconds=time_employee_temp.second)
                if time_employee and time_late_or_soon and time_late_or_soon > time_employee:
                    check_in_l_s = time_late_or_soon - time_employee
                    check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                    check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                    rec.check_out_soon = check_in_late_or_soon_hour
                else:
                    rec.check_out_soon = None
            else:
                rec.check_out_soon = None

    @api.constrains('check_out_noon')
    def constraint_check_out_noon(self):
        for rec in self:
            if rec.check_out_noon and rec.shift:
                time_late_or_soon = datetime.timedelta(hours=rec.shift.sudo().hour_end_noon)

                time_employee_temp = datetime.datetime(year=rec.check_out_noon.year,
                                                       month=rec.check_out_noon.month,
                                                       day=rec.check_out_noon.day,
                                                       hour=rec.check_out_noon.hour,
                                                       minute=rec.check_out_noon.minute,
                                                       second=rec.check_out_noon.second) \
                                     + datetime.timedelta(hours=7)
                time_employee = datetime.timedelta(hours=time_employee_temp.hour, minutes=time_employee_temp.minute,
                                                   seconds=time_employee_temp.second)
                if time_employee and time_late_or_soon and time_late_or_soon > time_employee:
                    check_in_l_s = time_late_or_soon - time_employee
                    check_in_l_s = datetime.datetime.strptime(str(check_in_l_s), "%H:%M:%S")
                    check_in_late_or_soon_hour = check_in_l_s.strftime("%H:%M:%S")
                    rec.check_out_noon_soon = check_in_late_or_soon_hour
                else:
                    rec.check_out_noon_soon = None
            else:
                rec.check_out_noon_soon = None

    @api.constrains('check_out_soon', 'check_in_late', 'check_in_noon_late', 'check_out_noon_soon')
    def update_check_late_soon(self):
        for rec in self:
            check_not_attendance = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                [('employee_multi_id', '=', rec.employee_multi_id.id),
                 ('attendance_config_ids', '=', rec.sudo().shift.id)], limit=1)
            check = True
            if check_not_attendance:
                if check_not_attendance.not_attendance:
                    check = False
            rec.check_late_soon = False
            if rec.year <= fields.datetime.now().year and check:
                if rec.month < fields.datetime.now().month \
                        or rec.day <= fields.datetime.now().day \
                        and rec.month == fields.datetime.now().month:
                    if rec.shift:
                        if not rec.check_in \
                                or not rec.check_out \
                                or not rec.check_in_noon and rec.work_break \
                                or not rec.check_out_noon and rec.work_break:
                            rec.check_late_soon = True
                        else:
                            if rec.check_in_late:
                                hours, minutes, seconds = map(int, rec.check_in_late.split(':'))
                                if hours * 3600 + minutes * 60 + seconds > 0:
                                    rec.check_late_soon = True
                            if rec.check_out_noon_soon:
                                hours2, minutes2, seconds2 = map(int, rec.check_out_noon_soon.split(':'))
                                if hours2 * 3600 + minutes2 * 60 + seconds2 > 0:
                                    rec.check_late_soon = True
                            if rec.check_in_noon_late:
                                hours1, minutes1, seconds1 = map(int, rec.check_in_noon_late.split(':'))
                                if hours1 * 3600 + minutes1 * 60 + seconds1 > 0:
                                    rec.check_late_soon = True
                            if rec.check_out_soon:
                                hours3, minutes3, seconds3 = map(int, rec.check_out_soon.split(':'))
                                if hours3 * 3600 + minutes3 * 60 + seconds3 > 0:
                                    rec.check_late_soon = True

    @api.multi
    def write(self, vals):
        for rec in self:
            '''symbol'''
            sy = 0
            if rec.shift:
                if rec.shift.sudo().work_break:
                    if vals.get('check_in') or vals.get('check_out_noon'):
                        if rec.check_out or rec.check_out_noon:
                            sy = 1
                        else:
                            sy = 0.5
                    elif vals.get('check_out') or vals.get('check_in_noon'):
                        if rec.check_in or rec.check_in_noon:
                            sy = 1
                        else:
                            sy = 0.5
                else:
                    if vals.get('check_in') or vals.get('check_out'):
                        sy = 1
                if sy > 0:
                    work_number = sy * rec.shift.sudo().work_day
                    syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                        [('work_number', '=', work_number), ('default_attendance', '=', True)], limit=1)
                    vals['symbol'] = None if not syy else syy.id
                ''''''
                ''''''
                if rec.shift.sudo().first_in_late_out or not rec.shift.sudo().work_break:
                    if 'check_in' in vals and rec.check_in and 'check_out' not in vals:
                        if not rec.check_out or rec.check_out and rec.check_in > rec.check_out:

                            if rec.shift.sudo().first_in_late_out:
                                vals['check_out'] = rec.check_in
                            else:
                                if rec.shift.sudo().hour_end > 0 and datetime.timedelta(
                                        hours=rec.shift.sudo().hour_end_start) <= datetime.timedelta(
                                    hours=rec.check_in.hour,
                                    minutes=rec.check_in.minute,
                                    seconds=rec.check_in.second) + datetime.timedelta(
                                    hours=7) < datetime.timedelta(
                                    hours=rec.shift.sudo()
                                            .hour_end_end):
                                    if not rec.shift.sudo().login_logout:
                                        vals['check_out'] = rec.check_in

                else:
                    '''chưa tính'''
                    continue
        return super(AttendanceDetails, self).write(vals)

    @api.model
    def create(self, vals):
        sy = 0
        if 'shift' in vals:
            shift = self.env['sea.hr.attendance.shift'].sudo().search([('id', '=', vals.get('shift'))])
            if shift:
                if shift.sudo().work_break:
                    if vals.get('check_in') or vals.get('check_out_noon') \
                            and vals.get('check_out') or vals.get('check_in_noon'):
                        sy = 0.5

                else:
                    if vals.get('check_in') or vals.get('check_out'):
                        sy = 1

                if sy > 0:
                    work_number = sy * shift.sudo().work_day
                    syy = self.env['sea.hr.timesheet.symbol'].sudo().search(
                        [('work_number', '=', work_number), ('default_attendance', '=', True)], limit=1)
                    vals['symbol'] = None if not syy else syy.id
        return super(AttendanceDetails, self).create(vals)

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            # print(type(rec.employee_multi_id.sudo().name.name))
            result.append((rec.id, '%s - %s/%s/%s' %
                           (rec.employee_multi_id.sudo().name.name, rec.day, rec.month, rec.year)))
        return result


class HRAttendanceRealtime(models.Model):
    _name = 'sea.hr.attendance.realtime'
    _description = "Attendance Employee"
    _sql_constraints = [('model_day_month_year_employee_multi_uniq', 'unique(employee_multi_id, day, month, year)',
                         'Attendance with this month of company is  already exist!!')]

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên", required=True,
                                        domain=lambda self: [('employee_current_status', '=', 'working'),
                                                             ('company_id', '=', self.env.user.company_id.id)])
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)
    company_id = fields.Many2one('res.company', related='employee_multi_id.company_id', string="Công Ty",
                                 store=True)
    year = fields.Integer(string="Năm", required=True, default=lambda self: fields.datetime.now().year)
    month = fields.Integer(string="Tháng", required=True, default=lambda self: fields.datetime.now().month)

    @api.constrains('month')
    def check_month(self):
        for record in self:
            if record.month < 0 or record.month > 12:
                raise ValidationError("Tháng từ 1-12")

    day = fields.Integer(string="Ngày", required=True, default=lambda self: fields.datetime.now().day)

    @api.constrains('day')
    def check_day(self):
        for record in self:
            last_day_of_month = int(calendar.monthrange(int(record.year), int(record.month))[1])
            if record.day < 0 or record.day > last_day_of_month:
                raise ValidationError(
                    "Số ngày tối đa của " + record.month + "/" + record.year + " là: " + last_day_of_month)

    @api.onchange('employee_multi_id')
    def onchange_employee_multi_id(self):
        for rec in self:
            rec.domain_compute()

    '''domain theo employee hoặc company'''

    def domain_compute(self):
        '''employee'''
        # shifts = self.env['sea.hr.attendance.shift.employee'].sudo().search(
        #     [('employee_multi_id', '=', self.employee_multi_id.id)]).attendance_config_ids
        # self.domain_day = shifts.ids
        '''company'''
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
        shifts = self.env['sea.hr.attendance.shift'].sudo().search(
            [('company_id', '=', self.company_id.id)])
        self.domain_day = shifts.ids

    domain_day = fields.Many2many('sea.hr.attendance.shift', string='Domain', compute='domain_compute')

    def compute_datetime(self):
        for rec in self:
            dates = int(date.weekday(date(int(rec.year), int(rec.month), rec.day)))
            thu = ""
            if dates == 0:
                thu = "Thứ hai"
            elif dates == 1:
                thu = "Thứ ba"
            elif dates == 2:
                thu = "Thứ tư"
            elif dates == 3:
                thu = "Thứ năm"
            elif dates == 4:
                thu = "Thứ sáu"
            elif dates == 5:
                thu = "Thứ bảy"
            elif dates == 6:
                thu = "Chủ nhật"

            rec.datetime_compute = str(thu) + ", " + str(rec.day) + "/" + str(rec.month) + "/" + str(rec.year)

        # datetime.datetime.strptime(str(rec.day) + "/" + str(rec.month) + "/" + str(rec.year),
        #                            '%d/%m/%Y').date()

    datetime_compute = fields.Char('Ngày', compute='compute_datetime')

    shift = fields.Many2many('sea.hr.attendance.shift', required=True, string="Ca làm việc",
                             domain="[('id', 'in', domain_day)]")

    def check_duplication_shift(self, list_day_id):
        '''Trùng thứ chấm công của nhau không được trùng'''
        list_attendance = [attendance for attendance in list_day_id]
        while True:
            if len(list_attendance) == 0:
                break
            attendance_0 = list_attendance[0]
            list_attendance.pop(0)
            for i in range(len(list_attendance)):
                if attendance_0.thu_2 and list_attendance[i].thu_2 \
                        or attendance_0.thu_3 and list_attendance[i].thu_3 \
                        or attendance_0.thu_4 and list_attendance[i].thu_4 \
                        or attendance_0.thu_5 and list_attendance[i].thu_5 \
                        or attendance_0.thu_6 and list_attendance[i].thu_6 \
                        or attendance_0.thu_7 and list_attendance[i].thu_7 \
                        or attendance_0.thu_8 and list_attendance[i].thu_8:
                    if attendance_0.first_in_late_out or list_attendance[i].first_in_late_out:
                        return list_attendance[i]
                    list_0 = attendance_0.duplicate_shifts(attendance_0)
                    list_s = list_attendance[i].duplicate_shifts(list_attendance[i])
                    error = set(list_0).intersection(set(list_s))
                    if error:
                        return list_attendance[i]
        return False

    @api.onchange('shift')
    def _onchange_shift(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.shift)
            if check:
                rec.shift = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    shift_details = fields.One2many('sea.hr.attendance.details', 'attendance_realtime_id',
                                    string="Chi tiết ca làm việc", readonly=1)

    '''Tính tổng theo thực tế'''
    symbol = fields.Many2one('sea.hr.timesheet.symbol', string='Ký hiệu', default=1)
    symbol_sign = fields.Many2one('sea.hr.timesheet.symbol', string='Ký hiệu từ đơn xin phép nghỉ')
    so_cong = fields.Float('Số công thực tế', related='symbol.work_number')

    overtime = fields.Float(string="Thời lượng tăng ca chính thức")

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            symbol = rec.symbol.sudo().symbol
            overtime = 0
            # if rec.shift_details:
            #     for i in rec.shift_details:
            #         if i.overtime_hr:
            #             overtime += i.overtime_hr
            if rec.overtime:
                overtime = rec.overtime
            time = overtime % 1
            if int(overtime) > 0 or time > 0:
                o = int(overtime)
                if time > 0:
                    time = time * 60
                    if 15 <= time < 45:
                        o += 0.5
                    elif time >= 45:
                        o += 1
                if o > 0:
                    symbol += str(o)

            result.append((rec.id, symbol))
        return result

    @api.model
    def create(self, vals):
        # print("val: ", vals)
        result = super(HRAttendanceRealtime, self).create(vals)
        if 'day' in vals and 'month' in vals and 'year' in vals and 'employee_multi_id' in vals:
            attendance_month = self.env['sea.hr.attendance.month'].sudo().search(
                [('employee_multi_id', '=', vals.get('employee_multi_id'),), ('month', '=', vals.get('month')),
                 ('year', '=', vals.get('year'))])
            if attendance_month:
                attendance_month.sudo().write({'day_' + str(vals.get('day')): result.id})
        return result

    mark_as_todo = fields.Boolean(string='Mark as todo', default=False)

    # def mark_as_todo_compute(self):
    #     for rec in self:
    #         attendance_id = self.env['sea.hr.attendance'].sudo().search(
    #             [('company_id', '=',
    #               rec.sudo().company_id.id),
    #              ('month', '=', rec.month),
    #              ('year', '=', rec.year)], limit=1)
    #         rec.mark_as_todo = attendance_id.mark_as_todo if attendance_id else False

    @api.multi
    def action_confirm(self):
        self.mark_as_todo = True
        return True

    @api.multi
    def action_un_confirm(self):
        for rec in self:
            attendance_id = self.env['sea.hr.attendance'].sudo().search(
                [('company_id', '=',
                  rec.sudo().company_id.id),
                 ('month', '=', rec.month),
                 ('year', '=', rec.year)], limit=1)
            if attendance_id:
                if attendance_id.mark_as_todo:
                    raise ValidationError(
                        "Bảng chấm công tháng " + str(rec.month) + "/" + str(rec.year) + " đã khóa!!!")
            self.mark_as_todo = False
        return True

    @api.multi
    def write(self, value):
        for rec in self:
            if rec.mark_as_todo and not value.get('mark_as_todo') or value.get('mark_as_todo'):
                '''khi đã mark_as_todo=true thì chỉ ghi lại chi tiết làm việc và không thay đổi thông tin nào các cả'''
                if 'overtime' in value:
                    value['overtime'] = rec.overtime
                if 'symbol' in value:
                    value['symbol'] = rec.symbol.id
                if 'shift' in value:
                    value['shift'] = rec.shift.id
                if 'employee_multi_id' in value:
                    value['employee_multi_id'] = rec.employee_multi_id.id
                if 'year' in value:
                    value['year'] = rec.year
                if 'month' in value:
                    value['month'] = rec.month
                if 'day' in value:
                    value['day'] = rec.day
        return super(HRAttendanceRealtime, self).write(value)
