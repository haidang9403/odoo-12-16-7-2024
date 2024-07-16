from odoo import api, models


class IrCron(models.Model):
    _inherit = 'ir.cron'

    def action_switch_ir_cron(self):
        database = self.env['database.uuid'].sudo().search([('key', '=', 'database.issue.invoice')])
        action_issue_invoice = self.env['ir.actions.server'].sudo().search(
            [('model_name', '=', 'invoice.consolidation')]).ids
        if database:
            active_write = False
            for data in database:
                if data.value == self.env['ir.config_parameter'].sudo().search([('id', '=', 2)]).value:
                    active_write = True
                    for active in self.env['ir.cron'].sudo().search(
                            [('ir_actions_server_id', 'in', action_issue_invoice), ('active', '=', False)]):
                        if active:
                            active.write({'active': True})
            if not active_write:
                for active in self.env['ir.cron'].sudo().search([('ir_actions_server_id', 'in', action_issue_invoice)]):
                    if active:
                        active.write({'active': False})
                self.env['res.company'].sudo().search([]).write({'sinvoice_enabled': False})

        else:
            for active in self.env['ir.cron'].sudo().search([('ir_actions_server_id', 'in', action_issue_invoice)]):
                if active:
                    active.write({'active': False})
            self.env['res.company'].sudo().search([]).write({'sinvoice_enabled': False})
