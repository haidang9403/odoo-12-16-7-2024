import logging
import uuid

from odoo import api, models, _


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    '''TKK 12/03/2024'''

    @api.multi
    def check_sent_mail(self, domain=False):
        # external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        # session_info = request.env['ir.http'].session_info()
        self.env.cr.execute("SELECT current_database();")
        db_name = self.env.cr.dictfetchall()[0]['current_database']
        ip_mac = (''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                           for ele in range(0, 8 * 6, 8)][::-1])).lower()
        # logging.info("BY TKK Public IP Address: %s", str(external_ip))
        # logging.info("BY TKK db_name: %s", str(session_info['db']))
        logging.info("BY TKK db_name: %s", str(db_name))
        logging.info("BY TKK IP MAC: %s", str(ip_mac))
        if not domain:
            domain = [('key', '=', 'database.uuid')]
        database_uuid = self.env['database.uuid'].sudo().search(domain).filtered(
            lambda l: l.ip_mac and l.db_name == db_name)
        if database_uuid:
            test = []
            for database in database_uuid:
                if database.ip_mac.lower().replace(':', '').replace('-', '').replace('.', '') == ip_mac:
                    test.append(database.value.replace("-", "."))
            # =================================================================
            if self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") in test:
                return False
        return True

    @api.multi
    def action_notify(self):
        # print("action_notify")
        mail_activity_types = [self.env['mail.activity.type'].sudo().search(
            [('name', '=', "To do for contract")], limit=1).id, self.env['mail.activity.type'].sudo().search(
            [('name', '=', "To do for probation contract")], limit=1).id]

        mail_activity_types_appraisal = self.env['mail.activity.type'].sudo().search(
            [('category', '=', "appraisal")], limit=1)
        mail_activity_types_appraisal_colleague = self.env['mail.activity.type'].sudo().search(
            [('category', '=', "appraisal_colleague")], limit=1)
        mail_activity_types_sign = self.env['mail.activity.type'].sudo().search(
            [('category', '=', 'sea_sign_document')], limit=1)
        if self.activity_type_id.id in mail_activity_types:
            # print("MAIL THÔNG BÁO HĐLĐ SẮP HẾT HẠN")
            body_template = self.env.ref('seatek_contracts_notification.message_activity_assigned_vietnamese')
            for activity in self:
                document_detail = self.env['hr.contract'].sudo().search([('id', '=', activity.res_id)])
                model_description = self.env['ir.model']._get(activity.res_model).display_name
                body = body_template.render(
                    dict(activity=activity, model_description=model_description,
                         document_detail=document_detail),
                    engine='ir.qweb',
                    minimal_qcontext=True
                )
                self.env['mail.thread'].message_notify(
                    partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
                    body=body,
                    subject=_('[No-Reply] THÔNG BÁO HĐLĐ SẮP HẾT HẠN: %s') % (
                        activity.res_name),
                    record_name=activity.res_name,
                    document_detail=document_detail,
                    model_description=model_description,
                    notif_layout='seatek_contracts_notification.mail_notification_light_vietnamese'
                )

        elif self.activity_type_id.id == mail_activity_types_appraisal.id:
            # print("MAIL THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ")
            body_template = self.env.ref('seatek_hr_appraisal.message_activity_assigned_appraisal_vietnamese')

            for activity in self:
                action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_hr_appraisal',
                                                                         'action_assigned_appraisal_user_action')
                action = action_id['id']
                document_detail = self.env['hr.survey.user.input'].sudo().search([('id', '=', activity.res_id)])
                model_description = self.env['ir.model']._get(activity.res_model).display_name

                body = body_template.render(
                    dict(activity=activity, model_description=model_description,
                         document_detail=document_detail, action=action),
                    engine='ir.qweb',
                    minimal_qcontext=True
                )
                self.env['mail.thread'].message_notify(
                    partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
                    body=body,
                    subject=_('(No-Reply) THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ: %s') % (
                        activity.res_name),
                    record_name=activity.res_name,
                    model_description=model_description,
                    document_detail=document_detail,
                    action=action,
                    notif_layout='seatek_hr_appraisal.mail_appraisal_light_vietnamese'
                )
        elif self.activity_type_id.id == mail_activity_types_appraisal_colleague.id:
            # print("MAIL THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ 1")
            body_template = self.env.ref('seatek_hr_appraisal.message_activity_assigned_appraisal_colleague_vietnamese')

            for activity in self:
                action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_hr_appraisal',
                                                                         'action_assigned_appraisal_user_action')
                action = action_id['id']
                document_detail = self.env['hr.survey.user.input'].sudo().search([('id', '=', activity.res_id)])
                model_description = self.env['ir.model']._get(activity.res_model).display_name

                body = body_template.render(
                    dict(activity=activity, model_description=model_description,
                         document_detail=document_detail, action=action),
                    engine='ir.qweb',
                    minimal_qcontext=True
                )
                self.env['mail.thread'].message_notify(
                    partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
                    body=body,
                    subject=_('(No-Reply) THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ: %s') % (
                        activity.res_name),
                    record_name=activity.res_name,
                    model_description=model_description,
                    document_detail=document_detail,
                    action=action,
                    notif_layout='seatek_hr_appraisal.mail_appraisal_light_vietnamese'
                )
        elif self.activity_type_id.id == mail_activity_types_sign.id:
            # print("MAIL THÔNG BÁO TRÌNH KÝ")
            body_template = self.env.ref('seatek_sign.message_activity_assigned_sign_document_vietnamese')
            for activity in self:
                action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_sign', 'seatek_signatures_action')
                action = action_id['id']
                document_detail = self.env['sea.sign.document'].sudo().search([('id', '=', activity.res_id)])
                model_description = self.env['ir.model']._get(activity.res_model).display_name
                body = body_template.render(
                    dict(activity=activity, model_description=model_description,
                         document_detail=document_detail, action=action),
                    engine='ir.qweb',
                    minimal_qcontext=True
                )
                self.env['mail.thread'].message_notify(
                    partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
                    body=body,
                    subject=_('%s - %s') % (
                        document_detail.document_detail.name, activity.res_name),
                    record_name=activity.res_name,
                    model_description=model_description,
                    document_detail=document_detail,
                    action=action,
                    notif_layout='seatek_hr_appraisal.mail_appraisal_light_vietnamese'
                )

        else:
            # print("MAIL HỆ THỐNG")
            body_template = self.env.ref('mail.message_activity_assigned')
            for activity in self:
                model_description = self.env['ir.model']._get(activity.res_model).display_name
                body = body_template.render(
                    dict(activity=activity, model_description=model_description),
                    engine='ir.qweb',
                    minimal_qcontext=True
                )
                self.env['mail.thread'].message_notify(
                    partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
                    body=body,
                    subject=_('%s: %s assigned to you') % (
                        activity.res_name, activity.summary or activity.activity_type_id.name),
                    record_name=activity.res_name,
                    model_description=model_description,
                    notif_layout='mail.mail_notification_light'
                )
        # return super(MailActivitySeatekSign, self).action_notify()

    '''by tkkhanh 16/01/2024
    edit hàm CREATE và hàm WRITE để dừng việc gửi mail nếu
    self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") not in list database.uuid'''

    @api.model
    def create(self, values):
        if not self.env.context.get('mail_activity_quick_update', False):
            domain = False
            if 'activity_type_id' in values:
                mail_activity_type = self.env['mail.activity.type'].search(
                    [('id', '=', values.get('activity_type_id'))])
                if mail_activity_type:
                    if mail_activity_type.res_model_id:
                        domain = ['|', ('key', '=', 'database.uuid'),
                                  ('res_model_id', '=', mail_activity_type.res_model_id.id)]
            if self.check_sent_mail(domain):
                # print("Do not send mail, edit by tkkhanh")
                context_dict = dict(self.env.context)
                context_dict['mail_activity_quick_update'] = True
                # Set the updated context back using with_context
                self = self.with_context(**context_dict)
                logging.info("BY TKK Do not send mail for seatek_mail_notification")
        return super(MailActivity, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('user_id') and not self.env.context.get('mail_activity_quick_update', False):
            domain = False
            if values['user_id'] != self.env.uid:
                if self.activity_type_id:
                    mail_activity_type = self.env['mail.activity.type'].search([('id', '=', values.get(
                        'activity_type_id') if 'activity_type_id' in values else self.activity_type_id.id)])
                    if mail_activity_type:
                        if mail_activity_type.res_model_id:
                            domain = ['|', ('key', '=', 'database.uuid'),
                                      ('res_model_id', '=', mail_activity_type.res_model_id.id)]
            if self.check_sent_mail(domain):
                # print("Do not send mail, edit by tkkhanh")
                context_dict = dict(self.env.context)
                context_dict['mail_activity_quick_update'] = True
                # Set the updated context back using with_context
                self = self.with_context(**context_dict)
                logging.info("BY TKK Do not send mail for seatek_mail_notification")

        return super(MailActivity, self).write(values)

    ''' -- '''
