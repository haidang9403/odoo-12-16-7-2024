import datetime
import logging
import uuid
from datetime import date

from odoo import api, models, fields
from odoo.addons.hr_contract.models.hr_contract import Contract as Contracts
from odoo.exceptions import ValidationError


class HrContractPeriodExtend(models.Model):
    _inherit = 'hr.contract.period'

    remaining_day_to_renew = fields.Integer(string='Remaining day to renew')

    @api.constrains('remaining_day_to_renew')
    def check_remaining_day_to_renew(self):
        if self.filtered(lambda c: c.remaining_day_to_renew < 0):
            raise ValidationError(('Số ngày còn lại để gia hạn trước khi hết hạn phải lớn hơn hoặc bằng 0.'))


class HrContractTypeExtend(models.Model):
    _inherit = 'hr.contract.type'

    remaining_day_to_renew = fields.Integer(string='Remaining day to renew')

    @api.constrains('remaining_day_to_renew')
    def check_remaining_day_to_renew(self):
        if self.filtered(lambda c: c.remaining_day_to_renew < 0):
            raise ValidationError(('Số ngày còn lại để gia hạn trước khi hết hạn phải lớn hơn hoặc bằng 0.'))


class create_mail_activity_hr_contracts(models.Model):
    _inherit = 'hr.contract'

    remaining_days = fields.Integer(string="Contract expiration date")
    sea_extend_contract = fields.One2many('mail.activity', 'contract_id', string="Sea Extend Contract", required=False)

    '''version 1.1'''

    @api.constrains('date_start', 'date_end')
    def _check_date_end(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                if rec.date_end < rec.date_start:
                    raise ValidationError(('Thời gian bắt đầu hợp đồng phải nhỏ hơn thời gian hết hạn.'))

    ''''''

    @api.multi
    def _track_subtype(self, init_values):
        self.ensure_one()
        if 'state' in init_values and self.state == 'close':
            return 'hr_contract.mt_contract_close'
        return super(Contracts, self)._track_subtype(init_values)

    Contracts._track_subtype = _track_subtype

    # @api.multi
    # def _change_state(self, rec):
    #     if rec.date_end:
    #         if rec.date_end < date.today():
    #             rec.write({'state': "close"})
    #             list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
    #             if list_addition:
    #                 for addition in list_addition:
    #                     if addition.state != 'close':
    #                         addition.write({'state': "close"})
    #             print("close", rec.employee_id.id)
    #     if rec.state == "pending" and not rec.sea_extend_contract:
    #         rec.write({'state': "draft"})
    #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
    #         if list_addition:
    #             for addition in list_addition:
    #                 if addition.state != 'draft':
    #                     addition.write({'state': "draft"})
    #         print("new", rec.employee_id.name)
    #     if rec.employee_id and rec.department_id and rec.job_id and not rec.sea_extend_contract and rec.state == "draft":
    #         rec.write({'state': "open"})
    #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
    #         if list_addition:
    #             for addition in list_addition:
    #                 if addition.state != 'open':
    #                     addition.write({'state': "open"})
    #         print("running", rec.employee_id.name)
    #
    #     list_addition_1 = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
    #     if list_addition_1:
    #         for addition in list_addition_1:
    #             if rec.state != 'pending':
    #                 if addition.state != rec.state:
    #                     # print(rec.state)
    #                     addition.write({'state': rec.state})

    '''version 1.1'''

    @api.multi
    def change_state_addition(self):
        for rec in self:
            list_addition = self.env['hr.contract'].sudo().search(
                [('ref_contract_id', '=', rec.id), ('contract_category', '!=', 'contract'),
                 ('state', 'not in', ['cancel', 'close'])])
            if list_addition:
                for addition in list_addition:
                    if addition.state != rec.state:
                        addition.write({'state': rec.state})
            # print(rec.state, ": ", rec.employee_id.id)

    @api.multi
    def cancel_schedule_activity(self):
        for rec in self:
            # unlink mail_activity => id = sea_extend_contract
            for sea_extend_contract in rec.sea_extend_contract:
                rec.env['mail.activity'].sudo().search(
                    [('id', '=', sea_extend_contract.id)]).sudo().unlink()

    @api.multi
    def create_or_write_mail(self):
        # user_id => Job Position
        # user_id = self.create_user_id_mail_activity(self)
        # user_id = 8
        user_ids = self.env['user.mail'].sudo().search([])
        ids = []
        for u in user_ids:
            ids.append(u.name.id)
        if self.job_id:
            if self.job_id.hr_responsible_id:
                user_id = self.job_id.hr_responsible_id.id
                if user_id not in ids:
                    ids.append(user_id)

        if self.sea_extend_contract:
            '''chỉnh ngày'''
            for sea_extend_contract in self.sea_extend_contract:
                if sea_extend_contract.date_deadline:
                    if sea_extend_contract.date_deadline != self.date_end:
                        sea_extend_contract.sudo().write(
                            {'date_deadline': self.date_end})
        else:
            for user_id in ids:
                '''tạo mới'''
                self.create_mail_activity(self, user_id,
                                          self.env[
                                              'mail.activity.type.id.of.hr.contract'].sudo().search(
                                              [('name', '=', 'not_probation')], limit=1).activity_type_id.id,
                                          'hr.contract')

    ''''''

    @api.multi
    def create_mail_activity(self, contract, user_id, activity_type_id, model):
        res_model = self.env['ir.model'].sudo().search([('model', '=', model)], limit=1)

        self.env['hr.contract'].sudo().search([('id', '=', contract.id)]).write(
            {'sea_extend_contract': [(0, 0, {'date_deadline': contract.date_end, 'res_id': contract.id,
                                             'res_model_id': res_model.id, 'res_model': res_model.model,
                                             'res_name': contract.name, 'activity_type_id': activity_type_id,
                                             'automated': True,
                                             'user_id': user_id, 'create_user_id': self.env.user.id})],
             # 'state': "pending"
             })

    @api.multi
    def check_contract_ir_cron(self):
        self.env.cr.execute("SELECT current_database();")
        db_name = self.env.cr.dictfetchall()[0]['current_database']
        ip_mac = (''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                           for ele in range(0, 8 * 6, 8)][::-1])).lower()
        # logging.info("BY TKK IP MAC: %s", str(ip_mac))
        # logging.info("BY TKK db_name: %s", str(db_name))
        res_model = self.env['ir.model'].sudo().search([('model', '=', 'hr.contract')], limit=1)
        domain = False if not res_model else ['|', ('key', '=', 'database.uuid'),
                                              ('res_model_id', '=', res_model.id)]
        database_uuid = self.env['database.uuid'].sudo().search(domain).filtered(
            lambda l: l.ip_mac and l.db_name == db_name)
        if database_uuid:
            test = []
            for database in database_uuid:
                if database.ip_mac.lower().replace(':', '').replace('-', '').replace('.', '') == ip_mac:
                    test.append(database.value.replace("-", "."))
            # =================================================================
            if self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") in test:
                return True
        return False

    @api.model
    def mail_activity_create(self):
        try:
            if self.check_contract_ir_cron():
                # print("start")
                # to_date = False
                for rec in self.env['hr.contract'].sudo().search(
                        [('state', 'not in', ['cancel', 'close']), ('contract_category', '=', 'addition'),
                         ('date_end', '<=', date.today())]):
                    # print("addition: ", rec.name)
                    rec.write({'state': "close"})

                self.env.cr.execute("SELECT MAX(remaining_day_to_renew) AS max_remaining_day_to_renew "
                                    "FROM ("
                                    "SELECT remaining_day_to_renew FROM public.hr_contract_type "
                                    "UNION ALL "
                                    "SELECT remaining_day_to_renew FROM public.hr_contract_period"
                                    ") AS combined_results;")
                remaining_day_to_renew = self.env.cr.dictfetchall()[0]['max_remaining_day_to_renew']
                # print("remaining_day_to_renew: ", remaining_day_to_renew)
                for rec in self.env['hr.contract'].sudo().search(
                        [('state', 'not in', ['cancel', 'close']), ('contract_category', '=', 'contract'),
                         ('date_end', '<=', date.today() + datetime.timedelta(days=remaining_day_to_renew))]):
                    # print("contract: ", rec.name)
                    if rec.date_end <= date.today():
                        rec.write({'state': "close"})
                    else:
                        change_open = True
                        number_of_days = False
                        if rec.contract_period_id:
                            number_of_days = rec.contract_period_id.sudo().remaining_day_to_renew
                        if not number_of_days and rec.type_id:
                            number_of_days = rec.type_id.sudo().remaining_day_to_renew
                        if number_of_days:
                            if rec.date_end <= date.today() + datetime.timedelta(days=number_of_days):
                                change_open = False
                                # to_date = True
                                if rec.state != 'pending':
                                    rec.write({'state': "pending"})

                        if change_open and rec.state != 'open':
                            rec.write({'state': "open"})

                    # if to_date:
                    #     ''' tạo đồng thời gửi mail hoặc thay đổi ngày hết hạn của schedule activity
                    #     khi trạng thái(state) thay đổi sang [pending] - To Renew của Category là contract'''
                    #     rec.create_or_write_mail()

                # for rec in self.env['hr.contract'].sudo().search(
                #         [('state', 'not in', ['cancel', 'close']), ('contract_category', '=', 'contract')]):
                #     if rec.date_end:
                #         # print(rec, rec.date_end)
                #         if rec.date_end < date.today():
                #             rec.write({'state': "close"})
                #             list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
                #             if list_addition:
                #                 for addition in list_addition:
                #                     if addition.state != 'close':
                #                         addition.write({'state': "close"})
                #             print("close", rec.employee_id.id)
                #         else:
                #             current_date = date.today()
                #             days = rec.date_end - current_date
                #             end_days = days.days
                #             # print(end_days)
                #
                #             # set user_id JOB Position
                #             # user_id = self.create_user_id_mail_activity(self)
                #             # user_id = 8
                #
                #             if not rec.sea_extend_contract:
                #                 # print(rec.sea_extend_contract.id)
                #                 user_ids = self.env['user.mail'].sudo().search([])
                #                 ids = []
                #                 for u in user_ids:
                #                     ids.append(u.name.id)
                #
                #                 if rec.job_id:
                #                     if rec.job_id.hr_responsible_id:
                #                         user_id = rec.job_id.hr_responsible_id.id
                #                         if user_id not in ids:
                #                             ids.append(user_id)
                #                 if ids is not None:
                #                     for user_id in ids:
                #                         mail_activity_type_not_probation = self.env[
                #                             'mail.activity.type.id.of.hr.contract'].sudo().search(
                #                             [('name', '=', 'not_probation')], limit=1)
                #                         mail_activity_type_probation = self.env[
                #                             'mail.activity.type.id.of.hr.contract'].sudo().search(
                #                             [('name', '=', 'probation')], limit=1)
                #                         # print(end_days, mail_activity_type_probation.activity_type_id.delay_count)
                #                         if rec.type_id.id != 4:
                #                             if end_days <= mail_activity_type_not_probation.activity_type_id.delay_count:
                #                                 self.create_mail_activity(rec, self.env['res.users'].sudo().search(
                #                                     [('id', '=', user_id)]).id,
                #                                                           mail_activity_type_not_probation.activity_type_id.id,
                #                                                           'hr.contract')
                #                                 print("insert all (probation)", end_days)
                #                         else:
                #                             if rec.type_id.id == 4 or rec.contract_period_id.id in [23, 24]:
                #                                 if end_days <= mail_activity_type_probation.activity_type_id.delay_count:
                #                                     self.create_mail_activity(rec, self.env['res.users'].sudo().search(
                #                                         [('id', '=', user_id)]).id,
                #                                                               mail_activity_type_probation.activity_type_id.id,
                #                                                               'hr.contract')
                #                                     print("insert probation", end_days)
                #
                #             elif rec.state != 'pending' and rec.date_end >= date.today():
                #                 # print(rec.date_end, date.today())
                #                 rec.write({'state': "pending"})
                #                 print("change state pending", rec.employee_id.name)
                #             rec.write({'remaining_days': end_days})
                #
                #     if rec.state == "pending" and not rec.sea_extend_contract:
                #         rec.write({'state': "draft"})
                #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
                #         if list_addition:
                #             for addition in list_addition:
                #                 if addition.state != 'draft':
                #                     addition.write({'state': "draft"})
                #         print("new", rec.employee_id.name)
                #     if rec.employee_id and rec.department_id and rec.job_id and \
                #             not rec.sea_extend_contract and rec.state == "draft":
                #         rec.write({'state': "open"})
                #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
                #         if list_addition:
                #             for addition in list_addition:
                #                 if addition.state != 'open':
                #                     addition.write({'state': "open"})
                #         print("running", rec.employee_id.name)
                #
                #     self._change_state(rec)
                #
                # for rec in self.env['hr.contract'].sudo().search(
                #         [('state', 'in', ['cancel', 'close']), ('contract_category', '=', 'contract')]):
                #     list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', rec.id)])
                #     if list_addition:
                #         for addition in list_addition:
                #             # if rec.state != 'close':
                #             if rec.state == 'close' and addition.state != 'close':
                #                 addition.write({'state': "close"})
                #             # if rec.state != 'cancel':
                #             if rec.state == 'cancel' and addition.state != 'cancel':
                #                 addition.write({'state': "cancel"})
            else:
                logging.error("do not start cron jobs 'Contracts: Contract notification'")
                # print("do not start")
            # print("insert mail.activity ok")
        except Exception as e:
            logging.error("BY TKK Exception cron jobs 'Contracts: Contract notification': %s", str(e))

    @api.multi
    def write(self, vals):
        to_date = False
        check_edit_state = False
        for rec in self:
            '''[CHỈ KHI TỒN TẠI NGÀY KẾT THÚC HĐLĐ và Category là contract]'''
            check_contract_category = False
            date_end = False
            type_id = False
            contract_period_id = False
            if 'contract_category' in vals:
                if vals.get('contract_category') == "contract":
                    check_contract_category = True
            elif rec.contract_category == "contract":
                check_contract_category = True
            if not check_contract_category and date_end:
                if 'contract_category' in vals or 'date_end' in vals:
                    da = False
                    if 'date_end' in vals:
                        if vals.get('date_end'):
                            da = True if datetime.datetime.strptime(vals.get('date_end'),
                                                                    '%Y-%m-%d').date() <= date.today() else False
                    elif rec.date_end:
                        da = True if rec.date_end <= date.today() else False
                    if da:
                        '''kết thúc HĐ'''
                        if rec.state != "close":
                            vals['state'] = "close"

            elif 'contract_category' in vals or 'date_end' in vals or 'type_id' in vals or 'contract_period_id' in vals:
                if 'date_end' in vals:
                    if vals.get('date_end'):
                        date_end = datetime.datetime.strptime(vals.get('date_end'), '%Y-%m-%d').date()
                elif rec.date_end:
                    date_end = rec.date_end

                if 'type_id' in vals:
                    if vals.get('type_id'):
                        type_id = vals.get('type_id')
                elif rec.type_id:
                    type_id = rec.type_id.id

                if 'contract_period_id' in vals:
                    if vals.get('contract_period_id'):
                        contract_period_id = vals.get('contract_period_id')
                elif rec.contract_period_id:
                    contract_period_id = rec.contract_period_id.id
            if 'state' in vals:
                if check_contract_category:
                    check_edit_state = True
                    to_date = True
                check_contract_category = False
            '''kiểm tra và chỉnh lại trạng thái của record có Category là contract '''
            '''nếu ['contract_category' or 'date_end' or 'contract_category'] thay đổi'''
            '''thay đổi trạng thái(nếu thỏa điều kiện) & đồng thời thay đổi các phụ lục tương ứng nếu có '''
            if check_contract_category and date_end:
                '''Thay đổi Category(contract_category)'''
                '''OR thay đổi ngày kết thúc(date_end)'''
                '''OR thay đổi Loại(type_id)'''
                if date_end <= date.today():
                    '''kết thúc HĐ'''
                    if rec.state != "close":
                        vals['state'] = "close"
                        check_edit_state = True
                else:
                    change_open = True
                    if contract_period_id or type_id:
                        '''chuyển trạng thái sang To Renew nếu hợp lệ'''
                        number_of_days = False
                        if contract_period_id:
                            contract_period = self.env['hr.contract.period'].sudo().search(
                                [('id', '=', contract_period_id)])
                            if contract_period:
                                if contract_period.remaining_day_to_renew:
                                    number_of_days = contract_period.remaining_day_to_renew
                        if not number_of_days:
                            contract_type = self.env['hr.contract.type'].sudo().search([('id', '=', type_id)])
                            if contract_type:
                                if contract_type.remaining_day_to_renew:
                                    number_of_days = contract_type.remaining_day_to_renew
                        if number_of_days:
                            if date_end <= date.today() + datetime.timedelta(days=number_of_days):
                                change_open = False
                                if rec.state != 'pending':
                                    vals['state'] = 'pending'
                                    check_edit_state = True
                                to_date = date.today() + datetime.timedelta(days=number_of_days)
                    if change_open and rec.state != 'open':
                        vals['state'] = 'open'
                        check_edit_state = True

        res = super(create_mail_activity_hr_contracts, self).write(vals)
        # if vals.get('contract_category') is not None:
        #     if vals.get('contract_category') == "contract":
        #         print("change contract_category")
        #
        # elif self.contract_category == "contract":
        #     # create or delete mail activity
        #     if vals.get('state') is not None:
        #         # change state close or cancel
        #         if vals.get('state') == "cancel" and self.sea_extend_contract:
        #
        #             list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', self.id)])
        #             if list_addition:
        #                 for addition in list_addition:
        #                     if addition.state != 'cancel':
        #                         addition.write({'state': "cancel"})
        #
        #             # unlink mail_activity => id = sea_extend_contract
        #             for sea_extend_contract in self.sea_extend_contract:
        #                 self.env['mail.activity'].sudo().search([('id', '=', sea_extend_contract.id)]).unlink()
        #             self.sea_extend_contract = None
        #             print("delete for mail activity on  write hr_contracts for contract")
        #         else:
        #             if vals.get('state') == "draft":
        #                 list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', self.id)])
        #                 if list_addition:
        #                     for addition in list_addition:
        #                         if addition.state != 'draft':
        #                             addition.write({'state': "draft"})
        #
        #             elif vals.get('state') == "open":
        #                 list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', self.id)])
        #                 if list_addition:
        #                     for addition in list_addition:
        #                         if addition.state != 'open':
        #                             addition.write({'state': "open"})
        #             else:
        #                 if vals.get('state') == "close":
        #                     list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', self.id)])
        #                     if list_addition:
        #                         for addition in list_addition:
        #                             if addition.state != 'close':
        #                                 addition.write({'state': "close"})
        #     else:
        #         if vals.get('date_end') is not None or vals.get('type_id') is not None or vals.get(
        #                 'contract_period_id') is not None:
        #             if self.state not in ["close", "cancel"]:
        #                 mail_activity_type_probation = self.env['mail.activity.type.id.of.hr.contract'].sudo().search(
        #                     [('name', '=', 'probation')], limit=1)
        #                 mail_activity_type_not_probation = self.env[
        #                     'mail.activity.type.id.of.hr.contract'].sudo().search(
        #                     [('name', '=', 'not_probation')], limit=1)
        #
        #                 date_probation = datetime.datetime.now() + datetime.timedelta(
        #                     days=mail_activity_type_probation.activity_type_id.delay_count)
        #                 date_not_probation = datetime.datetime.now() + datetime.timedelta(
        #                     days=mail_activity_type_not_probation.activity_type_id.delay_count)
        #                 # print(date_probation, date_not_probation, date_end)
        #
        #                 # user_id => Job Position
        #                 # user_id = self.create_user_id_mail_activity(self)
        #                 # user_id = 8
        #                 user_ids = self.env['user.mail'].sudo().search([])
        #                 ids = []
        #                 for u in user_ids:
        #                     ids.append(u.name.id)
        #
        #                 if self.job_id:
        #                     if self.job_id.hr_responsible_id:
        #                         user_id = self.job_id.hr_responsible_id.id
        #                         if user_id not in ids:
        #                             # print(user_ids)
        #                             ids.append(user_id)
        #
        #                 # TRƯỜNG HỢP CHANGE DATE_END OR CẢ HAI
        #                 # create or edit or delete on date_end
        #                 if vals.get('date_end') is not None:
        #                     # delete
        #                     if vals.get('date_end') in [None, False] and self.sea_extend_contract:
        #                         # unlink mail_activity => id = sea_extend_contract
        #                         for sea_extend_contract in self.sea_extend_contract:
        #                             self.env['mail.activity'].sudo().search(
        #                                 [('id', '=', sea_extend_contract.id)]).unlink()
        #                         self.sea_extend_contract = None
        #                         self._change_state(self)
        #                         print("delete mail activity for contract")
        #                     # edit or create
        #                     elif vals.get('contract_period_id') is not None or vals.get('type_id') is not None:
        #                         date_end = datetime.datetime.strptime(str(vals.get('date_end')), '%Y-%m-%d')
        #                         if vals.get('date_end') not in [None, False]:
        #                             # change contract_period_id and date_end
        #                             # create
        #                             if not self.sea_extend_contract:
        #
        #                                 if ids is not None:
        #                                     for user_id in ids:
        #                                         if vals.get('type_id') == 4 or vals.get('contract_period_id') in [23,
        #                                                                                                           24]:
        #                                             if date_end <= date_probation:
        #                                                 self.create_mail_activity(self,
        #                                                                           self.env['res.users'].sudo().search(
        #                                                                               [('id', '=', user_id)]).id,
        #                                                                           mail_activity_type_probation.activity_type_id.id,
        #                                                                           'hr.contract')
        #                                                 print("change date_end and type_id = 4")
        #                                         elif self.type_id.id != 4 and date_end <= date_not_probation:
        #                                             self.create_mail_activity(self, self.env['res.users'].sudo().search(
        #                                                 [('id', '=', user_id)]).id,
        #                                                                       mail_activity_type_not_probation.activity_type_id.id,
        #                                                                       'hr.contract')
        #                                             print("change date_end and type_id != 4")
        #
        #                             # edit
        #                             else:
        #                                 if date_end > date_not_probation:
        #                                     # unlink mail_activity => id = sea_extend_contract
        #                                     for sea_extend_contract in self.sea_extend_contract:
        #                                         self.env['mail.activity'].sudo().search(
        #                                             [('id', '=', sea_extend_contract.id)]).unlink()
        #                                     self.sea_extend_contract = None
        #                                     self._change_state(self)
        #                                     print("delete mail activity for contract")
        #                                 else:
        #                                     # write date_end
        #                                     for sea_extend_contract in self.sea_extend_contract:
        #                                         self.env['mail.activity'].sudo().search(
        #                                             [('id', '=', sea_extend_contract.id)]).write(
        #                                             {'date_deadline': vals.get('date_end')})
        #                                     if vals.get('type_id') is not None:
        #                                         if vals.get('type_id') != 4:
        #                                             for sea_extend_contract in self.sea_extend_contract:
        #                                                 self.env['mail.activity'].sudo().search(
        #                                                     [('id', '=', sea_extend_contract.id)]).write(
        #                                                     {
        #                                                         'activity_type_id': mail_activity_type_not_probation.activity_type_id.id})
        #                                         else:
        #                                             # write type_id
        #                                             if date_end <= date_probation:
        #                                                 for sea_extend_contract in self.sea_extend_contract:
        #                                                     self.env['mail.activity'].sudo().search(
        #                                                         [('id', '=', sea_extend_contract.id)]).write(
        #                                                         {
        #                                                             'activity_type_id': mail_activity_type_probation.activity_type_id.id})
        #                                             else:
        #                                                 # unlink mail_activity => id = sea_extend_contract
        #                                                 for sea_extend_contract in self.sea_extend_contract:
        #                                                     self.env['mail.activity'].sudo().search(
        #                                                         [('id', '=', sea_extend_contract.id)]).unlink()
        #                                                 self.sea_extend_contract = None
        #                                                 self._change_state(self)
        #                                                 print("delete mail activity for contract")
        #
        #                                     elif vals.get('contract_period_id') is not None:
        #                                         if vals.get('contract_period_id') in [23, 24]:
        #                                             for sea_extend_contract in self.sea_extend_contract:
        #                                                 self.env['mail.activity'].sudo().search(
        #                                                     [('id', '=', sea_extend_contract.id)]).write(
        #                                                     {
        #                                                         'activity_type_id': mail_activity_type_probation.activity_type_id.id})
        #
        #                                     # edit
        #                                     print("edit ok")
        #                     else:
        #                         date_end = datetime.datetime.strptime(str(vals.get('date_end')), '%Y-%m-%d')
        #                         if not self.sea_extend_contract:
        #                             if ids is not None:
        #                                 for user_id in ids:
        #                                     if self.type_id.id == 4 or self.contract_period_id in [23, 24]:
        #                                         if date_end <= date_probation:
        #                                             self.create_mail_activity(self, self.env['res.users'].sudo().search(
        #                                                 [('id', '=', user_id)]).id,
        #                                                                       mail_activity_type_probation.activity_type_id.id,
        #                                                                       'hr.contract')
        #                                             print("create only change date_end")
        #                                     else:
        #                                         if self.type_id.id != 4 and date_end <= date_not_probation:
        #                                             self.create_mail_activity(self, self.env['res.users'].sudo().search(
        #                                                 [('id', '=', user_id)]).id,
        #                                                                       mail_activity_type_not_probation.activity_type_id.id,
        #                                                                       'hr.contract')
        #                                             print("only change date_end with type_id !=4")
        #                         else:
        #                             if self.type_id.id == 4 and date_end > date_probation:
        #                                 # unlink mail_activity => id = sea_extend_contract
        #                                 for sea_extend_contract in self.sea_extend_contract:
        #                                     self.env['mail.activity'].sudo().search(
        #                                         [('id', '=', sea_extend_contract.id)]).unlink()
        #                                 self.sea_extend_contract = None
        #                                 self._change_state(self)
        #                             elif self.type_id.id != 4 and date_end > date_not_probation:
        #                                 # unlink mail_activity => id = sea_extend_contract
        #                                 for sea_extend_contract in self.sea_extend_contract:
        #                                     self.env['mail.activity'].sudo().search(
        #                                         [('id', '=', sea_extend_contract.id)]).unlink()
        #                                 self.sea_extend_contract = None
        #                                 self._change_state(self)
        #                             else:
        #                                 if self.type_id.id == 4 or self.contract_period_id in [23, 24]:
        #                                     if date_end <= date_probation:
        #                                         for sea_extend_contract in self.sea_extend_contract:
        #                                             self.env['mail.activity'].sudo().search(
        #                                                 [('id', '=', sea_extend_contract.id)]).write(
        #                                                 {'date_deadline': vals.get('date_end')})
        #                                             print("edit only change date_end ")
        #
        #                                 elif self.type_id.id != 4 and date_end <= date_not_probation:
        #                                     for sea_extend_contract in self.sea_extend_contract:
        #                                         self.env['mail.activity'].sudo().search(
        #                                             [('id', '=', sea_extend_contract.id)]).write(
        #                                             {'date_deadline': vals.get('date_end')})
        #                                         print("only change date_end with type_id != 4")
        #
        #                 # TRƯỜNG HỢP ONLY CHANGE TYPE_ID
        #                 # create on type_id
        #                 elif vals.get('type_id') is not None:
        #                     date_probation = date_probation.date()
        #                     date_not_probation = date_not_probation.date()
        #                     if self.date_end:
        #                         # create
        #                         if not self.sea_extend_contract:
        #                             if ids is not None:
        #                                 for user_id in ids:
        #                                     if vals.get('contract_period_id') in [23, 24] or vals.get(
        #                                             'type_id') == 4 and date_probation >= self.date_end:
        #                                         self.create_mail_activity(self, self.env['res.users'].sudo().search(
        #                                             [('id', '=', user_id)]).id,
        #                                                                   mail_activity_type_probation.activity_type_id.id,
        #                                                                   'hr.contract')
        #                                         print("create, change type_id = 4")
        #                                     elif vals.get('type_id') != 4 and date_not_probation >= self.date_end:
        #                                         self.create_mail_activity(self, self.env['res.users'].sudo().search(
        #                                             [('id', '=', user_id)]).id,
        #                                                                   mail_activity_type_not_probation.activity_type_id.id,
        #                                                                   'hr.contract')
        #                                         print("create change type_id != 4")
        #
        #                         # edit or unlink
        #                         else:
        #                             if vals.get('type_id') == 4:
        #                                 if date_probation >= self.date_end:
        #                                     for sea_extend_contract in self.sea_extend_contract:
        #                                         self.env['mail.activity'].sudo().search(
        #                                             [('id', '=', sea_extend_contract.id)]).write(
        #                                             {'activity_type_id', '=',
        #                                              mail_activity_type_probation.activity_type_id.id})
        #                                 else:
        #                                     # unlink mail_activity => id = sea_extend_contract
        #                                     for sea_extend_contract in self.sea_extend_contract:
        #                                         self.env['mail.activity'].sudo().search(
        #                                             [('id', '=', sea_extend_contract.id)]).unlink()
        #                                     self.sea_extend_contract = None
        #                                     self._change_state(self)

        '''Thay đổi trạng thái(state) => thay đổi luôn các phụ lục liên quan'''
        if check_edit_state:
            self.change_state_addition()
            if self.sea_extend_contract and self.state not in ["pending"]:
                self.cancel_schedule_activity()
        if to_date and self.state in ["pending"]:
            ''' tạo đồng thời gửi mail hoặc thay đổi ngày hết hạn của schedule activity 
            khi trạng thái(state) thay đổi sang [pending] - To Renew của Category là contract'''
            self.create_or_write_mail()
            # # user_id => Job Position
            # # user_id = self.create_user_id_mail_activity(self)
            # # user_id = 8
            # user_ids = self.env['user.mail'].sudo().search([])
            # ids = []
            # for u in user_ids:
            #     ids.append(u.name.id)
            # if self.job_id:
            #     if self.job_id.hr_responsible_id:
            #         user_id = self.job_id.hr_responsible_id.id
            #         if user_id not in ids:
            #             ids.append(user_id)
            #
            # for user_id in ids:
            #     if self.sea_extend_contract:
            #         '''chỉnh ngày'''
            #         for sea_extend_contract in self.sea_extend_contract:
            #             if sea_extend_contract.date_deadline:
            #                 if sea_extend_contract.date_deadline != self.date_end:
            #                     sea_extend_contract.sudo().write(
            #                         {'date_deadline': self.date_end})
            #     else:
            #         '''tạo mới'''
            #         self.create_mail_activity(self, self.env['res.users'].sudo().search(
            #             [('id', '=', user_id)]).id,
            #                                   self.env[
            #                                       'mail.activity.type.id.of.hr.contract'].sudo().search(
            #                                       [('name', '=', 'not_probation')], limit=1).activity_type_id.id,
            #                                   'hr.contract')
        return res

    @api.model
    def create(self, vals):
        # create_mail = False
        if vals.get('state') is None or vals.get('state') == "draft":
            vals.update({'state': 'open'})
            if vals.get('date_end'):
                if datetime.datetime.strptime(vals.get('date_end'),
                                              '%Y-%m-%d').date() <= date.today():
                    vals.update({'state': 'close'})
                # if vals.get('type_id') or vals.get('contract_period_id'):
                #     '''chuyển trạng thái sang To Renew nếu hợp lệ'''
                #     number_of_days = False
                #     if vals.get('contract_period_id'):
                #         contract_period = self.env['hr.contract.period'].sudo().search(
                #             [('id', '=', vals.get('contract_period_id'))])
                #         if contract_period:
                #             if contract_period.remaining_day_to_renew:
                #                 number_of_days = contract_period.remaining_day_to_renew
                #     if not number_of_days and vals.get('type_id'):
                #         contract_type = self.env['hr.contract.type'].sudo().search([('id', '=', vals.get('type_id'))])
                #         if contract_type:
                #             if contract_type.remaining_day_to_renew:
                #                 number_of_days = contract_type.remaining_day_to_renew
                #     if number_of_days:
                #         if datetime.datetime.strptime(vals.get('date_end'),
                #                              '%Y-%m-%d').date() <= date.today() + datetime.timedelta(
                #             days=number_of_days):
                #             vals.update({'state': 'pending'})
                #             create_mail = True
        rec = super(create_mail_activity_hr_contracts, self).create(vals)
        # if create_mail:
        #     print("create_mail: create_or_write_mail")
        #     self.create_or_write_mail()
        return rec

    ''''''
