import calendar
from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CalendarEmployee(models.Model):
    _name = 'sea.hr.calendar.employee'
    _description = "Calendar of Employee for Month"
    _sql_constraints = [('model_month_year_company_uniq', 'unique(attendance_id,employee_multi_id,month,year)',
                         'Attendance with this month of company is  already exist!!')]
    _order = 'company_code,department_code,job_code,s_identification_id , year, month asc'

    employee_multi_id = fields.Many2one('hr.employee.multi.company', string="Họ và tên",
                                        domain=lambda self: [('employee_current_status', '=', 'working'),
                                                             ('company_id', '=', self.env.user.company_id.id)])
    department_id = fields.Many2one('hr.department', string='Department', related='employee_multi_id.department_id',
                                    store=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_multi_id.job_id', store=True)
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

    day_1 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_1', 'calendar_id', 'shifts_id',
                             string="1", domain="[('id', 'in', domain_day)]")
    day_2 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_2', 'calendar_id', 'shifts_id',
                             string="2", domain="[('id', 'in', domain_day)]")
    day_3 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_3', 'calendar_id', 'shifts_id',
                             string="3", domain="[('id', 'in', domain_day)]")
    day_4 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_4', 'calendar_id', 'shifts_id',
                             string="4", domain="[('id', 'in', domain_day)]")
    day_5 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_5', 'calendar_id', 'shifts_id',
                             string="5", domain="[('id', 'in', domain_day)]")
    day_6 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_6', 'calendar_id', 'shifts_id',
                             string="6", domain="[('id', 'in', domain_day)]")
    day_7 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_7', 'calendar_id', 'shifts_id',
                             string="7", domain="[('id', 'in', domain_day)]")
    day_8 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_8', 'calendar_id', 'shifts_id',
                             string="8", domain="[('id', 'in', domain_day)]")
    day_9 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_9', 'calendar_id', 'shifts_id',
                             string="9", domain="[('id', 'in', domain_day)]")
    day_10 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_10', 'calendar_id', 'shifts_id',
                              string="10", domain="[('id', 'in', domain_day)]")
    day_11 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_11', 'calendar_id', 'shifts_id',
                              string="11", domain="[('id', 'in', domain_day)]")
    day_12 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_12', 'calendar_id', 'shifts_id',
                              string="12", domain="[('id', 'in', domain_day)]")
    day_13 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_13', 'calendar_id', 'shifts_id',
                              string="13", domain="[('id', 'in', domain_day)]")
    day_14 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_14', 'calendar_id', 'shifts_id',
                              string="14", domain="[('id', 'in', domain_day)]")
    day_15 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_15', 'calendar_id', 'shifts_id',
                              string="15", domain="[('id', 'in', domain_day)]")
    day_16 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_16', 'calendar_id', 'shifts_id',
                              string="16", domain="[('id', 'in', domain_day)]")
    day_17 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_17', 'calendar_id', 'shifts_id',
                              string="17", domain="[('id', 'in', domain_day)]")
    day_18 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_18', 'calendar_id', 'shifts_id',
                              string="18", domain="[('id', 'in', domain_day)]")
    day_19 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_19', 'calendar_id', 'shifts_id',
                              string="19", domain="[('id', 'in', domain_day)]")
    day_20 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_20', 'calendar_id', 'shifts_id',
                              string="20", domain="[('id', 'in', domain_day)]")
    day_21 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_21', 'calendar_id', 'shifts_id',
                              string="21", domain="[('id', 'in', domain_day)]")
    day_22 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_22', 'calendar_id', 'shifts_id',
                              string="22", domain="[('id', 'in', domain_day)]")
    day_23 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_23', 'calendar_id', 'shifts_id',
                              string="23", domain="[('id', 'in', domain_day)]")
    day_24 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_24', 'calendar_id', 'shifts_id',
                              string="24", domain="[('id', 'in', domain_day)]")
    day_25 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_25', 'calendar_id', 'shifts_id',
                              string="25", domain="[('id', 'in', domain_day)]")
    day_26 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_26', 'calendar_id', 'shifts_id',
                              string="26", domain="[('id', 'in', domain_day)]")
    day_27 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_27', 'calendar_id', 'shifts_id',
                              string="27", domain="[('id', 'in', domain_day)]")
    day_28 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_28', 'calendar_id', 'shifts_id',
                              string="28", domain="[('id', 'in', domain_day)]")
    day_29 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_29', 'calendar_id', 'shifts_id',
                              string="29", domain="[('id', 'in', domain_day)]")
    day_30 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_30', 'calendar_id', 'shifts_id',
                              string="30", domain="[('id', 'in', domain_day)]")
    day_31 = fields.Many2many('sea.hr.attendance.shift', 'calendar_employee_shifts_day_31', 'calendar_id', 'shifts_id',
                              string="31", domain="[('id', 'in', domain_day)]")

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         result.append((rec.id, 'Bảng chấm công NS: ' + str(rec.employee_multi_id.sudo().name.sudo().name)))
    #     return result

    def get_shift_of_employee_shift(self, employee_multi_id):
        shifts_employee = None
        get_shift = self.env['sea.hr.attendance.shift.employee'].sudo().search(
            [('employee_multi_id', '=', employee_multi_id)])
        if get_shift:
            '''xử lý trường hợp get_shift.attendance_config_ids == None'''
            if not get_shift.attendance_config_ids:
                employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', '=', employee_multi_id)])
                if employee_multi_id:
                    shift_company_department = self.env['sea.hr.attendance.shift'].sudo().search(
                        [('company_id', '=', employee_multi_id.sudo().company_id.id),
                         ('default_shift', '=', True),
                         ('department_id', '=', employee_multi_id.sudo().department_id.id)])
                    if shift_company_department:
                        shift_company = shift_company_department
                    else:
                        shift_company = self.env['sea.hr.attendance.shift'].sudo().search(
                            [('company_id', '=', employee_multi_id.sudo().company_id.id),
                             ('default_shift', '=', True), ('department_id', 'in', [None, False])])
                    shift = []
                    for i in shift_company:
                        shift.append((4, i.id))
                    if shift is not None:
                        get_shift.write({'attendance_config_ids': shift})

            shifts_employee = get_shift
        else:
            employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                [('id', '=', employee_multi_id)])
            if employee_multi_id:
                shift_company_department = self.env['sea.hr.attendance.shift'].sudo().search(
                    [('company_id', '=', employee_multi_id.sudo().company_id.id),
                     ('default_shift', '=', True), ('department_id', '=', employee_multi_id.sudo().department_id.id)])
                if shift_company_department:
                    shift_company = shift_company_department
                else:
                    shift_company = self.env['sea.hr.attendance.shift'].sudo().search(
                        [('company_id', '=', employee_multi_id.sudo().company_id.id),
                         ('default_shift', '=', True), ('department_id', 'in', [None, False])])
                shift = [(6, 0, [i.id for i in shift_company])] if shift_company else False
                if shift:
                    shifts_employee = self.env['sea.hr.attendance.shift.employee'].sudo().create({
                        'employee_multi_id': employee_multi_id.id,
                        'attendance_config_ids': shift
                    })

        return shifts_employee

    def check_duplication_shift(self, list_day_id):
        '''Các thứ chấm công của nhau không được trùng'''
        list_attendance = [attendance for attendance in list_day_id]
        while True:
            if len(list_attendance) == 0:
                break
            attendance_0 = list_attendance[0]
            list_attendance.pop(0)
            # if len(list_attendance) == 0:
            #     thu = self.get_thu(list_day_id)
            #     print(thu)
            #     if attendance_0.thu_2 and thu == 0 \
            #             or attendance_0.thu_3 and thu == 1 \
            #             or attendance_0.thu_4 and thu == 2 \
            #             or attendance_0.thu_5 and thu == 3 \
            #             or attendance_0.thu_6 and thu == 4 \
            #             or attendance_0.thu_7 and thu == 5 \
            #             or attendance_0.thu_8 and thu == 6:
            #         print('huuhu')
            #         pass
            #     else:
            #         print('hohoho')
            #         return attendance_0
            '''xem lại nha'''
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
                # else:
                #     '''chưa tính tới trường hợp ca đó không thuộc thứ đó "
                #     "TẠM LÀ VẬY vì nếu ca ngày ngày thứ 2 mà cac kia ngày thứ 3 thì có nghĩa nó sai'''
                #     return list_attendance[i]
        return False

    @api.onchange('day_1')
    def _onchange_day_1(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_1)
            if check:
                rec.day_1 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_2')
    def _onchange_day_2(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_2)
            if check:
                rec.day_2 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_3')
    def _onchange_day_3(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_3)
            if check:
                rec.day_3 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_4')
    def _onchange_day_4(self):

        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_4)
            if check:
                rec.day_4 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_5')
    def _onchange_day_5(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_5)
            if check:
                rec.day_5 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_6')
    def _onchange_day_6(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_6)
            if check:
                rec.day_6 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_7')
    def _onchange_day_7(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_7)
            if check:
                rec.day_7 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_8')
    def _onchange_day_8(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_8)
            if check:
                rec.day_8 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_9')
    def _onchange_day_9(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_9)
            if check:
                rec.day_9 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_10')
    def _onchange_day_10(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_10)
            if check:
                rec.day_10 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_11')
    def _onchange_day_11(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_11)
            if check:
                rec.day_11 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_12')
    def _onchange_day_12(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_12)
            if check:
                rec.day_12 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_13')
    def _onchange_day_13(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_13)
            if check:
                rec.day_13 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_14')
    def _onchange_day_14(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_14)
            if check:
                rec.day_14 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_15')
    def _onchange_day_15(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_15)
            if check:
                rec.day_15 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_16')
    def _onchange_day_16(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_16)
            if check:
                rec.day_16 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_17')
    def _onchange_day_17(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_17)
            if check:
                rec.day_17 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_18')
    def _onchange_day_18(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_18)
            if check:
                rec.day_18 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_19')
    def _onchange_day_19(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_19)
            if check:
                rec.day_19 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_20')
    def _onchange_day_20(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_20)
            if check:
                rec.day_20 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_21')
    def _onchange_day_21(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_21)
            if check:
                rec.day_21 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_22')
    def _onchange_day_22(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_22)
            if check:
                rec.day_22 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_23')
    def _onchange_day_23(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_23)
            if check:
                rec.day_23 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_24')
    def _onchange_day_24(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_24)
            if check:
                rec.day_24 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_25')
    def _onchange_day_25(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_25)
            if check:
                rec.day_25 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_26')
    def _onchange_day_26(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_26)
            if check:
                rec.day_26 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_27')
    def _onchange_day_27(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_27)
            if check:
                rec.day_27 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_28')
    def _onchange_day_28(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_28)
            if check:
                rec.day_28 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_29')
    def _onchange_day_29(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_29)
            if check:
                rec.day_29 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_30')
    def _onchange_day_30(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_30)
            if check:
                rec.day_30 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.onchange('day_31')
    def _onchange_day_31(self):
        '''xem lại còn trường hợp trùng các giờ bắt đầu tính và giờ kết thúc'''
        for rec in self:
            check = rec.check_duplication_shift(rec.day_31)
            if check:
                rec.day_31 = [(3, check.id)]
                return {'warning': {
                    'title': 'Lỗi thêm ca làm việc',
                    'message': "Bạn không thể thêm vì các ca làm việc trùng giờ nhau",
                }}

    @api.model
    def create(self, vals):
        if 'employee_multi_id' in vals and 'last_day_of_month' in vals and \
                'attendance_id' in vals and 'year' in vals and 'month' in vals:

            # day_ = []
            shifts_employee = self.get_shift_of_employee_shift(vals.get('employee_multi_id'))

            if shifts_employee:
                #     for shifts in shifts_employee.attendance_config_ids:
                #         if shifts:
                #             day_.append(shifts.id)

                if len(shifts_employee.attendance_config_ids.ids) != 0:
                    for i in range(vals.get('last_day_of_month') + 1):
                        if i > 0:
                            days = str('day_' + str(i))
                            dates = int(date.weekday(date(vals.get('year'), vals.get('month'), i)))

                            '''code này tự động tìm thứ 7 và chủ nhật và không gán LLV
                            vals[days] = [
                                (6, 0, shifts_employee.attendance_config_ids.ids if dates not in [5, 6] else [])]
                            '''
                            '''tính theo thứ của config shift'''
                            id_shift = []
                            for shifts in shifts_employee.attendance_config_ids:
                                if dates == 0 and shifts.thu_2 \
                                        or dates == 1 and shifts.thu_3 \
                                        or dates == 2 and shifts.thu_4 \
                                        or dates == 3 and shifts.thu_5 \
                                        or dates == 4 and shifts.thu_6 \
                                        or dates == 5 and shifts.thu_7 \
                                        or dates == 6 and shifts.thu_8:
                                    id_shift.append(shifts.id)
                                    # date_str = str(vals.get('year')) + '-' + str(vals.get('month')) + '-' + str(
                                    #     i) + ' ' + '00:00:00'
                                    # date_format = "%Y-%m-%d %H:%M:%S"
                                    # datetime_calendar = datetime.datetime.strptime(date_str, date_format)
                                    # value = {
                                    #     'employee_multi_id': vals.get('employee_multi_id'),
                                    #     'day': i,
                                    #     'month': vals.get('month'),
                                    #     'year': vals.get('year'),
                                    #     'shifts': shifts.id,
                                    #     'date_from': datetime_calendar,
                                    #     'date_to': datetime_calendar
                                    # }
                                    # self.env['sea.hr.calendar'].sudo().create(value)
                            vals[days] = [(6, 0, id_shift)]

        result = super(CalendarEmployee, self).create(vals)
        return result

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
    def get_thu(self, day=None):
        da = None
        if day == self.day_1:
            da = 1
        elif day == self.day_2:
            da = 2
        elif day == self.day_3:
            da = 3
        elif day == self.day_4:
            da = 4
        elif day == self.day_5:
            da = 5
        elif day == self.day_6:
            da = 6
        elif day == self.day_7:
            da = 7
        elif day == self.day_8:
            da = 8
        elif day == self.day_9:
            da = 9
        elif day == self.day_10:
            da = 10
        elif day == self.day_11:
            da = 11
        elif day == self.day_12:
            da = 12
        elif day == self.day_13:
            da = 13
        elif day == self.day_14:
            da = 14
        elif day == self.day_15:
            da = 15
        elif day == self.day_16:
            da = 16
        elif day == self.day_17:
            da = 17
        elif day == self.day_18:
            da = 18
        elif day == self.day_19:
            da = 19
        elif day == self.day_20:
            da = 20
        elif day == self.day_21:
            da = 21
        elif day == self.day_22:
            da = 22
        elif day == self.day_23:
            da = 23
        elif day == self.day_24:
            da = 24
        elif day == self.day_25:
            da = 25
        elif day == self.day_26:
            da = 26
        elif day == self.day_27:
            da = 27
        elif day == self.day_28:
            da = 28
        elif day == self.day_29:
            da = 29
        elif day == self.day_30:
            da = 30
        elif day == self.day_31:
            da = 31
        return int(date.weekday(date(self.year, self.month, da)))


