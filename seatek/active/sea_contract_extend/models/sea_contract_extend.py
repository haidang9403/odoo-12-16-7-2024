# -*- coding: utf-8 -*-
# Part of OpenSea12 , last modified 12/03/2020 by htkhoa
import datetime

from odoo import api, fields, models


class ContractPeriod(models.Model):
    _name = 'hr.contract.period'
    _description = 'Contract Period'
    _order = 'sequence, id'

    name = fields.Char(string='Contract Period', required=True, translate=True)
    sequence = fields.Integer(string="Code", help="Gives the sequence when displaying a list of Contract Period.",
                              default=10)


class SeaExtendContract(models.Model):
    _inherit = "hr.contract"
    _description = 'Sea Extend Contract'
    _order = 'date_start'

    contract_category = fields.Selection([('contract', 'Contract'),
                                          ('addition', 'Addition')], string='Category', help='Contract Category',
                                         required=True)
    ref_contract_id = fields.Many2one('hr.contract', string='Ref Contract',
                                      domain="[('employee_id','=',employee_id), ('contract_category', '=', 'contract'), ('state','not in',['close', 'cancel'])]")
    contract_period_id = fields.Many2one('hr.contract.period', string="Contract Period",
                                         default=lambda self: self.env['hr.contract.period'].search([], limit=1))
    contract_term = fields.Text(string='Contract Term')
    contract_extend_salary = fields.Monetary('Extend Salary', digits=(16, 2), required=False,
                                             track_visibility="onchange", help="Employee's monthly Extend Salary.")

    # Khanh 17:18 26/09/2022
    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.department_id = None

    @api.onchange('department_id')
    def _onchange_department_id(self):
        self.job_id = None

    #

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.ref_contract_id = False
            return {'domain': {'ref_contract_id': [('employee_id', '=', self.employee_id.id)]}}
        else:
            # remove the domain
            return {'domain': {'ref_contract_id': []}}

    '''dkh add 12082022'''
    end_days = fields.Char(string='End Days', default='')

    @api.model
    def _compute_end_days(self):
        for rec in self:
            if rec.date_start and rec.date_end:
                current_date = datetime.date.today()
                days = rec.date_end - current_date
                if int(days.days) <= 0:
                    end_days = 'Đã hết hạn'
                else:
                    end_days = str(days.days) + ' hết hạn'
                rec.write({'end_days': end_days})

    compute_end_days = fields.Char(string='compute end days', compute='_compute_end_days')

    '''TKK xóa ghi log của Lương và Lương bổ sung 13/01/2023'''
    wage = fields.Monetary('Wage', digits=(16, 2), required=True, track_visibility="",
                           help="Employee's monthly gross wage.")
    contract_extend_salary = fields.Monetary('Extend Salary', digits=(16, 2), required=False,
                                             track_visibility="", help="Employee's monthly Extend Salary.")
