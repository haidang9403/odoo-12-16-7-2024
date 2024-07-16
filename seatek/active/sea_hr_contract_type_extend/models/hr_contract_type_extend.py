# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import AccessError, UserError, ValidationError

class HrContractTyeExtend(models.Model):
    _inherit = 'hr.contract.type'

    remaining_days_for_extension_before_expiration = fields.Integer(string='Số ngày còn lại để gia hạn trước khi hết hạn',translate=True)

    # @api.constrains('remaining_days_for_extension_before_expiration')
    # def check_remaining_days_for_extension_before_expiration(self):
    #     if self.filtered(lambda c: c.remaining_days_for_extension_before_expiration<0):
    #         raise ValidationError(('Số ngày còn lại để gia hạn trước khi hết hạn phải lớn hơn hoặc bằng 0.'))