class SeaHrAttendance(models.Model):
    _inherit = 'sea.hr.attendance'

    calendar_of_month = fields.One2many('sea.hr.calendar.employee', 'attendance_id', string="Lịch làm việc trong tháng")

    def compute_date_current(self):
        for rec in self:
            if int(rec.month) >= fields.datetime.now().month and int(rec.year) == fields.datetime.now().year \
                    or int(rec.year) > fields.datetime.now().year:
                rec.date_current = False
            else:
                rec.date_current = True

    date_current = fields.Boolean('Date Current', compute='compute_date_current')

    '''add domain'''
    department_id_c = fields.Many2one('hr.department', string='Lọc theo Đơn Vị')
    employee_id_c = fields.Char(string='Tìm theo tên nhân sự hoặc mã SeaCode')
    ''''''

    # @api.onchange('department_code_c', 'employee_id_c')
    # def onchange_department_code_c_employee_id_c(self):
    #     for rec in self:
    #         if rec.department_code_c or rec.employee_id_c:
    #             hr_employee = False
    #             if rec.employee_id_c:
    #                 hr_employee = self.env['hr.employee'].sudo().search(
    #                     ['|', ('s_identification_id', 'ilike', rec.employee_id_c),
    #                      ('name', 'ilike', rec.employee_id_c), ('company_id', '=', rec.company_id.id)])
    #
    #             else:
    #                 rec.calendar_of_month_compute = rec.calendar_of_month.filtered(
    #                     lambda record: record.department_code == rec.department_code_c)
    #
    #             if hr_employee:
    #                 if rec.department_code_c:
    #                     rec.calendar_of_month_compute = rec.calendar_of_month.filtered(
    #                         lambda
    #                             record: record.department_code == rec.department_code_c and record.s_identification_id in [
    #                             i.s_identification_id for i in
    #                             hr_employee])
    #                 else:
    #                     rec.calendar_of_month_compute = rec.calendar_of_month.filtered(
    #                         lambda record: record.s_identification_id in [
    #                             i.s_identification_id for i in
    #                             hr_employee])
    #         else:
    #             rec.calendar_of_month_compute = rec.calendar_of_month

    def compute_calendar_of_month_compute(self):
        for rec in self:
            rec.calendar_of_month_compute = None
            calendar_of_month = rec.calendar_of_month
            if rec.department_id_c or rec.employee_id_c:
                hr_employee = False
                if rec.employee_id_c:
                    hr_employee = self.env['hr.employee'].sudo().search(
                        ['|', ('s_identification_id', 'ilike', rec.employee_id_c),
                         ('name', 'ilike', rec.employee_id_c), ('company_id', '=', rec.company_id.id)])

                else:
                    calendar_of_month = calendar_of_month.filtered(
                        lambda record: record.employee_multi_id.sudo().department_id.id == rec.department_id_c.id)

                if hr_employee:
                    if rec.department_id_c:
                        calendar_of_month = calendar_of_month.filtered(
                            lambda record: record.employee_multi_id.sudo().department_id.id ==
                                           rec.department_id_c.id and record.s_identification_id
                                           in [j.s_identification_id for j in hr_employee])
                    else:
                        calendar_of_month = calendar_of_month.filtered(
                            lambda record: record.s_identification_id in [
                                j.s_identification_id for j in hr_employee])
            if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_manager'):
                # if rec.department_id_c or rec.employee_id_c:
                #     hr_employee = False
                #     if rec.employee_id_c:
                #         hr_employee = self.env['hr.employee'].sudo().search(
                #             ['|', ('s_identification_id', 'ilike', rec.employee_id_c),
                #              ('name', 'ilike', rec.employee_id_c), ('company_id', '=', rec.company_id.id)])
                #
                #     else:
                #         rec.calendar_of_month_compute = calendar_of_month.filtered(
                #             lambda record: record.employee_multi_id.sudo().department_id.id == rec.department_id_c.id)
                #
                #     if hr_employee:
                #         if rec.department_id_c:
                #             rec.calendar_of_month_compute = calendar_of_month.filtered(
                #                 lambda record: record.employee_multi_id.sudo().department_id.id ==
                #                 rec.department_id_c.id and record.s_identification_id
                #                 in [j.s_identification_id for j in hr_employee])
                #         else:
                #             rec.calendar_of_month_compute = calendar_of_month.filtered(
                #                 lambda record: record.s_identification_id in [
                #                     j.s_identification_id for j in hr_employee])
                # else:
                rec.calendar_of_month_compute = calendar_of_month
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
                        rec.calendar_of_month_compute = calendar_of_month.filtered(
                            lambda record: record.employee_multi_id.id in list_employee)

    calendar_of_month_compute = fields.One2many('sea.hr.calendar.employee', 'attendance_id',
                                                string="Lịch làm việc trong tháng",
                                                compute='compute_calendar_of_month_compute')

    def upgrade_calendar(self):
        '''theo tháng chỉ cho tương lai'''
        for rec in self:
            if int(rec.month) >= fields.datetime.now().month and int(rec.year) == fields.datetime.now().year \
                    or int(rec.year) > fields.datetime.now().year:
                day = fields.datetime.now().day
                month = fields.datetime.now().month
                year = fields.datetime.now().year
                domain = [('attendance_id', '=', rec.id), ('month', '=', rec.month), ('year', '=', rec.year)]
                domain1 = [('company_id', '=', rec.company_id.id)]
                if rec.department_id_c:
                    domain.append(('department_id', '=', rec.department_id_c.id))
                    domain1.append(('department_id', '=', rec.department_id_c.id))
                employee_calendar = self.env['sea.hr.calendar.employee'].sudo().search(domain)
                if employee_calendar:
                    domain1.append(('employee_multi_id', 'not in', [i.employee_multi_id.id for i in employee_calendar]))
                    new = self.env['sea.hr.attendance.shift.employee'].sudo().search(domain1)
                    if new:
                        for e in new:
                            create_calendar = self.env['sea.hr.calendar.employee'].sudo().create({
                                'employee_multi_id': e.employee_multi_id.id,
                                'attendance_id': rec.id,
                                'last_day_of_month': int(int(calendar.monthrange(int(rec.year), int(rec.month))[1])),
                                'year': int(rec.year),
                                'month': int(rec.month)
                            })
                            if create_calendar:
                                if not self.env['sea.hr.attendance.month'].sudo().search(
                                        [('employee_multi_id', '=', e.employee_multi_id.id,), ('month', '=', month),
                                         ('year', '=', year), ('attendance_id', '=', rec.id)]):
                                    values = {
                                        'employee_multi_id': e.employee_multi_id.id,
                                        'attendance_id': rec.id,
                                        'last_day_of_month': int(
                                            int(calendar.monthrange(int(rec.year), int(rec.month))[1])),
                                        'year': int(rec.year),
                                        'month': int(rec.month),
                                    }
                                    self.env['sea.hr.attendance.month'].sudo().create(values)
                            # if create_calendar:
                            #     for i in range(fields.datetime.now().day):
                            #         day_delete = i + 1
                            #         create_calendar.write({'day_' + str(day_delete): []})
                '''for ngược từ ngày last_day_of_month trờ về để cập nhật từng cái'''
                for employee in employee_calendar.filtered(lambda m: m.id in rec.calendar_of_month_compute.ids):
                    for i in range(int(int(calendar.monthrange(int(rec.year), int(rec.month))[1])), 0, -1):
                        if i >= day or month < int(rec.month) and year == int(rec.year) or year < int(rec.year):
                            '''so sánh và uprade'''
                            day_ = employee.get_day(i)
                            shifts_employee = employee.get_shift_of_employee_shift(employee.employee_multi_id.id)
                            dates = int(date.weekday(date(int(rec.year), int(rec.month), i)))
                            id_shift = []
                            for shifts in shifts_employee.attendance_config_ids:
                                if dates == 0 and shifts.thu_2 \
                                        or dates == 1 and shifts.thu_3 \
                                        or dates == 2 and shifts.thu_4 \
                                        or dates == 3 and shifts.thu_5 \
                                        or dates == 4 and shifts.thu_6 \
                                        or dates == 5 and shifts.thu_7 \
                                        or dates == 6 and shifts.thu_8:
                                    id_shift.append(shifts.id)

                            residual_elements = set(day_.ids).difference(
                                set(id_shift))
                            missing_elements = set(id_shift).difference(
                                set(day_.ids))
                            if residual_elements:
                                employee.write({
                                    'day_' + str(i): [(3, attendance_config) for attendance_config in
                                                      residual_elements]})
                            if missing_elements:
                                employee.write({'day_' + str(i): [(4, attendance_config) for
                                                                  attendance_config in missing_elements]})
                        else:
                            break

            else:
                raise ValidationError("Không thể cập nhật ngày nhỏ hơn ngày hiện tại!")
