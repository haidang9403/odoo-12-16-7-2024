from odoo import api, models, fields


class mail_activity_type_id_of_hr_contract(models.Model):
    _name = 'mail.activity.type.id.of.hr.contract'
    _description = "Save mail activity type id for contracts"

    name = fields.Char('Name')
    activity_type_id = fields.Many2one(
        'mail.activity.type', 'Activity', ondelete='restrict')


class inherit_mail_activity(models.Model):
    _inherit = 'mail.activity.type'

    @api.model
    def mail_activity_type_create_action(self):
        not_probation = self.env['mail.activity.type'].sudo().create(
            {'name': "To do for contract", 'delay_from': "previous_activity",
             'delay_count': 45, 'delay_unit': "days", 'icon': "fa-tasks", 'res_model_id': 614})
        self.env['mail.activity.type.id.of.hr.contract'].sudo().create(
            {'name': "not_probation", 'activity_type_id': not_probation.id})

        probation = self.env['mail.activity.type'].sudo().create(
            {'name': "To do for probation contract", 'delay_from': "previous_activity",
             'delay_count': 7, 'delay_unit': "days", 'icon': "fa-tasks", 'res_model_id': 614})
        self.env['mail.activity.type.id.of.hr.contract'].sudo().create(
            {'name': "probation", 'activity_type_id': probation.id})
        print("insert mail.activity.type ok")
