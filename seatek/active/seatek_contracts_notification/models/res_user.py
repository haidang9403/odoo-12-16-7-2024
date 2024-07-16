# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, exceptions, fields, models, modules


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
        mail_activity_types = self.env[
            'mail.activity.type.id.of.hr.contract'].sudo().search([])
        if self.activity_type_id.id in [mail_activity_type.activity_type_id.id for mail_activity_type in
                                        mail_activity_types]:
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
