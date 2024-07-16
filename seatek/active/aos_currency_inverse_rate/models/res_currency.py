# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    currency_convert_method = fields.Selection([('verse','Verse'),('inverse','Inverse')], default='inverse', string='Convert Method')
    
class ResCurrency(models.Model):
    _inherit = 'res.currency'
    
    rounding = fields.Float(string='Rounding Factor', digits=(12, 10), default=0.01)

    @api.model
    def _get_conversion_rate(self, from_currency, to_currency, company, date):
        currency_rates = (from_currency + to_currency)._get_rates(company, date)
        #print ('-_get_conversion_rate--',self._context.get('force_rate'))
        if company.currency_convert_method == 'inverse':
            if self._context.get('force_rate'):            
                res = self._context.get('force_rate') / currency_rates.get(to_currency.id)
            else:
                res = currency_rates.get(from_currency.id) / currency_rates.get(to_currency.id)
        else:            
            if self._context.get('force_rate'):            
                res = currency_rates.get(to_currency.id) / self._context.get('force_rate')
            else:
                res = currency_rates.get(to_currency.id) / currency_rates.get(from_currency.id)
        return res
    

class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    
    kmk_date = fields.Date('Date KMK')
    kmk_number = fields.Char('Number KMK', size=16)
    
    