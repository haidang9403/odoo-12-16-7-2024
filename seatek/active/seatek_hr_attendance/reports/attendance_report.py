# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import calendar
import datetime
import io
from datetime import date

from odoo import models
from odoo.tools.translate import _


class BangChamCong(models.AbstractModel):
    _name = 'report.seatek_hr_attendance.report_attendance_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def employee_list(self, stt, row, sheet, attendenace_month_id, workbook, objects):
        salary_style = workbook.add_format({'bold': False,
                                            'font_size': 9,
                                            'font_name': "Times New Roman",
                                            'font_color': '#000000',
                                            'align': 'center',
                                            'border': 1,
                                            'text_wrap': True,
                                            'num_format': '#,###',
                                            'valign': 'vcenter'})
        content_style = workbook.add_format({'bold': False,
                                             'font_size': 9,
                                             'font_name': "Times New Roman",
                                             'font_color': '#000000',
                                             'align': 'center',
                                             'border': 1,
                                             'text_wrap': True,
                                             'valign': 'vcenter'})
        content_style_bold = workbook.add_format({'bold': True,
                                                  'font_size': 9,
                                                  'font_name': "Times New Roman",
                                                  'font_color': '#000000',
                                                  'align': 'center',
                                                  'border': 1,
                                                  'text_wrap': True,
                                                  'valign': 'vcenter'})
        content_style_bold.set_num_format(43)
        sheet.write('A%s' % row, stt, content_style)

        if attendenace_month_id.employee_multi_id.sudo().s_identification_id:
            sheet.write('B%s' % row, attendenace_month_id.employee_multi_id.sudo().s_identification_id, content_style)
        else:
            sheet.write('B%s' % row, '', content_style)
        if attendenace_month_id.employee_multi_id.sudo().name.name:
            sheet.write('C%s' % row, attendenace_month_id.employee_multi_id.sudo().name.name, content_style)
        else:
            sheet.write('C%s' % row, '', content_style)
        if attendenace_month_id.employee_multi_id.sudo().job_id.sudo().name:
            sheet.write('D%s' % row, attendenace_month_id.employee_multi_id.sudo().job_id.sudo().name, content_style)
        else:
            sheet.write('D%s' % row, '', content_style)

        header_style_no_bold = workbook.add_format({'font_size': 11,
                                                    'font_name': "Times New Roman",
                                                    'font_color': '#000000',
                                                    'align': 'center',
                                                    'border': 1,
                                                    'text_wrap': True,
                                                    'valign': 'vcenter'})
        header_style_no_bold_weekend = workbook.add_format({'bold': True,
                                                            'font_size': 11,
                                                            'font_name': "Times New Roman",
                                                            'font_color': '#CC0000',
                                                            'align': 'center',
                                                            'border': 1,
                                                            'bg_color': '#92D14F',
                                                            'text_wrap': True,
                                                            'valign': 'vcenter'})

        if attendenace_month_id.last_day_of_month:
            for i in range(31):
                symbol = False
                symbol_str = ''
                if i >= attendenace_month_id.last_day_of_month:
                    dates = int(
                        date.weekday(date(int(attendenace_month_id.year), int(int(attendenace_month_id.month) + 1),
                                          int(i + 1 - attendenace_month_id.last_day_of_month))))
                else:
                    dates = int(
                        date.weekday(date(int(attendenace_month_id.year), int(attendenace_month_id.month), int(i + 1))))
                    if i == 0:
                        symbol = attendenace_month_id.day_1.sudo()
                    elif i == 1:
                        symbol = attendenace_month_id.day_2.sudo()
                    elif i == 2:
                        symbol = attendenace_month_id.day_3.sudo()
                    elif i == 3:
                        symbol = attendenace_month_id.day_4.sudo()
                    elif i == 4:
                        symbol = attendenace_month_id.day_5.sudo()
                    elif i == 5:
                        symbol = attendenace_month_id.day_6.sudo()
                    elif i == 6:
                        symbol = attendenace_month_id.day_7.sudo()
                    elif i == 7:
                        symbol = attendenace_month_id.day_8.sudo()
                    elif i == 8:
                        symbol = attendenace_month_id.day_9.sudo()
                    elif i == 9:
                        symbol = attendenace_month_id.day_10.sudo()
                    elif i == 10:
                        symbol = attendenace_month_id.day_11.sudo()
                    elif i == 11:
                        symbol = attendenace_month_id.day_12.sudo()
                    elif i == 12:
                        symbol = attendenace_month_id.day_13.sudo()
                    elif i == 13:
                        symbol = attendenace_month_id.day_14.sudo()
                    elif i == 14:
                        symbol = attendenace_month_id.day_15.sudo()
                    elif i == 15:
                        symbol = attendenace_month_id.day_16.sudo()
                    elif i == 16:
                        symbol = attendenace_month_id.day_17.sudo()
                    elif i == 17:
                        symbol = attendenace_month_id.day_18.sudo()
                    elif i == 18:
                        symbol = attendenace_month_id.day_19.sudo()
                    elif i == 19:
                        symbol = attendenace_month_id.day_20.sudo()
                    elif i == 20:
                        symbol = attendenace_month_id.day_21.sudo()
                    elif i == 21:
                        symbol = attendenace_month_id.day_22.sudo()
                    elif i == 22:
                        symbol = attendenace_month_id.day_23.sudo()
                    elif i == 23:
                        symbol = attendenace_month_id.day_24.sudo()
                    elif i == 24:
                        symbol = attendenace_month_id.day_25.sudo()
                    elif i == 25:
                        symbol = attendenace_month_id.day_26.sudo()
                    elif i == 26:
                        symbol = attendenace_month_id.day_27.sudo()
                    elif i == 27:
                        symbol = attendenace_month_id.day_28.sudo()
                    elif i == 28:
                        symbol = attendenace_month_id.day_29.sudo()
                    elif i == 29:
                        symbol = attendenace_month_id.day_30.sudo()
                    elif i == 30:
                        symbol = attendenace_month_id.day_31.sudo()

                    if symbol:
                        symbol_str = symbol.symbol.sudo().symbol
                        overtime = 0
                        # if symbol.shift_details:
                        #     for j in symbol.shift_details:
                        #         if j.overtime_hr:
                        #             overtime += j.overtime_hr
                        if symbol.overtime:
                            overtime = symbol.overtime
                        time = overtime % 1
                        if int(overtime) > 0 or time > 0:
                            o = int(overtime)
                            if time > 0:
                                time = time * 60
                                if 15 <= time < 45:
                                    o += 0.5
                                elif time >= 45:
                                    o += 1
                            if o > 0:
                                symbol_str += str(o)
                        date_contract_tv = datetime.datetime.strptime(
                            str(attendenace_month_id.year) + ' ' + str(attendenace_month_id.month) + ' ' + str(i + 1),
                            "%Y %m %d")
                        contract_tv = self.env['hr.contract'].sudo().search(
                            [('employee_id', '=', attendenace_month_id.employee_multi_id.sudo().name.id),
                             ('state', '!=', 'cancel'), ('date_start', '<=', date_contract_tv),
                             ('date_end', '>=', date_contract_tv),
                             ('type_id', '=', 4), ('contract_category', '=', 'contract')])
                        if contract_tv:
                            symbol_str = str('t') + symbol_str

                sheet.write(row - 1, i + 4, symbol_str if dates not in [5, 6] and symbol else '',
                            header_style_no_bold if dates not in [5, 6] else header_style_no_bold_weekend)

                '''lấy danh sách'''

        '''các công thức tính toán'''
        aj = '=COUNTIF($E%s:$AI%s,\"tx\")+COUNTIF($E%s:$AI%s,\"tx/2\")/2+COUNTIF($E%s:$AI%s,\"tx1\")+COUNTIF($E%s:$AI%s,\"tx1.5\")+COUNTIF($E%s:$AI%s,\"tx2.5\")+COUNTIF($E%s:$AI%s,\"tx3.5\")+COUNTIF($E%s:$AI%s,\"tx4.5\")+COUNTIF($E%s:$AI%s,\"tx5.5\")+COUNTIF($E%s:$AI%s,\"tx6.5\")+COUNTIF($E%s:$AI%s,\"tx7.5\")+COUNTIF($E%s:$AI%s,\"tx2\")+COUNTIF($E%s:$AI%s,\"tx3\")+COUNTIF($E%s:$AI%s,\"tx4\")+COUNTIF($E%s:$AI%s,\"tx5\")+COUNTIF($E%s:$AI%s,\"tx6\")+COUNTIF($E%s:$AI%s,\"tx7\")+COUNTIF($E%s:$AI%s,\"tx8\")+COUNTIF($E%s:$AI%s,\"tct/2\")/2+COUNTIF($E%s:$AI%s,\"th/2\")/2+COUNTIF($E%s:$AI%s,\"tR/2\")/2+COUNTIF($E%s:$AI%s,\"tRO/2\")/2+COUNTIF($E%s:$AI%s,\"tO/2\")/2+COUNTIF($E%s:$AI%s,\"tSX/2\")/2+COUNTIF($E%s:$AI%s,\"tNB/2\")/2+COUNTIF($E%s:$AI%s,\"tNM/2\")/2'
        sheet.write('AJ%s' % row, aj % ((row,) * 50), content_style_bold)

        ak = '=COUNTIF($E%s:$AI%s,\"tCT\")+COUNTIF($E%s:$AI%s,\"tCT/2\")/2+COUNTIF($E%s:$AI%s,\"tSCT/2\")/2+COUNTIF($E%s:$AI%s,\"tCT1\")+COUNTIF($E%s:$AI%s,\"tCT1.5\")+COUNTIF($E%s:$AI%s,\"tCT2\")+COUNTIF($E%s:$AI%s,\"tCT2.5\")+COUNTIF($E%s:$AI%s,\"tCT3\")+COUNTIF($E%s:$AI%s,\"tCT3.5\")+COUNTIF($E%s:$AI%s,\"tCT4.5\")+COUNTIF($E%s:$AI%s,\"tCT4\")+COUNTIF($E%s:$AI%s,\"tCT5\")+COUNTIF($E%s:$AI%s,\"tCT5.5\")+COUNTIF($E%s:$AI%s,\"tCT6\")+COUNTIF($E%s:$AI%s,\"tCT6.5\")*COUNTIF($E%s:$AI%s,\"tCT7\")+COUNTIF($E%s:$AI%s,\"tCT7.5\")*COUNTIF($E%s:$AI%s,\"tCT8\")+COUNTIF($E%s:$AI%s,\"tCT8.5\")+COUNTIF($E%s:$AI%s,\"tCT9\")+COUNTIF($E%s:$AI%s,\"tCT9.5\")+COUNTIF($E%s:$AI%s,\"tCT10\")+COUNTIF($E%s:$AI%s,\"tCT10.5\")+COUNTIF($E%s:$AI%s,\"TH\")+COUNTIF($E%s:$AI%s,\"TH/2\")/2'
        sheet.write('AK%s' % row, ak % ((row,) * 50), content_style_bold)

        al = '=COUNTIF($E%s:$AI%s,\"TW\")+COUNTIF($E%s:$AI%s,\"TW/2\")/2+COUNTIF($E%s:$AI%s,\"TFW/2\")/2+COUNTIF($E%s:$AI%s,\"TWX/2\")/2'
        sheet.write('AL%s' % row, al % ((row,) * 8), content_style_bold)

        am = '=COUNTIF($E%s:$AI%s,\"tL\")+COUNTIF($E%s:$AI%s,\"tL/2\")/2+COUNTIF($E%s:$AI%s,\"tNM\")+COUNTIF($E%s:$AI%s,\"tNM/2\")/2+COUNTIF($E%s:$AI%s,\"tNB\")+COUNTIF($E%s:$AI%s,\"tNB/2\")/2+COUNTIF($E%s:$AI%s,\"tL1\")+COUNTIF($E%s:$AI%s,\"tL1.5\")+COUNTIF($E%s:$AI%s,\"tL2\")+COUNTIF($E%s:$AI%s,\"tL2.5\")+COUNTIF($E%s:$AI%s,\"tL3\")++COUNTIF($E%s:$AI%s,\"tL3.5\")+COUNTIF($E%s:$AI%s,\"tL4\")+COUNTIF($E%s:$AI%s,\"tL4.5\")+COUNTIF($E%s:$AI%s,\"tL5\")+COUNTIF($E%s:$AI%s,\"tL5.5\")+COUNTIF($E%s:$AI%s,\"tL6\")+COUNTIF($E%s:$AI%s,\"tL6.5\")+COUNTIF($E%s:$AI%s,\"tL7\")+COUNTIF($E%s:$AI%s,\"tL7.5\")+COUNTIF($E%s:$AI%s,\"tL8\")+COUNTIF($E%s:$AI%s,\"tL8.5\")+COUNTIF($E%s:$AI%s,\"tSL/2\")/2+COUNTIF($E%s:$AI%s,\"tSL1\")/2+COUNTIF($E%s:$AI%s,\"tSL2\")/2+COUNTIF($E%s:$AI%s,\"tSL3\")/2+COUNTIF($E%s:$AI%s,\"tSL4\")/2+COUNTIF($E%s:$AI%s,\"tSL5\")/2+COUNTIF($E%s:$AI%s,\"tSL6\")/2+COUNTIF($E%s:$AI%s,\"tSL7\")/2+COUNTIF($E%s:$AI%s,\"tSL8\")/2+COUNTIF($E%s:$AI%s,\"tSNM/2\")/2+COUNTIF($E%s:$AI%s,\"tBL\")+COUNTIF($E%s:$AI%s,\"tBL/2\")/2+COUNTIF($E%s:$AI%s,\"tBL1\")+COUNTIF($E%s:$AI%s,\"tBL2\")+COUNTIF($E%s:$AI%s,\"tBL3\")+COUNTIF($E%s:$AI%s,\"tBL4\")+COUNTIF($E%s:$AI%s,\"tBL5\")+COUNTIF($E%s:$AI%s,\"tBL6\")+COUNTIF($E%s:$AI%s,\"tBL7\")+COUNTIF($E%s:$AI%s,\"tBL8\")'
        sheet.write('AM%s' % row, am % ((row,) * 84), content_style_bold)

        an = '=COUNTIF($E%s:$AI%s,\"tF\")+COUNTIF($E%s:$AI%s,\"tF/2\")/2+COUNTIF($E%s:$AI%s,\"tR\")+COUNTIF($E%s:$AI%s,\"tR/2\")/2+COUNTIF($E%s:$AI%s,\"tSF/2\")/2+COUNTIF($E%s:$AI%s,\"tSR/2\")/2'
        sheet.write('AN%s' % row, an % ((row,) * 12), content_style_bold)

        ao = '=COUNTIF($E%s:$AI%s,\"tK\")'
        sheet.write('AO%s' % row, ao % ((row,) * 2), content_style_bold)

        ap = '=COUNTIF($E%s:$AI%s,\"tRO\")+COUNTIF($E%s:$AI%s,\"tRO/2\")/2+COUNTIF($E%s:$AI%s,\"tO\")+COUNTIF($E%s:$AI%s,\"tO/2\")/2+COUNTIF($E%s:$AI%s,\"tSRO/2\")/2+COUNTIF($E%s:$AI%s,\"tSO/2\")/2+COUNTIF($E%s:$AI%s,\"tTS/2\")/2+COUNTIF($E%s:$AI%s,\"tTS\")+COUNTIF($E%s:$AI%s,\"tCÔ\")+COUNTIF($E%s:$AI%s,\"tCÔ/2\")/2'
        sheet.write('AP%s' % row, ap % ((row,) * 20), content_style_bold)

        aq = '=COUNTIF($E%s:$AI%s,\"TKH\")+COUNTIF($E%s:$AI%s,\"TKH/2\")/2'
        sheet.write('AQ%s' % row, aq % ((row,) * 4), content_style_bold)

        ar = '=COUNTIF($E%s:$AI%s,\"x\")+COUNTIF($E%s:$AI%s,\"x/2\")/2+COUNTIF($E%s:$AI%s,\"F/2\")/2+COUNTIF($E%s:$AI%s,\"x0.5\")+COUNTIF($E%s:$AI%s,\"x1\")+COUNTIF($E%s:$AI%s,\"x1.5\")+COUNTIF($E%s:$AI%s,\"x2.5\")+COUNTIF($E%s:$AI%s,\"x3.5\")+COUNTIF($E%s:$AI%s,\"x4.5\")+COUNTIF($E%s:$AI%s,\"x5.5\")+COUNTIF($E%s:$AI%s,\"x6.5\")+COUNTIF($E%s:$AI%s,\"x7.5\")+COUNTIF($E%s:$AI%s,\"x2\")+COUNTIF($E%s:$AI%s,\"x3\")+COUNTIF($E%s:$AI%s,\"x4\")+COUNTIF($E%s:$AI%s,\"x5\")+COUNTIF($E%s:$AI%s,\"x6\")+COUNTIF($E%s:$AI%s,\"x7\")+COUNTIF($E%s:$AI%s,\"x8\")+COUNTIF($E%s:$AI%s,\"x9\")+COUNTIF($E%s:$AI%s,\"x10\")+COUNTIF($E%s:$AI%s,\"x11\")+COUNTIF($E%s:$AI%s,\"ct/2\")/2+COUNTIF($E%s:$AI%s,\"h/2\")/2+COUNTIF($E%s:$AI%s,\"R/2\")/2+COUNTIF($E%s:$AI%s,\"RO/2\")/2+COUNTIF($E%s:$AI%s,\"O/2\")/2+COUNTIF($E%s:$AI%s,\"SX/2\")/2+COUNTIF($E%s:$AI%s,\"XW/2\")/2+COUNTIF($E%s:$AI%s,\"WX/2\")/2+COUNTIF($E%s:$AI%s,\"NB/2\")/2+COUNTIF($E%s:$AI%s,\"WNX/2\")/2+COUNTIF($E%s:$AI%s,\"NM/2\")/2'
        sheet.write('AR%s' % row, ar % ((row,) * 66), content_style_bold)

        a_s = '=COUNTIF($E%s:$AI%s,\"CT\")+COUNTIF($E%s:$AI%s,\"CT/2\")/2+COUNTIF($E%s:$AI%s,\"SCT/2\")/2+COUNTIF($E%s:$AI%s,\"CT1\")+COUNTIF($E%s:$AI%s,\"CT1.5\")+COUNTIF($E%s:$AI%s,\"CT2\")+COUNTIF($E%s:$AI%s,\"CT2.5\")+COUNTIF($E%s:$AI%s,\"CT3\")+COUNTIF($E%s:$AI%s,\"CT3.5\")+COUNTIF($E%s:$AI%s,\"CT4.5\")+COUNTIF($E%s:$AI%s,\"CT4\")+COUNTIF($E%s:$AI%s,\"CT5\")+COUNTIF($E%s:$AI%s,\"CT5.5\")+COUNTIF($E%s:$AI%s,\"CT6\")+COUNTIF($E%s:$AI%s,\"CT6.5\")*COUNTIF($E%s:$AI%s,\"CT7\")+COUNTIF($E%s:$AI%s,\"CT7.5\")*COUNTIF($E%s:$AI%s,\"CT8\")+COUNTIF($E%s:$AI%s,\"CT8.5\")+COUNTIF($E%s:$AI%s,\"CT9\")+COUNTIF($E%s:$AI%s,\"CT9.5\")+COUNTIF($E%s:$AI%s,\"CT10\")+COUNTIF($E%s:$AI%s,\"CT10.5\")+COUNTIF($E%s:$AI%s,\"H\")+COUNTIF($E%s:$AI%s,\"H/2\")/2'
        sheet.write('AS%s' % row, a_s % ((row,) * 50), content_style_bold)

        at = '=COUNTIF($E%s:$AI%s,\"W\")+COUNTIF($E%s:$AI%s,\"WN/2\")/2+COUNTIF($E%s:$AI%s,\"FW/2\")/2+COUNTIF($E%s:$AI%s,\"WX/2\")/2+COUNTIF($E%s:$AI%s,\"XW/2\")/2'
        sheet.write('AT%s' % row, at % ((row,) * 10), content_style_bold)

        au = '=COUNTIF($E%s:$AI%s,\"L\")+COUNTIF($E%s:$AI%s,\"L/2\")/2+COUNTIF($E%s:$AI%s,\"NM\")+COUNTIF($E%s:$AI%s,\"NM/2\")/2+COUNTIF($E%s:$AI%s,\"NB\")+COUNTIF($E%s:$AI%s,\"NB/2\")/2+COUNTIF($E%s:$AI%s,\"L1\")+COUNTIF($E%s:$AI%s,\"L2\")+COUNTIF($E%s:$AI%s,\"L3\")+COUNTIF($E%s:$AI%s,\"L4\")+COUNTIF($E%s:$AI%s,\"L5\")+COUNTIF($E%s:$AI%s,\"L6\")+COUNTIF($E%s:$AI%s,\"L7\")+COUNTIF($E%s:$AI%s,\"L8\")+COUNTIF($E%s:$AI%s,\"SL/2\")/2+COUNTIF($E%s:$AI%s,\"SL1\")/2+COUNTIF($E%s:$AI%s,\"SL2\")/2+COUNTIF($E%s:$AI%s,\"SL3\")/2+COUNTIF($E%s:$AI%s,\"SL4\")/2+COUNTIF($E%s:$AI%s,\"SL5\")/2+COUNTIF($E%s:$AI%s,\"SL6\")/2+COUNTIF($E%s:$AI%s,\"SL7\")/2+COUNTIF($E%s:$AI%s,\"SL8\")/2+COUNTIF($E%s:$AI%s,\"SNM/2\")/2+COUNTIF($E%s:$AI%s,\"NBF/2\")/2+COUNTIF($E%s:$AI%s,\"BL\")+COUNTIF($E%s:$AI%s,\"BL/2\")/2+COUNTIF($E%s:$AI%s,\"BL1\")+COUNTIF($E%s:$AI%s,\"BL2\")+COUNTIF($E%s:$AI%s,\"BL3\")+COUNTIF($E%s:$AI%s,\"BL4\")+COUNTIF($E%s:$AI%s,\"BL5\")+COUNTIF($E%s:$AI%s,\"BL6\")+COUNTIF($E%s:$AI%s,\"BL7\")+COUNTIF($E%s:$AI%s,\"BL8\")'
        sheet.write('AU%s' % row, au % ((row,) * 70), content_style_bold)

        av = '=COUNTIF($E%s:$AI%s,\"F\")+COUNTIF($E%s:$AI%s,\"F/2\")/2+COUNTIF($E%s:$AI%s,\"R\")+COUNTIF($E%s:$AI%s,\"R/2\")/2+COUNTIF($E%s:$AI%s,\"SF/2\")/2+COUNTIF($E%s:$AI%s,\"SR/2\")/2+COUNTIF($E%s:$AI%s,\"WF/2\")/2+COUNTIF($E%s:$AI%s,\"FW/2\")/2+COUNTIF($E%s:$AI%s,\"KF/2\")/2+COUNTIF($E%s:$AI%s,\"FK/2\")/2+COUNTIF($E%s:$AI%s,\"NBF/2\")/2+COUNTIF($E%s:$AI%s,\"ROF/2\")/2+COUNTIF($E%s:$AI%s,\"FRO/2\")/2+COUNTIF($E%s:$AI%s,\"FWN/2\")/2'
        sheet.write('AV%s' % row, av % ((row,) * 28), content_style_bold)

        aw = '=COUNTIF($E%s:$AI%s,\"K\")+COUNTIF($E%s:$AI%s,\"KF/2\")/2+COUNTIF($E%s:$AI%s,\"FK/2\")/2+COUNTIF($E%s:$AI%s,\"KRO/2\")/2+COUNTIF($E%s:$AI%s,\"ROK/2\")/2+COUNTIF($E%s:$AI%s,\"KW/2\")/2+COUNTIF($E%s:$AI%s,\"WK/2\")/2+COUNTIF($E%s:$AI%s,\"K/2\")/2'
        sheet.write('AW%s' % row, aw % ((row,) * 16), content_style_bold)

        ax = '=COUNTIF($E%s:$AI%s,\"RO\")+COUNTIF($E%s:$AI%s,\"RO/2\")/2+COUNTIF($E%s:$AI%s,\"O\")+COUNTIF($E%s:$AI%s,\"O/2\")/2+COUNTIF($E%s:$AI%s,\"SRO/2\")/2+COUNTIF($E%s:$AI%s,\"SO/2\")/2+COUNTIF($E%s:$AI%s,\"TS/2\")/2+COUNTIF($E%s:$AI%s,\"TS\")+COUNTIF($E%s:$AI%s,\"CÔ\")+COUNTIF($E%s:$AI%s,\"CÔ/2\")/2+COUNTIF($E%s:$AI%s,\"ROW/2\")/2+COUNTIF($E%s:$AI%s,\"WRO/2\")/2+COUNTIF($E%s:$AI%s,\"KRO/2\")/2+COUNTIF($E%s:$AI%s,\"ROK/2\")/2+COUNTIF($E%s:$AI%s,\"ROF/2\")/2+COUNTIF($E%s:$AI%s,\"FRO/2\")/2+COUNTIF($E%s:$AI%s,\"Ô\")+COUNTIF($E%s:$AI%s,\"Ô/2\")/2'
        sheet.write('AX%s' % row, ax % ((row,) * 36), content_style_bold)

        ay = '=COUNTIF($E%s:$AI%s,\"KH\")+COUNTIF($E%s:$AI%s,\"KH/2\")/2'
        sheet.write('AY%s' % row, ay % (row, row, row, row), content_style_bold)

        az = '=COUNTIF($E%s:$AI%s,\"tX1\")+COUNTIF($E%s:$AI%s,\"tX1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tX2\")*2+COUNTIF($E%s:$AI%s,\"tX2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tX3\")*3+COUNTIF($E%s:$AI%s,\"tX3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tX4\")*4+COUNTIF($E%s:$AI%s,\"tX4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tX5\")*5+COUNTIF($E%s:$AI%s,\"tX5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tX6\")*6+COUNTIF($E%s:$AI%s,\"tX6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tX7\")*7+COUNTIF($E%s:$AI%s,\"tX7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tX8\")*8+ COUNTIF($E%s:$AI%s,\"tCT1\")*1+COUNTIF($E%s:$AI%s,\"tCT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tCT2\")*2+COUNTIF($E%s:$AI%s,\"tCT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tCT3\")*3+COUNTIF($E%s:$AI%s,\"tCT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tCT4\")*4+COUNTIF($E%s:$AI%s,\"tCT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tCT5\")*5+COUNTIF($E%s:$AI%s,\"tCT6\")*6+COUNTIF($E%s:$AI%s,\"tCT7\")*7+COUNTIF($E%s:$AI%s,\"tCT8\")*8+COUNTIF($E%s:$AI%s,\"tCT10.5\")*10.5'
        sheet.write('AZ%s' % row, az % ((row,) * 56), content_style_bold)

        ba = '=COUNTIF($E%s:$AI%s,\"tOT1\")+COUNTIF($E%s:$AI%s,\"tOT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tOT2\")*2+COUNTIF($E%s:$AI%s,\"tOT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tOT3\")*3+COUNTIF($E%s:$AI%s,\"tOT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tOT4\")*4+COUNTIF($E%s:$AI%s,\"tOT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tOT5\")*5+COUNTIF($E%s:$AI%s,\"tOT5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tOT6\")*6+COUNTIF($E%s:$AI%s,\"tOT6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tOT7\")*7+COUNTIF($E%s:$AI%s,\"tOT7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tOT8\")*8+COUNTIF($E%s:$AI%s,\"tTB1\")+COUNTIF($E%s:$AI%s,\"tTB1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tTB2\")*2+COUNTIF($E%s:$AI%s,\"tTB2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tTB3\")*3+COUNTIF($E%s:$AI%s,\"tTB3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tTB4\")*4+COUNTIF($E%s:$AI%s,\"tTB4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tTB5\")*5+COUNTIF($E%s:$AI%s,\"tTB5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tTB6\")*6+COUNTIF($E%s:$AI%s,\"tTB6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tTB7\")*7+COUNTIF($E%s:$AI%s,\"tTB7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tTB8\")*8+COUNTIF($E%s:$AI%s,\"tCN1\")+COUNTIF($E%s:$AI%s,\"tCN1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tCN2\")*2+COUNTIF($E%s:$AI%s,\"tCN2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tCN3\")*3+COUNTIF($E%s:$AI%s,\"tCN3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tCN4\")*4+COUNTIF($E%s:$AI%s,\"tCN4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tCN5\")*5+COUNTIF($E%s:$AI%s,\"tCN5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tCN6\")*6+COUNTIF($E%s:$AI%s,\"tCN6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tCN7\")*7+COUNTIF($E%s:$AI%s,\"tCN7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tCN8\")*8+COUNTIF($E%s:$AI%s,\"tBL1\")+COUNTIF($E%s:$AI%s,\"tBL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tBL2\")*2+COUNTIF($E%s:$AI%s,\"tBL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tBL3\")*3+COUNTIF($E%s:$AI%s,\"tBL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tBL4\")*4+COUNTIF($E%s:$AI%s,\"tBL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tBL5\")*5+COUNTIF($E%s:$AI%s,\"tBL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tBL6\")*6+COUNTIF($E%s:$AI%s,\"tBL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tBL7\")*7+COUNTIF($E%s:$AI%s,\"tBL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tBL8\")*8'
        sheet.write('BA%s' % row, ba % ((row,) * 120), content_style_bold)

        bb = '=COUNTIF($E%s:$AI%s,\"tL1\")+COUNTIF($E%s:$AI%s,\"tL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tL2\")*2+COUNTIF($E%s:$AI%s,\"tL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tL3\")*3+COUNTIF($E%s:$AI%s,\"tL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tL4\")*4+COUNTIF($E%s:$AI%s,\"tL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tL5\")*5+COUNTIF($E%s:$AI%s,\"tL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tL6\")*6+COUNTIF($E%s:$AI%s,\"tL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tL7\")*7+COUNTIF($E%s:$AI%s,\"tL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tL8\")*8+COUNTIF($E%s:$AI%s,\"tSL1\")*1+COUNTIF($E%s:$AI%s,\"tSL2\")*2+COUNTIF($E%s:$AI%s,\"tSL3\")*3+COUNTIF($E%s:$AI%s,\"tSL4\")*4+COUNTIF($E%s:$AI%s,\"tSL5\")*5+COUNTIF($E%s:$AI%s,\"tSL6\")*6+COUNTIF($E%s:$AI%s,\"tSL7\")*7+COUNTIF($E%s:$AI%s,\"tSL8\")*8'
        sheet.write('BB%s' % row, bb % ((row,) * 46), content_style_bold)

        bc = '=COUNTIF($E%s:$AI%s,\"X0.5\")*0.5+COUNTIF($E%s:$AI%s,\"X1\")+COUNTIF($E%s:$AI%s,\"X1.5\")*1.5+COUNTIF($E%s:$AI%s,\"X2\")*2+COUNTIF($E%s:$AI%s,\"X2.5\")*2.5+COUNTIF($E%s:$AI%s,\"X3\")*3+COUNTIF($E%s:$AI%s,\"X3.5\")*3.5+COUNTIF($E%s:$AI%s,\"X4\")*4+COUNTIF($E%s:$AI%s,\"X4.5\")*4.5+COUNTIF($E%s:$AI%s,\"X5\")*5+COUNTIF($E%s:$AI%s,\"X5.5\")*5.5+COUNTIF($E%s:$AI%s,\"X6\")*6+COUNTIF($E%s:$AI%s,\"X6.5\")*6.5+COUNTIF($E%s:$AI%s,\"X7\")*7+COUNTIF($E%s:$AI%s,\"X7.5\")*7.5+COUNTIF($E%s:$AI%s,\"X8\")*8+ COUNTIF($E%s:$AI%s,\"CT1\")*1+COUNTIF($E%s:$AI%s,\"CT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"CT2\")*2+COUNTIF($E%s:$AI%s,\"CT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"CT3\")*3+COUNTIF($E%s:$AI%s,\"CT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"CT4\")*4+COUNTIF($E%s:$AI%s,\"CT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"CT5\")*5+COUNTIF($E%s:$AI%s,\"CT6\")*6+COUNTIF($E%s:$AI%s,\"CT7\")*7+COUNTIF($E%s:$AI%s,\"CT8\")*8+COUNTIF($E%s:$AI%s,\"CT10.5\")*10.5'
        sheet.write('BC%s' % row, bc % ((row,) * 58), content_style_bold)

        bd = '=COUNTIF($E%s:$AI%s,\"OT1\")+COUNTIF($E%s:$AI%s,\"OT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"OT2\")*2+COUNTIF($E%s:$AI%s,\"OT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"OT3\")*3+COUNTIF($E%s:$AI%s,\"OT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"OT4\")*4+COUNTIF($E%s:$AI%s,\"OT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"OT5\")*5+COUNTIF($E%s:$AI%s,\"OT5.5\")*5.5+COUNTIF($E%s:$AI%s,\"OT6\")*6+COUNTIF($E%s:$AI%s,\"OT6.5\")*6.5+COUNTIF($E%s:$AI%s,\"OT7\")*7+COUNTIF($E%s:$AI%s,\"OT7.5\")*7.5+COUNTIF($E%s:$AI%s,\"OT8\")*8+COUNTIF($E%s:$AI%s,\"TB1\")+COUNTIF($E%s:$AI%s,\"TB1.5\")*1.5+COUNTIF($E%s:$AI%s,\"TB2\")*2+COUNTIF($E%s:$AI%s,\"TB2.5\")*2.5+COUNTIF($E%s:$AI%s,\"TB3\")*3+COUNTIF($E%s:$AI%s,\"TB3.5\")*3.5+COUNTIF($E%s:$AI%s,\"TB4\")*4+COUNTIF($E%s:$AI%s,\"TB4.5\")*4.5+COUNTIF($E%s:$AI%s,\"TB5\")*5+COUNTIF($E%s:$AI%s,\"TB5.5\")*5.5+COUNTIF($E%s:$AI%s,\"TB6\")*6+COUNTIF($E%s:$AI%s,\"TB6.5\")*6.5+COUNTIF($E%s:$AI%s,\"TB7\")*7+COUNTIF($E%s:$AI%s,\"TB7.5\")*7.5+COUNTIF($E%s:$AI%s,\"TB8\")*8+COUNTIF($E%s:$AI%s,\"CN1\")+COUNTIF($E%s:$AI%s,\"CN1.5\")*1.5+COUNTIF($E%s:$AI%s,\"CN2\")*2+COUNTIF($E%s:$AI%s,\"CN2.5\")*2.5+COUNTIF($E%s:$AI%s,\"CN3\")*3+COUNTIF($E%s:$AI%s,\"CN3.5\")*3.5+COUNTIF($E%s:$AI%s,\"CN4\")*4+COUNTIF($E%s:$AI%s,\"CN4.5\")*4.5+COUNTIF($E%s:$AI%s,\"CN5\")*5+COUNTIF($E%s:$AI%s,\"CN5.5\")*5.5+COUNTIF($E%s:$AI%s,\"CN6\")*6+COUNTIF($E%s:$AI%s,\"CN6.5\")*6.5+COUNTIF($E%s:$AI%s,\"CN7\")*7+COUNTIF($E%s:$AI%s,\"CN7.5\")*7.5+COUNTIF($E%s:$AI%s,\"CN8\")*8+COUNTIF($E%s:$AI%s,\"BL1\")+COUNTIF($E%s:$AI%s,\"BL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"BL2\")*2+COUNTIF($E%s:$AI%s,\"BL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"BL3\")*3+COUNTIF($E%s:$AI%s,\"BL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"BL4\")*4+COUNTIF($E%s:$AI%s,\"BL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"BL5\")*5+COUNTIF($E%s:$AI%s,\"BL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"BL6\")*6+COUNTIF($E%s:$AI%s,\"BL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"BL7\")*7+COUNTIF($E%s:$AI%s,\"BL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"BL8\")*8'
        sheet.write('BD%s' % row, bd % ((row,) * 120), content_style_bold)

        be = '=COUNTIF($E%s:$AI%s,\"L1\")+COUNTIF($E%s:$AI%s,\"L1.5\")*1.5+COUNTIF($E%s:$AI%s,\"L2\")*2+COUNTIF($E%s:$AI%s,\"L2.5\")*2.5+COUNTIF($E%s:$AI%s,\"L3\")*3+COUNTIF($E%s:$AI%s,\"L3.5\")*3.5+COUNTIF($E%s:$AI%s,\"L4\")*4+COUNTIF($E%s:$AI%s,\"L4.5\")*4.5+COUNTIF($E%s:$AI%s,\"L5\")*5+COUNTIF($E%s:$AI%s,\"L5.5\")*5.5+COUNTIF($E%s:$AI%s,\"L6\")*6+COUNTIF($E%s:$AI%s,\"L6.5\")*6.5+COUNTIF($E%s:$AI%s,\"L7\")*7+COUNTIF($E%s:$AI%s,\"L7.5\")*7.5+COUNTIF($E%s:$AI%s,\"L8\")*8+COUNTIF($E%s:$AI%s,\"SL1\")*1+COUNTIF($E%s:$AI%s,\"SL2\")*2+COUNTIF($E%s:$AI%s,\"SL3\")*3+COUNTIF($E%s:$AI%s,\"SL4\")*4+COUNTIF($E%s:$AI%s,\"SL5\")*5+COUNTIF($E%s:$AI%s,\"SL6\")*6+COUNTIF($E%s:$AI%s,\"SL7\")*7+COUNTIF($E%s:$AI%s,\"SL8\")*8'
        sheet.write('BE%s' % row, be % ((row,) * 46), content_style_bold)

        sheet.write('BF%s' % row, '=SUM(AJ%s:AY%s)' % ((row,) * 2), content_style_bold)
        sheet.write('BG%s' % row, '=BF%s=$C$8' % row, content_style_bold)

    def generate_xlsx_report(self, workbook, data, objects):
        # print(objects.department_id)
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        attendance_id = objects
        name = str(attendance_id.sudo().company_id.short_name)
        sheet = workbook.add_worksheet(_(name))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        if attendance_id.sudo().company_id:
            image_company = io.BytesIO(base64.b64decode(attendance_id.sudo().company_id.logo_web))
            sheet.insert_image('B1', "logocompany.png", {'image_data': image_company, 'x_scale': 0.5, 'y_scale': 0.5})
            title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
            title_style_name_company = workbook.add_format({'bold': True,
                                                            'font_size': 20,
                                                            'font_name': "Times New Roman",
                                                            'align': 'left',
                                                            'valign': 'vcenter'})
            sheet.write('D1', attendance_id.sudo().company_id.sudo().name, title_style_name_company)
            sheet.write('D2', attendance_id.sudo().company_id.sea_company_foreign, title_style_name_company)
            title_style = workbook.add_format({'bold': True,
                                               'font_size': 20,
                                               'font_name': "Times New Roman",
                                               'align': 'center',
                                               'valign': 'vcenter'})
            title_style_red = workbook.add_format({'bold': True,
                                                   'font_size': 20,
                                                   'font_name': "Times New Roman",
                                                   'font_color': '#C00000',
                                                   'align': 'center',
                                                   'valign': 'vcenter'})
            style_red = workbook.add_format({'bold': True,
                                             'font_size': 11,
                                             'font_name': "Times New Roman",
                                             'font_color': '#C00000',
                                             'align': 'center',
                                             'valign': 'vcenter'})
            sheet.merge_range('A4:AL4', 'BẢNG TỔNG HỢP CHẤM CÔNG', title_style)
            sheet.merge_range('A5:AL5', " tháng " + str(attendance_id.month) + "/" + str(attendance_id.year),
                              title_style_red)
            address = ''
            if attendance_id.sudo().company_id.street:
                address += attendance_id.sudo().company_id.street
            if attendance_id.sudo().company_id.street2:
                address += attendance_id.sudo().company_id.street2
            if attendance_id.sudo().company_id.city:
                address += attendance_id.sudo().company_id.city
            if attendance_id.sudo().company_id.state_id:
                address += attendance_id.sudo().company_id.state_id.name
            if attendance_id.sudo().company_id.country_id:
                address += ', ' + attendance_id.sudo().company_id.country_id.name
            sheet.write('D3', address, title_style_address_company)
            sheet.merge_range('A8:B8', 'Công chuẩn tháng:', style_red)

            c8 = '=NETWORKDAYS.INTL(E12,EOMONTH(E12,0),1)'
            sheet.write('C8', c8, style_red)
            d8 = '=NETWORKDAYS.INTL(E12,EOMONTH(E12,0),11)'
            sheet.write('D8', d8, style_red)

            sheet.write('E8', 15, style_red)
            sheet.write('F8', 15, style_red)
            sheet.write('D7', 'SAT', style_red)
            sheet.write('E7', 'ODD le', style_red)
            sheet.merge_range('F7:G7', 'EVE chan', style_red)
            sheet.set_row(5, 28)
            sheet.set_row(6, 28)
            sheet.set_row(9, 30)
            sheet.set_row(10, 48)
            sheet.set_row(12, 25)
            sheet.set_column('A:A', 5)
            sheet.set_column('B:B', 20)
            sheet.set_column('C:C', 28)
            sheet.set_column('D:D', 28)
            # sheet.freeze_panes(13, 3)

            header_style = workbook.add_format({'bold': True,
                                                'font_size': 11,
                                                'font_name': "Times New Roman",
                                                'font_color': '#000000',
                                                'align': 'center',
                                                'border': 1,
                                                'text_wrap': True,
                                                'valign': 'vcenter'})
            header_style_no_bold = workbook.add_format({'font_size': 11,
                                                        'font_name': "Times New Roman",
                                                        'font_color': '#000000',
                                                        'align': 'center',
                                                        'border': 1,
                                                        'text_wrap': True,
                                                        'valign': 'vcenter'})
            header_style_no_bold_thu = workbook.add_format({'font_size': 11,
                                                            'font_name': "Times New Roman",
                                                            'font_color': '#000000',
                                                            'align': 'center',
                                                            'border': 1,
                                                            'text_wrap': True,
                                                            'valign': 'vcenter',
                                                            'rotation': 90})
            header_style_no_bold_size_10 = workbook.add_format({'font_size': 10,
                                                                'font_name': "Times New Roman",
                                                                'font_color': '#000000',
                                                                'align': 'center',
                                                                'border': 1,
                                                                'text_wrap': True,
                                                                'valign': 'vcenter'})
            header_style_no_bold_size_10_weekend = workbook.add_format({'bold': True,
                                                                        'font_size': 10,
                                                                        'font_name': "Times New Roman",
                                                                        'font_color': '#CC0000',
                                                                        'align': 'center',
                                                                        'border': 1,
                                                                        'bg_color': '#92D14F',
                                                                        'text_wrap': True,
                                                                        'valign': 'vcenter'})
            header_style_no_bold_weekend = workbook.add_format({'bold': True,
                                                                'font_size': 11,
                                                                'font_name': "Times New Roman",
                                                                'font_color': '#CC0000',
                                                                'align': 'center',
                                                                'border': 1,
                                                                'bg_color': '#92D14F',
                                                                'text_wrap': True,
                                                                'valign': 'vcenter'})
            header_style_no_bold_weekend_thu = workbook.add_format({'bold': True,
                                                                    'font_size': 11,
                                                                    'font_name': "Times New Roman",
                                                                    'font_color': '#CC0000',
                                                                    'align': 'center',
                                                                    'border': 1,
                                                                    'bg_color': '#92D14F',
                                                                    'text_wrap': True,
                                                                    'valign': 'vcenter',
                                                                    'rotation': 90})

            sheet.merge_range('A10:A13', 'STT', header_style)
            sheet.merge_range('B10:B13', 'MÃ NV', header_style)
            sheet.merge_range('C10:C13', 'HỌ TÊN', header_style)
            sheet.merge_range('D10:D13', 'CHỨC DANH', header_style)

            last_day_of_month = int(calendar.monthrange(int(attendance_id.year), int(attendance_id.month))[1])
            sheet.merge_range(9, 4, 9, 34, 'Thứ, ngày trong tháng', header_style)
            if last_day_of_month:
                for i in range(31):
                    day = i + 1
                    month = attendance_id.month
                    year = attendance_id.year
                    if i < last_day_of_month:
                        pass
                    else:
                        day = i + 1 - last_day_of_month
                        if int(attendance_id.month) != 12:
                            month = int(attendance_id.month) + 1
                        else:
                            month = 1
                            year = int(attendance_id.year) + 1

                    dates = int(date.weekday(date(int(year), int(month), day)))
                    thu = ""
                    if dates == 0:
                        thu = "Thứ hai"
                    elif dates == 1:
                        thu = "Thứ ba"
                    elif dates == 2:
                        thu = "Thứ tư"
                    elif dates == 3:
                        thu = "Thứ năm"
                    elif dates == 4:
                        thu = "Thứ sáu"
                    elif dates == 5:
                        thu = "Thứ bảy"
                    elif dates == 6:
                        thu = "Chủ nhật"
                    sheet.write(10, i + 4, thu,
                                header_style_no_bold_thu if dates not in [5, 6] else header_style_no_bold_weekend_thu)

                    sheet.write(11, i + 4, str(day) + "/" + str(month) + "/" + str(year),
                                header_style_no_bold_size_10 if dates not in [5, 6] else header_style_no_bold_weekend)
                    sheet.write(12, i + 4, str(day),
                                header_style_no_bold if dates not in [5, 6] else header_style_no_bold_size_10_weekend)

                    '''lấy danh sách'''

            department_style = workbook.add_format({'bold': True,
                                                    'font_size': 9,
                                                    'font_name': "Times New Roman",
                                                    'font_color': '#000000',
                                                    'bg_color': '#C6E0B4',
                                                    'align': 'left',
                                                    'border': 1,
                                                    'text_wrap': True,
                                                    'valign': 'vcenter'})
            sum_style = workbook.add_format({'bold': True,
                                             'font_size': 9,
                                             'font_name': "Times New Roman",
                                             'font_color': '#000000',
                                             'bg_color': '#DDEBF7',
                                             'align': 'left',
                                             'border': 1,
                                             'text_wrap': True,
                                             'valign': 'vcenter'})
            sum_content_style_bold = workbook.add_format({'bold': True,
                                                          'font_size': 9,
                                                          'font_name': "Times New Roman",
                                                          'font_color': '#000000',
                                                          'align': 'center',
                                                          'bg_color': '#DDEBF7',
                                                          'border': 1,
                                                          'text_wrap': True,
                                                          'valign': 'vcenter'})
            sum_content_style_bold.set_num_format(43)
            row = 13
            stt = 0
            '''lọc theo user đăng nhập'''
            department_list = []
            employee_list_s = []
            # print(self.env.user.id)
            if self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_manager'):
                employee_list_s = self.env['hr.employee.multi.company'].sudo().search(
                    [('company_id', '=', self.env.user.company_id.id)]).ids

            elif self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                employee = self.env['hr.employee.multi.company'].sudo().search(
                    [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
                if employee:
                    department_list.append(employee.department_id.id)
                    employee_list_s.append(employee.id)
                    department_ids = self.env['hr.department'].sudo().search(
                        [('manager_ids', 'in', employee.name.sudo().id)])

                    if department_ids:
                        for department in department_ids:
                            department_list.append(department.id)
                            employee_ids = self.env['hr.employee.multi.company'].sudo().search(
                                [('department_id', '=', department.id),
                                 ('company_id', '=', self.env.user.company_id.id)])
                            if employee_ids:
                                for employees in employee_ids:
                                    employee_list_s.append(employees.id)
            # print(department_list)
            # print(employee_list_s)
            ''''''
            departments = None
            if self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_manager'):
                departments = self.env['hr.department'].sudo().search(
                    [('company_id', '=', attendance_id.sudo().company_id.id), ('active', '=', True)],
                    order='sort_name asc')
            else:
                if department_list is not None and self.env.user.has_group('seatek_hr_attendance.hr_attendance_user'):
                    departments = self.env['hr.department'].sudo().search(
                        [('id', 'in', department_list),
                         ('company_id', '=', attendance_id.sudo().company_id.id), ('active', '=', True)],
                        order='sort_name asc')
            list_in = []
            if departments is not None:
                for department in departments:
                    check = True
                    if attendance_id.department_id:
                        check = False
                        if attendance_id.department_id.id == department.id:
                            check = True
                    if check:
                        row += 1
                        job_positions = self.env['hr.job'].sudo().search(
                            [('company_id', '=', attendance_id.sudo().company_id.id),
                             ('department_id', '=', department.id)],
                            order='sequence asc')
                        sheet.set_row(row - 1, 20)
                        department_parent = ''
                        if department.parent_id:
                            department_parent = department.sudo().parent_id.name + '/'
                        sheet.write('A%s' % row, '', department_style)
                        sheet.merge_range('B%s:BE%s' % (row, row), department_parent + department.name,
                                          department_style)
                        write_tc = False
                        start = row + 1

                        for job_position in job_positions:
                            if employee_list_s is not None:
                                employee_ids = self.env['hr.employee.multi.company'].sudo().search(
                                    [('id', 'in', employee_list_s),
                                     ('id', 'in',
                                      [i.employee_multi_id.id for i in attendance_id.attendance_of_month_compute]),
                                     ('department_id', '=', department.id),
                                     ('job_id', '=', job_position.id)])
                            else:
                                employee_ids = self.env['hr.employee.multi.company'].sudo().search(
                                    [('id', 'in',
                                      [i.employee_multi_id.id for i in attendance_id.attendance_of_month_compute]),
                                     ('department_id', '=', department.id),
                                     ('job_id', '=', job_position.id)])
                            # print(employee_ids)
                            if employee_ids:
                                write_tc = True
                                employee_attendance = self.env['sea.hr.attendance.month'].sudo().search(
                                    [('employee_multi_id', 'in', employee_ids.ids),
                                     ('attendance_id', '=', attendance_id.id)])
                                for attendance in employee_attendance:
                                    if attendance.employee_multi_id:
                                        stt += 1
                                        row += 1
                                        list_in.append(attendance.employee_multi_id.sudo().id)
                                        # sheet.write('B%s' % row, attendance.employee_multi_id.sudo().name.name)
                                        self.employee_list(stt, row, sheet, attendance, workbook, objects)
                        end = row
                        if write_tc:
                            # stt += 1
                            row += 1
                            sheet.write('A%s' % row, '', sum_style)
                            sheet.merge_range('B%s:AI%s' % (row, row), 'Tổng cộng', sum_style)
                            '''các công thức tính toán'''

                            sheet.write('AJ%s' % row, '=SUM(AJ%s:AJ%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AK%s' % row, '=SUM(AK%s:AK%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AL%s' % row, '=SUM(AK%s:AK%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AM%s' % row, '=SUM(AM%s:AM%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AN%s' % row, '=SUM(AN%s:AN%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AO%s' % row, '=SUM(AO%s:Ao%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AP%s' % row, '=SUM(AP%s:AP%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AQ%s' % row, '=SUM(AQ%s:AQ%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AR%s' % row, '=SUM(AR%s:AR%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AS%s' % row, '=SUM(AS%s:AS%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AT%s' % row, '=SUM(AT%s:AT%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AU%s' % row, '=SUM(AU%s:AU%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AV%s' % row, '=SUM(AV%s:AV%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AW%s' % row, '=SUM(AW%s:AW%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AX%s' % row, '=SUM(AX%s:AX%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AY%s' % row, '=SUM(AY%s:AY%s)' % (start, end), sum_content_style_bold)
                            sheet.write('AZ%s' % row, '=SUM(AZ%s:AZ%s)' % (start, end), sum_content_style_bold)
                            sheet.write('BA%s' % row, '=SUM(BA%s:BA%s)' % (start, end), sum_content_style_bold)
                            sheet.write('BB%s' % row, '=SUM(BB%s:BB%s)' % (start, end), sum_content_style_bold)
                            sheet.write('BC%s' % row, '=SUM(BC%s:BC%s)' % (start, end), sum_content_style_bold)
                            sheet.write('BD%s' % row, '=SUM(BD%s:BD%s)' % (start, end), sum_content_style_bold)
                            sheet.write('BE%s' % row, '=SUM(BE%s:BE%s)' % (start, end), sum_content_style_bold)

            employee_multi_companies = None
            if self.env.user.has_group(
                    'seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_manager'):
                employee_multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                    [('id', 'in', [i.employee_multi_id.id for i in attendance_id.attendance_of_month_compute]),
                     ('id', 'not in', list_in)])
            else:
                if self.env.user.has_group('seatek_hr_attendance.hr_attendance_user') and employee_list_s is not None:
                    employee_multi_companies = self.env['hr.employee.multi.company'].sudo().search(
                        [('id', 'in', [i.employee_multi_id.id for i in attendance_id.attendance_of_month_compute]),
                         ('id', 'not in', list_in), ('id', 'in', employee_list_s)])

            # print(employee_multi_companies)
            if employee_multi_companies is not None and employee_multi_companies:
                row += 1
                sheet.write('A%s' % row, '', department_style)
                sheet.merge_range('B%s:BE%s' % (row, row), 'Không xác định', department_style)
                employee_attendance = self.env['sea.hr.attendance.month'].sudo().search(
                    [('employee_multi_id', 'in', employee_multi_companies.ids),
                     ('attendance_id', '=', attendance_id.id)])
                start = row + 1
                for attendance in employee_attendance:
                    stt += 1
                    row += 1
                    # sheet.write('B%s' % row, attendance.employee_multi_id.sudo().name.name)
                    self.employee_list(stt, row, sheet, attendance, workbook, objects)
                end = row
                stt += 1
                row += 1
                sheet.write('A%s' % row, '', sum_style)
                sheet.merge_range('B%s:AI%s' % (row, row), 'Tổng Cộng', sum_style)
                '''các công thức tính toán'''
                sheet.write('AJ%s' % row, '=SUM(AJ%s:AJ%s)' % (start, end), sum_content_style_bold)
                sheet.write('AK%s' % row, '=SUM(AK%s:AK%s)' % (start, end), sum_content_style_bold)
                sheet.write('AL%s' % row, '=SUM(AK%s:AK%s)' % (start, end), sum_content_style_bold)
                sheet.write('AM%s' % row, '=SUM(AM%s:AM%s)' % (start, end), sum_content_style_bold)
                sheet.write('AN%s' % row, '=SUM(AN%s:AN%s)' % (start, end), sum_content_style_bold)
                sheet.write('AO%s' % row, '=SUM(AO%s:Ao%s)' % (start, end), sum_content_style_bold)
                sheet.write('AP%s' % row, '=SUM(AP%s:AP%s)' % (start, end), sum_content_style_bold)
                sheet.write('AQ%s' % row, '=SUM(AQ%s:AQ%s)' % (start, end), sum_content_style_bold)
                sheet.write('AR%s' % row, '=SUM(AR%s:AR%s)' % (start, end), sum_content_style_bold)
                sheet.write('AS%s' % row, '=SUM(AS%s:AS%s)' % (start, end), sum_content_style_bold)
                sheet.write('AT%s' % row, '=SUM(AT%s:AT%s)' % (start, end), sum_content_style_bold)
                sheet.write('AU%s' % row, '=SUM(AU%s:AU%s)' % (start, end), sum_content_style_bold)
                sheet.write('AV%s' % row, '=SUM(AV%s:AV%s)' % (start, end), sum_content_style_bold)
                sheet.write('AW%s' % row, '=SUM(AW%s:AW%s)' % (start, end), sum_content_style_bold)
                sheet.write('AX%s' % row, '=SUM(AX%s:AX%s)' % (start, end), sum_content_style_bold)
                sheet.write('AY%s' % row, '=SUM(AY%s:AY%s)' % (start, end), sum_content_style_bold)
                sheet.write('AZ%s' % row, '=SUM(AZ%s:AZ%s)' % (start, end), sum_content_style_bold)
                sheet.write('BA%s' % row, '=SUM(BA%s:BA%s)' % (start, end), sum_content_style_bold)
                sheet.write('BB%s' % row, '=SUM(BB%s:BB%s)' % (start, end), sum_content_style_bold)
                sheet.write('BC%s' % row, '=SUM(BC%s:BC%s)' % (start, end), sum_content_style_bold)
                sheet.write('BD%s' % row, '=SUM(BD%s:BD%s)' % (start, end), sum_content_style_bold)
                sheet.write('BE%s' % row, '=SUM(BE%s:BE%s)' % (start, end), sum_content_style_bold)

            '''phần thêm công thức tính toán'''

            header_style_bg_bray = workbook.add_format({'bold': True,
                                                        'font_size': 11,
                                                        'font_name': "Times New Roman",
                                                        'font_color': '#000000',
                                                        'align': 'center',
                                                        'border': 1,
                                                        'bg_color': '#D6DCE4',
                                                        'text_wrap': True,
                                                        'valign': 'vcenter'})
            header_style_90 = workbook.add_format({'bold': True,
                                                   'font_size': 11,
                                                   'font_name': "Times New Roman",
                                                   'font_color': '#000000',
                                                   'align': 'center',
                                                   'border': 1,
                                                   'text_wrap': True,
                                                   'valign': 'vcenter',
                                                   'rotation': 90})
            header_style_bg_237 = workbook.add_format({'bold': True,
                                                       'font_size': 11,
                                                       'font_name': "Times New Roman",
                                                       'font_color': '#000000',
                                                       'align': 'center',
                                                       'border': 1,
                                                       'bg_color': '#EDEDED',
                                                       'text_wrap': True,
                                                       'valign': 'vcenter'})
            header_style_bg_yellow = workbook.add_format({'bold': True,
                                                          'font_size': 11,
                                                          'font_name': "Times New Roman",
                                                          'font_color': '#000000',
                                                          'align': 'center',
                                                          'border': 1,
                                                          'bg_color': '#FFFF00',
                                                          'text_wrap': True,
                                                          'valign': 'vcenter',
                                                          'rotation': 90})
            header_style_bg_green = workbook.add_format({'bold': True,
                                                         'font_size': 11,
                                                         'font_name': "Times New Roman",
                                                         'font_color': '#000000',
                                                         'align': 'center',
                                                         'border': 1,
                                                         'bg_color': '#E2EFDA',
                                                         'text_wrap': True,
                                                         'valign': 'vcenter',
                                                         'rotation': 90})
            header_style_bg_217 = workbook.add_format({'bold': True,
                                                       'font_size': 11,
                                                       'font_name': "Times New Roman",
                                                       'font_color': '#000000',
                                                       'align': 'center',
                                                       'border': 1,
                                                       'bg_color': '#D9D9D9',
                                                       'text_wrap': True,
                                                       'valign': 'vcenter',
                                                       'rotation': 90})
            header_style_bg_217_col_red = workbook.add_format({'bold': True,
                                                               'font_size': 11,
                                                               'font_name': "Times New Roman",
                                                               'font_color': '#C00000',
                                                               'align': 'center',
                                                               'border': 1,
                                                               'bg_color': '#D9D9D9',
                                                               'text_wrap': True,
                                                               'valign': 'vcenter',
                                                               'rotation': 90})

            header_style_bg_yellow_col_red = workbook.add_format({'bold': True,
                                                                  'font_size': 11,
                                                                  'font_name': "Times New Roman",
                                                                  'font_color': '#C00000',
                                                                  'align': 'center',
                                                                  'border': 1,
                                                                  'bg_color': '#FFFF00',
                                                                  'text_wrap': True,
                                                                  'valign': 'vcenter',
                                                                  'rotation': 90})

            sheet.merge_range('AJ10:AY10', 'TỔNG HỢP CÔNG THỰC TẾ', header_style_bg_bray)
            sheet.merge_range('AZ10:BE10', 'Ngoài giờ', header_style_bg_237)

            '''TỔNG HỢP CÔNG THỰC TẾ'''
            sheet.merge_range('AJ11:AJ13', 'Làm việc (TV)', header_style_bg_yellow)
            sheet.merge_range('AK11:AK13', 'Công tác/ Học tập (TV)', header_style_bg_yellow)
            sheet.merge_range('AL11:AL13', 'WFH(TV)', header_style_bg_yellow)
            sheet.merge_range('AM11:AM13', 'Lễ/NM/NB (TV)', header_style_bg_yellow)
            sheet.merge_range('AN11:AN13', 'F/R(TV)', header_style_bg_yellow)
            sheet.merge_range('AO11:AO13', 'Không phân công (TV)', header_style_bg_yellow)

            sheet.merge_range('AP11:AP13', 'RO/TS/ Kg F (TV)', header_style_bg_yellow_col_red)
            sheet.merge_range('AQ11:AQ13', 'Khoán riêng (TV)', header_style_bg_yellow_col_red)

            sheet.merge_range('AR11:AR13', 'Làm việc', header_style_bg_217)
            sheet.merge_range('AS11:AS13', 'Công tác/Học tập', header_style_bg_217)
            sheet.merge_range('AT11:AT13', 'WFH - COVID', header_style_bg_217)
            sheet.merge_range('AU11:AU13', 'Lễ/NM/NB', header_style_bg_217)
            sheet.merge_range('AV11:AV13', 'F/R', header_style_bg_217)
            sheet.merge_range('AW11:AW13', 'Không phân công', header_style_bg_217)

            sheet.merge_range('AX11:AX13', 'RO/TS/ Kg F', header_style_bg_217_col_red)
            sheet.merge_range('AY11:AY13', 'Khoán riêng', header_style_bg_217_col_red)

            '''NGOÀI GIỜ'''
            sheet.merge_range('AZ11:AZ13', 'Ngày thường(TV)', header_style_bg_green)
            sheet.merge_range('BA11:BA13', 'T7 CN/Bù lễ(TV)', header_style_bg_green)
            sheet.merge_range('BB11:BB13', 'Lễ Tết(TV)', header_style_bg_green)
            sheet.merge_range('BC11:BC13', 'Ngày thường', header_style_90)
            sheet.merge_range('BD11:BD13', 'T7CN/Bù lễ', header_style_90)
            sheet.merge_range('BE11:BE13', 'Lễ/Tết', header_style_90)


class BangViPhamChamCong(models.AbstractModel):
    _name = 'report.seatek_hr_attendance.report_attendance_violation_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    # def employee_list(self, stt, row, sheet, attendenace_month_id, workbook, objects):
    #     content_style = workbook.add_format({'bold': False,
    #                                          'font_size': 9,
    #                                          'font_name': "Times New Roman",
    #                                          'font_color': '#000000',
    #                                          'align': 'center',
    #                                          'border': 1,
    #                                          'text_wrap': True,
    #                                          'valign': 'vcenter'})
    #     content_style_bold = workbook.add_format({'bold': True,
    #                                               'font_size': 9,
    #                                               'font_name': "Times New Roman",
    #                                               'font_color': '#000000',
    #                                               'align': 'center',
    #                                               'border': 1,
    #                                               'text_wrap': True,
    #                                               'valign': 'vcenter'})
    #     content_style_bold.set_num_format(43)
    #     sheet.write('A%s' % row, stt, content_style)
    #
    #     if attendenace_month_id.employee_multi_id.sudo().s_identification_id:
    #         sheet.write('B%s' % row, attendenace_month_id.employee_multi_id.sudo().s_identification_id, content_style)
    #     else:
    #         sheet.write('B%s' % row, '', content_style)
    #     if attendenace_month_id.employee_multi_id.sudo().name.name:
    #         sheet.write('C%s' % row, attendenace_month_id.employee_multi_id.sudo().name.name, content_style)
    #     else:
    #         sheet.write('C%s' % row, '', content_style)
    #     if attendenace_month_id.employee_multi_id.sudo().job_id.sudo().name:
    #         sheet.write('D%s' % row, attendenace_month_id.employee_multi_id.sudo().job_id.sudo().name, content_style)
    #     else:
    #         sheet.write('D%s' % row, '', content_style)
    #
    #     header_style_no_bold = workbook.add_format({'font_size': 11,
    #                                                 'font_name': "Times New Roman",
    #                                                 'font_color': '#000000',
    #                                                 'align': 'center',
    #                                                 'border': 1,
    #                                                 'text_wrap': True,
    #                                                 'valign': 'vcenter'})
    #     header_style_no_bold_weekend = workbook.add_format({'bold': True,
    #                                                         'font_size': 11,
    #                                                         'font_name': "Times New Roman",
    #                                                         'font_color': '#CC0000',
    #                                                         'align': 'center',
    #                                                         'border': 1,
    #                                                         'bg_color': '#92D14F',
    #                                                         'text_wrap': True,
    #                                                         'valign': 'vcenter'})
    #
    #     if attendenace_month_id.last_day_of_month:
    #         for i in range(31):
    #             symbol = False
    #             symbol_str = ''
    #             if i >= attendenace_month_id.last_day_of_month:
    #                 dates = int(
    #                     date.weekday(date(int(attendenace_month_id.year), int(int(attendenace_month_id.month) + 1),
    #                                       int(i + 1 - attendenace_month_id.last_day_of_month))))
    #             else:
    #                 dates = int(
    #                     date.weekday(date(int(attendenace_month_id.year), int(attendenace_month_id.month), int(i + 1))))
    #                 if i == 0:
    #                     symbol = attendenace_month_id.day_1.sudo()
    #                 elif i == 1:
    #                     symbol = attendenace_month_id.day_2.sudo()
    #                 elif i == 2:
    #                     symbol = attendenace_month_id.day_3.sudo()
    #                 elif i == 3:
    #                     symbol = attendenace_month_id.day_4.sudo()
    #                 elif i == 4:
    #                     symbol = attendenace_month_id.day_5.sudo()
    #                 elif i == 5:
    #                     symbol = attendenace_month_id.day_6.sudo()
    #                 elif i == 6:
    #                     symbol = attendenace_month_id.day_7.sudo()
    #                 elif i == 7:
    #                     symbol = attendenace_month_id.day_8.sudo()
    #                 elif i == 8:
    #                     symbol = attendenace_month_id.day_9.sudo()
    #                 elif i == 9:
    #                     symbol = attendenace_month_id.day_10.sudo()
    #                 elif i == 10:
    #                     symbol = attendenace_month_id.day_11.sudo()
    #                 elif i == 11:
    #                     symbol = attendenace_month_id.day_12.sudo()
    #                 elif i == 12:
    #                     symbol = attendenace_month_id.day_13.sudo()
    #                 elif i == 13:
    #                     symbol = attendenace_month_id.day_14.sudo()
    #                 elif i == 14:
    #                     symbol = attendenace_month_id.day_15.sudo()
    #                 elif i == 15:
    #                     symbol = attendenace_month_id.day_16.sudo()
    #                 elif i == 16:
    #                     symbol = attendenace_month_id.day_17.sudo()
    #                 elif i == 17:
    #                     symbol = attendenace_month_id.day_18.sudo()
    #                 elif i == 18:
    #                     symbol = attendenace_month_id.day_19.sudo()
    #                 elif i == 19:
    #                     symbol = attendenace_month_id.day_20.sudo()
    #                 elif i == 20:
    #                     symbol = attendenace_month_id.day_21.sudo()
    #                 elif i == 21:
    #                     symbol = attendenace_month_id.day_22.sudo()
    #                 elif i == 22:
    #                     symbol = attendenace_month_id.day_23.sudo()
    #                 elif i == 23:
    #                     symbol = attendenace_month_id.day_24.sudo()
    #                 elif i == 24:
    #                     symbol = attendenace_month_id.day_25.sudo()
    #                 elif i == 25:
    #                     symbol = attendenace_month_id.day_26.sudo()
    #                 elif i == 26:
    #                     symbol = attendenace_month_id.day_27.sudo()
    #                 elif i == 27:
    #                     symbol = attendenace_month_id.day_28.sudo()
    #                 elif i == 28:
    #                     symbol = attendenace_month_id.day_29.sudo()
    #                 elif i == 29:
    #                     symbol = attendenace_month_id.day_30.sudo()
    #                 elif i == 30:
    #                     symbol = attendenace_month_id.day_31.sudo()
    #
    #                 if symbol:
    #                     symbol_str = symbol.symbol.sudo().symbol
    #                     overtime = 0
    #                     # if symbol.shift_details:
    #                     #     for j in symbol.shift_details:
    #                     #         if j.overtime_hr:
    #                     #             overtime += j.overtime_hr
    #                     if symbol.overtime:
    #                         overtime = symbol.overtime
    #                     time = overtime % 1
    #                     if int(overtime) > 0 or time > 0:
    #                         o = int(overtime)
    #                         if time > 0:
    #                             time = time * 60
    #                             if 15 <= time < 45:
    #                                 o += 0.5
    #                             elif time >= 45:
    #                                 o += 1
    #                         if o > 0:
    #                             symbol_str += str(o)
    #                     date_contract_tv = datetime.datetime.strptime(
    #                         str(attendenace_month_id.year) + ' ' + str(attendenace_month_id.month) + ' ' + str(i + 1),
    #                         "%Y %m %d")
    #                     contract_tv = self.env['hr.contract'].sudo().search(
    #                         [('employee_id', '=', attendenace_month_id.employee_multi_id.sudo().name.id),
    #                          ('state', '!=', 'cancel'), ('date_start', '<=', date_contract_tv),
    #                          ('date_end', '>=', date_contract_tv),
    #                          ('type_id', '=', 4), ('contract_category', '=', 'contract')])
    #                     if contract_tv:
    #                         symbol_str = str('t') + symbol_str
    #
    #             sheet.write(row - 1, i + 4, symbol_str if dates not in [5, 6] and symbol else '',
    #                         header_style_no_bold if dates not in [5, 6] else header_style_no_bold_weekend)
    #
    #             '''lấy danh sách'''
    #
    #     '''các công thức tính toán'''
    #     aj = '=COUNTIF($E%s:$AI%s,\"tx\")+COUNTIF($E%s:$AI%s,\"tx/2\")/2+COUNTIF($E%s:$AI%s,\"tx1\")+COUNTIF($E%s:$AI%s,\"tx1.5\")+COUNTIF($E%s:$AI%s,\"tx2.5\")+COUNTIF($E%s:$AI%s,\"tx3.5\")+COUNTIF($E%s:$AI%s,\"tx4.5\")+COUNTIF($E%s:$AI%s,\"tx5.5\")+COUNTIF($E%s:$AI%s,\"tx6.5\")+COUNTIF($E%s:$AI%s,\"tx7.5\")+COUNTIF($E%s:$AI%s,\"tx2\")+COUNTIF($E%s:$AI%s,\"tx3\")+COUNTIF($E%s:$AI%s,\"tx4\")+COUNTIF($E%s:$AI%s,\"tx5\")+COUNTIF($E%s:$AI%s,\"tx6\")+COUNTIF($E%s:$AI%s,\"tx7\")+COUNTIF($E%s:$AI%s,\"tx8\")+COUNTIF($E%s:$AI%s,\"tct/2\")/2+COUNTIF($E%s:$AI%s,\"th/2\")/2+COUNTIF($E%s:$AI%s,\"tR/2\")/2+COUNTIF($E%s:$AI%s,\"tRO/2\")/2+COUNTIF($E%s:$AI%s,\"tO/2\")/2+COUNTIF($E%s:$AI%s,\"tSX/2\")/2+COUNTIF($E%s:$AI%s,\"tNB/2\")/2+COUNTIF($E%s:$AI%s,\"tNM/2\")/2'
    #     sheet.write('AJ%s' % row, aj % ((row,) * 50), content_style_bold)
    #
    #     ak = '=COUNTIF($E%s:$AI%s,\"tCT\")+COUNTIF($E%s:$AI%s,\"tCT/2\")/2+COUNTIF($E%s:$AI%s,\"tSCT/2\")/2+COUNTIF($E%s:$AI%s,\"tCT1\")+COUNTIF($E%s:$AI%s,\"tCT1.5\")+COUNTIF($E%s:$AI%s,\"tCT2\")+COUNTIF($E%s:$AI%s,\"tCT2.5\")+COUNTIF($E%s:$AI%s,\"tCT3\")+COUNTIF($E%s:$AI%s,\"tCT3.5\")+COUNTIF($E%s:$AI%s,\"tCT4.5\")+COUNTIF($E%s:$AI%s,\"tCT4\")+COUNTIF($E%s:$AI%s,\"tCT5\")+COUNTIF($E%s:$AI%s,\"tCT5.5\")+COUNTIF($E%s:$AI%s,\"tCT6\")+COUNTIF($E%s:$AI%s,\"tCT6.5\")*COUNTIF($E%s:$AI%s,\"tCT7\")+COUNTIF($E%s:$AI%s,\"tCT7.5\")*COUNTIF($E%s:$AI%s,\"tCT8\")+COUNTIF($E%s:$AI%s,\"tCT8.5\")+COUNTIF($E%s:$AI%s,\"tCT9\")+COUNTIF($E%s:$AI%s,\"tCT9.5\")+COUNTIF($E%s:$AI%s,\"tCT10\")+COUNTIF($E%s:$AI%s,\"tCT10.5\")+COUNTIF($E%s:$AI%s,\"TH\")+COUNTIF($E%s:$AI%s,\"TH/2\")/2'
    #     sheet.write('AK%s' % row, ak % ((row,) * 50), content_style_bold)
    #
    #     al = '=COUNTIF($E%s:$AI%s,\"TW\")+COUNTIF($E%s:$AI%s,\"TW/2\")/2+COUNTIF($E%s:$AI%s,\"TFW/2\")/2+COUNTIF($E%s:$AI%s,\"TWX/2\")/2'
    #     sheet.write('AL%s' % row, al % ((row,) * 8), content_style_bold)
    #
    #     am = '=COUNTIF($E%s:$AI%s,\"tL\")+COUNTIF($E%s:$AI%s,\"tL/2\")/2+COUNTIF($E%s:$AI%s,\"tNM\")+COUNTIF($E%s:$AI%s,\"tNM/2\")/2+COUNTIF($E%s:$AI%s,\"tNB\")+COUNTIF($E%s:$AI%s,\"tNB/2\")/2+COUNTIF($E%s:$AI%s,\"tL1\")+COUNTIF($E%s:$AI%s,\"tL1.5\")+COUNTIF($E%s:$AI%s,\"tL2\")+COUNTIF($E%s:$AI%s,\"tL2.5\")+COUNTIF($E%s:$AI%s,\"tL3\")++COUNTIF($E%s:$AI%s,\"tL3.5\")+COUNTIF($E%s:$AI%s,\"tL4\")+COUNTIF($E%s:$AI%s,\"tL4.5\")+COUNTIF($E%s:$AI%s,\"tL5\")+COUNTIF($E%s:$AI%s,\"tL5.5\")+COUNTIF($E%s:$AI%s,\"tL6\")+COUNTIF($E%s:$AI%s,\"tL6.5\")+COUNTIF($E%s:$AI%s,\"tL7\")+COUNTIF($E%s:$AI%s,\"tL7.5\")+COUNTIF($E%s:$AI%s,\"tL8\")+COUNTIF($E%s:$AI%s,\"tL8.5\")+COUNTIF($E%s:$AI%s,\"tSL/2\")/2+COUNTIF($E%s:$AI%s,\"tSL1\")/2+COUNTIF($E%s:$AI%s,\"tSL2\")/2+COUNTIF($E%s:$AI%s,\"tSL3\")/2+COUNTIF($E%s:$AI%s,\"tSL4\")/2+COUNTIF($E%s:$AI%s,\"tSL5\")/2+COUNTIF($E%s:$AI%s,\"tSL6\")/2+COUNTIF($E%s:$AI%s,\"tSL7\")/2+COUNTIF($E%s:$AI%s,\"tSL8\")/2+COUNTIF($E%s:$AI%s,\"tSNM/2\")/2+COUNTIF($E%s:$AI%s,\"tBL\")+COUNTIF($E%s:$AI%s,\"tBL/2\")/2+COUNTIF($E%s:$AI%s,\"tBL1\")+COUNTIF($E%s:$AI%s,\"tBL2\")+COUNTIF($E%s:$AI%s,\"tBL3\")+COUNTIF($E%s:$AI%s,\"tBL4\")+COUNTIF($E%s:$AI%s,\"tBL5\")+COUNTIF($E%s:$AI%s,\"tBL6\")+COUNTIF($E%s:$AI%s,\"tBL7\")+COUNTIF($E%s:$AI%s,\"tBL8\")'
    #     sheet.write('AM%s' % row, am % ((row,) * 84), content_style_bold)
    #
    #     an = '=COUNTIF($E%s:$AI%s,\"tF\")+COUNTIF($E%s:$AI%s,\"tF/2\")/2+COUNTIF($E%s:$AI%s,\"tR\")+COUNTIF($E%s:$AI%s,\"tR/2\")/2+COUNTIF($E%s:$AI%s,\"tSF/2\")/2+COUNTIF($E%s:$AI%s,\"tSR/2\")/2'
    #     sheet.write('AN%s' % row, an % ((row,) * 12), content_style_bold)
    #
    #     ao = '=COUNTIF($E%s:$AI%s,\"tK\")'
    #     sheet.write('AO%s' % row, ao % ((row,) * 2), content_style_bold)
    #
    #     ap = '=COUNTIF($E%s:$AI%s,\"tRO\")+COUNTIF($E%s:$AI%s,\"tRO/2\")/2+COUNTIF($E%s:$AI%s,\"tO\")+COUNTIF($E%s:$AI%s,\"tO/2\")/2+COUNTIF($E%s:$AI%s,\"tSRO/2\")/2+COUNTIF($E%s:$AI%s,\"tSO/2\")/2+COUNTIF($E%s:$AI%s,\"tTS/2\")/2+COUNTIF($E%s:$AI%s,\"tTS\")+COUNTIF($E%s:$AI%s,\"tCÔ\")+COUNTIF($E%s:$AI%s,\"tCÔ/2\")/2'
    #     sheet.write('AP%s' % row, ap % ((row,) * 20), content_style_bold)
    #
    #     aq = '=COUNTIF($E%s:$AI%s,\"TKH\")+COUNTIF($E%s:$AI%s,\"TKH/2\")/2'
    #     sheet.write('AQ%s' % row, aq % ((row,) * 4), content_style_bold)
    #
    #     ar = '=COUNTIF($E%s:$AI%s,\"x\")+COUNTIF($E%s:$AI%s,\"x/2\")/2+COUNTIF($E%s:$AI%s,\"F/2\")/2+COUNTIF($E%s:$AI%s,\"x0.5\")+COUNTIF($E%s:$AI%s,\"x1\")+COUNTIF($E%s:$AI%s,\"x1.5\")+COUNTIF($E%s:$AI%s,\"x2.5\")+COUNTIF($E%s:$AI%s,\"x3.5\")+COUNTIF($E%s:$AI%s,\"x4.5\")+COUNTIF($E%s:$AI%s,\"x5.5\")+COUNTIF($E%s:$AI%s,\"x6.5\")+COUNTIF($E%s:$AI%s,\"x7.5\")+COUNTIF($E%s:$AI%s,\"x2\")+COUNTIF($E%s:$AI%s,\"x3\")+COUNTIF($E%s:$AI%s,\"x4\")+COUNTIF($E%s:$AI%s,\"x5\")+COUNTIF($E%s:$AI%s,\"x6\")+COUNTIF($E%s:$AI%s,\"x7\")+COUNTIF($E%s:$AI%s,\"x8\")+COUNTIF($E%s:$AI%s,\"x9\")+COUNTIF($E%s:$AI%s,\"x10\")+COUNTIF($E%s:$AI%s,\"x11\")+COUNTIF($E%s:$AI%s,\"ct/2\")/2+COUNTIF($E%s:$AI%s,\"h/2\")/2+COUNTIF($E%s:$AI%s,\"R/2\")/2+COUNTIF($E%s:$AI%s,\"RO/2\")/2+COUNTIF($E%s:$AI%s,\"O/2\")/2+COUNTIF($E%s:$AI%s,\"SX/2\")/2+COUNTIF($E%s:$AI%s,\"XW/2\")/2+COUNTIF($E%s:$AI%s,\"WX/2\")/2+COUNTIF($E%s:$AI%s,\"NB/2\")/2+COUNTIF($E%s:$AI%s,\"WNX/2\")/2+COUNTIF($E%s:$AI%s,\"NM/2\")/2'
    #     sheet.write('AR%s' % row, ar % ((row,) * 66), content_style_bold)
    #
    #     a_s = '=COUNTIF($E%s:$AI%s,\"CT\")+COUNTIF($E%s:$AI%s,\"CT/2\")/2+COUNTIF($E%s:$AI%s,\"SCT/2\")/2+COUNTIF($E%s:$AI%s,\"CT1\")+COUNTIF($E%s:$AI%s,\"CT1.5\")+COUNTIF($E%s:$AI%s,\"CT2\")+COUNTIF($E%s:$AI%s,\"CT2.5\")+COUNTIF($E%s:$AI%s,\"CT3\")+COUNTIF($E%s:$AI%s,\"CT3.5\")+COUNTIF($E%s:$AI%s,\"CT4.5\")+COUNTIF($E%s:$AI%s,\"CT4\")+COUNTIF($E%s:$AI%s,\"CT5\")+COUNTIF($E%s:$AI%s,\"CT5.5\")+COUNTIF($E%s:$AI%s,\"CT6\")+COUNTIF($E%s:$AI%s,\"CT6.5\")*COUNTIF($E%s:$AI%s,\"CT7\")+COUNTIF($E%s:$AI%s,\"CT7.5\")*COUNTIF($E%s:$AI%s,\"CT8\")+COUNTIF($E%s:$AI%s,\"CT8.5\")+COUNTIF($E%s:$AI%s,\"CT9\")+COUNTIF($E%s:$AI%s,\"CT9.5\")+COUNTIF($E%s:$AI%s,\"CT10\")+COUNTIF($E%s:$AI%s,\"CT10.5\")+COUNTIF($E%s:$AI%s,\"H\")+COUNTIF($E%s:$AI%s,\"H/2\")/2'
    #     sheet.write('AS%s' % row, a_s % ((row,) * 50), content_style_bold)
    #
    #     at = '=COUNTIF($E%s:$AI%s,\"W\")+COUNTIF($E%s:$AI%s,\"WN/2\")/2+COUNTIF($E%s:$AI%s,\"FW/2\")/2+COUNTIF($E%s:$AI%s,\"WX/2\")/2+COUNTIF($E%s:$AI%s,\"XW/2\")/2'
    #     sheet.write('AT%s' % row, at % ((row,) * 10), content_style_bold)
    #
    #     au = '=COUNTIF($E%s:$AI%s,\"L\")+COUNTIF($E%s:$AI%s,\"L/2\")/2+COUNTIF($E%s:$AI%s,\"NM\")+COUNTIF($E%s:$AI%s,\"NM/2\")/2+COUNTIF($E%s:$AI%s,\"NB\")+COUNTIF($E%s:$AI%s,\"NB/2\")/2+COUNTIF($E%s:$AI%s,\"L1\")+COUNTIF($E%s:$AI%s,\"L2\")+COUNTIF($E%s:$AI%s,\"L3\")+COUNTIF($E%s:$AI%s,\"L4\")+COUNTIF($E%s:$AI%s,\"L5\")+COUNTIF($E%s:$AI%s,\"L6\")+COUNTIF($E%s:$AI%s,\"L7\")+COUNTIF($E%s:$AI%s,\"L8\")+COUNTIF($E%s:$AI%s,\"SL/2\")/2+COUNTIF($E%s:$AI%s,\"SL1\")/2+COUNTIF($E%s:$AI%s,\"SL2\")/2+COUNTIF($E%s:$AI%s,\"SL3\")/2+COUNTIF($E%s:$AI%s,\"SL4\")/2+COUNTIF($E%s:$AI%s,\"SL5\")/2+COUNTIF($E%s:$AI%s,\"SL6\")/2+COUNTIF($E%s:$AI%s,\"SL7\")/2+COUNTIF($E%s:$AI%s,\"SL8\")/2+COUNTIF($E%s:$AI%s,\"SNM/2\")/2+COUNTIF($E%s:$AI%s,\"NBF/2\")/2+COUNTIF($E%s:$AI%s,\"BL\")+COUNTIF($E%s:$AI%s,\"BL/2\")/2+COUNTIF($E%s:$AI%s,\"BL1\")+COUNTIF($E%s:$AI%s,\"BL2\")+COUNTIF($E%s:$AI%s,\"BL3\")+COUNTIF($E%s:$AI%s,\"BL4\")+COUNTIF($E%s:$AI%s,\"BL5\")+COUNTIF($E%s:$AI%s,\"BL6\")+COUNTIF($E%s:$AI%s,\"BL7\")+COUNTIF($E%s:$AI%s,\"BL8\")'
    #     sheet.write('AU%s' % row, au % ((row,) * 70), content_style_bold)
    #
    #     av = '=COUNTIF($E%s:$AI%s,\"F\")+COUNTIF($E%s:$AI%s,\"F/2\")/2+COUNTIF($E%s:$AI%s,\"R\")+COUNTIF($E%s:$AI%s,\"R/2\")/2+COUNTIF($E%s:$AI%s,\"SF/2\")/2+COUNTIF($E%s:$AI%s,\"SR/2\")/2+COUNTIF($E%s:$AI%s,\"WF/2\")/2+COUNTIF($E%s:$AI%s,\"FW/2\")/2+COUNTIF($E%s:$AI%s,\"KF/2\")/2+COUNTIF($E%s:$AI%s,\"FK/2\")/2+COUNTIF($E%s:$AI%s,\"NBF/2\")/2+COUNTIF($E%s:$AI%s,\"ROF/2\")/2+COUNTIF($E%s:$AI%s,\"FRO/2\")/2+COUNTIF($E%s:$AI%s,\"FWN/2\")/2'
    #     sheet.write('AV%s' % row, av % ((row,) * 28), content_style_bold)
    #
    #     aw = '=COUNTIF($E%s:$AI%s,\"K\")+COUNTIF($E%s:$AI%s,\"KF/2\")/2+COUNTIF($E%s:$AI%s,\"FK/2\")/2+COUNTIF($E%s:$AI%s,\"KRO/2\")/2+COUNTIF($E%s:$AI%s,\"ROK/2\")/2+COUNTIF($E%s:$AI%s,\"KW/2\")/2+COUNTIF($E%s:$AI%s,\"WK/2\")/2+COUNTIF($E%s:$AI%s,\"K/2\")/2'
    #     sheet.write('AW%s' % row, aw % ((row,) * 16), content_style_bold)
    #
    #     ax = '=COUNTIF($E%s:$AI%s,\"RO\")+COUNTIF($E%s:$AI%s,\"RO/2\")/2+COUNTIF($E%s:$AI%s,\"O\")+COUNTIF($E%s:$AI%s,\"O/2\")/2+COUNTIF($E%s:$AI%s,\"SRO/2\")/2+COUNTIF($E%s:$AI%s,\"SO/2\")/2+COUNTIF($E%s:$AI%s,\"TS/2\")/2+COUNTIF($E%s:$AI%s,\"TS\")+COUNTIF($E%s:$AI%s,\"CÔ\")+COUNTIF($E%s:$AI%s,\"CÔ/2\")/2+COUNTIF($E%s:$AI%s,\"ROW/2\")/2+COUNTIF($E%s:$AI%s,\"WRO/2\")/2+COUNTIF($E%s:$AI%s,\"KRO/2\")/2+COUNTIF($E%s:$AI%s,\"ROK/2\")/2+COUNTIF($E%s:$AI%s,\"ROF/2\")/2+COUNTIF($E%s:$AI%s,\"FRO/2\")/2+COUNTIF($E%s:$AI%s,\"Ô\")+COUNTIF($E%s:$AI%s,\"Ô/2\")/2'
    #     sheet.write('AX%s' % row, ax % ((row,) * 36), content_style_bold)
    #
    #     ay = '=COUNTIF($E%s:$AI%s,\"KH\")+COUNTIF($E%s:$AI%s,\"KH/2\")/2'
    #     sheet.write('AY%s' % row, ay % (row, row, row, row), content_style_bold)
    #
    #     az = '=COUNTIF($E%s:$AI%s,\"tX1\")+COUNTIF($E%s:$AI%s,\"tX1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tX2\")*2+COUNTIF($E%s:$AI%s,\"tX2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tX3\")*3+COUNTIF($E%s:$AI%s,\"tX3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tX4\")*4+COUNTIF($E%s:$AI%s,\"tX4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tX5\")*5+COUNTIF($E%s:$AI%s,\"tX5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tX6\")*6+COUNTIF($E%s:$AI%s,\"tX6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tX7\")*7+COUNTIF($E%s:$AI%s,\"tX7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tX8\")*8+ COUNTIF($E%s:$AI%s,\"tCT1\")*1+COUNTIF($E%s:$AI%s,\"tCT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tCT2\")*2+COUNTIF($E%s:$AI%s,\"tCT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tCT3\")*3+COUNTIF($E%s:$AI%s,\"tCT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tCT4\")*4+COUNTIF($E%s:$AI%s,\"tCT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tCT5\")*5+COUNTIF($E%s:$AI%s,\"tCT6\")*6+COUNTIF($E%s:$AI%s,\"tCT7\")*7+COUNTIF($E%s:$AI%s,\"tCT8\")*8+COUNTIF($E%s:$AI%s,\"tCT10.5\")*10.5'
    #     sheet.write('AZ%s' % row, az % ((row,) * 56), content_style_bold)
    #
    #     ba = '=COUNTIF($E%s:$AI%s,\"tOT1\")+COUNTIF($E%s:$AI%s,\"tOT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tOT2\")*2+COUNTIF($E%s:$AI%s,\"tOT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tOT3\")*3+COUNTIF($E%s:$AI%s,\"tOT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tOT4\")*4+COUNTIF($E%s:$AI%s,\"tOT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tOT5\")*5+COUNTIF($E%s:$AI%s,\"tOT5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tOT6\")*6+COUNTIF($E%s:$AI%s,\"tOT6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tOT7\")*7+COUNTIF($E%s:$AI%s,\"tOT7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tOT8\")*8+COUNTIF($E%s:$AI%s,\"tTB1\")+COUNTIF($E%s:$AI%s,\"tTB1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tTB2\")*2+COUNTIF($E%s:$AI%s,\"tTB2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tTB3\")*3+COUNTIF($E%s:$AI%s,\"tTB3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tTB4\")*4+COUNTIF($E%s:$AI%s,\"tTB4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tTB5\")*5+COUNTIF($E%s:$AI%s,\"tTB5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tTB6\")*6+COUNTIF($E%s:$AI%s,\"tTB6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tTB7\")*7+COUNTIF($E%s:$AI%s,\"tTB7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tTB8\")*8+COUNTIF($E%s:$AI%s,\"tCN1\")+COUNTIF($E%s:$AI%s,\"tCN1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tCN2\")*2+COUNTIF($E%s:$AI%s,\"tCN2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tCN3\")*3+COUNTIF($E%s:$AI%s,\"tCN3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tCN4\")*4+COUNTIF($E%s:$AI%s,\"tCN4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tCN5\")*5+COUNTIF($E%s:$AI%s,\"tCN5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tCN6\")*6+COUNTIF($E%s:$AI%s,\"tCN6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tCN7\")*7+COUNTIF($E%s:$AI%s,\"tCN7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tCN8\")*8+COUNTIF($E%s:$AI%s,\"tBL1\")+COUNTIF($E%s:$AI%s,\"tBL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tBL2\")*2+COUNTIF($E%s:$AI%s,\"tBL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tBL3\")*3+COUNTIF($E%s:$AI%s,\"tBL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tBL4\")*4+COUNTIF($E%s:$AI%s,\"tBL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tBL5\")*5+COUNTIF($E%s:$AI%s,\"tBL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tBL6\")*6+COUNTIF($E%s:$AI%s,\"tBL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tBL7\")*7+COUNTIF($E%s:$AI%s,\"tBL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tBL8\")*8'
    #     sheet.write('BA%s' % row, ba % ((row,) * 120), content_style_bold)
    #
    #     bb = '=COUNTIF($E%s:$AI%s,\"tL1\")+COUNTIF($E%s:$AI%s,\"tL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"tL2\")*2+COUNTIF($E%s:$AI%s,\"tL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"tL3\")*3+COUNTIF($E%s:$AI%s,\"tL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"tL4\")*4+COUNTIF($E%s:$AI%s,\"tL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"tL5\")*5+COUNTIF($E%s:$AI%s,\"tL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"tL6\")*6+COUNTIF($E%s:$AI%s,\"tL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"tL7\")*7+COUNTIF($E%s:$AI%s,\"tL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"tL8\")*8+COUNTIF($E%s:$AI%s,\"tSL1\")*1+COUNTIF($E%s:$AI%s,\"tSL2\")*2+COUNTIF($E%s:$AI%s,\"tSL3\")*3+COUNTIF($E%s:$AI%s,\"tSL4\")*4+COUNTIF($E%s:$AI%s,\"tSL5\")*5+COUNTIF($E%s:$AI%s,\"tSL6\")*6+COUNTIF($E%s:$AI%s,\"tSL7\")*7+COUNTIF($E%s:$AI%s,\"tSL8\")*8'
    #     sheet.write('BB%s' % row, bb % ((row,) * 46), content_style_bold)
    #
    #     bc = '=COUNTIF($E%s:$AI%s,\"X0.5\")*0.5+COUNTIF($E%s:$AI%s,\"X1\")+COUNTIF($E%s:$AI%s,\"X1.5\")*1.5+COUNTIF($E%s:$AI%s,\"X2\")*2+COUNTIF($E%s:$AI%s,\"X2.5\")*2.5+COUNTIF($E%s:$AI%s,\"X3\")*3+COUNTIF($E%s:$AI%s,\"X3.5\")*3.5+COUNTIF($E%s:$AI%s,\"X4\")*4+COUNTIF($E%s:$AI%s,\"X4.5\")*4.5+COUNTIF($E%s:$AI%s,\"X5\")*5+COUNTIF($E%s:$AI%s,\"X5.5\")*5.5+COUNTIF($E%s:$AI%s,\"X6\")*6+COUNTIF($E%s:$AI%s,\"X6.5\")*6.5+COUNTIF($E%s:$AI%s,\"X7\")*7+COUNTIF($E%s:$AI%s,\"X7.5\")*7.5+COUNTIF($E%s:$AI%s,\"X8\")*8+ COUNTIF($E%s:$AI%s,\"CT1\")*1+COUNTIF($E%s:$AI%s,\"CT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"CT2\")*2+COUNTIF($E%s:$AI%s,\"CT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"CT3\")*3+COUNTIF($E%s:$AI%s,\"CT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"CT4\")*4+COUNTIF($E%s:$AI%s,\"CT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"CT5\")*5+COUNTIF($E%s:$AI%s,\"CT6\")*6+COUNTIF($E%s:$AI%s,\"CT7\")*7+COUNTIF($E%s:$AI%s,\"CT8\")*8+COUNTIF($E%s:$AI%s,\"CT10.5\")*10.5'
    #     sheet.write('BC%s' % row, bc % ((row,) * 58), content_style_bold)
    #
    #     bd = '=COUNTIF($E%s:$AI%s,\"OT1\")+COUNTIF($E%s:$AI%s,\"OT1.5\")*1.5+COUNTIF($E%s:$AI%s,\"OT2\")*2+COUNTIF($E%s:$AI%s,\"OT2.5\")*2.5+COUNTIF($E%s:$AI%s,\"OT3\")*3+COUNTIF($E%s:$AI%s,\"OT3.5\")*3.5+COUNTIF($E%s:$AI%s,\"OT4\")*4+COUNTIF($E%s:$AI%s,\"OT4.5\")*4.5+COUNTIF($E%s:$AI%s,\"OT5\")*5+COUNTIF($E%s:$AI%s,\"OT5.5\")*5.5+COUNTIF($E%s:$AI%s,\"OT6\")*6+COUNTIF($E%s:$AI%s,\"OT6.5\")*6.5+COUNTIF($E%s:$AI%s,\"OT7\")*7+COUNTIF($E%s:$AI%s,\"OT7.5\")*7.5+COUNTIF($E%s:$AI%s,\"OT8\")*8+COUNTIF($E%s:$AI%s,\"TB1\")+COUNTIF($E%s:$AI%s,\"TB1.5\")*1.5+COUNTIF($E%s:$AI%s,\"TB2\")*2+COUNTIF($E%s:$AI%s,\"TB2.5\")*2.5+COUNTIF($E%s:$AI%s,\"TB3\")*3+COUNTIF($E%s:$AI%s,\"TB3.5\")*3.5+COUNTIF($E%s:$AI%s,\"TB4\")*4+COUNTIF($E%s:$AI%s,\"TB4.5\")*4.5+COUNTIF($E%s:$AI%s,\"TB5\")*5+COUNTIF($E%s:$AI%s,\"TB5.5\")*5.5+COUNTIF($E%s:$AI%s,\"TB6\")*6+COUNTIF($E%s:$AI%s,\"TB6.5\")*6.5+COUNTIF($E%s:$AI%s,\"TB7\")*7+COUNTIF($E%s:$AI%s,\"TB7.5\")*7.5+COUNTIF($E%s:$AI%s,\"TB8\")*8+COUNTIF($E%s:$AI%s,\"CN1\")+COUNTIF($E%s:$AI%s,\"CN1.5\")*1.5+COUNTIF($E%s:$AI%s,\"CN2\")*2+COUNTIF($E%s:$AI%s,\"CN2.5\")*2.5+COUNTIF($E%s:$AI%s,\"CN3\")*3+COUNTIF($E%s:$AI%s,\"CN3.5\")*3.5+COUNTIF($E%s:$AI%s,\"CN4\")*4+COUNTIF($E%s:$AI%s,\"CN4.5\")*4.5+COUNTIF($E%s:$AI%s,\"CN5\")*5+COUNTIF($E%s:$AI%s,\"CN5.5\")*5.5+COUNTIF($E%s:$AI%s,\"CN6\")*6+COUNTIF($E%s:$AI%s,\"CN6.5\")*6.5+COUNTIF($E%s:$AI%s,\"CN7\")*7+COUNTIF($E%s:$AI%s,\"CN7.5\")*7.5+COUNTIF($E%s:$AI%s,\"CN8\")*8+COUNTIF($E%s:$AI%s,\"BL1\")+COUNTIF($E%s:$AI%s,\"BL1.5\")*1.5+COUNTIF($E%s:$AI%s,\"BL2\")*2+COUNTIF($E%s:$AI%s,\"BL2.5\")*2.5+COUNTIF($E%s:$AI%s,\"BL3\")*3+COUNTIF($E%s:$AI%s,\"BL3.5\")*3.5+COUNTIF($E%s:$AI%s,\"BL4\")*4+COUNTIF($E%s:$AI%s,\"BL4.5\")*4.5+COUNTIF($E%s:$AI%s,\"BL5\")*5+COUNTIF($E%s:$AI%s,\"BL5.5\")*5.5+COUNTIF($E%s:$AI%s,\"BL6\")*6+COUNTIF($E%s:$AI%s,\"BL6.5\")*6.5+COUNTIF($E%s:$AI%s,\"BL7\")*7+COUNTIF($E%s:$AI%s,\"BL7.5\")*7.5+COUNTIF($E%s:$AI%s,\"BL8\")*8'
    #     sheet.write('BD%s' % row, bd % ((row,) * 120), content_style_bold)
    #
    #     be = '=COUNTIF($E%s:$AI%s,\"L1\")+COUNTIF($E%s:$AI%s,\"L1.5\")*1.5+COUNTIF($E%s:$AI%s,\"L2\")*2+COUNTIF($E%s:$AI%s,\"L2.5\")*2.5+COUNTIF($E%s:$AI%s,\"L3\")*3+COUNTIF($E%s:$AI%s,\"L3.5\")*3.5+COUNTIF($E%s:$AI%s,\"L4\")*4+COUNTIF($E%s:$AI%s,\"L4.5\")*4.5+COUNTIF($E%s:$AI%s,\"L5\")*5+COUNTIF($E%s:$AI%s,\"L5.5\")*5.5+COUNTIF($E%s:$AI%s,\"L6\")*6+COUNTIF($E%s:$AI%s,\"L6.5\")*6.5+COUNTIF($E%s:$AI%s,\"L7\")*7+COUNTIF($E%s:$AI%s,\"L7.5\")*7.5+COUNTIF($E%s:$AI%s,\"L8\")*8+COUNTIF($E%s:$AI%s,\"SL1\")*1+COUNTIF($E%s:$AI%s,\"SL2\")*2+COUNTIF($E%s:$AI%s,\"SL3\")*3+COUNTIF($E%s:$AI%s,\"SL4\")*4+COUNTIF($E%s:$AI%s,\"SL5\")*5+COUNTIF($E%s:$AI%s,\"SL6\")*6+COUNTIF($E%s:$AI%s,\"SL7\")*7+COUNTIF($E%s:$AI%s,\"SL8\")*8'
    #     sheet.write('BE%s' % row, be % ((row,) * 46), content_style_bold)
    #
    #     sheet.write('BF%s' % row, '=SUM(AJ%s:AY%s)' % ((row,) * 2), content_style_bold)
    #     sheet.write('BG%s' % row, '=BF%s=$C$8' % row, content_style_bold)

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet_list = [
            {'id': 0, 'name': 'TỔNG HỢP'}]
        attendance_id = objects
        domain = [('check_late_soon', '=', True),
                  ('month', '=', attendance_id.month),
                  ('year', '=', attendance_id.year)]
        if attendance_id.department_id:
            domain.append(('department_id', '=', attendance_id.department_id.id))

        if self.env.user.has_group('seatek_hr_attendance.hr_attendance_administrator') or self.env.user.has_group(
                'seatek_hr_attendance.hr_attendance_manager'):
            department_list = self.env['hr.department'].sudo().search(
                [('company_id', '=', self.env.user.company_id.id),
                 ('id', '=', attendance_id.department_id.id)]) if attendance_id.department_id else self.env[
                'hr.department'].sudo().search(
                [('company_id', '=', self.env.user.company_id.id)])
            if department_list:
                for depart in department_list:
                    employee_department = self.env['hr.employee.multi.company'].sudo().search(
                        [('department_id', '=', depart.id)])
                    if employee_department:
                        if self.env['sea.hr.attendance.details'].sudo().search(domain + [('employee_multi_id', 'in',
                                                                                          employee_department.ids)]):
                            red = {'check_in': 0, 'check_in_noon': 0, 'check_out_noon': 0, 'check_out': 0,
                                   'check_in_late': 0,
                                   'check_in_noon_late': 0, 'check_out_noon_soon': 0, 'check_out_soon': 0,
                                   'day_details': []}
                            for attendance_of_month in attendance_id.attendance_of_month_compute.filtered(
                                    lambda record: record.employee_multi_id.id in employee_department.ids):
                                count = attendance_of_month.count_soon_late()
                                red['check_in_late'] += count.get('check_in_late')
                                red['check_in_noon_late'] += count.get('check_in_noon_late')
                                red['check_out_noon_soon'] += count.get('check_out_noon_soon')
                                red['check_out_soon'] += count.get('check_out_soon')

                                red['check_in'] += count.get('check_in')
                                red['check_in_noon'] += count.get('check_in_noon')
                                red['check_out_noon'] += count.get('check_out_noon')
                                red['check_out'] += count.get('check_out')
                                if len(count.get('day_details')) > 0:
                                    red['day_details'] += count.get('day_details')
                            sheet_list.append(
                                {'id': depart.id, 'name': depart.name,

                                 'check_in': red['check_in'],
                                 'check_in_late': red['check_in_late'],

                                 'check_out': red['check_out'],
                                 'check_out_soon': red['check_out_soon'],

                                 'check_in_noon': red['check_in_noon'],
                                 'check_in_noon_late': red['check_in_noon_late'],

                                 'check_out_noon_soon': red['check_out_noon_soon'],
                                 'check_out_noon': red['check_out_noon'],
                                 'day_details': red.get('day_details'),
                                 })

        else:
            employee_multi_id = self.env['hr.employee.multi.company'].sudo().search(
                [('user_id', '=', self.env.user.id), ('company_id', '=', self.env.user.company_id.id)], limit=1)
            if employee_multi_id:
                department_ids = []
                employee = self.env['hr.employee'].sudo().search([('id', '=', employee_multi_id.name.id)])
                if self.env['sea.hr.attendance.details'].sudo().search(domain + [('employee_multi_id', '=',
                                                                                  employee_multi_id.id)]):
                    department_ids.append(employee_multi_id.department_id.id)
                if employee:
                    department_list = self.env['hr.department'].sudo().search(
                        [('manager_ids', '=', employee.id)])
                    if department_list:
                        for depart in department_list:
                            employee_department = self.env['hr.employee.multi.company'].sudo().search(
                                [('department_id', '=', depart.id)])
                            if employee_department:
                                if self.env['sea.hr.attendance.details'].sudo().search(
                                        domain + [('employee_multi_id', 'in',
                                                   employee_department.ids)]):
                                    department_ids.append(depart.id)
                for de in self.env['hr.department'].sudo().search(
                        [('id', 'in', department_ids)]):
                    sheet = {'check_in': 0, 'check_in_noon': 0, 'check_out_noon': 0,
                             'check_out': 0, 'check_in_late': 0,
                             'check_in_noon_late': 0, 'check_out_noon_soon': 0, 'check_out_soon': 0, 'day_details': []}
                    for attendance_of_month in attendance_id.attendance_of_month_compute.filtered(
                            lambda record: record.department_id.id == de.id):
                        count = attendance_of_month.count_soon_late()
                        sheet['check_in_late'] += count.get('check_in_late')
                        sheet['check_in_noon_late'] += count.get('check_in_noon_late')
                        sheet['check_out_noon_soon'] += count.get('check_out_noon_soon')
                        sheet['check_out_soon'] += count.get('check_out_soon')

                        sheet['check_in'] += count.get('check_in')
                        sheet['check_in_noon'] += count.get('check_in_noon')
                        sheet['check_out_noon'] += count.get('check_out_noon')
                        sheet['check_out'] += count.get('check_out')
                        if len(count.get('day_details')) > 0:
                            sheet['day_details'] += count.get('day_details')
                    sheet_list.append({'id': de.id, 'name': de.name, 'check_in': sheet.get('check_in'),
                                       'check_in_noon': sheet.get('check_in_noon'),
                                       'check_out_noon': sheet.get('check_out_noon'),
                                       'check_out': sheet.get('check_out'),
                                       'check_in_late': sheet.get('check_in_late'),
                                       'check_in_noon_late': sheet.get('check_in_noon_late'),
                                       'check_out_noon_soon': sheet.get('check_out_noon_soon'),
                                       'check_out_soon': sheet.get('check_out_soon'),
                                       'day_details': sheet.get('day_details'),
                                       })
        for i in sheet_list:
            name = str(i.get('name'))
            sheet = workbook.add_worksheet(_(name))
            sheet.set_landscape()
            sheet.fit_to_pages(1, 0)
            sheet.set_zoom(100)
            if attendance_id.sudo().company_id:
                image_company = io.BytesIO(base64.b64decode(attendance_id.sudo().company_id.logo_web))
                sheet.insert_image('B1', "logocompany.png",
                                   {'image_data': image_company, 'x_scale': 0.5, 'y_scale': 0.5})
                title_style_address_company = workbook.add_format({'font_size': 16, 'font_name': "Times New Roman"})
                title_style_name_company = workbook.add_format({'bold': True,
                                                                'font_size': 20,
                                                                'font_name': "Times New Roman",
                                                                'align': 'left',
                                                                'valign': 'vcenter'})
                sheet.write('D1', attendance_id.sudo().company_id.sudo().name, title_style_name_company)
                sheet.write('D2', attendance_id.sudo().company_id.sea_company_foreign, title_style_name_company)
                title_style = workbook.add_format({'bold': True,
                                                   'font_size': 20,
                                                   'font_name': "Times New Roman",
                                                   'align': 'center',
                                                   'valign': 'vcenter'})
                title_style_red = workbook.add_format({'bold': True,
                                                       'font_size': 20,
                                                       'font_name': "Times New Roman",
                                                       'font_color': '#C00000',
                                                       'align': 'center',
                                                       'valign': 'vcenter'})
                address = ''
                if attendance_id.sudo().company_id.street:
                    address += attendance_id.sudo().company_id.street
                if attendance_id.sudo().company_id.street2:
                    address += attendance_id.sudo().company_id.street2
                if attendance_id.sudo().company_id.city:
                    address += attendance_id.sudo().company_id.city
                if attendance_id.sudo().company_id.state_id:
                    address += attendance_id.sudo().company_id.state_id.name
                if attendance_id.sudo().company_id.country_id:
                    address += ', ' + attendance_id.sudo().company_id.country_id.name
                sheet.write('D3', address, title_style_address_company)

                department_style = workbook.add_format({'bold': True,
                                                        'font_size': 11,
                                                        'font_name': "Times New Roman",
                                                        'font_color': '#000000',
                                                        'bg_color': '#9BC2E6',
                                                        # 'bg_color': '#C6E0B4',
                                                        'align': 'center',
                                                        'border': 1,
                                                        'text_wrap': True,
                                                        'valign': 'vcenter'})
                total_style = workbook.add_format({'bold': True,
                                                   'font_size': 11,
                                                   'font_name': "Times New Roman",
                                                   'font_color': '#000000',
                                                   'bg_color': '#FFD966',
                                                   'align': 'center',
                                                   'border': 1,
                                                   'text_wrap': True,
                                                   'valign': 'vcenter'})
                text_style = workbook.add_format({'bold': False,
                                                  'font_size': 11,
                                                  'font_name': "Times New Roman",
                                                  'font_color': '#000000',
                                                  'align': 'center',
                                                  'border': 1,
                                                  'text_wrap': True,
                                                  'valign': 'vcenter'})
                row = 8
                if i.get('id') == 0:
                    sheet.merge_range('A5:K5', 'BẢNG TỔNG HỢP SỐ LƯỢNG CÁC VI PHẠM LIÊN QUAN ĐẾN CHẤM CÔNG',
                                      title_style)
                    sheet.merge_range('A6:K6', " Tháng " + str(attendance_id.month) + "/" + str(attendance_id.year),
                                      title_style_red)
                    sheet.set_column('B:B', 70)
                    sheet.set_column('C:C', 15)
                    sheet.set_column('D:D', 15)
                    sheet.set_column('E:E', 17)
                    sheet.set_column('F:F', 15)
                    sheet.set_column('G:G', 27)
                    sheet.set_column('H:H', 24)
                    sheet.set_column('I:I', 27)
                    sheet.set_column('J:J', 25)
                    sheet.write('A%s' % row, 'STT', department_style)
                    sheet.write('B%s' % row, 'Phòng/Ban', department_style)
                    sheet.write('C%s' % row, 'Không check in', department_style)
                    sheet.write('D%s' % row, 'Check in trễ', department_style)
                    sheet.write('E%s' % row, 'Không check out', department_style)
                    sheet.write('F%s' % row, 'Check out sớm', department_style)
                    sheet.write('G%s' % row, 'Không Check in ca tiếp theo', department_style)
                    sheet.write('H%s' % row, 'Check in ca tiếp theo trễ', department_style)
                    sheet.write('I%s' % row, 'Không check out ca đầu tiên', department_style)
                    sheet.write('J%s' % row, 'Check out ca đầu tiên sớm', department_style)
                    sheet.write('K%s' % row, 'Tổng', department_style)
                    row += 1
                    start = row
                    end = row + len(sheet_list) - 2
                    stt = 1
                    dep_list = [condition for condition in sheet_list if
                                condition != {'id': 0, 'name': 'TỔNG HỢP'}]

                    for depart in dep_list:
                        sheet.write('A%s' % row, stt, text_style)
                        sheet.write('B%s' % row, depart.get('name'), text_style)
                        sheet.write('C%s' % row, depart.get('check_in'), text_style)
                        sheet.write('D%s' % row, depart.get('check_in_late'), text_style)
                        sheet.write('E%s' % row, depart.get('check_out'), text_style)
                        sheet.write('F%s' % row, depart.get('check_out_soon'), text_style)
                        sheet.write('G%s' % row, depart.get('check_in_noon'), text_style)
                        sheet.write('H%s' % row, depart.get('check_in_noon_late'), text_style)
                        sheet.write('I%s' % row, depart.get('check_out_noon'), text_style)
                        sheet.write('J%s' % row, depart.get('check_out_noon_soon'), text_style)
                        sheet.write('K%s' % row, '=SUM(C%s:J%s)' % ((row,) * 2), total_style)
                        row += 1
                        stt += 1
                    sheet.write('A%s' % row, '', total_style)
                    sheet.write('B%s' % row, 'TỔNG CỘNG', total_style)
                    sheet.write('C%s' % row, '=SUM(C%s:C%s)' % (start, end), total_style)
                    sheet.write('D%s' % row, '=SUM(D%s:D%s)' % (start, end), total_style)
                    sheet.write('E%s' % row, '=SUM(E%s:E%s)' % (start, end), total_style)
                    sheet.write('F%s' % row, '=SUM(F%s:F%s)' % (start, end), total_style)
                    sheet.write('G%s' % row, '=SUM(G%s:G%s)' % (start, end), total_style)
                    sheet.write('H%s' % row, '=SUM(H%s:H%s)' % (start, end), total_style)
                    sheet.write('I%s' % row, '=SUM(I%s:I%s)' % (start, end), total_style)
                    sheet.write('J%s' % row, '=SUM(J%s:J%s)' % (start, end), total_style)
                    sheet.write('K%s' % row, '=SUM(K%s:K%s)' % (start, end), total_style)

                else:
                    sheet.set_column('B:B', 20)
                    sheet.set_column('C:C', 28)
                    sheet.set_column('D:D', 28)
                    sheet.set_column('E:E', 12)
                    sheet.set_column('F:F', 20)
                    sheet.set_column('G:G', 25)
                    sheet.set_column('H:H', 30)
                    sheet.set_column('I:I', 15)
                    sheet.set_column('J:J', 20)
                    sheet.set_column('K:K', 20)
                    sheet.set_column('L:L', 20)
                    sheet.set_column('M:M', 20)
                    sheet.set_column('N:N', 15)
                    sheet.set_column('O:O', 15)
                    sheet.set_column('P:P', 15)
                    sheet.set_column('Q:Q', 15)
                    sheet.merge_range('A5:Q5', 'DANH SÁCH CÁC VI PHẠM LIÊN QUAN ĐẾN CHẤM CÔNG',
                                      title_style)
                    sheet.merge_range('A6:Q6', i.get('name'),
                                      title_style)
                    sheet.merge_range('A7:Q7', " Tháng " + str(attendance_id.month) + "/" + str(attendance_id.year),
                                      title_style_red)
                    row += 1
                    sheet.write('A%s' % row, 'STT', department_style)
                    sheet.write('B%s' % row, 'Mã SC', department_style)
                    sheet.write('C%s' % row, 'HỌ VÀ TÊN', department_style)
                    sheet.write('D%s' % row, 'CHỨC DANH', department_style)
                    sheet.write('E%s' % row, 'Ngày', department_style)
                    sheet.write('F%s' % row, 'Ca làm việc', department_style)
                    sheet.write('G%s' % row, 'Miêu tả lỗi', department_style)
                    sheet.write('H%s' % row, 'Ghi chú', department_style)
                    sheet.write('I%s' % row, 'Trạng thái', department_style)
                    sheet.write('J%s' % row, 'Thời gian check in', department_style)
                    sheet.write('K%s' % row, 'Thời gian check out nghỉ giữa ca', department_style)
                    sheet.write('L%s' % row, 'Thời gian check in kết thúc nghỉ giữa ca', department_style)
                    sheet.write('M%s' % row, 'Thời gian check out', department_style)
                    sheet.write('N%s' % row, 'Check in trễ', department_style)
                    sheet.write('O%s' % row, 'Check out ca đầu tiên sớm', department_style)
                    sheet.write('P%s' % row, 'Check in ca tiếp theo trễ', department_style)
                    sheet.write('Q%s' % row, 'Check out sớm', department_style)
                    row += 1
                    stt = 1
                    details = i.get('day_details')
                    for detail in details:
                        sheet.write('A%s' % row, stt, text_style)
                        sheet.write('B%s' % row, detail.employee_multi_id.sudo().s_identification_id,
                                    text_style)
                        sheet.write('C%s' % row, detail.employee_multi_id.sudo().name.name, text_style)
                        sheet.write('D%s' % row,
                                    detail.employee_multi_id.sudo().job_id.name if detail.employee_multi_id.sudo().job_id.name else "",
                                    text_style)
                        sheet.write('E%s' % row, str(detail.day) + '/' + str(detail.month) + '/' + str(detail.year),
                                    text_style)
                        sheet.write('F%s' % row, detail.shift.name, text_style)
                        sheet.write('G%s' % row, attendance_id.attendance_of_month_compute.get_soon_late(
                            detail.attendance_realtime_id),
                                    text_style)
                        sheet.write('H%s' % row,
                                    str(detail.note if detail.note else ''),
                                    text_style)
                        sheet.write('I%s' % row, str('Chấp nhận' if detail.explanation_approved else 'Không chấp nhận'),
                                    text_style)
                        sheet.write('J%s' % row,
                                    str(detail.check_in + datetime.timedelta(hours=7) if detail.check_in else ''),
                                    text_style)
                        sheet.write('K%s' % row, str(detail.check_in_noon + datetime.timedelta(
                            hours=7) if detail.check_in_noon else ''), text_style)
                        sheet.write('L%s' % row, str(detail.check_out_noon + datetime.timedelta(
                            hours=7) if detail.check_out_noon else ''),
                                    text_style)
                        sheet.write('M%s' % row,
                                    str(detail.check_out + datetime.timedelta(hours=7) if detail.check_out else ''),
                                    text_style)

                        sheet.write('N%s' % row, str(detail.check_in_late if detail.check_in_late else ''), text_style)
                        sheet.write('O%s' % row, str(detail.check_in_noon_late if detail.check_in_noon_late else ''),
                                    text_style)
                        sheet.write('P%s' % row, str(detail.check_out_noon_soon if detail.check_out_noon_soon else ''),
                                    text_style)
                        sheet.write('Q%s' % row, str(detail.check_out_soon if detail.check_out_soon else ''),
                                    text_style)
                        row += 1
                        stt += 1
