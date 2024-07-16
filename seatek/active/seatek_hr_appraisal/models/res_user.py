# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models, modules



# class MailActivity(models.Model):
#     _inherit = 'mail.activity'
#
#     @api.multi
#     def action_notify(self):
#         mail_activity_types = [self.env['mail.activity.type'].sudo().search(
#             [('name', '=', "To do for contract")], limit=1).id, self.env['mail.activity.type'].sudo().search(
#             [('name', '=', "To do for probation contract")], limit=1).id]
#
#         mail_activity_types_appraisal = self.env['mail.activity.type'].sudo().search(
#             [('category', '=', "appraisal")], limit=1)
#         mail_activity_types_appraisal_colleague = self.env['mail.activity.type'].sudo().search(
#             [('category', '=', "appraisal_colleague")], limit=1)
#         mail_activity_types_sign = self.env['mail.activity.type'].sudo().search(
#             [('category', '=', 'sign_document')], limit=1)
#         if self.activity_type_id.id in mail_activity_types:
#             body_template = self.env.ref('seatek_contracts_notification.message_activity_assigned_vietnamese')
#             for activity in self:
#                 document_detail = self.env['hr.contract'].sudo().search([('id', '=', activity.res_id)])
#                 model_description = self.env['ir.model']._get(activity.res_model).display_name
#                 body = body_template.render(
#                     dict(activity=activity, model_description=model_description,
#                          document_detail=document_detail),
#                     engine='ir.qweb',
#                     minimal_qcontext=True
#                 )
#                 self.env['mail.thread'].message_notify(
#                     partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
#                     body=body,
#                     subject=_('(No-Reply) THÔNG BÁO HĐLĐ SẮP HẾT HẠN: %s') % (
#                         activity.res_name),
#                     record_name=activity.res_name,
#                     document_detail=document_detail,
#                     model_description=model_description,
#                     notif_layout='seatek_contracts_notification.mail_notification_light_vietnamese'
#                 )
#
#         elif self.activity_type_id.id==mail_activity_types_appraisal.id:
#             body_template = self.env.ref('seatek_hr_appraisal.message_activity_assigned_appraisal_vietnamese')
#
#             for activity in self:
#                 action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_hr_appraisal',
#                                                                          'action_assigned_appraisal_user_action')
#                 action = action_id['id']
#                 document_detail = self.env['hr.survey.user.input'].sudo().search([('id', '=', activity.res_id)])
#                 model_description = self.env['ir.model']._get(activity.res_model).display_name
#
#                 body = body_template.render(
#                     dict(activity=activity, model_description=model_description,
#                          document_detail=document_detail, action=action),
#                     engine='ir.qweb',
#                     minimal_qcontext=True
#                 )
#                 self.env['mail.thread'].message_notify(
#                     partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
#                     body=body,
#                     subject=_('(No-Reply) THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ: %s') % (
#                         activity.res_name),
#                     record_name=activity.res_name,
#                     model_description=model_description,
#                     document_detail=document_detail,
#                     action=action,
#                     notif_layout='seatek_sign.mail_appraisal_light_vietnamese'
#                 )
#         elif self.activity_type_id.id==mail_activity_types_appraisal_colleague.id:
#             body_template = self.env.ref('seatek_hr_appraisal.message_activity_assigned_appraisal_colleague_vietnamese')
#
#             for activity in self:
#
#                 action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_hr_appraisal',
#                                                                          'action_assigned_appraisal_user_action')
#                 action = action_id['id']
#                 document_detail = self.env['hr.survey.user.input'].sudo().search([('id', '=', activity.res_id)])
#                 model_description = self.env['ir.model']._get(activity.res_model).display_name
#
#                 body = body_template.render(
#                     dict(activity=activity, model_description=model_description,
#                          document_detail=document_detail, action=action),
#                     engine='ir.qweb',
#                     minimal_qcontext=True
#                 )
#                 self.env['mail.thread'].message_notify(
#                     partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
#                     body=body,
#                     subject=_('(No-Reply) THÔNG BÁO BÀI ĐÁNH GIÁ NHÂN SỰ: %s') % (
#                         activity.res_name),
#                     record_name=activity.res_name,
#                     model_description=model_description,
#                     document_detail=document_detail,
#                     action=action,
#                     notif_layout='seatek_sign.mail_appraisal_light_vietnamese'
#                 )
#         elif self.activity_type_id.id==mail_activity_types_sign.id:
#             body_template = self.env.ref('seatek_sign.message_activity_assigned_sign_document_vietnamese')
#             for activity in self:
#                 action_id = self.env['ir.actions.act_window'].for_xml_id('seatek_sign', 'seatek_signatures_action')
#                 action = action_id['id']
#                 document_detail = self.env['sea.sign.document'].sudo().search([('id', '=', activity.res_id)])
#                 model_description = self.env['ir.model']._get(activity.res_model).display_name
#                 body = body_template.render(
#                     dict(activity=activity, model_description=model_description,
#                          document_detail=document_detail, action=action),
#                     engine='ir.qweb',
#                     minimal_qcontext=True
#                 )
#                 self.env['mail.thread'].message_notify(
#                     partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
#                     body=body,
#                     subject=_('%s - %s') % (
#                         document_detail.document_detail.name, activity.res_name),
#                     record_name=activity.res_name,
#                     model_description=model_description,
#                     document_detail=document_detail,
#                     action=action,
#                     notif_layout='seatek_sign.mail_appraisal_light_vietnamese'
#                 )
#
#         else:
#             body_template = self.env.ref('mail.message_activity_assigned')
#             for activity in self:
#                 model_description = self.env['ir.model']._get(activity.res_model).display_name
#                 body = body_template.render(
#                     dict(activity=activity, model_description=model_description),
#                     engine='ir.qweb',
#                     minimal_qcontext=True
#                 )
#                 self.env['mail.thread'].message_notify(
#                     partner_ids=activity.user_id.sudo().partner_id.sudo().ids,
#                     body=body,
#                     subject=_('%s: %s assigned to you') % (
#                         activity.res_name, activity.summary or activity.activity_type_id.name),
#                     record_name=activity.res_name,
#                     model_description=model_description,
#                     notif_layout='mail.mail_notification_light'
#                 )


