from odoo import api, models, fields, _
from werkzeug import urls
from odoo.addons.http_routing.models.ir_http import slug


class Summary_Level(models.Model):
    _name = 'hr.survey.summary'
    _description = 'Summary'

    name = fields.Char(string='Criteria', require=True)
    survey_order=fields.Integer('Survey Order')
    is_parent_page = fields.Boolean(string='Is Parent Page', default=False)
    enable_edit_title = fields.Boolean(string='Title editable', default=False)
    comment = fields.Char(string='Comment', require=False)
    score = fields.Float(string='Score', default=0)
    max_score = fields.Integer(string="Scale", default=5)
    percentage = fields.Float(string='Percentage %', default=0)
    enable_edit_percentage=fields.Boolean(string="Percentage editable",default=False)
    is_percent = fields.Boolean(string='Res.Percentage', default=False)
    survey_id = fields.Many2one('hr.survey', string='Survey', index=True, invisible=1, ondelete='cascade')
    hr_survey_id = fields.Many2one('hr.survey', string='Survey', index=True, invisible=1, ondelete='cascade')
    data_type = fields.Selection([('score', 'Score'), ('percentage', 'Percentage')], string='Data Type',
                                 default='score', required=True)
    calculation_method = fields.Selection([('sum', 'Summary'), ('average', 'Average')],
                                          string='Calculation method', default='average', require=True)
    can_input = fields.Boolean(default=True, string='Can Input')
    is_rating=fields.Boolean(default=False,string='Is Rating')

    summary_level = fields.Integer(string='Level')
    fields_sum = fields.Many2many('hr.survey.summary', 'hr_survey_summary_rel_rel', 's_uid', 'f_uid', string='Factors')
    page_id = fields.Many2one('hr.survey.summary', ondelete='cascade')
    # you  can create summary in summary
    summary_id = fields.Many2one('hr.survey.summary', string='Criteria', index=True, invisible=1, ondelete='cascade')
    summary_ids = fields.One2many('hr.survey.summary', 'summary_id', string='Summary', copy=True)
    validation_required = fields.Boolean('Require', default=True)
    page_for_manager=fields.Boolean(string='For Manager',default=False)
    can_delete=fields.Boolean(default=False)
    prefix=fields.Char(string='STT',default='')
    @api.onchange('can_input')
    def _onchange_can_input(self):
        if not self.can_input:
            self.enable_edit_title = False
            self.validation_required = False

    @api.model
    def create(self, vals):
        if vals.get('survey_id'):
            vals.update({'hr_survey_id': vals.get('survey_id')})
        else:
            data = self.env['hr.survey.summary'].search([('id', '=', vals.get('summary_id'))])
            vals.update({'hr_survey_id': data.hr_survey_id.id})
        return super(Summary_Level, self).create(vals)

    @api.onchange('summary_ids')
    def _onchange_summary_ids(self):
        total = 0
        percent_total = 100
        for summary in self.summary_ids:
            if not summary.is_percent:
                total = total + 1
            else:
                percent_total = percent_total - summary.percentage
                if percent_total < 0:
                    percent_total = 0
        if total > 0:
            if self.summary_ids:
                percent = percent_total / total
                for i in self.summary_ids:
                    if not i.is_percent:
                        i.percentage=float(percent)

    @api.multi
    def write(self, values):

        if values.get('can_input') is not None:
            if not values.get('can_input'):
                values.update({'validation_required': False})
        if values.get('fields_sum'):
            field_sum = values['fields_sum'][0][2]
            # delete
            search_record = self.env['hr.survey.summary.field.sum'].sudo().search([('id_parent', '=', self.id)])
            search_record.unlink()
            for i in field_sum:
                self.env['hr.survey.summary.field.sum'].sudo().create({'id_parent': self.id, 'id_child': i})

        rec =super(Summary_Level, self).write(values)
        total = 0
        percent_total = 100
        if self.summary_ids:
            for summary in self.summary_ids:
                if not summary.is_percent:
                    total = total + 1
                else:
                    percent_total = percent_total - summary.percentage
                    if percent_total < 0:
                        percent_total = 0
            if total > 0:
                if self.summary_ids:
                    percent = percent_total / total
                    for i in self.summary_ids:
                        if not i.is_percent:
                            i.percentage=float(percent)
        return rec


class HRSurveyParentFieldSum(models.Model):
    _name = 'hr.survey.summary.field.sum'
    _description = 'HR Survey Parent Field Sum'

    id_parent = fields.Many2one('hr.survey.summary', ondelete='cascade')
    id_child = fields.Many2one('hr.survey.summary', ondelete='cascade')


