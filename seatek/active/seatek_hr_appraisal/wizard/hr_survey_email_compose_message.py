# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re
import uuid

from werkzeug import urls

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import pycompat

_logger = logging.getLogger(__name__)

emails_split = re.compile(r"[;,\n\r]+")
email_validator = re.compile(r"[^@]+@[^@]+\.[^@]+")


class HRSurveyMailComposeMessage(models.Model):
    _name = 'hr.survey.mail.compose.message'
    _inherit = 'mail.compose.message'
    _description = 'Email composition wizard for HR Survey'

    def default_survey_id(self):
        context = self.env.context
        if context.get('model') == 'hr.survey':
            return context.get('res_id')

    survey_id = fields.Many2one('hr.survey', string='Survey', default=default_survey_id, required=True,ondelete='cascade')
    public = fields.Selection([('public_link', 'Share the public web link to your audience.'),
                               ('email_public_link', 'Send by email the public web link to your audience.'),
                               ('email_private',
                                'Send private invitation to your audience (only one response per recipient and per invitation).')],
                              string='Share options', default='public_link', required=True)
    public_url = fields.Char(compute="_compute_survey_url", string="Public url")
    public_url_html = fields.Char(compute="_compute_survey_url", string="Public HTML web link")
    partner_ids = fields.Many2many('res.partner', 'survey_mail_compose_message_res_partner_rel', 'wizard_id',
                                   'partner_id', string='Existing contacts')
    attachment_ids = fields.Many2many('ir.attachment', 'survey_mail_compose_message_ir_attachments_rel', 'wizard_id',
                                      'attachment_id', string='Attachments')
    multi_email = fields.Text(string='List of emails', help="This list of emails of recipients will not be converted in contacts.\
        Emails must be separated by commas, semicolons or newline.")
    date_deadline = fields.Date(string="Deadline to which the invitation to respond is valid",
                                help="Deadline to which the invitation to respond for this survey is valid. If the field is empty,\
        the invitation is still valid.")

    @api.depends('survey_id')
    def _compute_survey_url(self):
        for wizard in self:
            wizard.public_url = wizard.survey_id.public_url
            wizard.public_url_html = wizard.survey_id.public_url_html

    @api.model
    def default_get(self, fields):
        res = super(HRSurveyMailComposeMessage, self).default_get(fields)
        context = self.env.context
        if context.get('active_model') == 'res.partner' and context.get('active_ids'):
            res.update({'partner_ids': context['active_ids']})
        return res

    @api.onchange('multi_email')
    def onchange_multi_email(self):
        emails = list(set(emails_split.split(self.multi_email or "")))
        emails_checked = []
        error_message = ""
        for email in emails:
            email = email.strip()
            if email:
                if not email_validator.match(email):
                    error_message += "\n'%s'" % email
                else:
                    emails_checked.append(email)
        if error_message:
            raise UserError(_("Incorrect Email Address: %s") % error_message)

        emails_checked.sort()
        self.multi_email = '\n'.join(emails_checked)

    #------------------------------------------------------
    # Wizard validation and send
    #------------------------------------------------------

    @api.multi
    def send_mail_action(self):
        return self.send_mail()

    @api.multi
    def send_mail(self, auto_commit=False):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed """

        SurveyUserInput = self.env['hr.survey.user.input']
        Partner = self.env['res.partner']
        Mail = self.env['mail.mail']
        notif_layout = self.env.context.get('notif_layout', self.env.context.get('custom_layout'))

        def create_response_and_send_mail(wizard, partner_id, email):
            """ Create one mail by recipients and replace __URL__ by link with identification token """
            #set url
            url = wizard.survey_id.public_url

            # post the message
            values = {
                'model': None,
                'res_id': None,
                'subject': wizard.subject,
                'body': wizard.body.replace("__URL__", url),
                'body_html': wizard.body.replace("__URL__", url),
                'parent_id': None,
                'attachment_ids': wizard.attachment_ids and [(6, 0, wizard.attachment_ids.ids)] or None,
                'email_from': wizard.email_from or None,
                'auto_delete': True,
            }
            if partner_id:
                values['recipient_ids'] = [(4, partner_id)]
            else:
                values['email_to'] = email

            # optional support of notif_layout in context
            if notif_layout:
                try:
                    template = self.env.ref(notif_layout, raise_if_not_found=True)
                except ValueError:
                    _logger.warning('QWeb template %s not found when sending survey mails. Sending without layouting.' % notif_layout)
                else:
                    template_ctx = {
                        'message': self.env['mail.message'].sudo().new(dict(body=values['body_html'], record_name=wizard.survey_id.title)),
                        'model_description': self.env['ir.model']._get('hr.survey').display_name,
                        'company': self.env.user.company_id,
                    }
                    body = template.render(template_ctx, engine='ir.qweb', minimal_qcontext=True)
                    values['body_html'] = self.env['mail.thread']._replace_local_links(body)

            Mail.create(values).send()

        for wizard in self:
            # check if __URL__ is in the text
            if wizard.body.find("__URL__") < 0:
                raise UserError(_("The content of the text don't contain '__URL__'. \
                    __URL__ is automaticaly converted into the special url of the survey."))

            context = self.env.context
            if not wizard.multi_email and not wizard.partner_ids and (context.get('default_partner_ids') or context.get('default_multi_email')):
                wizard.multi_email = context.get('default_multi_email')
                wizard.partner_ids = context.get('default_partner_ids')

            # quick check of email list
            emails_list = []
            if wizard.multi_email:
                emails = set(emails_split.split(wizard.multi_email)) - set(wizard.partner_ids.mapped('email'))
                for email in emails:
                    email = email.strip()
                    if email_validator.match(email):
                        emails_list.append(email)

            # remove public anonymous access
            partner_list = []
            for partner in wizard.partner_ids:
                partner_list.append({'id': partner.id, 'email': partner.email})

            if not len(emails_list) and not len(partner_list):
                if wizard.model == 'res.partner' and wizard.res_id:
                    return False
                raise UserError(_("Please enter at least one valid recipient."))

            for email in emails_list:
                partner = Partner.search([('email', '=', email)], limit=1)
                create_response_and_send_mail(wizard, partner.id, email)

            for partner in partner_list:
                create_response_and_send_mail(wizard, partner['id'], partner['email'])

        return {'type': 'ir.actions.act_window_close'}
