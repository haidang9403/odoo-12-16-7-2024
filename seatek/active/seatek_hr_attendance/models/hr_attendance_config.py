from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HRAttendanceConfig(models.Model):
    _name = 'sea.hr.attendance.shift'
    _description = "Attendance Shifts for Company"

    company_id = fields.Many2one('res.company', string='Công Ty',
                                 default=lambda self: self.env.user.company_id.id)

    name = fields.Char(string="Ca làm việc", required=True)
    abbreviations = fields.Char(string="Tên viết tắt", required=True)
    number_time = fields.Float(string='Số giờ làm việc')
    work_day = fields.Float('Pay rate', required=True, default=1.0)

    first_in_late_out = fields.Boolean(string="First in - Late out", default=False)
    hour_start = fields.Float(string="Giờ bắt đầu", required=True)
    hour_start_start = fields.Float(string="GBĐ từ", required=True)
    hour_start_end = fields.Float(string="GBĐ đến", required=True)

    hour_end = fields.Float(string="Giờ kết thúc", required=True)
    hour_end_start = fields.Float(string="GKT từ", required=True)
    hour_end_end = fields.Float(string="GKT đến", required=True)

    hour_start_noon = fields.Float(string="Giờ bắt đầu nghỉ giữa ca", required=True)
    hour_start_noon_start = fields.Float(string="GBĐ nghỉ giữa ca từ", required=True)
    hour_start_noon_end = fields.Float(string="GBĐ nghỉ giữa ca đến", required=True)

    hour_end_noon = fields.Float(string="Giờ kết thúc nghỉ giữa ca", required=True)
    hour_end_noon_start = fields.Float(string="GKT nghỉ giữa ca từ", required=True)
    hour_end_noon_end = fields.Float(string="GKT nghỉ giữa ca đến", required=True)

    thu_2 = fields.Boolean('Thứ 2', default=True)
    thu_3 = fields.Boolean('Thứ 3', default=True)
    thu_4 = fields.Boolean('Thứ 4', default=True)
    thu_5 = fields.Boolean('Thứ 5', default=True)
    thu_6 = fields.Boolean('Thứ 6', default=True)
    thu_7 = fields.Boolean('Thứ 7', default=False)
    thu_8 = fields.Boolean('Chủ nhật', default=False)

    work_break = fields.Boolean(string="Nghỉ giữa ca", default=False)

    @api.constrains('first_in_late_out')
    def check_first_in_late_out(self):
        for record in self:
            if record.first_in_late_out:
                record.hour_start_noon = 0
                record.hour_start_noon_start = 0
                record.hour_start_noon_end = 0

                record.hour_end_noon = 0
                record.hour_end_noon_start = 0
                record.hour_end_noon_end = 0

                record.hour_start_start = 0
                record.hour_start_end = 0

                record.hour_end_start = 0
                record.hour_end_end = 0

            self.check_hour_start()
            self.check_hour_start_noon()
            self.check_hour_end_noon()
            self.check_hour_end()

    @api.constrains('work_break')
    def check_work_break(self):
        for record in self:
            if not record.work_break:
                record.hour_start_noon = 0
                record.hour_start_noon_start = 0
                record.hour_start_noon_end = 0

                record.hour_end_noon = 0
                record.hour_end_noon_start = 0
                record.hour_end_noon_end = 0

            self.check_hour_start()
            self.check_hour_start_noon()
            self.check_hour_end_noon()
            self.check_hour_end()

    '''check xong'''

    @api.constrains('hour_start')
    def check_hour_start(self):
        for record in self:
            if record.hour_start < 0 or record.hour_start >= 24:
                raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
            else:
                self.check_hour_start_start()
                self.check_hour_start_end()

    @api.constrains('hour_start_start')
    def check_hour_start_start(self):
        for record in self:
            if not record.first_in_late_out:
                if record.hour_start_start < 0 or record.hour_start_start >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_start < record.hour_start_start:
                    raise ValidationError("GBĐ từ không được lớn hơn GBĐ")

    @api.constrains('hour_start_end')
    def check_hour_start_end(self):
        for record in self:
            if not record.first_in_late_out:
                if record.hour_start_end < 0 or record.hour_start_end >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_start > record.hour_start_end:
                    raise ValidationError("GBĐ đến không được nhỏ hơn GBĐ")

    @api.constrains('hour_end')
    def check_hour_end(self):
        for record in self:
            if record.hour_end < 0 or record.hour_end >= 24:
                raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
            else:
                self.check_hour_end_start()
                self.check_hour_end_end()

    @api.constrains('hour_end_start')
    def check_hour_end_start(self):
        for record in self:
            if not record.first_in_late_out:
                if record.hour_end_start < 0 or record.hour_end_start >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_end < record.hour_end_start:
                    raise ValidationError("GKT từ không được lớn hơn GKT")
                elif record.hour_end_noon_end > record.hour_end_start \
                        and record.work_break:
                    raise ValidationError("GKT từ không được nhỏ hơn GKT nghỉ trưa đến")

    @api.constrains('hour_end_end')
    def check_hour_end_end(self):
        for record in self:
            if not record.first_in_late_out:
                if record.hour_end_end < 0 or record.hour_end_end >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_end > record.hour_end_end:
                    raise ValidationError("GKT đến không được nhỏ hơn GKT")

    @api.constrains('hour_start_noon')
    def check_hour_start_noon(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_start_noon < 0 or record.hour_start_noon >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                else:
                    self.check_hour_start_noon_start()
                    self.check_hour_start_noon_end()

    @api.constrains('hour_start_noon_start')
    def check_hour_start_noon_start(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_start_noon_start < 0 or record.hour_start_noon_start >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_start_noon < record.hour_start_noon_start:
                    raise ValidationError("GBĐ nghỉ trưa từ không được lớn hơn GBĐ nghỉ trưa")
                elif record.hour_start_end > record.hour_start_noon_start:
                    raise ValidationError("GBĐ nghỉ trưa từ không được nhỏ hơn GBĐ đến")

    @api.constrains('hour_start_noon_end')
    def check_hour_start_noon_end(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_start_noon_end < 0 or record.hour_start_noon_end >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_start_noon > record.hour_start_noon_end:
                    raise ValidationError("GBĐ nghỉ trưa đến không được nhỏ hơn GBĐ nghỉ trưa")

    @api.constrains('hour_end_noon')
    def check_hour_end_noon(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_end_noon < 0 or record.hour_end_noon >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                else:
                    self.check_hour_end_noon_start()
                    self.check_hour_end_noon_end()

    @api.constrains('hour_end_noon_start')
    def check_hour_end_noon_start(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_end_noon_start < 0 or record.hour_end_noon_start >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_end_noon < record.hour_end_noon_start:
                    raise ValidationError("GKT trưa từ không được lớn hơn GKT nghỉ trưa")
                elif record.hour_start_noon_end > record.hour_end_noon_start:
                    raise ValidationError("GKT nghỉ trưa từ không được nhỏ hơn GBĐ nghỉ trưa đến")

    @api.constrains('hour_end_noon_end')
    def check_hour_end_noon_end(self):
        for record in self:
            if record.work_break and not record.first_in_late_out:
                if record.hour_end_noon_end < 0 or record.hour_end_noon_end >= 24:
                    raise ValidationError("số giờ chỉ từ 00:00 - 23:59")
                elif record.hour_end_noon > record.hour_end_noon_end:
                    raise ValidationError("GKT nghỉ trưa đến không được nhỏ hơn GKT nghỉ trưa")

    ''''''

    type_of_shift = fields.Selection([
        ('split_shift', 'Ca gãy'),
        ('full_time_shift', 'Ca xuyên ngày')],
        # ('hanh_chinh', 'Giờ hành chính')],
        string='Type of shift', required=1)
    login_logout = fields.Boolean(string="Đăng nhập/Đăng xuất", default=False)
    for_full_time_shift = fields.Selection([
        ('check_in_day', 'Ngày check in'),
        ('check_out_day', 'Ngày check out')],
        string='Workday calculated for full time shift')

    @api.multi
    def duplicate_shifts(self, attendance):

        lists = [round(attendance.hour_start, 2)]  # lấy giờ BĐ kiểu float làm tròn lên 2 số
        end = attendance.hour_start
        if attendance.type_of_shift == 'full_time_shift':
            '''Ca suốt'''
            stop = False
            while True:
                end += 0.01666666666667  # tương đương 1 phút
                # ca xuyên đêm nên đến 24h sẽ tiếp tục tính qua ngày hôm sau
                if end >= 24.0:
                    end -= 24
                    stop = True
                if end > attendance.hour_end and stop:
                    break

                lists.append(round(end, 2))

        elif attendance.type_of_shift != 'full_time_shift':
            '''Ca gãy'''
            while True:
                end += 0.01666666666667  # tương đương 1 phút
                if end > attendance.hour_end:
                    break
                lists.append(round(end, 2))
        return lists

    department_id = fields.Many2one('hr.department', string='Department')

    '''default trên 2 ca không trùng giờ'''

    @api.constrains('default_shift')
    def check_default_shift(self):
        for rec in self:
            if rec.default_shift:
                if rec.department_id not in [None, False]:
                    shift_company = self.env['sea.hr.attendance.shift'].sudo().search(
                        [('company_id', '=', rec.company_id.id), ('department_id', '=', rec.department_id.id),
                         ('default_shift', '=', True), ('id', '!=', rec.id)])
                else:
                    shift_company = self.env['sea.hr.attendance.shift'].sudo().search(
                        [('company_id', '=', rec.company_id.id), ('department_id', 'in', [None, False]),
                         ('default_shift', '=', True), ('id', '!=', rec.id)])

                if shift_company:
                    if rec.first_in_late_out:
                        raise ValidationError("Lỗi cài đặt trùng ca, "
                                              "ca default đã có nhưng ca này lại là First in Late out")
                    for shift in shift_company:
                        if shift.first_in_late_out:
                            raise ValidationError("Lỗi cài đặt trùng ca, "
                                                  "đã có một ca default First in Late out")
                        else:
                            '''Trùng thứ chấm công của nhau không được trùng'''
                            if rec.thu_2 and shift.thu_2 \
                                    or rec.thu_3 and shift.thu_3 \
                                    or rec.thu_4 and shift.thu_4 \
                                    or rec.thu_5 and shift.thu_5 \
                                    or rec.thu_6 and shift.thu_6 \
                                    or rec.thu_7 and shift.thu_7 \
                                    or rec.thu_8 and shift.thu_8:
                                list_0 = rec.duplicate_shifts(rec)
                                list_s = shift.duplicate_shifts(shift)
                                error = set(list_0).intersection(set(list_s))
                                if error:
                                    raise ValidationError("Trùng giờ của các ca default ...")

    default_shift = fields.Boolean('Default shift', default=False)

    def add_shift_default(self):
        for rec in self:
            if rec.department_id:
                employee_multi = self.env['hr.employee.multi.company'].sudo().search(
                    [('department_id', '=', rec.department_id.id), ('company_id', '=', rec.company_id.id),
                     ('employee_current_status', '=', "working")])
            else:
                attendance_shift_not_department = self.env['sea.hr.attendance.shift'].sudo().search(
                    [('default_shift', '=', True), ('department_id', 'in', [None, False]),
                     ('company_id', '=', rec.company_id.id)])
                attendance_shift = self.env['sea.hr.attendance.shift'].sudo().search(
                    [('default_shift', '=', True), ('id', 'not in', attendance_shift_not_department.ids),
                     ('company_id', '=', rec.company_id.id)])

                employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('department_id', 'in', [i.department_id.id for i in attendance_shift])])

                employee_multi = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', rec.company_id.id), ('employee_current_status', '=', "working"),
                     ('id', 'not in', employee_multi_id.ids)])
            update = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                [('employee_multi_id', 'in', employee_multi.ids)])
            for employee in update:
                if rec.id not in employee.attendance_config_ids.ids:
                    '''tính trường hợp ca trùng giờ (không tính)'''
                    list_attendance = [attendance for attendance in employee.attendance_config_ids]
                    list_0 = rec.duplicate_shifts(rec)
                    error = False
                    for i in range(len(list_attendance)):
                        if rec.thu_2 and list_attendance[i].thu_2 \
                                or rec.thu_3 and list_attendance[i].thu_3 \
                                or rec.thu_4 and list_attendance[i].thu_4 \
                                or rec.thu_5 and list_attendance[i].thu_5 \
                                or rec.thu_6 and list_attendance[i].thu_6 \
                                or rec.thu_7 and list_attendance[i].thu_7 \
                                or rec.thu_8 and list_attendance[i].thu_8:
                            if rec.first_in_late_out or list_attendance[i].first_in_late_out:
                                break
                            else:
                                '''Trùng thứ chấm công của nhau không được trùng'''
                                list_s = list_attendance[i].duplicate_shifts(list_attendance[i])
                                error = set(list_0).intersection(set(list_s))
                                if error:
                                    break

                    if not error or rec.department_id:
                        # print('thêm ca', rec, 'cho', employee.employee_multi_id.sudo().name.name)
                        employee.write({'attendance_config_ids': [(4, rec.id)]})

                        '''check ghi đè'''
                        if rec.department_id:
                            # print('ghi đè', rec)
                            attendance_shift_not_department = self.env['sea.hr.attendance.shift'].sudo().search(
                                [('default_shift', '=', True), ('department_id', 'in', [None, False]),
                                 ('company_id', '=', rec.company_id.id)])
                            for i in attendance_shift_not_department:
                                if i.id in employee.attendance_config_ids.ids:
                                    employee.attendance_config_ids = [(3, i.id)]
                            # for e in employee.attendance_config_ids:
                            #     if not e.department_id:
                            #         employee.attendance_config_ids = [(3, rec.id)]

            create = self.env['hr.employee.multi.company'].sudo().search(
                [('company_id', '=', rec.company_id.id), ('employee_current_status', '=', "working"),
                 ('id', 'in', employee_multi.ids),
                 ('id', 'not in',
                  [i.employee_multi_id.id for i in
                   self.env['sea.hr.attendance.shift.employee'].sudo().search([])])])
            for employee in create:
                shift = [(6, 0, [rec.id])]
                if shift:
                    shifts_employee = self.env['sea.hr.attendance.shift.employee'].sudo().create({
                        'employee_multi_id': employee.id,
                        'attendance_config_ids': shift
                    })
                    # print('tạo mới', shifts_employee)

    def remove_shift_default(self):
        for rec in self:
            employee_multi = self.env['hr.employee.multi.company'].sudo().search(
                [('company_id', '=', rec.company_id.id), ('employee_current_status', '=', "working")])
            shift_employee = self.env['sea.hr.attendance.shift.employee'].sudo().search(
                [('employee_multi_id', 'in', employee_multi.ids)])
            for employee in shift_employee:
                if rec.id in employee.attendance_config_ids.ids:
                    employee.attendance_config_ids = [(3, rec.id)]
                    # print('xóa ca', employee.employee_multi_id.sudo().name.name)

                    if not employee.attendance_config_ids:
                        attendance_shift_not_department = self.env['sea.hr.attendance.shift'].sudo().search(
                            [('default_shift', '=', True), ('department_id', 'in', [None, False]),
                             ('company_id', '=', rec.company_id.id)])
                        # print('thêm ca default')
                        for i in attendance_shift_not_department:
                            i.add_shift_default()

    @api.multi
    def write(self, vals):
        rec = super(HRAttendanceConfig, self).write(vals)
        self.check_default_shift()
        if 'default_shift' in vals:
            if vals.get('default_shift'):
                self.add_shift_default()
            elif not vals.get('default_shift'):
                self.remove_shift_default()
        if 'department_id' in vals:
            self.remove_shift_default()
            self.add_shift_default()

        return rec

    @api.model
    def create(self, vals):
        rec = super(HRAttendanceConfig, self).create(vals)
        if rec.default_shift:
            rec.add_shift_default()
        return rec

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.name if rec.abbreviations in [None, False] else rec.abbreviations))
        return result


