# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class Survey(http.Controller):

    def _check_bad_cases(self, survey):
        if not survey.sudo().exists():
            return werkzeug.utils.redirect("/hr_survey/")

        if request.env.user._is_public():
            return request.render("seatek_hr_appraisal.auth_required", {'survey': survey})

        # # In case of non open surveys
        # if survey.stage_id.closed:
        #     return request.render("survey.notopen")
        #
        # # If there is no pages
        # if not survey.page_ids:
        #     return request.render("survey.nopages", {'survey': survey})

        return None

    # def _check_deadline(self, user_input):
    #     '''Prevent opening of the survey if the deadline has turned out
    #
    #     ! This will NOT disallow access to users who have already partially filled the survey !'''
    #     deadline = user_input.deadline
    #     if deadline:
    #         dt_deadline = fields.Datetime.from_string(deadline)
    #         dt_now = datetime.now()
    #         if dt_now > dt_deadline:  # survey is not open anymore
    #             return request.render("survey.notopen")
    #     return None

    ## ROUTES HANDLERS ##

    def get_question(self, page_id, user_input):
        search = request.env['hr.survey.user.input.line'].sudo().search(
            [('parent_page_id', '=', page_id), ('user_input_id', '=', user_input.id), ('summary_level', '!=', None)])
        return search

    @http.route(['/hr_survey/change/<model("hr.survey"):survey>'],
                type='http', auth='public', website=True)
    def change_survey(self, survey, **post):
        UserInput = request.env['hr.survey.user.input']
        Survey = request.env['hr.survey']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(survey)
        if errpage:
            return errpage

        user_input = UserInput.sudo().search([('user_id', '=', request.env.user.id), ('survey_id', '=', survey.id)],
                                             limit=1)

        # # Do not open expired survey
        # errpage = self._check_deadline(user_input)
        # if errpage:
        #     return errpage

        # Select the right page
        if user_input.state == 'new':  # Intro page
            data = {'survey': survey, 'summary': None}
            return request.render('seatek_hr_appraisal.survey_init', data)
        else:
            page, page_nr, last, total_page = Survey.next_page(user_input, 0, go_back=False)
            questions = self.get_question(page.id, user_input)
            data = {'survey': survey, 'page': page, 'page_nr': page_nr, 'questions': questions, 'total_page': total_page}
            if last:
                data.update({'last': True})
            return request.render('seatek_hr_appraisal.survey', data)

    # Survey start
    @http.route(['/hr_survey/start/<model("hr.survey"):survey>'],
                type='http', auth='public', website=True)
    def start_survey(self, survey, **post):
        UserInput = request.env['hr.survey.user.input']

        # Controls if the survey can be displayed
        errpage = self._check_bad_cases(survey)
        if errpage:
            return errpage

        user_input = UserInput.sudo().search([('user_id', '=', request.env.user.id), ('survey_id', '=', survey.id)],
                                             limit=1)

        if user_input.state == 'new':
            data = {'survey': survey, 'summary': None}
            return request.render('seatek_hr_appraisal.survey_init', data)
        else:
            return request.redirect('/hr_survey/fill/%s' % survey.id)

    @http.route(['/hr_survey/fill/<model("hr.survey"):survey>/',
                 '/hr_survey/fill/<model("hr.survey"):survey>/<string:prev>'],
                type='http', auth='public', website=True)
    def fill_survey(self, survey, prev=None, **post):
        Survey = request.env['hr.survey']
        UserInput = request.env['hr.survey.user.input']

        errpage = self._check_bad_cases(survey)
        if errpage:
            return errpage

        user_input = UserInput.sudo().search([('user_id', '=', request.env.user.id), ('survey_id', '=', survey.id)],
                                             limit=1)
        if not user_input:  # Invalid token
            return request.render("seatek_hr_appraisal.403", {'survey': survey})

        # Do not display expired survey (even if some pages have already been
        # displayed -- There's a time for everything!)
        # errpage = self._check_deadline(user_input)
        # if errpage:
        #     return errpage

        # Select the right page
        if user_input.state == 'new':  # First page
            page, page_nr, last, total_page = Survey.next_page(user_input, 0, go_back=False)
            questions = self.get_question(page.id, user_input)
            data = {'survey': survey, 'page': page, 'page_nr': page_nr, 'questions': questions, 'total_page': total_page}
            if last:
                data.update({'last': True})
            return request.render('seatek_hr_appraisal.survey', data)

        elif user_input.state == 'done':  # Display success message
            return request.render('seatek_hr_appraisal.s_finished', {'survey': survey,
                                                                     'user_input': user_input})

        elif user_input.state == 'skip':
            flag = (True if prev and prev == 'prev' else False)
            page, page_nr, last, total_page = Survey.next_page(user_input, user_input.last_displayed_page_id.id, go_back=flag)

            if not page:
                page, page_nr, last, total_page = Survey.next_page(user_input, user_input.last_displayed_page_id.id, go_back=True)
            questions = self.get_question(page.id, user_input)
            data = {'survey': survey, 'page': page, 'page_nr': page_nr, 'questions': questions, 'total_page': total_page}
            if last:
                data.update({'last': True})
            return request.render('seatek_hr_appraisal.survey', data)
        else:
            return request.render("seatek_hr_appraisal.403", {'survey': survey})

    # AJAX prefilling of a survey
    @http.route(['/hr_survey/prefill/<model("hr.survey"):survey>',
                 '/hr_survey/prefill/<model("hr.survey"):survey>/<model("hr.survey.summary"):page>'],
                type='http', auth='public', website=True)
    def prefill(self, survey, page=None, **post):
        UserInput = request.env['hr.survey.user.input']
        UserInputLine = request.env['hr.survey.user.input.line']

        ret = {}

        # Fetch previous answers
        if page:
            user_input = UserInput.sudo().search([('user_id', '=', request.env.user.id), ('survey_id', '=', survey.id)],
                                                 limit=1)
            previous_answers = self.get_question(page.id, user_input)
        else:
            previous_answers = UserInputLine.sudo().search([('survey_id', '=', survey.id)])

        # Return non empty answers in a JSON compatible format
        for answer in previous_answers:
            if not answer.skipped:
                answer_tag = '%s_%s' % (answer.page_id.id, answer.question_id.id)
                answer_value = None
                if answer.data_type == 'score':
                    answer_value = answer.value
                elif answer.data_type == 'percentage':
                    answer_value = answer.value

                if answer_value:
                    ret.setdefault(answer_tag, []).append(answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s marked as non skipped" % answer_tag)

            if not answer.skipped:
                answer_tag = '%s_%s' % (answer.page_id.id, answer.question_id.id)
                answer_value = None
                if answer.enable_edit_title:
                    answer_tag = "%s_%s" % (answer_tag, 'question')
                    answer_value = answer.question_name
                if answer_value:
                    ret.setdefault(answer_tag, []).append(answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s marked as non skipped" % answer_tag)

            if not answer.skipped:
                answer_tag = '%s_%s' % (answer.page_id.id, answer.question_id.id)
                answer_value = None
                if answer.can_input:
                    answer_tag = "%s_%s" % (answer_tag, 'comment')
                    answer_value = answer.user_comment
                if answer_value:
                    ret.setdefault(answer_tag, []).append(answer_value)
                else:
                    _logger.warning(
                        "[survey] No answer has been found for question %s marked as non skipped" % answer_tag)
        return json.dumps(ret, default=str)

    # AJAX submission of a page
    @http.route(['/hr_survey/submit/<model("hr.survey"):survey>'], type='http', methods=['POST'], auth='public',
                website=True)
    def submit(self, survey, **post):
        _logger.debug('Incoming data: %s', post)
        page_id = int(post['page_id'])

        user_input = request.env['hr.survey.user.input'].sudo().search([('user_id', '=', request.env.user.id), ('survey_id', '=', survey.id)], limit=1)
        questions_temp = self.get_question(page_id, user_input)
        ids = []
        for i in questions_temp:
            if i.can_input:
                ids.append(i.id)
        questions = request.env['hr.survey.user.input.line'].browse(ids)

        # Answer validation
        errors = {}
        for question in questions:
            answer_tag = '%s_%s' % (question.page_id.id, question.question_id.id)
            errors.update(question.validate_question(post, answer_tag))

        ret = {}
        if len(errors):
            # Return errors messages to webpage
            ret['errors'] = errors
        else:
            # Store answers into database
            try:
                user_input = request.env['hr.survey.user.input'].sudo().search(
                    [('survey_id', '=', survey.id), ('user_id', '=', request.env.user.id)], limit=1)
            except KeyError:  # Invalid token
                return request.render("seatek_hr_appraisal.403", {'survey': survey})

            user_id = request.env.user.id

            for question in questions:
                answer_tag = "%s_%s" % (question.page_id.id, question.question_id.id)
                request.env['hr.survey.user.input.line'].sudo(user=user_id).save_lines(user_input.id, question, post,
                                                                                       answer_tag)

            go_back = post['button_submit'] == 'previous'
            next_page, _, last, total_page = request.env['hr.survey'].next_page(user_input, page_id, go_back=go_back)
            vals = {'last_displayed_page_id': page_id, 'total_page': total_page}
            if next_page is None and not go_back:
                vals.update({'state': 'done'})
            else:
                vals.update({'state': 'skip'})
            user_input.sudo(user=user_id).write(vals)
            ret['redirect'] = '/hr_survey/fill/%s' % survey.id
            if go_back:
                ret['redirect'] += '/prev'
        return json.dumps(ret)

