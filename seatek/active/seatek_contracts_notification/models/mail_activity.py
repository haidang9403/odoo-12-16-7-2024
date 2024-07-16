import logging

from odoo import api, models, fields, _


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    contract_id = fields.Many2one('hr.contract', 'of hr.contracts')
    #
    # '''đem qua module mới'''
    #
    # @api.multi
    # def action_notify(self):
    #     mail_activity_types = [self.env['mail.activity.type'].sudo().search(
    #         [('name', '=', "To do for contract")], limit=1).id, self.env['mail.activity.type'].sudo().search(
    #         [('name', '=', "To do for probation contract")], limit=1).id]
    #     if self.activity_type_id.id in mail_activity_types:
    #         body_template = self.env.ref('seatek_contracts_notification.message_activity_assigned_vietnamese')
    #
    #         for activity in self:
    #             document_detail = self.env['hr.contract'].sudo().search([('id', '=', activity.res_id)])
    #             model_description = self.env['ir.model']._get(activity.res_model).display_name
    #             body = body_template.render(
    #                 dict(activity=activity, model_description=model_description,
    #                      document_detail=document_detail),
    #                 engine='ir.qweb',
    #                 minimal_qcontext=True
    #             )
    #             self.env['mail.thread'].message_notify(
    #                 partner_ids=activity.user_id.partner_id.ids,
    #                 body=body,
    #                 subject=_('(No-Reply) THÔNG BÁO HĐLĐ SẮP HẾT HẠN: %s') % (
    #                     activity.res_name),
    #                 record_name=activity.res_name,
    #                 document_detail=document_detail,
    #                 model_description=model_description,
    #                 notif_layout='seatek_contracts_notification.mail_notification_light_vietnamese'
    #             )
    #     else:
    #         body_template = self.env.ref('mail.message_activity_assigned')
    #         for activity in self:
    #             model_description = self.env['ir.model']._get(activity.res_model).display_name
    #             body = body_template.render(
    #                 dict(activity=activity, model_description=model_description),
    #                 engine='ir.qweb',
    #                 minimal_qcontext=True
    #             )
    #             self.env['mail.thread'].message_notify(
    #                 partner_ids=activity.user_id.partner_id.ids,
    #                 body=body,
    #                 subject=_('%s: %s assigned to you') % (
    #                     activity.res_name, activity.summary or activity.activity_type_id.name),
    #                 record_name=activity.res_name,
    #                 model_description=model_description,
    #                 notif_layout='mail.mail_notification_light'
    #             )
    #
    # '''by tkkhanh 16/01/2024
    # edit hàm CREATE và hàm WRITE để dừng việc gửi mail nếu
    # self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") not in list database.uuid'''
    #
    # @api.model
    # def create(self, values):
    #     if not self.env.context.get('mail_activity_quick_update', False):
    #         domain = [('key', '=', 'database.uuid')]
    #         if 'activity_type_id' in values:
    #             mail_activity_type = self.env['mail.activity.type'].search(
    #                 [('id', '=', values.get('activity_type_id'))])
    #             if mail_activity_type:
    #                 if mail_activity_type.res_model_id:
    #                     domain = ['|', ('key', '=', 'database.uuid'),
    #                               ('res_model_id', '=', mail_activity_type.res_model_id.id)]
    #         database_uuid = self.env['database.uuid'].sudo().search(domain)
    #         if database_uuid:
    #             test = []
    #             for database in database_uuid:
    #                 test.append(database.value.replace("-", "."))
    #             # =================================================================
    #             if self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") not in test:
    #                 print("Do not send mail, edit by tkkhanh")
    #                 context_dict = dict(self.env.context)
    #                 context_dict['mail_activity_quick_update'] = True
    #                 # Set the updated context back using with_context
    #                 self = self.with_context(**context_dict)
    #                 logging.exception("Do not send mail for CONTRACT: %s", str(values))
    #
    #     return super(MailActivity, self).create(values)
    #
    # @api.multi
    # def write(self, values):
    #     if values.get('user_id') and not self.env.context.get('mail_activity_quick_update', False):
    #         if values['user_id'] != self.env.uid:
    #             domain = [('key', '=', 'database.uuid')]
    #             if self.activity_type_id:
    #                 mail_activity_type = self.env['mail.activity.type'].search([('id', '=', values.get(
    #                     'activity_type_id') if 'activity_type_id' in values else self.activity_type_id.id)])
    #                 if mail_activity_type:
    #                     if mail_activity_type.res_model_id:
    #                         domain = ['|', ('key', '=', 'database.uuid'),
    #                                   ('res_model_id', '=', mail_activity_type.res_model_id.id)]
    #             database_uuid = self.env['database.uuid'].sudo().search(domain)
    #             if database_uuid:
    #                 test = []
    #                 for database in database_uuid:
    #                     test.append(database.value.replace("-", "."))
    #                 # =================================================================
    #                 if self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-",
    #                                                                                                  ".") not in test:
    #                     print("Do not send mail, edit by tkkhanh")
    #                     context_dict = dict(self.env.context)
    #                     context_dict['mail_activity_quick_update'] = True
    #                     # Set the updated context back using with_context
    #                     self = self.with_context(**context_dict)
    #
    #     return super(MailActivity, self).write(values)
    #
    # ''' -- '''