class Users(models.Model):
    """ Update of res.users class
        - add a preference about sending emails about notifications
        - make a new user follow itself
        - add a welcome message
        - add suggestion preference
        - if adding groups to a user, check mail.channels linked to this user
          group, and the user. This is done by overriding the write method.
    """
    _inherit = 'res.users'

    @api.model
    def systray_get_activities(self):
        mail_activity_types = self.env['mail.activity.type.id.of.hr.contract'].sudo().search([])
        if self.activity_type_id.id in [mail_activity_type.activity_type_id.id for mail_activity_type in mail_activity_types]:
            query = """SELECT m.id, count(*), act.res_model as model,
                                   CASE
                                       WHEN %(today)s::date - act.date_deadline::date = 0 Then 'today'
                                       WHEN %(today)s::date - act.date_deadline::date > 0 Then 'overdue'
                                       WHEN %(today)s::date - act.date_deadline::date < 0 Then 'planned'
                                   END AS states
                               FROM mail_activity AS act
                               INNER JOIN hr_contract s ON act.res_id = s.id 
                               INNER JOIN ir_model AS m ON act.res_model_id = m.id
                               WHERE user_id = %(user_id)s and s.company_id = %(company_id)s	
                               GROUP BY m.id, states, act.res_model;
                               """
        else:
            query = """SELECT m.id, count(*), act.res_model as model,
                                    CASE
                                        WHEN %(today)s::date - act.date_deadline::date = 0 Then 'today'
                                        WHEN %(today)s::date - act.date_deadline::date > 0 Then 'overdue'
                                        WHEN %(today)s::date - act.date_deadline::date < 0 Then 'planned'
                                    END AS states
                                FROM mail_activity AS act
                                JOIN ir_model AS m ON act.res_model_id = m.id
                                WHERE user_id = %(user_id)s
                                GROUP BY m.id, states, act.res_model;
                                """

        self.env.cr.execute(query, {
            'today': fields.Date.context_today(self),
            'user_id': self.env.uid,
            'company_id': self.env.user.company_id.id
        })
        activity_data = self.env.cr.dictfetchall()
        # print(activity_data)
        model_ids = [a['id'] for a in activity_data]
        model_names = {n[0]: n[1] for n in self.env['ir.model'].browse(model_ids).name_get()}

        user_activities = {}
        for activity in activity_data:
            if not user_activities.get(activity['model']):
                if activity['model'] == "hr.survey.user.input":
                    continue
                elif activity['model'] == 'sea.sign.document':
                    continue
                else:
                    user_activities[activity['model']] = {
                        'name': model_names[activity['id']],
                        'model': activity['model'],
                        'type': 'activity',
                        'icon': modules.module.get_module_icon(self.env[activity['model']]._original_module),
                        'total_count': 0, 'today_count': 0, 'overdue_count': 0, 'planned_count': 0,
                    }
                user_activities[activity['model']]['%s_count' % activity['states']] += activity['count']
                if activity['states'] in ('today', 'overdue'):
                    user_activities[activity['model']]['total_count'] += activity['count']

        return list(user_activities.values())
