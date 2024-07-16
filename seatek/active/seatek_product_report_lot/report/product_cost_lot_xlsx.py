
# Author: Damien Crier
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models,fields
import datetime
import io
import base64
class ProductCostLotXslx(models.AbstractModel):
    _name = 'report.a_f_r.report_product_cost_lot_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('Product Cost lot'))

        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(85)
        self.set_columns_width(sheet)
        image_company = io.BytesIO(base64.b64decode(self.env.user.company_id.logo_web))
        sheet.insert_image('C1', "logocompany.png", {'image_data': image_company, 'x_scale': 1, 'y_scale': 1})
        style_name_company = workbook.add_format({'bold': True,
                                                        'font_size': 16,
                                                        'font_name': "Times New Roman",
                                                        'valign': 'vcenter'})
        sheet.write('D1', self.env.user.company_id.name, style_name_company)
        sheet.write('D2', self.env.user.company_id.sea_company_foreign, style_name_company)
        address=''
        if self.env.user.company_id.street:
            address += self.env.user.company_id.street
        if self.env.user.company_id.street2:
            address += self.env.user.company_id.street2
        if self.env.user.company_id.city:
            address += self.env.user.company_id.city
        if self.env.user.company_id.state_id:
            address += self.env.user.company_id.state_id.name
        if self.env.user.company_id.country_id:
            address += ', ' + self.env.user.company_id.country_id.name
        style_company_address = workbook.add_format({'bold': False,
                                                  'font_size': 16,
                                                  'font_name': "Times New Roman",
                                                  'valign': 'vcenter'})
        sheet.write('D3', address, style_company_address)
        style_report_title = workbook.add_format({'bold': True,
                                                     'font_size': 26,
                                                     'font_name': "Times New Roman",
                                                     'valign': 'vcenter'})
        sheet.write('D8', "BÁO CÁO GIÁ SẢN PHẨM THEO LÔ", style_report_title)
        row=9
        column=0
        self.generate_product_lots(workbook,sheet,row,column,objects)
    def set_columns_width(self,sheet):
        #D
        pos=1
        sheet.set_column(pos, pos, 23)
        pos+=1
        sheet.set_column(pos, pos, 25)
        pos += 1
        sheet.set_column(pos, pos+7, 23)
    def generate_product_lots(self,workbook,sheet,row_start,column_start,objects):
        row=row_start
        column=column_start

        for detail in objects.product_cost_lot_detail:
            row=self.generate_product_lot_detail(workbook,sheet,row,column,detail)


    def generate_product_lot_detail(self,workbook, sheet, row, column,detail):
        if detail.lot_id:
            style_product_name = workbook.add_format({'bold': True,
                                                      'font_size': 16,
                                                      'font_name': "Times New Roman",
                                                      'valign': 'vcenter',
                                                      'align': 'left'})
            format_amount_bold = workbook.add_format({'bold': True})


            column+=1
            sheet.write_string(row, column, detail.product_id.name or '', style_product_name)
            row += 1
            row=self.generate_lot_detail_title(workbook,sheet,row,column)
            row=self.generate_lot_detail(workbook,sheet,row,column,detail.lot_detail)
            row+=1
        return row

    def generate_lot_detail_title(self, workbook, sheet, row, column):
        style_detail_title = workbook.add_format({'bg_color': '#76adea','border': 1,'bold': True,
                                              'font_size': 14,
                                              'font_name': "Times New Roman",
                                              'valign': 'vcenter',
                                              'align': 'center',
                                                'text_wrap': True})
        sheet.write_string(row, column, 'Tên', style_detail_title)
        column+=1
        sheet.write_string(row, column, 'SL Nhập', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'Giá vốn', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'SL xuất', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'Giá mục tiêu', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'Tổng giá bán mục tiêu', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'Tổng bán', style_detail_title)
        column += 1
        sheet.write_string(row, column, 'Chênh lệch', style_detail_title)
        row+=1
        return row
    def generate_lot_detail(self,workbook, sheet, row, column,lot_detail):
        try:


            for detail in lot_detail:
                column_temp = column
                style_lot_name = workbook.add_format({'border': 1,'bold': False,
                                                          'font_size': 14,
                                                          'font_name': "Times New Roman",
                                                          'valign': 'vcenter','align': 'left'})
                style_lot_detail = workbook.add_format({'border': 1,'bold': False,
                                                      'font_size': 14,
                                                      'font_name': "Times New Roman",
                                                      'valign': 'vcenter',
                                                        'align': 'right',
                                                        'num_format':'#,##0.00%'})
                sheet.write_string(row, column_temp, detail.lot_id.name or '',style_lot_name)
                column_temp+=1
                sheet.write_string(row, column_temp, str(detail.lot_id.product_qty), style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp,str(detail.product_cost) ,style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp, str(detail.product_output_qty) ,style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp, str(detail.product_sale_target_price) ,style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp, str(detail.product_sale_target_total) , style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp, str(detail.product_sale_total) , style_lot_detail)
                column_temp += 1
                sheet.write_string(row, column_temp, str(detail.differential_value) , style_lot_detail)
                row+=1
        except Exception as e:
            print("Error",e)
        return row