class HR_Survey(models.Model):
    _name = 'hr.survey'
    _description = 'Survey'

    name = fields.Char(string='Survey', require=True)
    description = fields.Char(string='Description')
    number_of_criteria = fields.Integer(string='Criteria', default=0)

    page_summary_ids = fields.One2many('hr.survey.summary', 'survey_id', string='Page', copy=True)
    mark_as_todo = fields.Boolean(string='Mark as To Do', default=False)
    state_done = fields.Boolean(string="Done", default=False)

    public_url = fields.Char("Public link", compute="_compute_survey_url")
    public_url_html = fields.Char("Public link (html version)", compute="_compute_survey_url")
    print_url = fields.Char("Print link", compute="_compute_survey_url")
    result_url = fields.Char("Results link", compute="_compute_survey_url")

    @api.multi
    def write(self, values):
        rec =super(HR_Survey, self).write(values)
        total = 0
        percent_total = 100
        if self.page_summary_ids:
            for summary in self.page_summary_ids:
                if not summary.is_percent:
                    total = total + 1
                else:
                    percent_total = percent_total - summary.percentage
                    if percent_total < 0:
                        percent_total = 0
            if total > 0:
                if self.page_summary_ids:
                    percent = percent_total / total
                    for i in self.page_summary_ids:
                        if not i.is_percent:
                            i.percentage = percent
        return rec

    def _compute_survey_url(self):
        """ Computes a public URL for the survey """
        base_url = '/' if self.env.context.get('relative_url') else \
            self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for survey in self:
            survey.public_url = urls.url_join(base_url, "hr_survey/start/%s" % (slug(survey)))
            survey.print_url = urls.url_join(base_url, "hr_survey/print/%s" % (slug(survey)))
            survey.result_url = urls.url_join(base_url, "hr_survey/results/%s" % (slug(survey)))
            survey.public_url_html = '<a href="%s">%s</a>' % (survey.public_url, _("Click here to start survey"))

    @api.model
    def create(self, values):
        res = super(HR_Survey, self).create(values)
        res.mark_as_todo = True
        datas = self.env['hr.survey.summary'].search([('survey_id', '=', res.id)])
        level = -1
        for data in datas:
            self.set_page_id(data.id, data.id, level)

        return res

    def set_page_id(self, summary_id, page_id, level):
        level = level + 1
        datas = self.env['hr.survey.summary'].search([('summary_id', '=', summary_id)])
        for data in datas:
            data.page_id = page_id
            data.summary_level = level
            self.set_page_id(data.id, page_id, level)

    '''Thay đổi sang trạng thái khóa dữ liệu
        Người dùng sẽ không thay đổi được dữ liệu'''
    def action_confirm_next(self,survey_summary,level):
        surveys=self.env['hr.survey.summary'].sudo().search([('hr_survey_id','=',self.id),('summary_id','=',survey_summary.id)])
        for survey in surveys:
            survey.summary_level = level
            self.action_confirm_next(survey, level + 1)

    @api.multi
    @api.model
    def action_confirm(self):
        self.mark_as_todo = False
        self.state_done = True
        parents = self.env['hr.survey.summary'].sudo().search( [('hr_survey_id', '=', self.id), ('is_parent_page', '=', True)])
        for parent in parents:
            level=1
            parent.summary_level=level
            pages=self.env['hr.survey.summary'].sudo().search([('hr_survey_id','=',self.id),('summary_id','=',parent.id)])
            for page in pages:
                page.summary_level=level+1
                self.action_confirm_next(page,level)
        self.env['hr.survey.summary'].create({'name':'TỔNG HỢP',
                                              'is_parent_page': True,
                                              'enable_edit_title': False,
                                              'survey_id': self.id,
                                              'hr_survey_id':self.id,
                                              'data_type':'score',
                                              'calculation_method':'average',
                                              'can_input':False,
                                              'is_rating':True,
                                              'summary_level':0})
        return True

    '''Tính tỉ trọng các phần tử con của 1 page'''
    @api.onchange('page_summary_ids')
    def _onchange_parent_level(self):
        if self.page_summary_ids:
            self.hr_survey_id = self.id
            self.number_of_criteria = len(self.page_summary_ids)
            total = 0
            percent_total = 100
            for summary in self.page_summary_ids:
                summary.is_parent_page = True
                if not summary.is_percent:
                    total = total + 1
                else:
                    percent_total = percent_total - summary.percentage
                    if percent_total < 0:
                        percent_total = 0
            if total > 0:
                if self.page_summary_ids:
                    percent = percent_total / total
                    for i in self.page_summary_ids:
                        if not i.is_percent:
                            i.percentage = int(percent)

    @api.model
    def next_page(self, user_input, page_id, go_back=False):
        return True
        survey = user_input.survey_id
        summary = list(enumerate(survey.page_summary_ids))

        ids = []
        if summary:
            for i in range(0, len(summary)):
                search_summary = self.env['hr.survey.summary'].sudo().search([('summary_id', '=', summary[i][1].id)])
                for data in search_summary:
                    if data:
                        ids.append(data.id)

        search = self.env['hr.survey.summary'].sudo().browse(ids)
        summaries = list(enumerate(search))

        # First page
        if page_id == 0:
            return summaries[0][1], 0, len(summaries) == 1, len(summaries)

        current_page_index = summaries.index(next(p for p in summaries if p[1].id == page_id))

        # All the pages have been displayed
        if current_page_index == len(summaries) - 1 and not go_back:
            return None, -1, False, len(summaries)

        # Let's get back, baby!
        elif go_back:
            return summaries[current_page_index - 1][1], current_page_index - 1, False, len(summaries)
        else:
            # This will show the last page
            if current_page_index == len(summaries) - 2:
                return summaries[current_page_index + 1][1], current_page_index + 1, True, len(summaries)
            # This will show a regular page
            else:
                return summaries[current_page_index + 1][1], current_page_index + 1, False, len(summaries)

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        return True
        default = dict(default or {})
        if 'state_done' not in default:
            default['state_done'] = False
        if 'name' not in default:
            default['name'] = self.name + ' (copy)'
        return super(HR_Survey, self).copy(default)