class AttendanceConfigEmployee(models.Model):
    _name = 'sea.hr.attendance.shift.employee'
    _description = "Attendance Shift for Employee"
    _sql_constraints = [('model_employee_multi_id_uniq', 'unique(employee_multi_id)',
                         "The Employee's shift already exists!!")]

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên", required=True)
    s_identification_id = fields.Char(string='SC Code', related='employee_multi_id.s_identification_id', store=True)
    company_id = fields.Many2one('res.company', related='employee_multi_id.company_id', string="Công Ty", store=True)
    department_id = fields.Many2one('hr.department', string='Department', related='employee_multi_id.department_id',
                                    store=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_multi_id.job_id', store=True)
    attendance_config_ids = fields.Many2many('sea.hr.attendance.shift', string="Shift", required=True)
    not_attendance = fields.Boolean('Not Attendance', default=False)

    @api.onchange('attendance_config_ids')
    def _onchange_attendance_config_ids(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc tính'''
        for rec in self:
            list_attendance = [attendance for attendance in rec.attendance_config_ids]
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
                    rec.attendance_config_ids = [(3, list_attendance[i].id)]
                    return {'warning': {
                        'title': 'Lỗi thêm ca làm việc',
                        'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                    }}

    @api.model
    def create(self, vals):
        rec = super(AttendanceConfigEmployee, self).create(vals)
        return rec

    @api.multi
    def write(self, vals):
        return super(AttendanceConfigEmployee, self).write(vals)


class WorkNumber(models.Model):
    _name = 'sea.hr.timesheet.symbol'
    _description = "Work number for employees per day"

    company_id = fields.Many2one('res.company', string="Công Ty")
    name = fields.Char('name', related='symbol')
    symbol = fields.Char('Symbol', required=True)
    work_number = fields.Float('Work number', required=True)
    note = fields.Char('Note')
    only_sign = fields.Boolean('Sign Only', default=False)
    default_attendance = fields.Boolean('Default Attendance', default=False)

    @api.constrains('default_attendance', 'work_number')
    def constrains_default_attendance(self):
        for record in self:
            if record.default_attendance:
                for i in self.env['sea.hr.timesheet.symbol'].sudo().search(
                        [('default_attendance', '=', True), ('id', '!=', record.id)]):
                    if i.work_number == record.work_number:
                        raise ValidationError("Work number trùng")
                        break

    @api.multi
    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, rec.symbol))
        return result
