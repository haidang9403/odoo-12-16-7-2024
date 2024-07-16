from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DatabaseUuid(models.Model):
    _name = 'database.uuid'

    key = fields.Char('Key')
    value = fields.Char('Value')
    res_model_id = fields.Many2one(
        'ir.model', 'Model', index=True,
        domain=['&', ('is_mail_thread', '=', True), ('transient', '=', False)],
        help='Specify a model if the activity should be specific to a model'
             ' and not available when managing activities for other models.')
    ip_mac = fields.Char("IP MAC")
    db_name = fields.Char("Database_name")

    @api.constrains('key', 'res_model_id')
    def check_key_res_model_id(self):
        if self.env['database.uuid'].sudo().search([('key', '=', self.key), ('id', '!=', self.id)]):
            raise ValidationError(_('Key=database.uuid is already exist!'))
        elif self.res_model_id:
            if self.env['database.uuid'].sudo().search(
                    [('res_model_id', '=', self.res_model_id.id), ('id', '!=', self.id)]):
                raise ValidationError(_('res_model_id is already exist!'))

#
# class IrCron(models.Model):
#     _inherit = 'ir.cron'
#
#     @api.model
#     def switch_ir_cron(self):
#         print("test database => Switch off active")
#         database_uuid = self.env['database.uuid'].sudo().search([('key', '=', 'database.uuid')])
#         ir_actions_server_id = self.env['ir.actions.server'].sudo().search(
#             [('model_name', '=', 'hr.contract'), ('code', '=', 'model.mail_activity_create()')])
#         if database_uuid:
#             test = []
#             for database in database_uuid:
#                 test.append(database.value.replace("-", "."))
#             # =================================================================
#             if self.env['ir.cron'].sudo().search([('ir_actions_server_id', '=', ir_actions_server_id.id)]).active in [
#                 False]:
#                 if self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") in test:
#                     self.env['ir.cron'].sudo().search(
#                         [('ir_actions_server_id', '=', ir_actions_server_id.id), ('active', '=', False)]).write(
#                         {'active': True})
#                     print("Switch True ok")
#
#             elif self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value.replace("-", ".") not in test:
#                 self.env['ir.cron'].sudo().search([('ir_actions_server_id', '=', ir_actions_server_id.id)]).write(
#                     {'active': False})
#                 print("Switch False ok")
#
#         elif self.env['ir.cron'].sudo().search([('ir_actions_server_id', '=', ir_actions_server_id.id)]).active in [
#             True]:
#             self.env['ir.cron'].sudo().search([('ir_actions_server_id', '=', ir_actions_server_id.id)]).write(
#                 {'active': False})
#             print("Switch False ok")
