import datetime

from odoo import models, api
from odoo.fields import Datetime
from odoo.tools.view_validation import validate


class HrContractExtend(models.Model):
    _inherit = 'hr.contract'

    # @api.constrains('type_id','date_start', 'date_end')
    # def _check_date_end(self):
    #     remaining_date= self[0].type_id.remaining_days_for_extension_before_expiration
    #     # remaining_date =  Datetime.today().date() + datetime.timedelta(days=self[0].type_id.remaining_days_for_extension_before_expiration)
    #     if self.filtered(lambda c: c.date_end and c.date_end > c.date_start and c.date_end < c.date_start + datetime.timedelta(days= remaining_date)):
    #         raise ValidationError(('Thời hạn hợp đồng phải lớn hơn số ngày còn lại để được gia hạn trước khi hết hạn.'))

    # # scheduler
    # @api.multi
    # def process_scheduler_stage_contract_queue(self):
    #     list_contract = self.env['hr.contract'].sudo().search([('contract_category', '=', 'contract')])
    #
    #     state = ''
    #     for contract in list_contract:
    #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', contract['id'])])
    #
    #         remaining_date = 0
    #         for re in self.env['hr.contract.type'].sudo().search([('id', '=', contract['type_id'].id)]):
    #             remaining_date = re['remaining_days_for_extension_before_expiration']
    #
    #         date_end = contract['date_end']
    #
    #         if date_end is False:
    #             state = 'open'
    #         else:
    #             if date_end <= Datetime.now().date():
    #                 state = 'close'
    #             else:
    #                 if date_end > Datetime.now().date() + datetime.timedelta(days=remaining_date):
    #                     state = 'open'
    #                 else:
    #                     state = 'pending'
    #
    #         contract.write({'state': state})
    #         for item in list_addition:
    #             item.write({'state': state})
    #     return True

    # @api.multi
    # def write(self, vals):
    #     list_contract = self.env['hr.contract'].sudo().search(
    #         ['&', ('id', '=', self.id), ('contract_category', '=', 'contract')])
    #     state = ''
    #     for contract in list_contract:
    #         list_addition = self.env['hr.contract'].sudo().search([('ref_contract_id', '=', contract['id'])])
    #
    #         remaining_date = 0
    #         for re in self.env['hr.contract.type'].sudo().search([('id', '=', contract['type_id'].id)]):
    #             remaining_date = re['remaining_days_for_extension_before_expiration']
    #
    #         date_end = contract['date_end']
    #         if vals.get('date_end') is None:
    #             date_end = contract['date_end']
    #         else:
    #             if vals['date_end'] is False:
    #                 date_end = False
    #             else:
    #                 date_temp = datetime.datetime.strptime(vals['date_end'], '%Y-%m-%d')
    #                 date_end = datetime.date(date_temp.year, date_temp.month, date_temp.day)
    #
    #         if date_end is False:
    #             state = 'open'
    #         else:
    #             if date_end <= Datetime.now().date():
    #                 state = 'close'
    #             else:
    #                 if date_end > Datetime.now().date() + datetime.timedelta(days=remaining_date):
    #                     state = 'open'
    #                 else:
    #                     state = 'pending'
    #
    #         vals.update({'state': state})
    #         for item in list_addition:
    #             item.write({'state': state})
    #
    #     return super(HrContractExtend, self).write(vals)

    # @api.model
    # def create(self, vals):
    #     if vals.get('state') is None:
    #         vals.update({'state': 'open'})
    #     return super(HrContractExtend, self).create(vals)
