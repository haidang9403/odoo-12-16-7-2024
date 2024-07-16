import base64
import io
import logging
from datetime import date, timedelta
from odoo import models
from odoo.tools.translate import _

class ReportHrDirectory(models.AbstractModel):
    _name = 'report.hr_directory_reports.report_directory_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        tong_hop_title = workbook.add_format({'bold': True,
                                              'font_size': 14,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center',
                                              'text_wrap': True})
        tong_hop_date = workbook.add_format({'bold': True, 'border': 1,
                                             'font_size': 14,
                                             'font_name': "Times New Roman",
                                             'valign': 'vcenter',
                                             'align': 'center', 'bg_color': '#B6DDE8'})
        data_style_child = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman"})
        data_style_parent = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'border': 1,
             # 'text_wrap': True,
             'font_name': "Times New Roman", 'bold': True, 'bg_color': '#DAEEF3'})
        data_style_child_center = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman", 'align': 'center'})
        data_style_parent_center = workbook.add_format(
            {'font_size': 14, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman", 'bold': True, 'bg_color': '#DAEEF3', 'align': 'center'})
        street = ''
        vat = ''
        email_group = ''
        phone = ''
        fax = ''
        sheetTH = workbook.add_worksheet(_("TH Danh Bạ"))
        sheetTH.set_landscape()
        sheetTH.set_zoom(80)
        sheetTH.set_column('A:A', 10)
        sheetTH.set_column('B:B', 90)


        sheetTH.merge_range("A1:B1", "DANH BẠ TOÀN HỆ THỐNG", workbook.add_format({'font_size': 20, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
             'font_name': "Times New Roman", 'bold': True, 'bg_color': '#DAEEF3', 'align': 'center'}))

        sheetTH.merge_range("A3:A4", "STT", tong_hop_date)
        sheetTH.merge_range("B3:B4", "ĐƠN VỊ", tong_hop_date)
        index_TH = 4
        stt_TH = 1
        for id in data['company_ids']:
            company = self.env['res.company'].sudo().search([('id', '=', id)])
            sheetTH.write(index_TH, 0, stt_TH, data_style_child_center)
            sheetTH.write(index_TH, 1, company.name, data_style_child)
            index_TH += 1
            stt_TH += 1

        stt_company = 1
        for id in data['company_ids']:
            company_id = self.env['res.company'].sudo().search([('id', '=', id)])
            sheet = workbook.add_worksheet(_(''.join([str(stt_company), '.', company_id.short_name])))
            stt_company += 1
            sheet.set_landscape()
            sheet.fit_to_pages(1, 0)
            sheet.set_zoom(80)

            if company_id.street:
                street = company_id.street
            if company_id.vat:
                vat = company_id.vat
            if company_id.email_group:
                email_group = company_id.email_group
            if company_id.email_group:
                phone = company_id.email_group
            if company_id.fax:
                fax = company_id.fax
            title = company_id.name + '\n' + street + '\nMTS: ' + vat + \
                    '\n Email Group: ' + email_group + '\n Điện Thoại: ' + phone + ' - Fax: ' + fax

            sheet.merge_range('A1:H1', title, tong_hop_title)
            sheet.merge_range('A2:H2', 'DANH BẠ ĐIỆN THOẠI', workbook.add_format({'bold': True,
                                                                                  'font_size': 20,
                                                                                  'font_name': "Times New Roman",
                                                                                  'valign': 'vcenter',
                                                                                  'align': 'center',
                                                                                  'text_wrap': True,
                                                                                  'color': '#FF0000'}))

            sheet.freeze_panes(4, 2)
            sheet.set_row(0, 120)
            sheet.set_row(1, 50)
            row = 2
            # while row < 999:
            #     sheet.set_row(row, 35)
            #     row += 1

            sheet.set_column('A:A', 20)
            sheet.set_column('B:B', 70)
            sheet.set_column('C:C', 30)
            sheet.set_column('D:D', 14)
            sheet.set_column('E:E', 24)
            sheet.set_column('F:F', 20)
            sheet.set_column('G:G', 40)
            sheet.set_column('H:H', 45)

            sheet.write('A4', 'STT', tong_hop_date)
            sheet.write('B4', 'HỌ VÀ TÊN', tong_hop_date)
            sheet.write('C4', 'CHỨC VỤ', tong_hop_date)
            sheet.write('D4', 'SỐ NỘI BỘ', tong_hop_date)
            sheet.write('E4', 'SỐ ĐIỆN THOẠI', tong_hop_date)
            sheet.write('F4', 'Fax', tong_hop_date)
            sheet.write('G4', 'EMAIL', tong_hop_date)
            sheet.write('H4', 'GHI CHÚ', tong_hop_date)

            date_update = None
            for directory in self.env['hr.directory'].sudo().search([('company_id', '=', company_id.id)]):
                if date_update == None:
                    date_update = directory.write_date
                else:
                    if directory.write_date > date_update:
                        date_update = directory.write_date
            if date_update != None:
                sheet.merge_range('G3:H3', date_update, workbook.add_format({'bold': True, 'border': 1,
                                                                         'font_size': 13,
                                                                         'font_name': "Times New Roman",
                                                                         'valign': 'vcenter',
                                                                         'align': 'left', 'num_format': '"Ngày cập nhật:" dd-mm-yyyy'}))

            index = 4
            stt = 1

            # [index, parent, directory, has_child]
            list_directory = []
            list_root = []
            list_parent = []
            list_child = []
            index_root = 0
            for root in self.env['hr.directory'].sudo().search(
                    ['&', ('company_id', '=', company_id.id), ('parent_directory', '=', None)]):
                index_root += 1
                list_root.append(root)
                list_parent.append(root)
                if index_root< 10:
                    list_directory.append([''.join(['0', str(index_root)]), None, root, True])
                else:
                    list_directory.append([str(index_root), None, root, True])



            for directory in self.env['hr.directory'].sudo().search(['&',('company_id', '=', company_id.id), ('parent_directory', '!=', None)]):
                list_d = self.env['hr.directory'].sudo().search(
                    ['&', ('company_id', '=', company_id.id), ('parent_directory', '=', directory.id)])

                if len(list_d) > 0:
                    list_parent.append(directory)
            # stt_parent = 1

            for parent in list_parent:
                stt_parent =1
                parent_dir = None
                index_dir = str(index_root)
                for dir_root in list_directory:
                        if parent == dir_root[2]:
                            # index_dir = dir_root[0] + ".0"
                            parent_dir = dir_root

                list_dir = self.env['hr.directory'].sudo().search(['&', ('company_id', '=', company_id.id), ('parent_directory', '=', parent.id)])
                for directory in list_dir:
                    if directory in list_parent:
                        if parent_dir != None:
                            ind = ''.join([parent_dir[0], '.', str(stt_parent)])
                            list_directory.append([ind, parent_dir[2], directory, True])
                            stt_parent += 1
                        else:
                            list_child.append(directory)

                    # else:
                    #     ind = ''.join([index_dir, '.0', str(stt)])
                    #     list_directory.append([ind, parent, directory, False])
                    #     stt += 1
            for child in list_child:
                parent_dir = None
                count = 1
                for dir in list_directory:
                    if dir[2] == child['parent_directory']:
                        parent_dir = dir
                    if child['parent_directory'] == dir[1]:
                        count += 1
                if parent_dir !=None:
                    ind = ''.join([parent_dir[0], '.', str(count)])
                    list_directory.append([ind, parent_dir[2], child, True])
                    stt_parent += 1


            for parent in list_parent:
                stt_parent = 1
                index_dir = str(index_root)
                # if parent in list_root:
                #     list_directory.append([str(index_root), None, parent, True])
                #     index_root += 1
                # else:
                for dir_root in list_directory:
                    if parent == dir_root[2]:
                        index_dir = dir_root[0] + ""

                list_dir = self.env['hr.directory'].sudo().search(
                    ['&', ('company_id', '=', company_id.id), ('parent_directory', '=', parent.id)])
                stt =1
                for directory in list_dir:
                    if directory not in list_parent:
                    #     ind = ''.join([index_dir, '.', str(stt_parent)])
                    #     list_directory.append([ind, parent, directory, True])
                    #     stt_parent += 1
                    # else:
                        ind = ''.join([index_dir, '.0.0', str(stt)])
                        list_directory.append([ind, parent, directory, False])
                        stt += 1

            list_directory.sort()
            if len(list_directory) != len(list_root):
                 for directory in list_directory:
                    # if directory[2] in list_parent:
                        if '.' in directory[0]:
                            i_num = directory[0].index('.')
                            num = int(directory[0][0:i_num])
                            directory[0] = ''.join([self.toRoman(num), directory[0][i_num: len(directory[0])]])
                        else:
                            num = int(directory[0])
                            directory[0] = self.toRoman(num)
            else:
                list_parent.clear()

            i = 1
            stt_obj = 0
            stt_parent = 1
            stt_p = 0
            for obj in list_directory:
                if obj[2] in list_parent:
                    data_style = data_style_parent
                    data_style_center = data_style_parent_center
                    stt_obj = obj[0]
                    if obj[1] == None:
                        stt_p = 1
                        stt_obj = self.toRoman(stt_parent)
                        stt_parent += 1
                        obj[0] = stt_obj
                    # else:
                    #     for d in list_directory:
                    #         if d[2] == obj[1]:
                    #             stt_obj = ''.join([d[0], '.', str(stt_p)])
                    #             stt_p += 1
                    #             obj[0] = stt_obj
                    #             break
                    stt_obj = stt_obj.replace('.0', '')
                else:
                    data_style = data_style_child
                    data_style_center = data_style_child_center
                    stt_obj = i
                    i += 1

                sheet.write(index, 0, stt_obj, data_style_center)
                sheet.write(index, 1, obj[2].name, data_style)
                if obj[2].position:
                    sheet.write(index, 2, obj[2].position, data_style)
                else:
                    sheet.write(index, 2, '', data_style)
                if obj[2].internal_num:
                    sheet.write(index, 3, obj[2].internal_num, data_style_center)
                else:
                    sheet.write(index, 3, '', data_style_center)
                if obj[2].phone:
                    sheet.write(index, 4, obj[2].phone, data_style)
                else:
                    sheet.write(index, 4, '', data_style)
                if obj[2].fax:
                    sheet.write(index, 5, obj[2].fax, data_style)
                else:
                    sheet.write(index, 5, '', data_style)
                if obj[2].email:
                    sheet.write(index, 6, obj[2].email, data_style)
                else:
                    sheet.write(index, 6, '', data_style)
                if obj[2].note:
                    sheet.write(index, 7, obj[2].note, data_style)
                else:
                    sheet.write(index, 7, '', data_style)
                index += 1

            index += 2
            data_style_user_guide = workbook.add_format(
                {'font_size': 13, 'valign': 'vcenter', 'border': 1, 'text_wrap': True,
                 'font_name': "Times New Roman", 'color': 'FF0000', 'bold': True})
            sheet.merge_range('A' + str(index) + ':H' + str(index), 'Hướng dẫn:', data_style_user_guide)
            index += 1
            sheet.merge_range('B' + str(index) + ':H' + str(index), 'Chuyển máy nhấn Flash/Transfer + số nội bộ', data_style_user_guide)
            index += 1
            sheet.merge_range('B' + str(index) + ':H' + str(index), 'Rước cuộc gọi nhấn *4001', data_style_user_guide)
            index += 1
            sheet.merge_range('B' + str(index) + ':H' + str(index), 'Bấm 9 gọi ra ngoài', data_style_user_guide)

    def toRoman(self, num):
        """Chuyển đổi số sang số La Mã."""
        roman_numerals = {
            1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
            50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
        }
        result = ''
        for value, numeral in sorted(roman_numerals.items(), reverse=True):
            while num >= value:
                result += numeral
                num -= value
        return result
