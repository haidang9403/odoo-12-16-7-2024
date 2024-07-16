# -*- coding: utf-8 -*-
import os
import base64
import datetime
import pysftp
import logging
from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PosSaleReportVivo(models.TransientModel):
    _name = 'pos.sale.vivo'

    start_date = fields.Datetime(string='Date From', default=fields.Datetime.now())
    end_date = fields.Datetime(string='Date To', default=fields.Datetime.now())
    pos_config_ids = fields.Many2many('pos.config', 'pos_sale_vivo_configs',
                                      default=lambda s: s.env['pos.config'].search([('id', '=', 8)]))

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def get_config_data(self):
        start_date = datetime.datetime(year=self.start_date.year, month=self.start_date.month, day=self.start_date.day,
                                       hour=0, minute=0, second=0)
        end_date = datetime.datetime(year=self.end_date.year, month=self.end_date.month, day=self.end_date.day, hour=23,
                                     minute=59, second=59)
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'config_ids': self.pos_config_ids.ids
        }
        domain = []
        if data.get('start_date'):
            domain.append(('date_order', '>=', data.get('start_date')))
        if data.get('end_date'):
            domain.append(('date_order', '<=', data.get('end_date')))
        if data.get('config_ids'):
            domain.append(('config_id', 'in', data.get('config_ids')))
        orders = self.env['pos.order'].search(domain)
        return orders

    def cron_pos_vivo_report(self):
        orders_count_0 = 0
        orders_count_1 = 0
        orders_count_2 = 0
        orders_count_3 = 0
        orders_count_4 = 0
        orders_count_5 = 0
        orders_count_6 = 0

        orders_count_7 = 0
        amount_total_7 = 0
        amount_tax_7 = 0
        amount_disc_7 = 0
        amount_service_7 = 0
        amount_pax_7 = 0
        amount_cash_7 = 0
        amount_atm_7 = 0
        amount_visa_7 = 0
        amount_mastercard_7 = 0
        amount_amex_7 = 0
        amount_voucher_7 = 0
        amount_other_7 = 0

        orders_count_8 = 0
        amount_total_8 = 0
        amount_tax_8 = 0
        amount_disc_8 = 0
        amount_service_8 = 0
        amount_pax_8 = 0
        amount_cash_8 = 0
        amount_atm_8 = 0
        amount_visa_8 = 0
        amount_mastercard_8 = 0
        amount_amex_8 = 0
        amount_voucher_8 = 0
        amount_other_8 = 0

        orders_count_9 = 0
        amount_total_9 = 0
        amount_tax_9 = 0
        amount_disc_9 = 0
        amount_service_9 = 0
        amount_pax_9 = 0
        amount_cash_9 = 0
        amount_atm_9 = 0
        amount_visa_9 = 0
        amount_mastercard_9 = 0
        amount_amex_9 = 0
        amount_voucher_9 = 0
        amount_other_9 = 0

        orders_count_10 = 0
        amount_total_10 = 0
        amount_tax_10 = 0
        amount_disc_10 = 0
        amount_service_10 = 0
        amount_pax_10 = 0
        amount_cash_10 = 0
        amount_atm_10 = 0
        amount_visa_10 = 0
        amount_mastercard_10 = 0
        amount_amex_10 = 0
        amount_voucher_10 = 0
        amount_other_10 = 0

        orders_count_11 = 0
        amount_total_11 = 0
        amount_tax_11 = 0
        amount_disc_11 = 0
        amount_service_11 = 0
        amount_pax_11 = 0
        amount_cash_11 = 0
        amount_atm_11 = 0
        amount_visa_11 = 0
        amount_mastercard_11 = 0
        amount_amex_11 = 0
        amount_voucher_11 = 0
        amount_other_11 = 0

        orders_count_12 = 0
        amount_total_12 = 0
        amount_tax_12 = 0
        amount_disc_12 = 0
        amount_service_12 = 0
        amount_pax_12 = 0
        amount_cash_12 = 0
        amount_atm_12 = 0
        amount_visa_12 = 0
        amount_mastercard_12 = 0
        amount_amex_12 = 0
        amount_voucher_12 = 0
        amount_other_12 = 0

        orders_count_13 = 0
        amount_total_13 = 0
        amount_tax_13 = 0
        amount_disc_13 = 0
        amount_service_13 = 0
        amount_pax_13 = 0
        amount_cash_13 = 0
        amount_atm_13 = 0
        amount_visa_13 = 0
        amount_mastercard_13 = 0
        amount_amex_13 = 0
        amount_voucher_13 = 0
        amount_other_13 = 0

        orders_count_14 = 0
        amount_total_14 = 0
        amount_tax_14 = 0
        amount_disc_14 = 0
        amount_service_14 = 0
        amount_pax_14 = 0
        amount_cash_14 = 0
        amount_atm_14 = 0
        amount_visa_14 = 0
        amount_mastercard_14 = 0
        amount_amex_14 = 0
        amount_voucher_14 = 0
        amount_other_14 = 0

        orders_count_15 = 0
        amount_total_15 = 0
        amount_tax_15 = 0
        amount_disc_15 = 0
        amount_service_15 = 0
        amount_pax_15 = 0
        amount_cash_15 = 0
        amount_atm_15 = 0
        amount_visa_15 = 0
        amount_mastercard_15 = 0
        amount_amex_15 = 0
        amount_voucher_15 = 0
        amount_other_15 = 0

        orders_count_16 = 0
        amount_total_16 = 0
        amount_tax_16 = 0
        amount_disc_16 = 0
        amount_service_16 = 0
        amount_pax_16 = 0
        amount_cash_16 = 0
        amount_atm_16 = 0
        amount_visa_16 = 0
        amount_mastercard_16 = 0
        amount_amex_16 = 0
        amount_voucher_16 = 0
        amount_other_16 = 0

        orders_count_17 = 0
        amount_total_17 = 0
        amount_tax_17 = 0
        amount_disc_17 = 0
        amount_service_17 = 0
        amount_pax_17 = 0
        amount_cash_17 = 0
        amount_atm_17 = 0
        amount_visa_17 = 0
        amount_mastercard_17 = 0
        amount_amex_17 = 0
        amount_voucher_17 = 0
        amount_other_17 = 0

        orders_count_18 = 0
        amount_total_18 = 0
        amount_tax_18 = 0
        amount_disc_18 = 0
        amount_service_18 = 0
        amount_pax_18 = 0
        amount_cash_18 = 0
        amount_atm_18 = 0
        amount_visa_18 = 0
        amount_mastercard_18 = 0
        amount_amex_18 = 0
        amount_voucher_18 = 0
        amount_other_18 = 0

        orders_count_19 = 0
        amount_total_19 = 0
        amount_tax_19 = 0
        amount_disc_19 = 0
        amount_service_19 = 0
        amount_pax_19 = 0
        amount_cash_19 = 0
        amount_atm_19 = 0
        amount_visa_19 = 0
        amount_mastercard_19 = 0
        amount_amex_19 = 0
        amount_voucher_19 = 0
        amount_other_19 = 0

        orders_count_20 = 0
        amount_total_20 = 0
        amount_tax_20 = 0
        amount_disc_20 = 0
        amount_service_20 = 0
        amount_pax_20 = 0
        amount_cash_20 = 0
        amount_atm_20 = 0
        amount_visa_20 = 0
        amount_mastercard_20 = 0
        amount_amex_20 = 0
        amount_voucher_20 = 0
        amount_other_20 = 0

        orders_count_21 = 0
        amount_total_21 = 0
        amount_tax_21 = 0
        amount_disc_21 = 0
        amount_service_21 = 0
        amount_pax_21 = 0
        amount_cash_21 = 0
        amount_atm_21 = 0
        amount_visa_21 = 0
        amount_mastercard_21 = 0
        amount_amex_21 = 0
        amount_voucher_21 = 0
        amount_other_21 = 0

        orders_count_22 = 0
        amount_total_22 = 0
        amount_tax_22 = 0
        amount_disc_22 = 0
        amount_service_22 = 0
        amount_pax_22 = 0
        amount_cash_22 = 0
        amount_atm_22 = 0
        amount_visa_22 = 0
        amount_mastercard_22 = 0
        amount_amex_22 = 0
        amount_voucher_22 = 0
        amount_other_22 = 0

        orders_count_23 = 0
        amount_total_23 = 0
        amount_tax_23 = 0
        amount_disc_23 = 0
        amount_service_23 = 0
        amount_pax_23 = 0
        amount_cash_23 = 0
        amount_atm_23 = 0
        amount_visa_23 = 0
        amount_mastercard_23 = 0
        amount_amex_23 = 0
        amount_voucher_23 = 0
        amount_other_23 = 0

        time_tz_7 = datetime.timedelta(hours=7)
        date = datetime.datetime.today() + time_tz_7
        date_cron = ''.join(str(date.strftime('%d/%m/%Y')).split('/'))
        date_cron_file_name = ''.join(str(date.strftime('%Y/%m/%d')).split('/'))
        get_year = date.year
        get_month = date.month
        get_day = date.day
        start_date = datetime.datetime(get_year, get_month, get_day, 0, 0)
        end_date = datetime.datetime(get_year, get_month, get_day, 23, 0)
        data = {
            'start_date': start_date,
            'end_date': end_date,
            'config_ids': 8
        }
        domain = []
        if data.get('start_date'):
            domain.append(('date_order', '>=', data.get('start_date')))
        if data.get('start_date'):
            domain.append(('date_order', '<=', data.get('end_date')))
        if data.get('config_ids'):
            domain.append(('config_id', '=', data.get('config_ids')))
        orders = self.env['pos.order'].search(domain)

        if len(orders) > 0:
            pos_session = ''
        else:
            pos_session = '0'
        for order in reversed(orders):
            time_tz_7 = datetime.timedelta(hours=7)
            time_tz_1 = datetime.timedelta(hours=1)
            pos_session = (str(order.session_id.name)[-4:])
            order_date_real = order.date_order + time_tz_7
            date_time_order = order.date_order
            get_year_order = date_time_order.year
            get_month_order = date_time_order.month
            get_day_order = date_time_order.day

            date_time_0 = datetime.datetime(get_year_order, get_month_order, get_day_order, 0, 0)
            date_time_1 = date_time_0 + time_tz_1
            date_time_2 = date_time_1 + time_tz_1
            date_time_3 = date_time_2 + time_tz_1
            date_time_4 = date_time_3 + time_tz_1
            date_time_5 = date_time_4 + time_tz_1
            date_time_6 = date_time_5 + time_tz_1
            date_time_7 = date_time_6 + time_tz_1
            date_time_8 = date_time_7 + time_tz_1
            date_time_9 = date_time_8 + time_tz_1
            date_time_10 = date_time_9 + time_tz_1
            date_time_11 = date_time_10 + time_tz_1
            date_time_12 = date_time_11 + time_tz_1
            date_time_13 = date_time_12 + time_tz_1
            date_time_14 = date_time_13 + time_tz_1
            date_time_15 = date_time_14 + time_tz_1
            date_time_16 = date_time_15 + time_tz_1
            date_time_17 = date_time_16 + time_tz_1
            date_time_18 = date_time_17 + time_tz_1
            date_time_19 = date_time_18 + time_tz_1
            date_time_20 = date_time_19 + time_tz_1
            date_time_21 = date_time_20 + time_tz_1
            date_time_22 = date_time_21 + time_tz_1
            date_time_23 = date_time_22 + time_tz_1

            cash = 0
            atm = 0
            voucher = 0
            other = 0

            if date_time_0 <= order_date_real <= date_time_1:
                orders_count_0 += 1
            elif date_time_1 <= order_date_real <= date_time_2:
                orders_count_1 += 1
            elif date_time_2 <= order_date_real <= date_time_3:
                orders_count_2 += 1
            elif date_time_3 <= order_date_real <= date_time_4:
                orders_count_3 += 1
            elif date_time_4 <= order_date_real <= date_time_5:
                orders_count_4 += 1
            elif date_time_5 <= order_date_real <= date_time_6:
                orders_count_5 += 1
            elif date_time_6 <= order_date_real <= date_time_7:
                orders_count_6 += 1
            elif date_time_7 <= order_date_real <= date_time_8:
                orders_count_7 += 1
            elif date_time_8 <= order_date_real <= date_time_9:
                orders_count_8 += 1
                amount_total_8 += round(order.amount_total - order.amount_tax)
                amount_tax_8 += round(order.amount_tax)
                tax_line_8 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_8 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_8 += cash - tax_line_8
                        amount_atm_8 += atm
                    else:
                        amount_cash_8 += cash
                        amount_atm_8 += atm - tax_line_8
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_8 += cash - tax_line_8
                        amount_voucher_8 += voucher
                    else:
                        amount_cash_8 += cash
                        amount_voucher_8 += voucher - tax_line_8
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_8 += cash - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_cash_8 += cash
                        amount_other_8 += other - tax_line_8
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_8 += atm - tax_line_8
                        amount_voucher_8 += voucher
                    else:
                        amount_atm_8 += atm
                        amount_voucher_8 += voucher - tax_line_8
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_8 += atm - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_atm_8 += atm
                        amount_other_8 += other - tax_line_8
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_8 += voucher - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_voucher_8 += voucher
                        amount_other_8 += other - tax_line_8
                elif abs(cash) > 0:
                    amount_cash_8 += cash - tax_line_8
                elif abs(atm) > 0:
                    amount_atm_8 += atm - tax_line_8
                elif abs(voucher) > 0:
                    amount_voucher_8 += voucher - tax_line_8
                elif abs(other) > 0:
                    amount_other_8 += other - tax_line_8

            elif date_time_9 <= order_date_real <= date_time_10:
                orders_count_9 += 1
                amount_total_9 += round(order.amount_total - order.amount_tax)
                amount_tax_9 += round(order.amount_tax)
                tax_line_9 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_9 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_9 += cash - tax_line_9
                        amount_atm_9 += atm
                    else:
                        amount_cash_9 += cash
                        amount_atm_9 += atm - tax_line_9
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_9 += cash - tax_line_9
                        amount_voucher_9 += voucher
                    else:
                        amount_cash_9 += cash
                        amount_voucher_9 += voucher - tax_line_9
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_9 += cash - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_cash_9 += cash
                        amount_other_9 += other - tax_line_9
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_9 += atm - tax_line_9
                        amount_voucher_9 += voucher
                    else:
                        amount_atm_9 += atm
                        amount_voucher_9 += voucher - tax_line_9
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_9 += atm - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_atm_9 += atm
                        amount_other_9 += other - tax_line_9
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_9 += voucher - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_voucher_9 += voucher
                        amount_other_9 += other - tax_line_9
                elif abs(cash) > 0:
                    amount_cash_9 += cash - tax_line_9
                elif abs(atm) > 0:
                    amount_atm_9 += atm - tax_line_9
                elif abs(voucher) > 0:
                    amount_voucher_9 += voucher - tax_line_9
                elif abs(other) > 0:
                    amount_other_9 += other - tax_line_9

            elif date_time_10 <= order_date_real <= date_time_11:
                orders_count_10 += 1
                amount_total_10 += round(order.amount_total - order.amount_tax)
                amount_tax_10 += round(order.amount_tax)
                tax_line_10 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_10 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_10 += cash - tax_line_10
                        amount_atm_10 += atm
                    else:
                        amount_cash_10 += cash
                        amount_atm_10 += atm - tax_line_10
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_10 += cash - tax_line_10
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_10 += cash
                        amount_voucher_10 += voucher - tax_line_10
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_10 += cash - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_cash_10 += cash
                        amount_other_10 += other - tax_line_10
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_10 += atm - tax_line_10
                        amount_voucher_10 += voucher
                    else:
                        amount_atm_10 += atm
                        amount_voucher_10 += voucher - tax_line_10
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_10 += atm - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_atm_10 += atm
                        amount_other_10 += other - tax_line_10
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_10 += voucher - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_voucher_10 += voucher
                        amount_other_10 += other - tax_line_10
                elif abs(cash) > 0:
                    amount_cash_10 += cash - tax_line_10
                elif abs(atm) > 0:
                    amount_atm_10 += atm - tax_line_10
                elif abs(voucher) > 0:
                    amount_voucher_10 += voucher - tax_line_10
                elif abs(other) > 0:
                    amount_other_10 += other - tax_line_10

            elif date_time_11 <= order_date_real <= date_time_12:
                orders_count_11 += 1
                amount_total_11 += round(order.amount_total - order.amount_tax)
                amount_tax_11 += round(order.amount_tax)
                tax_line_11 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_11 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_11 += cash - tax_line_11
                        amount_atm_11 += atm
                    else:
                        amount_cash_11 += cash
                        amount_atm_11 += atm - tax_line_11
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_11 += cash - tax_line_11
                        amount_voucher_11 += voucher
                    else:
                        amount_cash_11 += cash
                        amount_voucher_11 += voucher - tax_line_11
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_11 += cash - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_cash_11 += cash
                        amount_other_11 += other - tax_line_11
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_11 += atm - tax_line_11
                        amount_voucher_11 += voucher
                    else:
                        amount_atm_11 += atm
                        amount_voucher_11 += voucher - tax_line_11
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_11 += atm - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_atm_11 += atm
                        amount_other_11 += other - tax_line_11
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_11 += voucher - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_voucher_11 += voucher
                        amount_other_11 += other - tax_line_11
                elif abs(cash) > 0:
                    amount_cash_11 += cash - tax_line_11
                elif abs(atm) > 0:
                    amount_atm_11 += atm - tax_line_11
                elif abs(voucher) > 0:
                    amount_voucher_11 += voucher - tax_line_11
                elif abs(other) > 0:
                    amount_other_11 += other - tax_line_11

            elif date_time_12 <= order_date_real <= date_time_13:
                orders_count_12 += 1
                amount_total_12 += round(order.amount_total - order.amount_tax)
                amount_tax_12 += round(order.amount_tax)
                tax_line_12 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_12 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_12 += cash - tax_line_12
                        amount_atm_12 += atm
                    else:
                        amount_cash_12 += cash
                        amount_atm_12 += atm - tax_line_12
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_12 += cash - tax_line_12
                        amount_voucher_12 += voucher
                    else:
                        amount_cash_12 += cash
                        amount_voucher_12 += voucher - tax_line_12
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_12 += cash - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_cash_12 += cash
                        amount_other_12 += other - tax_line_12
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_12 += atm - tax_line_12
                        amount_voucher_12 += voucher
                    else:
                        amount_atm_12 += atm
                        amount_voucher_12 += voucher - tax_line_12
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_12 += atm - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_atm_12 += atm
                        amount_other_12 += other - tax_line_12
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_12 += voucher - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_voucher_12 += voucher
                        amount_other_12 += other - tax_line_12
                elif abs(cash) > 0:
                    amount_cash_12 += cash - tax_line_12
                elif abs(atm) > 0:
                    amount_atm_12 += atm - tax_line_12
                elif abs(voucher) > 0:
                    amount_voucher_12 += voucher - tax_line_12
                elif abs(other) > 0:
                    amount_other_12 += other - tax_line_12

            elif date_time_13 <= order_date_real <= date_time_14:
                orders_count_13 += 1
                amount_total_13 += round(order.amount_total - order.amount_tax)
                amount_tax_13 += round(order.amount_tax)
                tax_line_13 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_13 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_13 += cash - tax_line_13
                        amount_atm_13 += atm
                    else:
                        amount_cash_13 += cash
                        amount_atm_13 += atm - tax_line_13
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_13 += cash - tax_line_13
                        amount_voucher_13 += voucher
                    else:
                        amount_cash_13 += cash
                        amount_voucher_13 += voucher - tax_line_13
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_13 += cash - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_cash_13 += cash
                        amount_other_13 += other - tax_line_13
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_13 += atm - tax_line_13
                        amount_voucher_13 += voucher
                    else:
                        amount_atm_13 += atm
                        amount_voucher_13 += voucher - tax_line_13
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_13 += atm - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_atm_13 += atm
                        amount_other_13 += other - tax_line_13
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_13 += voucher - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_voucher_13 += voucher
                        amount_other_13 += other - tax_line_13
                elif abs(cash) > 0:
                    amount_cash_13 += cash - tax_line_13
                elif abs(atm) > 0:
                    amount_atm_13 += atm - tax_line_13
                elif abs(voucher) > 0:
                    amount_voucher_13 += voucher - tax_line_13
                elif abs(other) > 0:
                    amount_other_13 += other - tax_line_13

            elif date_time_14 <= order_date_real <= date_time_15:
                orders_count_14 += 1
                amount_total_14 += round(order.amount_total - order.amount_tax)
                amount_tax_14 += round(order.amount_tax)
                tax_line_14 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_14 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_14 += cash - tax_line_14
                        amount_atm_14 += atm
                    else:
                        amount_cash_14 += cash
                        amount_atm_14 += atm - tax_line_14
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_14 += cash - tax_line_14
                        amount_voucher_14 += voucher
                    else:
                        amount_cash_14 += cash
                        amount_voucher_14 += voucher - tax_line_14
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_14 += cash - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_cash_14 += cash
                        amount_other_14 += other - tax_line_14
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_14 += atm - tax_line_14
                        amount_voucher_14 += voucher
                    else:
                        amount_atm_14 += atm
                        amount_voucher_14 += voucher - tax_line_14
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_14 += atm - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_atm_14 += atm
                        amount_other_14 += other - tax_line_14
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_14 += voucher - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_voucher_14 += voucher
                        amount_other_14 += other - tax_line_14
                elif abs(cash) > 0:
                    amount_cash_14 += cash - tax_line_14
                elif abs(atm) > 0:
                    amount_atm_14 += atm - tax_line_14
                elif abs(voucher) > 0:
                    amount_voucher_14 += voucher - tax_line_14
                elif abs(other) > 0:
                    amount_other_14 += other - tax_line_14

            elif date_time_15 <= order_date_real <= date_time_16:
                orders_count_15 += 1
                amount_total_15 += round(order.amount_total - order.amount_tax)
                amount_tax_15 += round(order.amount_tax)
                tax_line_15 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_15 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_15 += cash - tax_line_15
                        amount_atm_15 += atm
                    else:
                        amount_cash_15 += cash
                        amount_atm_15 += atm - tax_line_15
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_15 += cash - tax_line_15
                        amount_voucher_15 += voucher
                    else:
                        amount_cash_16 += cash
                        amount_voucher_15 += voucher - tax_line_15
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_15 += cash - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_cash_15 += cash
                        amount_other_15 += other - tax_line_15
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_15 += atm - tax_line_15
                        amount_voucher_16 += voucher
                    else:
                        amount_atm_15 += atm
                        amount_voucher_15 += voucher - tax_line_15
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_15 += atm - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_atm_15 += atm
                        amount_other_15 += other - tax_line_15
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_15 += voucher - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_voucher_15 += voucher
                        amount_other_15 += other - tax_line_15
                elif abs(cash) > 0:
                    amount_cash_15 += cash - tax_line_15
                elif abs(atm) > 0:
                    amount_atm_15 += atm - tax_line_15
                elif abs(voucher) > 0:
                    amount_voucher_15 += voucher - tax_line_15
                elif abs(other) > 0:
                    amount_other_15 += other - tax_line_15

            elif date_time_16 <= order_date_real <= date_time_17:
                orders_count_16 += 1
                amount_total_16 += round(order.amount_total - order.amount_tax)
                amount_tax_16 += round(order.amount_tax)
                tax_line_16 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_16 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)

                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_16 += cash - tax_line_16
                        amount_atm_16 += atm
                    else:
                        amount_cash_16 += cash
                        amount_atm_16 += atm - tax_line_16
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_16 += cash - tax_line_16
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_16 += cash
                        amount_voucher_16 += voucher - tax_line_16
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_16 += cash - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_cash_16 += cash
                        amount_other_16 += other - tax_line_16
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_16 += atm - tax_line_16
                        amount_voucher_16 += voucher
                    else:
                        amount_atm_16 += atm
                        amount_voucher_16 += voucher - tax_line_16
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_16 += atm - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_atm_16 += atm
                        amount_other_16 += other - tax_line_16
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_16 += voucher - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_voucher_16 += voucher
                        amount_other_16 += other - tax_line_16
                elif abs(cash) > 0:
                    amount_cash_16 += cash - tax_line_16
                elif abs(atm) > 0:
                    amount_atm_16 += atm - tax_line_16
                elif abs(voucher) > 0:
                    amount_voucher_16 += voucher - tax_line_16
                elif abs(other) > 0:
                    amount_other_16 += other - tax_line_16

            elif date_time_17 <= order_date_real <= date_time_18:
                orders_count_17 += 1
                amount_total_17 += round(order.amount_total - order.amount_tax)
                amount_tax_17 += round(order.amount_tax)
                tax_line_17 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_17 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_17 += cash - tax_line_17
                        amount_atm_17 += atm
                    else:
                        amount_cash_17 += cash
                        amount_atm_17 += atm - tax_line_17
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_17 += cash - tax_line_17
                        amount_voucher_17 += voucher
                    else:
                        amount_cash_17 += cash
                        amount_voucher_17 += voucher - tax_line_17
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_17 += cash - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_cash_17 += cash
                        amount_other_17 += other - tax_line_17
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_17 += atm - tax_line_17
                        amount_voucher_17 += voucher
                    else:
                        amount_atm_17 += atm
                        amount_voucher_17 += voucher - tax_line_17
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_17 += atm - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_atm_17 += atm
                        amount_other_17 += other - tax_line_17
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_17 += voucher - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_voucher_17 += voucher
                        amount_other_17 += other - tax_line_17
                elif abs(cash) > 0:
                    amount_cash_17 += cash - tax_line_17
                elif abs(atm) > 0:
                    amount_atm_17 += atm - tax_line_17
                elif abs(voucher) > 0:
                    amount_voucher_17 += voucher - tax_line_17
                elif abs(other) > 0:
                    amount_other_17 += other - tax_line_17

            elif date_time_18 <= order_date_real <= date_time_19:
                orders_count_18 += 1
                amount_total_18 += round(order.amount_total - order.amount_tax)
                amount_tax_18 += round(order.amount_tax)
                tax_line_18 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_18 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_18 += cash - tax_line_18
                        amount_atm_18 += atm
                    else:
                        amount_cash_18 += cash
                        amount_atm_18 += atm - tax_line_18
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_18 += cash - tax_line_18
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_18 += cash
                        amount_voucher_16 += voucher - tax_line_18
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_18 += cash - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_cash_18 += cash
                        amount_other_18 += other - tax_line_18
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_18 += atm - tax_line_18
                        amount_voucher_18 += voucher
                    else:
                        amount_atm_18 += atm
                        amount_voucher_18 += voucher - tax_line_18
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_18 += atm - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_atm_18 += atm
                        amount_other_18 += other - tax_line_18
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_18 += voucher - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_voucher_18 += voucher
                        amount_other_18 += other - tax_line_18
                elif abs(cash) > 0:
                    amount_cash_18 += cash - tax_line_18
                elif abs(atm) > 0:
                    amount_atm_18 += atm - tax_line_18
                elif abs(voucher) > 0:
                    amount_voucher_18 += voucher - tax_line_18
                elif abs(other) > 0:
                    amount_other_18 += other - tax_line_18

            elif date_time_19 <= order_date_real <= date_time_20:
                orders_count_19 += 1
                amount_total_19 += round(order.amount_total - order.amount_tax)
                amount_tax_19 += round(order.amount_tax)
                tax_line_19 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_19 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_19 += cash - tax_line_19
                        amount_atm_19 += atm
                    else:
                        amount_cash_19 += cash
                        amount_atm_19 += atm - tax_line_19
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_19 += cash - tax_line_19
                        amount_voucher_19 += voucher
                    else:
                        amount_cash_19 += cash
                        amount_voucher_19 += voucher - tax_line_19
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_19 += cash - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_cash_19 += cash
                        amount_other_19 += other - tax_line_19
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_19 += atm - tax_line_19
                        amount_voucher_19 += voucher
                    else:
                        amount_atm_19 += atm
                        amount_voucher_19 += voucher - tax_line_19
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_19 += atm - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_atm_19 += atm
                        amount_other_19 += other - tax_line_19
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_19 += voucher - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_voucher_19 += voucher
                        amount_other_19 += other - tax_line_19
                elif abs(cash) > 0:
                    amount_cash_19 += cash - tax_line_19
                elif abs(atm) > 0:
                    amount_atm_19 += atm - tax_line_19
                elif abs(voucher) > 0:
                    amount_voucher_19 += voucher - tax_line_19
                elif abs(other) > 0:
                    amount_other_19 += other - tax_line_19

            elif date_time_20 <= order_date_real <= date_time_21:
                orders_count_20 += 1
                amount_total_20 += round(order.amount_total - order.amount_tax)
                amount_tax_20 += round(order.amount_tax)
                tax_line_20 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_20 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_20 += cash - tax_line_20
                        amount_atm_20 += atm
                    else:
                        amount_cash_20 += cash
                        amount_atm_20 += atm - tax_line_20
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_20 += cash - tax_line_20
                        amount_voucher_20 += voucher
                    else:
                        amount_cash_20 += cash
                        amount_voucher_20 += voucher - tax_line_20
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_20 += cash - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_cash_20 += cash
                        amount_other_20 += other - tax_line_20
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_20 += atm - tax_line_20
                        amount_voucher_20 += voucher
                    else:
                        amount_atm_20 += atm
                        amount_voucher_20 += voucher - tax_line_20
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_20 += atm - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_atm_20 += atm
                        amount_other_20 += other - tax_line_20
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_20 += voucher - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_voucher_20 += voucher
                        amount_other_20 += other - tax_line_20
                elif abs(cash) > 0:
                    amount_cash_20 += cash - tax_line_20
                elif abs(atm) > 0:
                    amount_atm_20 += atm - tax_line_20
                elif abs(voucher) > 0:
                    amount_voucher_20 += voucher - tax_line_20
                elif abs(other) > 0:
                    amount_other_20 += other - tax_line_20

            elif date_time_21 <= order_date_real <= date_time_22:
                orders_count_21 += 1
                amount_total_21 += round(order.amount_total - order.amount_tax)
                amount_tax_21 += round(order.amount_tax)
                tax_line_21 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_21 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_21 += cash - tax_line_21
                        amount_atm_21 += atm
                    else:
                        amount_cash_21 += cash
                        amount_atm_21 += atm - tax_line_21
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_21 += cash - tax_line_21
                        amount_voucher_21 += voucher
                    else:
                        amount_cash_21 += cash
                        amount_voucher_21 += voucher - tax_line_21
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_21 += cash - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_cash_21 += cash
                        amount_other_21 += other - tax_line_21
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_21 += atm - tax_line_21
                        amount_voucher_21 += voucher
                    else:
                        amount_atm_21 += atm
                        amount_voucher_21 += voucher - tax_line_21
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_21 += atm - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_atm_21 += atm
                        amount_other_21 += other - tax_line_21
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_21 += voucher - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_voucher_21 += voucher
                        amount_other_21 += other - tax_line_21
                elif abs(cash) > 0:
                    amount_cash_21 += cash - tax_line_21
                elif abs(atm) > 0:
                    amount_atm_21 += atm - tax_line_21
                elif abs(voucher) > 0:
                    amount_voucher_21 += voucher - tax_line_21
                elif abs(other) > 0:
                    amount_other_21 += other - tax_line_21

            elif date_time_22 <= order_date_real <= date_time_23:
                orders_count_22 += 1
                amount_total_22 += round(order.amount_total - order.amount_tax)
                amount_tax_22 += round(order.amount_tax)
                tax_line_22 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_22 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_22 += cash - tax_line_22
                        amount_atm_22 += atm
                    else:
                        amount_cash_22 += cash
                        amount_atm_22 += atm - tax_line_22
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_22 += cash - tax_line_22
                        amount_voucher_22 += voucher
                    else:
                        amount_cash_22 += cash
                        amount_voucher_22 += voucher - tax_line_22
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_22 += cash - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_cash_22 += cash
                        amount_other_22 += other - tax_line_22
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_22 += atm - tax_line_22
                        amount_voucher_22 += voucher
                    else:
                        amount_atm_22 += atm
                        amount_voucher_22 += voucher - tax_line_22
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_22 += atm - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_atm_22 += atm
                        amount_other_22 += other - tax_line_22
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_22 += voucher - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_voucher_22 += voucher
                        amount_other_22 += other - tax_line_22
                elif abs(cash) > 0:
                    amount_cash_22 += cash - tax_line_22
                elif abs(atm) > 0:
                    amount_atm_22 += atm - tax_line_22
                elif abs(voucher) > 0:
                    amount_voucher_22 += voucher - tax_line_22
                elif abs(other) > 0:
                    amount_other_22 += other - tax_line_22

            elif date_time_23 <= order_date_real <= date_time_0:
                orders_count_23 += 1
                amount_total_23 += round(order.amount_total - order.amount_tax)
                amount_tax_23 += round(order.amount_tax)
                tax_line_23 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_23 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_23 += cash - tax_line_23
                        amount_atm_23 += atm
                    else:
                        amount_cash_23 += cash
                        amount_atm_23 += atm - tax_line_23
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_23 += cash - tax_line_23
                        amount_voucher_23 += voucher
                    else:
                        amount_cash_23 += cash
                        amount_voucher_23 += voucher - tax_line_23
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_23 += cash - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_cash_23 += cash
                        amount_other_23 += other - tax_line_23
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_23 += atm - tax_line_23
                        amount_voucher_23 += voucher
                    else:
                        amount_atm_23 += atm
                        amount_voucher_23 += voucher - tax_line_23
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_23 += atm - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_atm_23 += atm
                        amount_other_23 += other - tax_line_23
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_23 += voucher - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_voucher_23 += voucher
                        amount_other_23 += other - tax_line_23
                elif abs(cash) > 0:
                    amount_cash_23 += cash - tax_line_23
                elif abs(atm) > 0:
                    amount_atm_23 += atm - tax_line_23
                elif abs(voucher) > 0:
                    amount_voucher_23 += voucher - tax_line_23
                elif abs(other) > 0:
                    amount_other_23 += other - tax_line_23

        line_0 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '00' + '|' + str(orders_count_0)
        line_1 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '01' + '|' + str(orders_count_1)
        line_2 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '02' + '|' + str(orders_count_2)
        line_3 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '03' + '|' + str(orders_count_3)
        line_4 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '04' + '|' + str(orders_count_4)
        line_5 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '05' + '|' + str(orders_count_5)
        line_6 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '06' + '|' + str(orders_count_6)
        line_7 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '07' + '|' + str(orders_count_7)
        line_8 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '08' + '|' + str(orders_count_8)
        line_9 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '09' + '|' + str(orders_count_9)
        line_10 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '10' + '|' + str(orders_count_10)
        line_11 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '11' + '|' + str(orders_count_11)
        line_12 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '12' + '|' + str(orders_count_12)
        line_13 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '13' + '|' + str(orders_count_13)
        line_14 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '14' + '|' + str(orders_count_14)
        line_15 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '15' + '|' + str(orders_count_15)
        line_16 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '16' + '|' + str(orders_count_16)
        line_17 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '17' + '|' + str(orders_count_17)
        line_18 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '18' + '|' + str(orders_count_18)
        line_19 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '19' + '|' + str(orders_count_19)
        line_20 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '20' + '|' + str(orders_count_20)
        line_21 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '21' + '|' + str(orders_count_21)
        line_22 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '22' + '|' + str(orders_count_22)
        line_23 = '17000025' + '|' + pos_session + '|' + date_cron + '|' + '23' + '|' + str(orders_count_23)

        line_no_data = '|0.00|0.00|0.00|0.00|0|0.00|0.00|0.00|0.00|0.00|0.00|0.00|Y'

        if orders_count_0 == 0:
            line_0 += line_no_data
        if orders_count_1 == 0:
            line_1 += line_no_data
        if orders_count_2 == 0:
            line_2 += line_no_data
        if orders_count_3 == 0:
            line_3 += line_no_data
        if orders_count_4 == 0:
            line_4 += line_no_data
        if orders_count_5 == 0:
            line_5 += line_no_data
        if orders_count_6 == 0:
            line_6 += line_no_data
        if orders_count_7 == 0:
            line_7 += line_no_data
        else:
            line_7 = line_7 + '|' + '{:.2f}'.format(amount_total_7) + '|' + '{:.2f}'.format(
                amount_tax_7) + '|' + '{:.2f}'.format(amount_disc_7) + '|' \
                     + '{:.2f}'.format(amount_service_7) + '|' + str(amount_pax_7) + '|' + '{:.2f}'.format(
                amount_cash_7) + '|' + '{:.2f}'.format(amount_atm_7) \
                     + '|' + '{:.2f}'.format(amount_visa_7) + '|' + '{:.2f}'.format(
                amount_mastercard_7) + '|' + '{:.2f}'.format(amount_amex_7) \
                     + '|' + '{:.2f}'.format(amount_voucher_7) + '|' + '{:.2f}'.format(
                amount_other_7) + '|' + 'Y'
        if orders_count_8 == 0:
            line_8 += line_no_data
        else:
            line_8 = line_8 + '|' + '{:.2f}'.format(amount_total_8) + '|' + '{:.2f}'.format(
                amount_tax_8) + '|' + '{:.2f}'.format(amount_disc_8) + '|' \
                     + '{:.2f}'.format(amount_service_8) + '|' + str(amount_pax_8) + '|' + '{:.2f}'.format(
                amount_cash_8) + '|' + '{:.2f}'.format(amount_atm_8) \
                     + '|' + '{:.2f}'.format(amount_visa_8) + '|' + '{:.2f}'.format(
                amount_mastercard_8) + '|' + '{:.2f}'.format(amount_amex_8) \
                     + '|' + '{:.2f}'.format(amount_voucher_8) + '|' + '{:.2f}'.format(
                amount_other_8) + '|' + 'Y'
        if orders_count_9 == 0:
            line_9 += line_no_data
        else:
            line_9 = line_9 + '|' + '{:.2f}'.format(amount_total_9) + '|' + '{:.2f}'.format(
                amount_tax_9) + '|' + '{:.2f}'.format(amount_disc_9) + '|' \
                     + '{:.2f}'.format(amount_service_9) + '|' + str(amount_pax_9) + '|' + '{:.2f}'.format(
                amount_cash_9) + '|' + '{:.2f}'.format(amount_atm_9) \
                     + '|' + '{:.2f}'.format(amount_visa_9) + '|' + '{:.2f}'.format(
                amount_mastercard_9) + '|' + '{:.2f}'.format(amount_amex_9) \
                     + '|' + '{:.2f}'.format(amount_voucher_9) + '|' + '{:.2f}'.format(
                amount_other_9) + '|' + 'Y'
        if orders_count_10 == 0:
            line_10 += line_no_data
        else:
            line_10 = line_10 + '|' + '{:.2f}'.format(amount_total_10) + '|' + '{:.2f}'.format(
                amount_tax_10) + '|' + '{:.2f}'.format(amount_disc_10) + '|' \
                      + '{:.2f}'.format(amount_service_10) + '|' + str(amount_pax_10) + '|' + '{:.2f}'.format(
                amount_cash_10) + '|' + '{:.2f}'.format(amount_atm_10) \
                      + '|' + '{:.2f}'.format(amount_visa_10) + '|' + '{:.2f}'.format(
                amount_mastercard_10) + '|' + '{:.2f}'.format(amount_amex_10) \
                      + '|' + '{:.2f}'.format(amount_voucher_10) + '|' + '{:.2f}'.format(
                amount_other_10) + '|' + 'Y'
        if orders_count_11 == 0:
            line_11 += line_no_data
        else:
            line_11 = line_11 + '|' + '{:.2f}'.format(amount_total_11) + '|' + '{:.2f}'.format(
                amount_tax_11) + '|' + '{:.2f}'.format(amount_disc_11) + '|' \
                      + '{:.2f}'.format(amount_service_11) + '|' + str(amount_pax_11) + '|' + '{:.2f}'.format(
                amount_cash_11) + '|' + '{:.2f}'.format(amount_atm_11) \
                      + '|' + '{:.2f}'.format(amount_visa_11) + '|' + '{:.2f}'.format(
                amount_mastercard_11) + '|' + '{:.2f}'.format(amount_amex_11) \
                      + '|' + '{:.2f}'.format(amount_voucher_11) + '|' + '{:.2f}'.format(
                amount_other_11) + '|' + 'Y'
        if orders_count_12 == 0:
            line_12 += line_no_data
        else:
            line_12 = line_12 + '|' + '{:.2f}'.format(amount_total_12) + '|' + '{:.2f}'.format(
                amount_tax_12) + '|' + '{:.2f}'.format(amount_disc_12) + '|' \
                      + '{:.2f}'.format(amount_service_12) + '|' + str(amount_pax_12) + '|' + '{:.2f}'.format(
                amount_cash_12) + '|' + '{:.2f}'.format(amount_atm_12) \
                      + '|' + '{:.2f}'.format(amount_visa_12) + '|' + '{:.2f}'.format(
                amount_mastercard_12) + '|' + '{:.2f}'.format(amount_amex_12) \
                      + '|' + '{:.2f}'.format(amount_voucher_12) + '|' + '{:.2f}'.format(
                amount_other_12) + '|' + 'Y'
        if orders_count_13 == 0:
            line_13 += line_no_data
        else:
            line_13 = line_13 + '|' + '{:.2f}'.format(amount_total_13) + '|' + '{:.2f}'.format(
                amount_tax_13) + '|' + '{:.2f}'.format(amount_disc_13) + '|' \
                      + '{:.2f}'.format(amount_service_13) + '|' + str(amount_pax_13) + '|' + '{:.2f}'.format(
                amount_cash_13) + '|' + '{:.2f}'.format(amount_atm_13) \
                      + '|' + '{:.2f}'.format(amount_visa_13) + '|' + '{:.2f}'.format(
                amount_mastercard_13) + '|' + '{:.2f}'.format(amount_amex_13) \
                      + '|' + '{:.2f}'.format(amount_voucher_13) + '|' + '{:.2f}'.format(
                amount_other_13) + '|' + 'Y'
        if orders_count_14 == 0:
            line_14 += line_no_data
        else:
            line_14 = line_14 + '|' + '{:.2f}'.format(amount_total_14) + '|' + '{:.2f}'.format(
                amount_tax_14) + '|' + '{:.2f}'.format(amount_disc_14) + '|' \
                      + '{:.2f}'.format(amount_service_14) + '|' + str(amount_pax_14) + '|' + '{:.2f}'.format(
                amount_cash_14) + '|' + '{:.2f}'.format(amount_atm_14) \
                      + '|' + '{:.2f}'.format(amount_visa_14) + '|' + '{:.2f}'.format(
                amount_mastercard_14) + '|' + '{:.2f}'.format(amount_amex_14) \
                      + '|' + '{:.2f}'.format(amount_voucher_14) + '|' + '{:.2f}'.format(
                amount_other_14) + '|' + 'Y'
        if orders_count_15 == 0:
            line_15 += line_no_data
        else:
            line_15 = line_15 + '|' + '{:.2f}'.format(amount_total_15) + '|' + '{:.2f}'.format(
                amount_tax_15) + '|' + '{:.2f}'.format(amount_disc_15) + '|' \
                      + '{:.2f}'.format(amount_service_15) + '|' + str(amount_pax_15) + '|' + '{:.2f}'.format(
                amount_cash_15) + '|' + '{:.2f}'.format(amount_atm_15) \
                      + '|' + '{:.2f}'.format(amount_visa_15) + '|' + '{:.2f}'.format(
                amount_mastercard_15) + '|' + '{:.2f}'.format(amount_amex_15) \
                      + '|' + '{:.2f}'.format(amount_voucher_15) + '|' + '{:.2f}'.format(
                amount_other_15) + '|' + 'Y'
        if orders_count_16 == 0:
            line_16 += line_no_data
        else:
            line_16 = line_16 + '|' + '{:.2f}'.format(amount_total_16) + '|' + '{:.2f}'.format(
                amount_tax_16) + '|' + '{:.2f}'.format(amount_disc_16) + '|' \
                      + '{:.2f}'.format(amount_service_16) + '|' + str(amount_pax_16) + '|' + '{:.2f}'.format(
                amount_cash_16) + '|' + '{:.2f}'.format(amount_atm_16) \
                      + '|' + '{:.2f}'.format(amount_visa_16) + '|' + '{:.2f}'.format(
                amount_mastercard_16) + '|' + '{:.2f}'.format(amount_amex_16) \
                      + '|' + '{:.2f}'.format(amount_voucher_16) + '|' + '{:.2f}'.format(
                amount_other_16) + '|' + 'Y'
        if orders_count_17 == 0:
            line_17 += line_no_data
        else:
            line_17 = line_17 + '|' + '{:.2f}'.format(amount_total_17) + '|' + '{:.2f}'.format(
                amount_tax_17) + '|' + '{:.2f}'.format(amount_disc_17) + '|' \
                      + '{:.2f}'.format(amount_service_17) + '|' + str(amount_pax_17) + '|' + '{:.2f}'.format(
                amount_cash_17) + '|' + '{:.2f}'.format(amount_atm_17) \
                      + '|' + '{:.2f}'.format(amount_visa_17) + '|' + '{:.2f}'.format(
                amount_mastercard_17) + '|' + '{:.2f}'.format(amount_amex_17) \
                      + '|' + '{:.2f}'.format(amount_voucher_17) + '|' + '{:.2f}'.format(
                amount_other_17) + '|' + 'Y'
        if orders_count_18 == 0:
            line_18 += line_no_data
        else:
            line_18 = line_18 + '|' + '{:.2f}'.format(amount_total_18) + '|' + '{:.2f}'.format(
                amount_tax_18) + '|' + '{:.2f}'.format(amount_disc_18) + '|' \
                      + '{:.2f}'.format(amount_service_18) + '|' + str(amount_pax_18) + '|' + '{:.2f}'.format(
                amount_cash_18) + '|' + '{:.2f}'.format(amount_atm_18) \
                      + '|' + '{:.2f}'.format(amount_visa_18) + '|' + '{:.2f}'.format(
                amount_mastercard_18) + '|' + '{:.2f}'.format(amount_amex_18) \
                      + '|' + '{:.2f}'.format(amount_voucher_18) + '|' + '{:.2f}'.format(
                amount_other_18) + '|' + 'Y'
        if orders_count_19 == 0:
            line_19 += line_no_data
        else:
            line_19 = line_19 + '|' + '{:.2f}'.format(amount_total_19) + '|' + '{:.2f}'.format(
                amount_tax_19) + '|' + '{:.2f}'.format(amount_disc_19) + '|' \
                      + '{:.2f}'.format(amount_service_19) + '|' + str(amount_pax_19) + '|' + '{:.2f}'.format(
                amount_cash_19) + '|' + '{:.2f}'.format(amount_atm_19) \
                      + '|' + '{:.2f}'.format(amount_visa_19) + '|' + '{:.2f}'.format(
                amount_mastercard_19) + '|' + '{:.2f}'.format(amount_amex_19) \
                      + '|' + '{:.2f}'.format(amount_voucher_19) + '|' + '{:.2f}'.format(
                amount_other_19) + '|' + 'Y'
        if orders_count_20 == 0:
            line_20 += line_no_data
        else:
            line_20 = line_20 + '|' + '{:.2f}'.format(amount_total_20) + '|' + '{:.2f}'.format(
                amount_tax_20) + '|' + '{:.2f}'.format(amount_disc_20) + '|' \
                      + '{:.2f}'.format(amount_service_20) + '|' + str(amount_pax_20) + '|' + '{:.2f}'.format(
                amount_cash_20) + '|' + '{:.2f}'.format(amount_atm_20) \
                      + '|' + '{:.2f}'.format(amount_visa_20) + '|' + '{:.2f}'.format(
                amount_mastercard_20) + '|' + '{:.2f}'.format(amount_amex_20) \
                      + '|' + '{:.2f}'.format(amount_voucher_20) + '|' + '{:.2f}'.format(
                amount_other_20) + '|' + 'Y'
        if orders_count_21 == 0:
            line_21 += line_no_data
        else:
            line_21 = line_21 + '|' + '{:.2f}'.format(amount_total_21) + '|' + '{:.2f}'.format(
                amount_tax_21) + '|' + '{:.2f}'.format(amount_disc_21) + '|' \
                      + '{:.2f}'.format(amount_service_21) + '|' + str(amount_pax_21) + '|' + '{:.2f}'.format(
                amount_cash_21) + '|' + '{:.2f}'.format(amount_atm_21) \
                      + '|' + '{:.2f}'.format(amount_visa_21) + '|' + '{:.2f}'.format(
                amount_mastercard_21) + '|' + '{:.2f}'.format(amount_amex_21) \
                      + '|' + '{:.2f}'.format(amount_voucher_21) + '|' + '{:.2f}'.format(
                amount_other_21) + '|' + 'Y'
        if orders_count_22 == 0:
            line_22 += line_no_data
        else:
            line_22 = line_22 + '|' + '{:.2f}'.format(amount_total_22) + '|' + '{:.2f}'.format(
                amount_tax_22) + '|' + '{:.2f}'.format(amount_disc_22) + '|' \
                      + '{:.2f}'.format(amount_service_22) + '|' + str(amount_pax_22) + '|' + '{:.2f}'.format(
                amount_cash_22) + '|' + '{:.2f}'.format(amount_atm_22) \
                      + '|' + '{:.2f}'.format(amount_visa_22) + '|' + '{:.2f}'.format(
                amount_mastercard_22) + '|' + '{:.2f}'.format(amount_amex_22) \
                      + '|' + '{:.2f}'.format(amount_voucher_22) + '|' + '{:.2f}'.format(
                amount_other_22) + '|' + 'Y'
        if orders_count_23 == 0:
            line_23 += line_no_data
        else:
            line_23 = line_23 + '|' + '{:.2f}'.format(amount_total_23) + '|' + '{:.2f}'.format(
                amount_tax_23) + '|' + '{:.2f}'.format(amount_disc_23) + '|' \
                      + '{:.2f}'.format(amount_service_23) + '|' + str(amount_pax_23) + '|' + '{:.2f}'.format(
                amount_cash_23) + '|' + '{:.2f}'.format(amount_atm_23) \
                      + '|' + '{:.2f}'.format(amount_visa_23) + '|' + '{:.2f}'.format(
                amount_mastercard_23) + '|' + '{:.2f}'.format(amount_amex_23) \
                      + '|' + '{:.2f}'.format(amount_voucher_23) + '|' + '{:.2f}'.format(
                amount_other_23) + '|' + 'Y'
        print(line_0)
        print(line_1)
        print(line_2)
        print(line_3)
        print(line_4)
        print(line_5)
        print(line_6)
        print(line_7)
        print(line_8)
        print(line_9)
        print(line_10)
        print(line_11)
        print(line_12)
        print(line_13)
        print(line_14)
        print(line_15)
        print(line_16)
        print(line_17)
        print(line_18)
        print(line_19)
        print(line_20)
        print(line_21)
        print(line_22)
        print(line_23)

        sea_prefix = 'H17000025_'
        sea_vivo_date_str = date_cron_file_name
        sea_file_name = sea_prefix + sea_vivo_date_str + '.txt'
        try:
            # Use Linux
            with open('/opt/odoo/vivo_report/' + sea_file_name, 'w') as wf:

            # Use Windows
            # with open(os.getcwd() + '\\vivo_report' + '\\' + sea_file_name, 'w') as wf:
                data_line = (line_0 + '\n' + line_1 + '\n' + line_2 + '\n' + line_3 + '\n' + line_4 + '\n' + line_5 + '\n'
                             + line_6 + '\n' + line_7 + '\n' + line_8 + '\n' + line_9 + '\n' + line_10 + '\n' + line_11
                             + '\n' + line_12 + '\n' + line_13 + '\n' + line_14 + '\n' + line_15 + '\n' + line_16
                             + '\n' + line_17 + '\n' + line_18 + '\n' + line_19 + '\n' + line_20 + '\n' + line_21
                             + '\n' + line_22 + '\n' + line_23)
                wf.write(data_line)
        except:
            print("Error creating txt file")
            _logger.info("Error creating txt file")

        # Send File to SFTP
        host = 'scvivocity.synthesis.bz'
        port = 22
        username = '17000025'
        password = 'UVuSNEY8'
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            conn = pysftp.Connection(host=host, port=port, username=username, password=password, cnopts=cnopts)
            print("Connection established successfully")
            _logger.info("Connection established successfully..!")
        except:
            print('Failed to establish connection to targeted server')
            _logger.error("Failed to establish connection to targeted server..!")
        try:
            # Use Linux
            local_file = '/opt/odoo/vivo_report/' + sea_file_name

            # Use Windows
            # local_file = os.getcwd() + '\\vivo_report' + '\\' + sea_file_name

            target_location = sea_file_name
            conn.put(local_file, target_location)
            print('Push Successfully..!')
            _logger.info("Push Successfully..!")
        except:
            print('Push Fail..!')
            _logger.error("Push Fail..!")

    def button_get_txt(self):
        orders = self.get_config_data()
        orders_count_0 = 0
        orders_count_1 = 0
        orders_count_2 = 0
        orders_count_3 = 0
        orders_count_4 = 0
        orders_count_5 = 0
        orders_count_6 = 0

        orders_count_7 = 0
        amount_total_7 = 0
        amount_tax_7 = 0
        amount_disc_7 = 0
        amount_service_7 = 0
        amount_pax_7 = 0
        amount_cash_7 = 0
        amount_atm_7 = 0
        amount_visa_7 = 0
        amount_mastercard_7 = 0
        amount_amex_7 = 0
        amount_voucher_7 = 0
        amount_other_7 = 0

        orders_count_8 = 0
        amount_total_8 = 0
        amount_tax_8 = 0
        amount_disc_8 = 0
        amount_service_8 = 0
        amount_pax_8 = 0
        amount_cash_8 = 0
        amount_atm_8 = 0
        amount_visa_8 = 0
        amount_mastercard_8 = 0
        amount_amex_8 = 0
        amount_voucher_8 = 0
        amount_other_8 = 0

        orders_count_9 = 0
        amount_total_9 = 0
        amount_tax_9 = 0
        amount_disc_9 = 0
        amount_service_9 = 0
        amount_pax_9 = 0
        amount_cash_9 = 0
        amount_atm_9 = 0
        amount_visa_9 = 0
        amount_mastercard_9 = 0
        amount_amex_9 = 0
        amount_voucher_9 = 0
        amount_other_9 = 0

        orders_count_10 = 0
        amount_total_10 = 0
        amount_tax_10 = 0
        amount_disc_10 = 0
        amount_service_10 = 0
        amount_pax_10 = 0
        amount_cash_10 = 0
        amount_atm_10 = 0
        amount_visa_10 = 0
        amount_mastercard_10 = 0
        amount_amex_10 = 0
        amount_voucher_10 = 0
        amount_other_10 = 0

        orders_count_11 = 0
        amount_total_11 = 0
        amount_tax_11 = 0
        amount_disc_11 = 0
        amount_service_11 = 0
        amount_pax_11 = 0
        amount_cash_11 = 0
        amount_atm_11 = 0
        amount_visa_11 = 0
        amount_mastercard_11 = 0
        amount_amex_11 = 0
        amount_voucher_11 = 0
        amount_other_11 = 0

        orders_count_12 = 0
        amount_total_12 = 0
        amount_tax_12 = 0
        amount_disc_12 = 0
        amount_service_12 = 0
        amount_pax_12 = 0
        amount_cash_12 = 0
        amount_atm_12 = 0
        amount_visa_12 = 0
        amount_mastercard_12 = 0
        amount_amex_12 = 0
        amount_voucher_12 = 0
        amount_other_12 = 0

        orders_count_13 = 0
        amount_total_13 = 0
        amount_tax_13 = 0
        amount_disc_13 = 0
        amount_service_13 = 0
        amount_pax_13 = 0
        amount_cash_13 = 0
        amount_atm_13 = 0
        amount_visa_13 = 0
        amount_mastercard_13 = 0
        amount_amex_13 = 0
        amount_voucher_13 = 0
        amount_other_13 = 0

        orders_count_14 = 0
        amount_total_14 = 0
        amount_tax_14 = 0
        amount_disc_14 = 0
        amount_service_14 = 0
        amount_pax_14 = 0
        amount_cash_14 = 0
        amount_atm_14 = 0
        amount_visa_14 = 0
        amount_mastercard_14 = 0
        amount_amex_14 = 0
        amount_voucher_14 = 0
        amount_other_14 = 0

        orders_count_15 = 0
        amount_total_15 = 0
        amount_tax_15 = 0
        amount_disc_15 = 0
        amount_service_15 = 0
        amount_pax_15 = 0
        amount_cash_15 = 0
        amount_atm_15 = 0
        amount_visa_15 = 0
        amount_mastercard_15 = 0
        amount_amex_15 = 0
        amount_voucher_15 = 0
        amount_other_15 = 0

        orders_count_16 = 0
        amount_total_16 = 0
        amount_tax_16 = 0
        amount_disc_16 = 0
        amount_service_16 = 0
        amount_pax_16 = 0
        amount_cash_16 = 0
        amount_atm_16 = 0
        amount_visa_16 = 0
        amount_mastercard_16 = 0
        amount_amex_16 = 0
        amount_voucher_16 = 0
        amount_other_16 = 0

        orders_count_17 = 0
        amount_total_17 = 0
        amount_tax_17 = 0
        amount_disc_17 = 0
        amount_service_17 = 0
        amount_pax_17 = 0
        amount_cash_17 = 0
        amount_atm_17 = 0
        amount_visa_17 = 0
        amount_mastercard_17 = 0
        amount_amex_17 = 0
        amount_voucher_17 = 0
        amount_other_17 = 0

        orders_count_18 = 0
        amount_total_18 = 0
        amount_tax_18 = 0
        amount_disc_18 = 0
        amount_service_18 = 0
        amount_pax_18 = 0
        amount_cash_18 = 0
        amount_atm_18 = 0
        amount_visa_18 = 0
        amount_mastercard_18 = 0
        amount_amex_18 = 0
        amount_voucher_18 = 0
        amount_other_18 = 0

        orders_count_19 = 0
        amount_total_19 = 0
        amount_tax_19 = 0
        amount_disc_19 = 0
        amount_service_19 = 0
        amount_pax_19 = 0
        amount_cash_19 = 0
        amount_atm_19 = 0
        amount_visa_19 = 0
        amount_mastercard_19 = 0
        amount_amex_19 = 0
        amount_voucher_19 = 0
        amount_other_19 = 0

        orders_count_20 = 0
        amount_total_20 = 0
        amount_tax_20 = 0
        amount_disc_20 = 0
        amount_service_20 = 0
        amount_pax_20 = 0
        amount_cash_20 = 0
        amount_atm_20 = 0
        amount_visa_20 = 0
        amount_mastercard_20 = 0
        amount_amex_20 = 0
        amount_voucher_20 = 0
        amount_other_20 = 0

        orders_count_21 = 0
        amount_total_21 = 0
        amount_tax_21 = 0
        amount_disc_21 = 0
        amount_service_21 = 0
        amount_pax_21 = 0
        amount_cash_21 = 0
        amount_atm_21 = 0
        amount_visa_21 = 0
        amount_mastercard_21 = 0
        amount_amex_21 = 0
        amount_voucher_21 = 0
        amount_other_21 = 0

        orders_count_22 = 0
        amount_total_22 = 0
        amount_tax_22 = 0
        amount_disc_22 = 0
        amount_service_22 = 0
        amount_pax_22 = 0
        amount_cash_22 = 0
        amount_atm_22 = 0
        amount_visa_22 = 0
        amount_mastercard_22 = 0
        amount_amex_22 = 0
        amount_voucher_22 = 0
        amount_other_22 = 0

        orders_count_23 = 0
        amount_total_23 = 0
        amount_tax_23 = 0
        amount_disc_23 = 0
        amount_service_23 = 0
        amount_pax_23 = 0
        amount_cash_23 = 0
        amount_atm_23 = 0
        amount_visa_23 = 0
        amount_mastercard_23 = 0
        amount_amex_23 = 0
        amount_voucher_23 = 0
        amount_other_23 = 0

        time_tz_7 = datetime.timedelta(hours=7)
        time_tz_1 = datetime.timedelta(hours=1)
        if len(orders) > 0:
            date_order_share = ''
            date_order_real = ''
            pos_session = ''
        else:
            date = self.start_date + time_tz_7
            date_order_share = ''.join(str(date.strftime('%d/%m/%Y')).split('/'))
            date_order_real = ''.join(str(date.strftime('%Y/%m/%d')).split('/'))
            pos_session = '0'

        for order in reversed(orders):
            date_order_share = ''.join(str(order.date_order.strftime('%d/%m/%Y')).split('/'))
            date_order_real = ''.join(str(order.date_order.strftime('%Y/%m/%d')).split('/'))
            pos_session = (str(order.session_id.name)[-4:])

            order_date_real = order.date_order + time_tz_7
            date_time_order = order.date_order
            get_year_order = date_time_order.year
            get_month_order = date_time_order.month
            get_day_order = date_time_order.day

            date_time_0 = datetime.datetime(get_year_order, get_month_order, get_day_order, 0, 0)
            date_time_1 = date_time_0 + time_tz_1
            date_time_2 = date_time_1 + time_tz_1
            date_time_3 = date_time_2 + time_tz_1
            date_time_4 = date_time_3 + time_tz_1
            date_time_5 = date_time_4 + time_tz_1
            date_time_6 = date_time_5 + time_tz_1
            date_time_7 = date_time_6 + time_tz_1
            date_time_8 = date_time_7 + time_tz_1
            date_time_9 = date_time_8 + time_tz_1
            date_time_10 = date_time_9 + time_tz_1
            date_time_11 = date_time_10 + time_tz_1
            date_time_12 = date_time_11 + time_tz_1
            date_time_13 = date_time_12 + time_tz_1
            date_time_14 = date_time_13 + time_tz_1
            date_time_15 = date_time_14 + time_tz_1
            date_time_16 = date_time_15 + time_tz_1
            date_time_17 = date_time_16 + time_tz_1
            date_time_18 = date_time_17 + time_tz_1
            date_time_19 = date_time_18 + time_tz_1
            date_time_20 = date_time_19 + time_tz_1
            date_time_21 = date_time_20 + time_tz_1
            date_time_22 = date_time_21 + time_tz_1
            date_time_23 = date_time_22 + time_tz_1

            cash = 0
            atm = 0
            voucher = 0
            other = 0

            if date_time_0 <= order_date_real <= date_time_1:
                orders_count_0 += 1
            elif date_time_1 <= order_date_real <= date_time_2:
                orders_count_1 += 1
            elif date_time_2 <= order_date_real <= date_time_3:
                orders_count_2 += 1
            elif date_time_3 <= order_date_real <= date_time_4:
                orders_count_3 += 1
            elif date_time_4 <= order_date_real <= date_time_5:
                orders_count_4 += 1
            elif date_time_5 <= order_date_real <= date_time_6:
                orders_count_5 += 1
            elif date_time_6 <= order_date_real <= date_time_7:
                orders_count_6 += 1
            elif date_time_7 <= order_date_real <= date_time_8:
                orders_count_7 += 1
            elif date_time_8 <= order_date_real <= date_time_9:
                orders_count_8 += 1
                amount_total_8 += round(order.amount_total - order.amount_tax)
                amount_tax_8 += round(order.amount_tax)
                tax_line_8 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_8 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_8 += cash - tax_line_8
                        amount_atm_8 += atm
                    else:
                        amount_cash_8 += cash
                        amount_atm_8 += atm - tax_line_8
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_8 += cash - tax_line_8
                        amount_voucher_8 += voucher
                    else:
                        amount_cash_8 += cash
                        amount_voucher_8 += voucher - tax_line_8
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_8 += cash - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_cash_8 += cash
                        amount_other_8 += other - tax_line_8
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_8 += atm - tax_line_8
                        amount_voucher_8 += voucher
                    else:
                        amount_atm_8 += atm
                        amount_voucher_8 += voucher - tax_line_8
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_8 += atm - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_atm_8 += atm
                        amount_other_8 += other - tax_line_8
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_8 += voucher - tax_line_8
                        amount_other_8 += other
                    else:
                        amount_voucher_8 += voucher
                        amount_other_8 += other - tax_line_8
                elif abs(cash) > 0:
                    amount_cash_8 += cash - tax_line_8
                elif abs(atm) > 0:
                    amount_atm_8 += atm - tax_line_8
                elif abs(voucher) > 0:
                    amount_voucher_8 += voucher - tax_line_8
                elif abs(other) > 0:
                    amount_other_8 += other - tax_line_8

            elif date_time_9 <= order_date_real <= date_time_10:
                orders_count_9 += 1
                amount_total_9 += round(order.amount_total - order.amount_tax)
                amount_tax_9 += round(order.amount_tax)
                tax_line_9 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_9 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_9 += cash - tax_line_9
                        amount_atm_9 += atm
                    else:
                        amount_cash_9 += cash
                        amount_atm_9 += atm - tax_line_9
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_9 += cash - tax_line_9
                        amount_voucher_9 += voucher
                    else:
                        amount_cash_9 += cash
                        amount_voucher_9 += voucher - tax_line_9
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_9 += cash - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_cash_9 += cash
                        amount_other_9 += other - tax_line_9
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_9 += atm - tax_line_9
                        amount_voucher_9 += voucher
                    else:
                        amount_atm_9 += atm
                        amount_voucher_9 += voucher - tax_line_9
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_9 += atm - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_atm_9 += atm
                        amount_other_9 += other - tax_line_9
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_9 += voucher - tax_line_9
                        amount_other_9 += other
                    else:
                        amount_voucher_9 += voucher
                        amount_other_9 += other - tax_line_9
                elif abs(cash) > 0:
                    amount_cash_9 += cash - tax_line_9
                elif abs(atm) > 0:
                    amount_atm_9 += atm - tax_line_9
                elif abs(voucher) > 0:
                    amount_voucher_9 += voucher - tax_line_9
                elif abs(other) > 0:
                    amount_other_9 += other - tax_line_9

            elif date_time_10 <= order_date_real <= date_time_11:
                orders_count_10 += 1
                amount_total_10 += round(order.amount_total - order.amount_tax)
                amount_tax_10 += round(order.amount_tax)
                tax_line_10 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_10 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_10 += cash - tax_line_10
                        amount_atm_10 += atm
                    else:
                        amount_cash_10 += cash
                        amount_atm_10 += atm - tax_line_10
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_10 += cash - tax_line_10
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_10 += cash
                        amount_voucher_10 += voucher - tax_line_10
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_10 += cash - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_cash_10 += cash
                        amount_other_10 += other - tax_line_10
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_10 += atm - tax_line_10
                        amount_voucher_10 += voucher
                    else:
                        amount_atm_10 += atm
                        amount_voucher_10 += voucher - tax_line_10
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_10 += atm - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_atm_10 += atm
                        amount_other_10 += other - tax_line_10
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_10 += voucher - tax_line_10
                        amount_other_10 += other
                    else:
                        amount_voucher_10 += voucher
                        amount_other_10 += other - tax_line_10
                elif abs(cash) > 0:
                    amount_cash_10 += cash - tax_line_10
                elif abs(atm) > 0:
                    amount_atm_10 += atm - tax_line_10
                elif abs(voucher) > 0:
                    amount_voucher_10 += voucher - tax_line_10
                elif abs(other) > 0:
                    amount_other_10 += other - tax_line_10

            elif date_time_11 <= order_date_real <= date_time_12:
                orders_count_11 += 1
                amount_total_11 += round(order.amount_total - order.amount_tax)
                amount_tax_11 += round(order.amount_tax)
                tax_line_11 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_11 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_11 += cash - tax_line_11
                        amount_atm_11 += atm
                    else:
                        amount_cash_11 += cash
                        amount_atm_11 += atm - tax_line_11
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_11 += cash - tax_line_11
                        amount_voucher_11 += voucher
                    else:
                        amount_cash_11 += cash
                        amount_voucher_11 += voucher - tax_line_11
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_11 += cash - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_cash_11 += cash
                        amount_other_11 += other - tax_line_11
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_11 += atm - tax_line_11
                        amount_voucher_11 += voucher
                    else:
                        amount_atm_11 += atm
                        amount_voucher_11 += voucher - tax_line_11
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_11 += atm - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_atm_11 += atm
                        amount_other_11 += other - tax_line_11
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_11 += voucher - tax_line_11
                        amount_other_11 += other
                    else:
                        amount_voucher_11 += voucher
                        amount_other_11 += other - tax_line_11
                elif abs(cash) > 0:
                    amount_cash_11 += cash - tax_line_11
                elif abs(atm) > 0:
                    amount_atm_11 += atm - tax_line_11
                elif abs(voucher) > 0:
                    amount_voucher_11 += voucher - tax_line_11
                elif abs(other) > 0:
                    amount_other_11 += other - tax_line_11

            elif date_time_12 <= order_date_real <= date_time_13:
                orders_count_12 += 1
                amount_total_12 += round(order.amount_total - order.amount_tax)
                amount_tax_12 += round(order.amount_tax)
                tax_line_12 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_12 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_12 += cash - tax_line_12
                        amount_atm_12 += atm
                    else:
                        amount_cash_12 += cash
                        amount_atm_12 += atm - tax_line_12
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_12 += cash - tax_line_12
                        amount_voucher_12 += voucher
                    else:
                        amount_cash_12 += cash
                        amount_voucher_12 += voucher - tax_line_12
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_12 += cash - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_cash_12 += cash
                        amount_other_12 += other - tax_line_12
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_12 += atm - tax_line_12
                        amount_voucher_12 += voucher
                    else:
                        amount_atm_12 += atm
                        amount_voucher_12 += voucher - tax_line_12
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_12 += atm - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_atm_12 += atm
                        amount_other_12 += other - tax_line_12
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_12 += voucher - tax_line_12
                        amount_other_12 += other
                    else:
                        amount_voucher_12 += voucher
                        amount_other_12 += other - tax_line_12
                elif abs(cash) > 0:
                    amount_cash_12 += cash - tax_line_12
                elif abs(atm) > 0:
                    amount_atm_12 += atm - tax_line_12
                elif abs(voucher) > 0:
                    amount_voucher_12 += voucher - tax_line_12
                elif abs(other) > 0:
                    amount_other_12 += other - tax_line_12

            elif date_time_13 <= order_date_real <= date_time_14:
                orders_count_13 += 1
                amount_total_13 += round(order.amount_total - order.amount_tax)
                amount_tax_13 += round(order.amount_tax)
                tax_line_13 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_13 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_13 += cash - tax_line_13
                        amount_atm_13 += atm
                    else:
                        amount_cash_13 += cash
                        amount_atm_13 += atm - tax_line_13
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_13 += cash - tax_line_13
                        amount_voucher_13 += voucher
                    else:
                        amount_cash_13 += cash
                        amount_voucher_13 += voucher - tax_line_13
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_13 += cash - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_cash_13 += cash
                        amount_other_13 += other - tax_line_13
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_13 += atm - tax_line_13
                        amount_voucher_13 += voucher
                    else:
                        amount_atm_13 += atm
                        amount_voucher_13 += voucher - tax_line_13
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_13 += atm - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_atm_13 += atm
                        amount_other_13 += other - tax_line_13
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_13 += voucher - tax_line_13
                        amount_other_13 += other
                    else:
                        amount_voucher_13 += voucher
                        amount_other_13 += other - tax_line_13
                elif abs(cash) > 0:
                    amount_cash_13 += cash - tax_line_13
                elif abs(atm) > 0:
                    amount_atm_13 += atm - tax_line_13
                elif abs(voucher) > 0:
                    amount_voucher_13 += voucher - tax_line_13
                elif abs(other) > 0:
                    amount_other_13 += other - tax_line_13

            elif date_time_14 <= order_date_real <= date_time_15:
                orders_count_14 += 1
                amount_total_14 += round(order.amount_total - order.amount_tax)
                amount_tax_14 += round(order.amount_tax)
                tax_line_14 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_14 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_14 += cash - tax_line_14
                        amount_atm_14 += atm
                    else:
                        amount_cash_14 += cash
                        amount_atm_14 += atm - tax_line_14
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_14 += cash - tax_line_14
                        amount_voucher_14 += voucher
                    else:
                        amount_cash_14 += cash
                        amount_voucher_14 += voucher - tax_line_14
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_14 += cash - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_cash_14 += cash
                        amount_other_14 += other - tax_line_14
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_14 += atm - tax_line_14
                        amount_voucher_14 += voucher
                    else:
                        amount_atm_14 += atm
                        amount_voucher_14 += voucher - tax_line_14
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_14 += atm - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_atm_14 += atm
                        amount_other_14 += other - tax_line_14
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_14 += voucher - tax_line_14
                        amount_other_14 += other
                    else:
                        amount_voucher_14 += voucher
                        amount_other_14 += other - tax_line_14
                elif abs(cash) > 0:
                    amount_cash_14 += cash - tax_line_14
                elif abs(atm) > 0:
                    amount_atm_14 += atm - tax_line_14
                elif abs(voucher) > 0:
                    amount_voucher_14 += voucher - tax_line_14
                elif abs(other) > 0:
                    amount_other_14 += other - tax_line_14

            elif date_time_15 <= order_date_real <= date_time_16:
                orders_count_15 += 1
                amount_total_15 += round(order.amount_total - order.amount_tax)
                amount_tax_15 += round(order.amount_tax)
                tax_line_15 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_15 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_15 += cash - tax_line_15
                        amount_atm_15 += atm
                    else:
                        amount_cash_15 += cash
                        amount_atm_15 += atm - tax_line_15
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_15 += cash - tax_line_15
                        amount_voucher_15 += voucher
                    else:
                        amount_cash_16 += cash
                        amount_voucher_15 += voucher - tax_line_15
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_15 += cash - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_cash_15 += cash
                        amount_other_15 += other - tax_line_15
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_15 += atm - tax_line_15
                        amount_voucher_16 += voucher
                    else:
                        amount_atm_15 += atm
                        amount_voucher_15 += voucher - tax_line_15
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_15 += atm - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_atm_15 += atm
                        amount_other_15 += other - tax_line_15
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_15 += voucher - tax_line_15
                        amount_other_15 += other
                    else:
                        amount_voucher_15 += voucher
                        amount_other_15 += other - tax_line_15
                elif abs(cash) > 0:
                    amount_cash_15 += cash - tax_line_15
                elif abs(atm) > 0:
                    amount_atm_15 += atm - tax_line_15
                elif abs(voucher) > 0:
                    amount_voucher_15 += voucher - tax_line_15
                elif abs(other) > 0:
                    amount_other_15 += other - tax_line_15

            elif date_time_16 <= order_date_real <= date_time_17:
                orders_count_16 += 1
                amount_total_16 += round(order.amount_total - order.amount_tax)
                amount_tax_16 += round(order.amount_tax)
                tax_line_16 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_16 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)

                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_16 += cash - tax_line_16
                        amount_atm_16 += atm
                    else:
                        amount_cash_16 += cash
                        amount_atm_16 += atm - tax_line_16
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_16 += cash - tax_line_16
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_16 += cash
                        amount_voucher_16 += voucher - tax_line_16
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_16 += cash - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_cash_16 += cash
                        amount_other_16 += other - tax_line_16
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_16 += atm - tax_line_16
                        amount_voucher_16 += voucher
                    else:
                        amount_atm_16 += atm
                        amount_voucher_16 += voucher - tax_line_16
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_16 += atm - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_atm_16 += atm
                        amount_other_16 += other - tax_line_16
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_16 += voucher - tax_line_16
                        amount_other_16 += other
                    else:
                        amount_voucher_16 += voucher
                        amount_other_16 += other - tax_line_16
                elif abs(cash) > 0:
                    amount_cash_16 += cash - tax_line_16
                elif abs(atm) > 0:
                    amount_atm_16 += atm - tax_line_16
                elif abs(voucher) > 0:
                    amount_voucher_16 += voucher - tax_line_16
                elif abs(other) > 0:
                    amount_other_16 += other - tax_line_16

            elif date_time_17 <= order_date_real <= date_time_18:
                orders_count_17 += 1
                amount_total_17 += round(order.amount_total - order.amount_tax)
                amount_tax_17 += round(order.amount_tax)
                tax_line_17 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_17 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_17 += cash - tax_line_17
                        amount_atm_17 += atm
                    else:
                        amount_cash_17 += cash
                        amount_atm_17 += atm - tax_line_17
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_17 += cash - tax_line_17
                        amount_voucher_17 += voucher
                    else:
                        amount_cash_17 += cash
                        amount_voucher_17 += voucher - tax_line_17
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_17 += cash - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_cash_17 += cash
                        amount_other_17 += other - tax_line_17
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_17 += atm - tax_line_17
                        amount_voucher_17 += voucher
                    else:
                        amount_atm_17 += atm
                        amount_voucher_17 += voucher - tax_line_17
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_17 += atm - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_atm_17 += atm
                        amount_other_17 += other - tax_line_17
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_17 += voucher - tax_line_17
                        amount_other_17 += other
                    else:
                        amount_voucher_17 += voucher
                        amount_other_17 += other - tax_line_17
                elif abs(cash) > 0:
                    amount_cash_17 += cash - tax_line_17
                elif abs(atm) > 0:
                    amount_atm_17 += atm - tax_line_17
                elif abs(voucher) > 0:
                    amount_voucher_17 += voucher - tax_line_17
                elif abs(other) > 0:
                    amount_other_17 += other - tax_line_17

            elif date_time_18 <= order_date_real <= date_time_19:
                orders_count_18 += 1
                amount_total_18 += round(order.amount_total - order.amount_tax)
                amount_tax_18 += round(order.amount_tax)
                tax_line_18 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_18 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_18 += cash - tax_line_18
                        amount_atm_18 += atm
                    else:
                        amount_cash_18 += cash
                        amount_atm_18 += atm - tax_line_18
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_18 += cash - tax_line_18
                        amount_voucher_16 += voucher
                    else:
                        amount_cash_18 += cash
                        amount_voucher_16 += voucher - tax_line_18
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_18 += cash - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_cash_18 += cash
                        amount_other_18 += other - tax_line_18
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_18 += atm - tax_line_18
                        amount_voucher_18 += voucher
                    else:
                        amount_atm_18 += atm
                        amount_voucher_18 += voucher - tax_line_18
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_18 += atm - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_atm_18 += atm
                        amount_other_18 += other - tax_line_18
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_18 += voucher - tax_line_18
                        amount_other_18 += other
                    else:
                        amount_voucher_18 += voucher
                        amount_other_18 += other - tax_line_18
                elif abs(cash) > 0:
                    amount_cash_18 += cash - tax_line_18
                elif abs(atm) > 0:
                    amount_atm_18 += atm - tax_line_18
                elif abs(voucher) > 0:
                    amount_voucher_18 += voucher - tax_line_18
                elif abs(other) > 0:
                    amount_other_18 += other - tax_line_18

            elif date_time_19 <= order_date_real <= date_time_20:
                orders_count_19 += 1
                amount_total_19 += round(order.amount_total - order.amount_tax)
                amount_tax_19 += round(order.amount_tax)
                tax_line_19 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_19 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_19 += cash - tax_line_19
                        amount_atm_19 += atm
                    else:
                        amount_cash_19 += cash
                        amount_atm_19 += atm - tax_line_19
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_19 += cash - tax_line_19
                        amount_voucher_19 += voucher
                    else:
                        amount_cash_19 += cash
                        amount_voucher_19 += voucher - tax_line_19
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_19 += cash - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_cash_19 += cash
                        amount_other_19 += other - tax_line_19
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_19 += atm - tax_line_19
                        amount_voucher_19 += voucher
                    else:
                        amount_atm_19 += atm
                        amount_voucher_19 += voucher - tax_line_19
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_19 += atm - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_atm_19 += atm
                        amount_other_19 += other - tax_line_19
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_19 += voucher - tax_line_19
                        amount_other_19 += other
                    else:
                        amount_voucher_19 += voucher
                        amount_other_19 += other - tax_line_19
                elif abs(cash) > 0:
                    amount_cash_19 += cash - tax_line_19
                elif abs(atm) > 0:
                    amount_atm_19 += atm - tax_line_19
                elif abs(voucher) > 0:
                    amount_voucher_19 += voucher - tax_line_19
                elif abs(other) > 0:
                    amount_other_19 += other - tax_line_19

            elif date_time_20 <= order_date_real <= date_time_21:
                orders_count_20 += 1
                amount_total_20 += round(order.amount_total - order.amount_tax)
                amount_tax_20 += round(order.amount_tax)
                tax_line_20 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_20 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_20 += cash - tax_line_20
                        amount_atm_20 += atm
                    else:
                        amount_cash_20 += cash
                        amount_atm_20 += atm - tax_line_20
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_20 += cash - tax_line_20
                        amount_voucher_20 += voucher
                    else:
                        amount_cash_20 += cash
                        amount_voucher_20 += voucher - tax_line_20
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_20 += cash - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_cash_20 += cash
                        amount_other_20 += other - tax_line_20
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_20 += atm - tax_line_20
                        amount_voucher_20 += voucher
                    else:
                        amount_atm_20 += atm
                        amount_voucher_20 += voucher - tax_line_20
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_20 += atm - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_atm_20 += atm
                        amount_other_20 += other - tax_line_20
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_20 += voucher - tax_line_20
                        amount_other_20 += other
                    else:
                        amount_voucher_20 += voucher
                        amount_other_20 += other - tax_line_20
                elif abs(cash) > 0:
                    amount_cash_20 += cash - tax_line_20
                elif abs(atm) > 0:
                    amount_atm_20 += atm - tax_line_20
                elif abs(voucher) > 0:
                    amount_voucher_20 += voucher - tax_line_20
                elif abs(other) > 0:
                    amount_other_20 += other - tax_line_20

            elif date_time_21 <= order_date_real <= date_time_22:
                orders_count_21 += 1
                amount_total_21 += round(order.amount_total - order.amount_tax)
                amount_tax_21 += round(order.amount_tax)
                tax_line_21 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_21 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_21 += cash - tax_line_21
                        amount_atm_21 += atm
                    else:
                        amount_cash_21 += cash
                        amount_atm_21 += atm - tax_line_21
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_21 += cash - tax_line_21
                        amount_voucher_21 += voucher
                    else:
                        amount_cash_21 += cash
                        amount_voucher_21 += voucher - tax_line_21
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_21 += cash - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_cash_21 += cash
                        amount_other_21 += other - tax_line_21
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_21 += atm - tax_line_21
                        amount_voucher_21 += voucher
                    else:
                        amount_atm_21 += atm
                        amount_voucher_21 += voucher - tax_line_21
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_21 += atm - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_atm_21 += atm
                        amount_other_21 += other - tax_line_21
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_21 += voucher - tax_line_21
                        amount_other_21 += other
                    else:
                        amount_voucher_21 += voucher
                        amount_other_21 += other - tax_line_21
                elif abs(cash) > 0:
                    amount_cash_21 += cash - tax_line_21
                elif abs(atm) > 0:
                    amount_atm_21 += atm - tax_line_21
                elif abs(voucher) > 0:
                    amount_voucher_21 += voucher - tax_line_21
                elif abs(other) > 0:
                    amount_other_21 += other - tax_line_21

            elif date_time_22 <= order_date_real <= date_time_23:
                orders_count_22 += 1
                amount_total_22 += round(order.amount_total - order.amount_tax)
                amount_tax_22 += round(order.amount_tax)
                tax_line_22 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_22 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_22 += cash - tax_line_22
                        amount_atm_22 += atm
                    else:
                        amount_cash_22 += cash
                        amount_atm_22 += atm - tax_line_22
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_22 += cash - tax_line_22
                        amount_voucher_22 += voucher
                    else:
                        amount_cash_22 += cash
                        amount_voucher_22 += voucher - tax_line_22
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_22 += cash - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_cash_22 += cash
                        amount_other_22 += other - tax_line_22
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_22 += atm - tax_line_22
                        amount_voucher_22 += voucher
                    else:
                        amount_atm_22 += atm
                        amount_voucher_22 += voucher - tax_line_22
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_22 += atm - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_atm_22 += atm
                        amount_other_22 += other - tax_line_22
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_22 += voucher - tax_line_22
                        amount_other_22 += other
                    else:
                        amount_voucher_22 += voucher
                        amount_other_22 += other - tax_line_22
                elif abs(cash) > 0:
                    amount_cash_22 += cash - tax_line_22
                elif abs(atm) > 0:
                    amount_atm_22 += atm - tax_line_22
                elif abs(voucher) > 0:
                    amount_voucher_22 += voucher - tax_line_22
                elif abs(other) > 0:
                    amount_other_22 += other - tax_line_22

            elif date_time_23 <= order_date_real <= date_time_0:
                orders_count_23 += 1
                amount_total_23 += round(order.amount_total - order.amount_tax)
                amount_tax_23 += round(order.amount_tax)
                tax_line_23 = round(order.amount_tax)
                for line in order.lines:
                    amount_disc_23 += round((line.qty * line.price_unit * line.discount) / 100)
                for payment in order.statement_ids:
                    if payment.journal_id.type == 'cash' and payment.journal_id.id != 18:
                        cash += round(payment.amount)
                    if payment.journal_id.id == 23:
                        atm += round(payment.amount)
                    if payment.journal_id.id == 18:
                        voucher += round(payment.amount)
                    if payment.journal_id.id == 24:
                        other += round(payment.amount)
                if abs(cash) > 0 and abs(atm) > 0:
                    if abs(cash) >= abs(atm):
                        amount_cash_23 += cash - tax_line_23
                        amount_atm_23 += atm
                    else:
                        amount_cash_23 += cash
                        amount_atm_23 += atm - tax_line_23
                elif abs(cash) > 0 and abs(voucher) > 0:
                    if abs(cash) >= abs(voucher):
                        amount_cash_23 += cash - tax_line_23
                        amount_voucher_23 += voucher
                    else:
                        amount_cash_23 += cash
                        amount_voucher_23 += voucher - tax_line_23
                elif abs(cash) > 0 and abs(other) > 0:
                    if abs(cash) >= abs(other):
                        amount_cash_23 += cash - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_cash_23 += cash
                        amount_other_23 += other - tax_line_23
                elif abs(atm) > 0 and abs(voucher) > 0:
                    if abs(atm) >= abs(voucher):
                        amount_atm_23 += atm - tax_line_23
                        amount_voucher_23 += voucher
                    else:
                        amount_atm_23 += atm
                        amount_voucher_23 += voucher - tax_line_23
                elif abs(atm) > 0 and abs(other) > 0:
                    if abs(atm) >= abs(other):
                        amount_atm_23 += atm - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_atm_23 += atm
                        amount_other_23 += other - tax_line_23
                elif abs(voucher) > 0 and abs(other) > 0:
                    if abs(voucher) >= abs(other):
                        amount_voucher_23 += voucher - tax_line_23
                        amount_other_23 += other
                    else:
                        amount_voucher_23 += voucher
                        amount_other_23 += other - tax_line_23
                elif abs(cash) > 0:
                    amount_cash_23 += cash - tax_line_23
                elif abs(atm) > 0:
                    amount_atm_23 += atm - tax_line_23
                elif abs(voucher) > 0:
                    amount_voucher_23 += voucher - tax_line_23
                elif abs(other) > 0:
                    amount_other_23 += other - tax_line_23

        line_0 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '00' + '|' + str(orders_count_0)
        line_1 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '01' + '|' + str(orders_count_1)
        line_2 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '02' + '|' + str(orders_count_2)
        line_3 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '03' + '|' + str(orders_count_3)
        line_4 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '04' + '|' + str(orders_count_4)
        line_5 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '05' + '|' + str(orders_count_5)
        line_6 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '06' + '|' + str(orders_count_6)
        line_7 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '07' + '|' + str(orders_count_7)
        line_8 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '08' + '|' + str(orders_count_8)
        line_9 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '09' + '|' + str(orders_count_9)
        line_10 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '10' + '|' + str(orders_count_10)
        line_11 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '11' + '|' + str(orders_count_11)
        line_12 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '12' + '|' + str(orders_count_12)
        line_13 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '13' + '|' + str(orders_count_13)
        line_14 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '14' + '|' + str(orders_count_14)
        line_15 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '15' + '|' + str(orders_count_15)
        line_16 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '16' + '|' + str(orders_count_16)
        line_17 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '17' + '|' + str(orders_count_17)
        line_18 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '18' + '|' + str(orders_count_18)
        line_19 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '19' + '|' + str(orders_count_19)
        line_20 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '20' + '|' + str(orders_count_20)
        line_21 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '21' + '|' + str(orders_count_21)
        line_22 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '22' + '|' + str(orders_count_22)
        line_23 = '17000025' + '|' + pos_session + '|' + date_order_share + '|' + '23' + '|' + str(orders_count_23)

        line_no_data = '|0.00|0.00|0.00|0.00|0|0.00|0.00|0.00|0.00|0.00|0.00|0.00|Y'

        if orders_count_0 == 0:
            line_0 += line_no_data
        if orders_count_1 == 0:
            line_1 += line_no_data
        if orders_count_2 == 0:
            line_2 += line_no_data
        if orders_count_3 == 0:
            line_3 += line_no_data
        if orders_count_4 == 0:
            line_4 += line_no_data
        if orders_count_5 == 0:
            line_5 += line_no_data
        if orders_count_6 == 0:
            line_6 += line_no_data
        if orders_count_7 == 0:
            line_7 += line_no_data
        else:
            line_7 = line_7 + '|' + '{:.2f}'.format(amount_total_7) + '|' + '{:.2f}'.format(
                amount_tax_7) + '|' + '{:.2f}'.format(amount_disc_7) + '|' \
                     + '{:.2f}'.format(amount_service_7) + '|' + str(amount_pax_7) + '|' + '{:.2f}'.format(
                amount_cash_7) + '|' + '{:.2f}'.format(amount_atm_7) \
                     + '|' + '{:.2f}'.format(amount_visa_7) + '|' + '{:.2f}'.format(
                amount_mastercard_7) + '|' + '{:.2f}'.format(amount_amex_7) \
                     + '|' + '{:.2f}'.format(amount_voucher_7) + '|' + '{:.2f}'.format(amount_other_7) + '|' + 'Y'
        if orders_count_8 == 0:
            line_8 += line_no_data
        else:
            line_8 = line_8 + '|' + '{:.2f}'.format(amount_total_8) + '|' + '{:.2f}'.format(
                amount_tax_8) + '|' + '{:.2f}'.format(amount_disc_8) + '|' \
                     + '{:.2f}'.format(amount_service_8) + '|' + str(amount_pax_8) + '|' + '{:.2f}'.format(
                amount_cash_8) + '|' + '{:.2f}'.format(amount_atm_8) \
                     + '|' + '{:.2f}'.format(amount_visa_8) + '|' + '{:.2f}'.format(
                amount_mastercard_8) + '|' + '{:.2f}'.format(amount_amex_8) \
                     + '|' + '{:.2f}'.format(amount_voucher_8) + '|' + '{:.2f}'.format(amount_other_8) + '|' + 'Y'
        if orders_count_9 == 0:
            line_9 += line_no_data
        else:
            line_9 = line_9 + '|' + '{:.2f}'.format(amount_total_9) + '|' + '{:.2f}'.format(
                amount_tax_9) + '|' + '{:.2f}'.format(amount_disc_9) + '|' \
                     + '{:.2f}'.format(amount_service_9) + '|' + str(amount_pax_9) + '|' + '{:.2f}'.format(
                amount_cash_9) + '|' + '{:.2f}'.format(amount_atm_9) \
                     + '|' + '{:.2f}'.format(amount_visa_9) + '|' + '{:.2f}'.format(
                amount_mastercard_9) + '|' + '{:.2f}'.format(amount_amex_9) \
                     + '|' + '{:.2f}'.format(amount_voucher_9) + '|' + '{:.2f}'.format(amount_other_9) + '|' + 'Y'
        if orders_count_10 == 0:
            line_10 += line_no_data
        else:
            line_10 = line_10 + '|' + '{:.2f}'.format(amount_total_10) + '|' + '{:.2f}'.format(
                amount_tax_10) + '|' + '{:.2f}'.format(amount_disc_10) + '|' \
                      + '{:.2f}'.format(amount_service_10) + '|' + str(amount_pax_10) + '|' + '{:.2f}'.format(
                amount_cash_10) + '|' + '{:.2f}'.format(amount_atm_10) \
                      + '|' + '{:.2f}'.format(amount_visa_10) + '|' + '{:.2f}'.format(
                amount_mastercard_10) + '|' + '{:.2f}'.format(amount_amex_10) \
                      + '|' + '{:.2f}'.format(amount_voucher_10) + '|' + '{:.2f}'.format(amount_other_10) + '|' + 'Y'
        if orders_count_11 == 0:
            line_11 += line_no_data
        else:
            line_11 = line_11 + '|' + '{:.2f}'.format(amount_total_11) + '|' + '{:.2f}'.format(
                amount_tax_11) + '|' + '{:.2f}'.format(amount_disc_11) + '|' \
                      + '{:.2f}'.format(amount_service_11) + '|' + str(amount_pax_11) + '|' + '{:.2f}'.format(
                amount_cash_11) + '|' + '{:.2f}'.format(amount_atm_11) \
                      + '|' + '{:.2f}'.format(amount_visa_11) + '|' + '{:.2f}'.format(
                amount_mastercard_11) + '|' + '{:.2f}'.format(amount_amex_11) \
                      + '|' + '{:.2f}'.format(amount_voucher_11) + '|' + '{:.2f}'.format(amount_other_11) + '|' + 'Y'
        if orders_count_12 == 0:
            line_12 += line_no_data
        else:
            line_12 = line_12 + '|' + '{:.2f}'.format(amount_total_12) + '|' + '{:.2f}'.format(
                amount_tax_12) + '|' + '{:.2f}'.format(amount_disc_12) + '|' \
                      + '{:.2f}'.format(amount_service_12) + '|' + str(amount_pax_12) + '|' + '{:.2f}'.format(
                amount_cash_12) + '|' + '{:.2f}'.format(amount_atm_12) \
                      + '|' + '{:.2f}'.format(amount_visa_12) + '|' + '{:.2f}'.format(
                amount_mastercard_12) + '|' + '{:.2f}'.format(amount_amex_12) \
                      + '|' + '{:.2f}'.format(amount_voucher_12) + '|' + '{:.2f}'.format(amount_other_12) + '|' + 'Y'
        if orders_count_13 == 0:
            line_13 += line_no_data
        else:
            line_13 = line_13 + '|' + '{:.2f}'.format(amount_total_13) + '|' + '{:.2f}'.format(
                amount_tax_13) + '|' + '{:.2f}'.format(amount_disc_13) + '|' \
                      + '{:.2f}'.format(amount_service_13) + '|' + str(amount_pax_13) + '|' + '{:.2f}'.format(
                amount_cash_13) + '|' + '{:.2f}'.format(amount_atm_13) \
                      + '|' + '{:.2f}'.format(amount_visa_13) + '|' + '{:.2f}'.format(
                amount_mastercard_13) + '|' + '{:.2f}'.format(amount_amex_13) \
                      + '|' + '{:.2f}'.format(amount_voucher_13) + '|' + '{:.2f}'.format(amount_other_13) + '|' + 'Y'
        if orders_count_14 == 0:
            line_14 += line_no_data
        else:
            line_14 = line_14 + '|' + '{:.2f}'.format(amount_total_14) + '|' + '{:.2f}'.format(
                amount_tax_14) + '|' + '{:.2f}'.format(amount_disc_14) + '|' \
                      + '{:.2f}'.format(amount_service_14) + '|' + str(amount_pax_14) + '|' + '{:.2f}'.format(
                amount_cash_14) + '|' + '{:.2f}'.format(amount_atm_14) \
                      + '|' + '{:.2f}'.format(amount_visa_14) + '|' + '{:.2f}'.format(
                amount_mastercard_14) + '|' + '{:.2f}'.format(amount_amex_14) \
                      + '|' + '{:.2f}'.format(amount_voucher_14) + '|' + '{:.2f}'.format(amount_other_14) + '|' + 'Y'
        if orders_count_15 == 0:
            line_15 += line_no_data
        else:
            line_15 = line_15 + '|' + '{:.2f}'.format(amount_total_15) + '|' + '{:.2f}'.format(
                amount_tax_15) + '|' + '{:.2f}'.format(amount_disc_15) + '|' \
                      + '{:.2f}'.format(amount_service_15) + '|' + str(amount_pax_15) + '|' + '{:.2f}'.format(
                amount_cash_15) + '|' + '{:.2f}'.format(amount_atm_15) \
                      + '|' + '{:.2f}'.format(amount_visa_15) + '|' + '{:.2f}'.format(
                amount_mastercard_15) + '|' + '{:.2f}'.format(amount_amex_15) \
                      + '|' + '{:.2f}'.format(amount_voucher_15) + '|' + '{:.2f}'.format(amount_other_15) + '|' + 'Y'
        if orders_count_16 == 0:
            line_16 += line_no_data
        else:
            line_16 = line_16 + '|' + '{:.2f}'.format(amount_total_16) + '|' + '{:.2f}'.format(
                amount_tax_16) + '|' + '{:.2f}'.format(amount_disc_16) + '|' \
                      + '{:.2f}'.format(amount_service_16) + '|' + str(amount_pax_16) + '|' + '{:.2f}'.format(
                amount_cash_16) + '|' + '{:.2f}'.format(amount_atm_16) \
                      + '|' + '{:.2f}'.format(amount_visa_16) + '|' + '{:.2f}'.format(
                amount_mastercard_16) + '|' + '{:.2f}'.format(amount_amex_16) \
                      + '|' + '{:.2f}'.format(amount_voucher_16) + '|' + '{:.2f}'.format(amount_other_16) + '|' + 'Y'
        if orders_count_17 == 0:
            line_17 += line_no_data
        else:
            line_17 = line_17 + '|' + '{:.2f}'.format(amount_total_17) + '|' + '{:.2f}'.format(
                amount_tax_17) + '|' + '{:.2f}'.format(amount_disc_17) + '|' \
                      + '{:.2f}'.format(amount_service_17) + '|' + str(amount_pax_17) + '|' + '{:.2f}'.format(
                amount_cash_17) + '|' + '{:.2f}'.format(amount_atm_17) \
                      + '|' + '{:.2f}'.format(amount_visa_17) + '|' + '{:.2f}'.format(
                amount_mastercard_17) + '|' + '{:.2f}'.format(amount_amex_17) \
                      + '|' + '{:.2f}'.format(amount_voucher_17) + '|' + '{:.2f}'.format(amount_other_17) + '|' + 'Y'
        if orders_count_18 == 0:
            line_18 += line_no_data
        else:
            line_18 = line_18 + '|' + '{:.2f}'.format(amount_total_18) + '|' + '{:.2f}'.format(
                amount_tax_18) + '|' + '{:.2f}'.format(amount_disc_18) + '|' \
                      + '{:.2f}'.format(amount_service_18) + '|' + str(amount_pax_18) + '|' + '{:.2f}'.format(
                amount_cash_18) + '|' + '{:.2f}'.format(amount_atm_18) \
                      + '|' + '{:.2f}'.format(amount_visa_18) + '|' + '{:.2f}'.format(
                amount_mastercard_18) + '|' + '{:.2f}'.format(amount_amex_18) \
                      + '|' + '{:.2f}'.format(amount_voucher_18) + '|' + '{:.2f}'.format(amount_other_18) + '|' + 'Y'
        if orders_count_19 == 0:
            line_19 += line_no_data
        else:
            line_19 = line_19 + '|' + '{:.2f}'.format(amount_total_19) + '|' + '{:.2f}'.format(
                amount_tax_19) + '|' + '{:.2f}'.format(amount_disc_19) + '|' \
                      + '{:.2f}'.format(amount_service_19) + '|' + str(amount_pax_19) + '|' + '{:.2f}'.format(
                amount_cash_19) + '|' + '{:.2f}'.format(amount_atm_19) \
                      + '|' + '{:.2f}'.format(amount_visa_19) + '|' + '{:.2f}'.format(
                amount_mastercard_19) + '|' + '{:.2f}'.format(amount_amex_19) \
                      + '|' + '{:.2f}'.format(amount_voucher_19) + '|' + '{:.2f}'.format(amount_other_19) + '|' + 'Y'
        if orders_count_20 == 0:
            line_20 += line_no_data
        else:
            line_20 = line_20 + '|' + '{:.2f}'.format(amount_total_20) + '|' + '{:.2f}'.format(
                amount_tax_20) + '|' + '{:.2f}'.format(amount_disc_20) + '|' \
                      + '{:.2f}'.format(amount_service_20) + '|' + str(amount_pax_20) + '|' + '{:.2f}'.format(
                amount_cash_20) + '|' + '{:.2f}'.format(amount_atm_20) \
                      + '|' + '{:.2f}'.format(amount_visa_20) + '|' + '{:.2f}'.format(
                amount_mastercard_20) + '|' + '{:.2f}'.format(amount_amex_20) \
                      + '|' + '{:.2f}'.format(amount_voucher_20) + '|' + '{:.2f}'.format(amount_other_20) + '|' + 'Y'
        if orders_count_21 == 0:
            line_21 += line_no_data
        else:
            line_21 = line_21 + '|' + '{:.2f}'.format(amount_total_21) + '|' + '{:.2f}'.format(
                amount_tax_21) + '|' + '{:.2f}'.format(amount_disc_21) + '|' \
                      + '{:.2f}'.format(amount_service_21) + '|' + str(amount_pax_21) + '|' + '{:.2f}'.format(
                amount_cash_21) + '|' + '{:.2f}'.format(amount_atm_21) \
                      + '|' + '{:.2f}'.format(amount_visa_21) + '|' + '{:.2f}'.format(
                amount_mastercard_21) + '|' + '{:.2f}'.format(amount_amex_21) \
                      + '|' + '{:.2f}'.format(amount_voucher_21) + '|' + '{:.2f}'.format(amount_other_21) + '|' + 'Y'
        if orders_count_22 == 0:
            line_22 += line_no_data
        else:
            line_22 = line_22 + '|' + '{:.2f}'.format(amount_total_22) + '|' + '{:.2f}'.format(
                amount_tax_22) + '|' + '{:.2f}'.format(amount_disc_22) + '|' \
                      + '{:.2f}'.format(amount_service_22) + '|' + str(amount_pax_22) + '|' + '{:.2f}'.format(
                amount_cash_22) + '|' + '{:.2f}'.format(amount_atm_22) \
                      + '|' + '{:.2f}'.format(amount_visa_22) + '|' + '{:.2f}'.format(
                amount_mastercard_22) + '|' + '{:.2f}'.format(amount_amex_22) \
                      + '|' + '{:.2f}'.format(amount_voucher_22) + '|' + '{:.2f}'.format(amount_other_22) + '|' + 'Y'
        if orders_count_23 == 0:
            line_23 += line_no_data
        else:
            line_23 = line_23 + '|' + '{:.2f}'.format(amount_total_23) + '|' + '{:.2f}'.format(
                amount_tax_23) + '|' + '{:.2f}'.format(amount_disc_23) + '|' \
                      + '{:.2f}'.format(amount_service_23) + '|' + str(amount_pax_23) + '|' + '{:.2f}'.format(
                amount_cash_23) + '|' + '{:.2f}'.format(amount_atm_23) \
                      + '|' + '{:.2f}'.format(amount_visa_23) + '|' + '{:.2f}'.format(
                amount_mastercard_23) + '|' + '{:.2f}'.format(amount_amex_23) \
                      + '|' + '{:.2f}'.format(amount_voucher_23) + '|' + '{:.2f}'.format(amount_other_23) + '|' + 'Y'
        print(line_0)
        print(line_1)
        print(line_2)
        print(line_3)
        print(line_4)
        print(line_5)
        print(line_6)
        print(line_7)
        print(line_8)
        print(line_9)
        print(line_10)
        print(line_11)
        print(line_12)
        print(line_13)
        print(line_14)
        print(line_15)
        print(line_16)
        print(line_17)
        print(line_18)
        print(line_19)
        print(line_20)
        print(line_21)
        print(line_22)
        print(line_23)

        sea_prefix = 'H17000025_'
        sea_vivo_date_str = date_order_real
        sea_file_name = sea_prefix + sea_vivo_date_str + '.txt'
        try:
            # Use Linux
            with open('/opt/odoo/vivo_report/' + sea_file_name, 'w') as wf:

            # Use Windows
            # with open(os.getcwd() + '\\vivo_report' + '\\' + sea_file_name, 'w') as wf:
                data_line = (line_0 + '\n' + line_1 + '\n' + line_2 + '\n' + line_3 + '\n' + line_4 + '\n' +
                             line_5 + '\n' + line_6 + '\n' + line_7 + '\n' + line_8 + '\n' + line_9 + '\n' +
                             line_10 + '\n' + line_11 + '\n' + line_12 + '\n' + line_13 + '\n' + line_14 + '\n' +
                             line_15 + '\n' + line_16 + '\n' + line_17 + '\n' + line_18 + '\n' + line_19 + '\n' +
                             line_20 + '\n' + line_21 + '\n' + line_22 + '\n' + line_23)
                wf.write(data_line)
        except:
            print("")

        # Download file
        try:
            # Use Linux
            f_read = open('/opt/odoo/vivo_report/' + sea_file_name, 'rb')

            # Use Windows
            # f_read = open(os.getcwd() + '\\vivo_report' + '\\' + sea_file_name, 'rb')

            # Use Common
            file_data = f_read.read()
            values = {
                'name': sea_file_name,
                'datas_fname': sea_file_name,
                'res_model': 'ir.ui.view',
                'res_id': False,
                'type': 'binary',
                'public': True,
                'datas': base64.b64encode(file_data),
                # 'datas': file_data.encode('utf8').encode('base64'),
            }
            attachment_id = self.env['ir.attachment'].sudo().create(values)

            # Prepare your download URL
            # Use Windows
            # download_url = '/web/content/' + str(attachment_id.id) + '?download=True'

            # Use Linux
            download_url = str(attachment_id.id) + '?download=True'

            # Use Common
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')

            return {
                "type": "ir.actions.act_url",

                # Use Windows
                # "url": str(base_url) + str(download_url),

                # User Pilot
                # "url": 'https://pilot.seateklab.vn/web/content/' + str(download_url),

                # User Production
                "url": 'https://shop.dannygreen.vn/web/content/' + str(download_url),

                "target": "new",
            }
        except:
            raise UserError(_("Execution is not allowed. Contact Admin for help.!!!"))
