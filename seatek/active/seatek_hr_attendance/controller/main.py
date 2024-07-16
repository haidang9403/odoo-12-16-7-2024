import datetime

from odoo import http, fields
from odoo.http import request


class Attendance(http.Controller):

    @http.route('/load/calendar', type="json", website=True, auth='user')
    def load_calendar(self, id):
        # print('khánh nè', id)
        calendar_create = request.env['sea.hr.calendar.employee'].sudo().search(
            [('id', '=', id)])
        list_not_delete = []

        if calendar_create:
            '''xóa LLV cũ của những employee này để cập nhật lại LLV mới'''
            calendar_delete = request.env['sea.hr.calendar'].sudo().search(
                [('employee_multi_id', '=', calendar_create.employee_multi_id.id)])
            calendar_delete.sudo().unlink()
            ''''''
            for calendar in calendar_create:
                for i in range(calendar.last_day_of_month):
                    day = i + 1
                    shifts = calendar.get_day(day)
                    for shift in shifts:
                        date_str = str(calendar.year) + '-' + str(calendar.month) + '-' + str(
                            day) + ' ' + '00:00:00'
                        date_format = "%Y-%m-%d %H:%M:%S"
                        datetime_calendar = datetime.datetime.strptime(date_str, date_format)
                        calendar_exit = request.env['sea.hr.calendar'].sudo().search(
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
                            id_e = request.env['sea.hr.calendar'].sudo().create(value)
                            list_not_delete.append(id_e.id)
                        else:
                            list_not_delete.append(calendar_exit.id)
        get_date_current = fields.Datetime.now().date()
        calendar_all = request.env['sea.hr.calendar'].sudo().search(
            [('id', 'not in', list_not_delete), ('create_date', '<', get_date_current)])
        # print('len', len(calendar_all))
        if calendar_all:
            calendar_all.sudo().unlink()
            # print('Done')

        return True

        # ajax.jsonRpc('/khanh/tran', 'call', {
        # }).then(function (data) {
        #         console.log(data);
        #     });
        # var self = this;
        # console.log(this.record.data.id)
        # rpc.query({
        #         route: '/khanh/tran',
        #         params: {
        #             id: this.record.data.id
        #         }
        #     }).then(function (data) {
        #        console.log('thís',self)
        #         console.log(data[1])
        #         console.log(data['last_day_of_month'])
        #         var last_day_of_month = data['last_day_of_month']
        #         for (var i = 1; i <= last_day_of_month; i++) {
        #             console.log(i+' '+data[i])
        #             }
        #     });

    @http.route('/load/check_add_line_calendar', type="json", website=True, auth='user')
    def check_add_line_calendar(self):
        # print('khánh', request)
        if request.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_administrator') or request.env.user.has_group(
            'seatek_hr_attendance.hr_attendance_manager'):
            employee = request.env['hr.employee.multi.company'].sudo().search(
                [('employee_current_status', '=', 'working'),
                 ('company_id', '=', request.env.user.company_id.id)])
            if employee:
                return True
        else:
            if request.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                employee_multi_id = request.env['hr.employee.multi.company'].sudo().search(
                    [('user_id', '=', request.env.user.id), ('company_id', '=', request.env.user.company_id.id)],
                    limit=1)
                if employee_multi_id:
                    employee = request.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                    if employee:
                        department_list = request.env['hr.department'].sudo().search(
                            [('manager_ids', '=', employee.id)])
                        if department_list:
                            return True
        return False

    @http.route('/load/check_group', type="json", website=True, auth='user')
    def check_group(self):
        if request.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator'):
            return 3
        elif request.env.user.has_group('seatek_hr_attendance.hr_attendance_manager'):
            return 2
        elif request.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
            return 1
        return 0

    # @http.route('/load/search', type="json", website=True, auth='user')
    # def load_calendar(self, id_, sc):
    #     rec = request.env['sea.hr.attendance'].sudo().search([('id', '=', id_)])
    #     print('khánh nè', sc, id_, rec)
    #     if rec:
    #         rec.write({'employee_id': sc})
    #     #     # rec.search_s_identification(sc)
    #     #     # if request.env.user.has_group(
    #     #     #         'seatek_hr_attendance.hr_attendance_administrator') or request.env.user.has_group(
    #     #     #         'seatek_hr_attendance.hr_attendance_manager'):
    #     #     #     if sc != '':
    #     #     #         hr_employee = False
    #     #     #         hr_employee = request.env['hr.employee'].sudo().search(
    #     #     #             ['|', ('s_identification_id', 'ilike', sc),
    #     #     #              ('name', 'ilike', sc), ('company_id', '=', rec.company_id.id)])
    #     #     #
    #     #     #         if hr_employee:
    #     #     #             rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #     #     #                 lambda record: record.s_identification_id in [i.s_identification_id for i in
    #     #     #                                                               hr_employee])
    #     #     #     else:
    #     #     #         rec.attendance_of_month_compute = rec.attendance_of_month
    #     #     # else:
    #     #     #     if request.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
    #     #     #         employee_multi_id = request.env['hr.employee.multi.company'].sudo().search(
    #     #     #             [('user_id', '=', request.env.user.id), ('company_id', '=', request.env.user.company_id.id)],
    #     #     #             limit=1)
    #     #     #         if employee_multi_id:
    #     #     #             employee = request.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
    #     #     #             if employee:
    #     #     #                 department_list = request.env['hr.department'].sudo().search(
    #     #     #                     [('manager_ids', '=', employee.id)])
    #     #     #             list_employee = [employee_multi_id.id]
    #     #     #             if department_list:
    #     #     #                 employee_department = request.env['hr.employee.multi.company'].sudo().search(
    #     #     #                     [('department_id', 'in', department_list.ids)])
    #     #     #                 if employee_department:
    #     #     #                     for i in employee_department:
    #     #     #                         list_employee.append(i.id)
    #     #     #             rec.attendance_of_month_compute = rec.attendance_of_month.filtered(
    #     #     #                 lambda record: record.employee_multi_id.id in list_employee)
    #     # print("value: ", rec.employee_id)
    #     return True

    # @http.route('/load/list_department', type="json", website=True, auth='user')
    # def get_department(self):
    #     departments = request.env['hr.department'].sudo().search(
    #         [('company_id', '=', request.env.user.company_id.id)])
    #     list_department = []
    #     for department in departments:
    #         list_department.append({'name': department.name,
    #                                 'id': department.id})
    #     return list_department
