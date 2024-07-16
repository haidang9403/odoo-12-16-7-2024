import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AssetReportXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.export_inventory_asset_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):

        self.generate_xlsx_report_tscd(workbook,data,objects,'tscd')
        self.generate_xlsx_report_ccdc(workbook,data,objects,'ccdc')
        self.generate_xlsx_report_ccdccpb(workbook,data,objects,'ccdccpb')
    def generate_xlsx_report_tscd(self,workbook, data, objects,asset_type):

        worksheet_tscd = workbook.add_worksheet('TSCD')
        # worksheet_ccdc = workbook.add_worksheet('CCDC')
        # worksheet_ccdccpb = workbook.add_worksheet('CCDCCPB')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        header_f1 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 14, 'font_name': 'Times New Roman'})
        header_f2 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f3 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f4 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f5 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 15, 'font_name': 'Times New Roman'})
        header_f6 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f7 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_table = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f1 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f2 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f3 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'num_format': '#,##0', 'font_name': 'Times New Roman'})
        body_f4 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f1 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        signature_f2 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f3 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})

        text_center = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})
        text_left = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})

        short_date = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mm/yyyy',
             'font_name': 'Tahoma', 'font_size': 10})
        money = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0',
                                     'font_size': 10, 'font_name': 'Tahoma'})
        no_data = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Tahoma'})

        row_no = 0

        # Report Header
        worksheet_tscd.set_column(0, 0, 7), worksheet_tscd.set_column(1, 1, 40), worksheet_tscd.set_column(2, 2, 15)
        worksheet_tscd.set_column(3, 3, 15), worksheet_tscd.set_column(4, 4, 6), worksheet_tscd.set_column(5, 5, 12)
        worksheet_tscd.set_column(6, 6, 14), worksheet_tscd.set_column(7, 7, 6), worksheet_tscd.set_column(8, 8, 12)
        worksheet_tscd.set_column(9, 9, 16), worksheet_tscd.set_column(10, 10, 6), worksheet_tscd.set_column(11, 11, 12)
        worksheet_tscd.set_column(12, 12, 14), worksheet_tscd.set_column(13, 13, 50), worksheet_tscd.set_column(14, 14, 50)
        worksheet_tscd.set_column(15, 15, 50)

        worksheet_tscd.merge_range(row_no, 0, row_no, 3, 'Đơn vị: ' + company_name, header_f1)
        worksheet_tscd.write(row_no, 13, 'Mẫu số 05 - TSCĐ', header_f2)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 3, 'Bộ phận: ', header_f3)
        worksheet_tscd.merge_range(row_no, 11, row_no, 13, '(Ban hành theo Thông tư số 200/2014/TT-BTC Ngày 22/12/2014 của Bộ Tài chính)', header_f4)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 13, 'BIÊN BẢN KIỂM KÊ TSCD', header_f5)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 13, 'Áp dụng cho CCDC đang được sử dụng chờ phân bổ', header_f6)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, 'Thời gian kiểm kê: … giờ, ngày    tháng    năm 20  ', header_f7)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, 'Ban kiểm kê gồm:', header_f7)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_tscd.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_tscd.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_tscd.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_tscd.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_tscd.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_tscd.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_tscd.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_tscd.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_tscd.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_tscd.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_tscd.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_tscd.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_tscd.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 2
        worksheet_tscd.merge_range(row_no, 0, row_no, 2, 'Đã kiểm kê CCDC, kết quả như sau:', header_f7)
        row_no += 2
        worksheet_tscd.merge_range(row_no, 0, row_no + 1, 0, 'STT', header_table)
        worksheet_tscd.merge_range(row_no, 1, row_no + 1, 1, 'Tên CCDC', header_table)
        worksheet_tscd.merge_range(row_no, 2, row_no + 1, 2, 'Mã số', header_table)
        worksheet_tscd.merge_range(row_no, 3, row_no + 1, 3, 'Nơi sử dụng', header_table)
        worksheet_tscd.merge_range(row_no, 4, row_no, 6, 'Theo số kế toán', header_table)
        worksheet_tscd.merge_range(row_no, 7, row_no, 9, 'Theo số kiểm kê', header_table)
        worksheet_tscd.merge_range(row_no, 10, row_no, 12, 'Chênh lệch', header_table)
        worksheet_tscd.merge_range(row_no, 13, row_no + 1, 13, 'Ghi chú', header_table)
        worksheet_tscd.merge_range(row_no, 14, row_no + 1, 14, 'Đề xuất xử lý', header_table)
        worksheet_tscd.merge_range(row_no, 15, row_no + 1, 15, 'Giải trình của đơn vị', header_table)
        row_no += 1
        worksheet_tscd.write(row_no, 4, 'Số lượng', header_table)
        worksheet_tscd.write(row_no, 5, 'Nguyên giá', header_table)
        worksheet_tscd.write(row_no, 6, 'Giá trị còn lại', header_table)
        worksheet_tscd.write(row_no, 7, 'Số lượng', header_table)
        worksheet_tscd.write(row_no, 8, 'Nguyên giá', header_table)
        worksheet_tscd.write(row_no, 9, 'Giá trị còn lại', header_table)
        worksheet_tscd.write(row_no, 10, 'Số lượng', header_table)
        worksheet_tscd.write(row_no, 11, 'Nguyên giá', header_table)
        worksheet_tscd.write(row_no, 12, 'Giá trị còn lại', header_table)
        row_no += 1
        domain = [('company_id', '=', self.env.user.company_id.id)]
        asset_types=self.env['account.asset.type'].sudo().search([('type_template','=',asset_type)])
        if asset_types:
            domain.append(('asset_type','in',asset_types.ids))
        '''Don vi su dung tai san'''
        if data.get('department_id'):
            domain.append(('management_dept', '=', data.get('department_id')))
        if data.get('location_id'):
            domain.append(('sea_office_id', '=', data.get('location_id')))

        asset_objects = self.env['account.asset.asset'].search(domain,order='management_dept')
        line_row = 0
        department_list = []
        for asset in asset_objects:
            if asset.management_dept:
                department_list.append(asset.management_dept.id)
        department_id=[]
        if len(department_list)>0:
            department_id = set(department_list)

        row_no += 1
        offices = []
        for asset_line in asset_objects:
            if asset_line.sea_office_id:
                offices.append((asset_line.sea_office_id.id))
        offices = set(offices)
        for dept in department_id:
            row_no += 1

            department_name = self.env['hr.department'].browse(dept)

            worksheet_tscd.merge_range(row_no, 0, row_no, 15, department_name.sudo().name if department_name else '', body_f4)




            for office in offices:
                for asset_line in asset_objects:
                    if asset_line.management_dept and asset_line.sea_office_id:
                        if dept == asset_line.management_dept.id and office==asset_line.sea_office_id.id:
                            row_no += 1
                            worksheet_tscd.merge_range(row_no, 1, row_no, 15,
                                           asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                            break
                for asset_line in asset_objects:
                    if dept == asset_line.management_dept.id and asset_line.sea_office_id:
                        if office==asset_line.sea_office_id.id:
                            row_no += 1
                            line_row += 1
                            worksheet_tscd.write(row_no, 0, line_row, body_f1)
                            worksheet_tscd.write(row_no, 1, asset_line.name, body_f2)
                            worksheet_tscd.write(row_no, 2, asset_line.code, body_f2)
                            worksheet_tscd.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                            worksheet_tscd.write(row_no, 4, asset_line.quantity, body_f1)
                            worksheet_tscd.write(row_no, 5, asset_line.value, body_f3)
                            worksheet_tscd.write(row_no, 6, asset_line.value_residual, body_f3)
                            worksheet_tscd.write(row_no, 7, '', body_f4)
                            worksheet_tscd.write(row_no, 8, '', body_f4)
                            worksheet_tscd.write(row_no, 9, '', body_f4)
                            worksheet_tscd.write(row_no, 10, '', body_f4)
                            worksheet_tscd.write(row_no, 11, '', body_f4)
                            worksheet_tscd.write(row_no, 12, '', body_f4)
                            worksheet_tscd.write(row_no, 13, '', body_f4)
                            worksheet_tscd.write(row_no, 14, '', body_f4)
                            worksheet_tscd.write(row_no, 15, '', body_f4)

            have_no_office=False
            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    have_no_office = True
                    break
            if have_no_office:
                row_no += 1
                worksheet_tscd.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)

            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    row_no += 1
                    line_row += 1
                    worksheet_tscd.write(row_no, 0, line_row, body_f1)
                    worksheet_tscd.write(row_no, 1, asset_line.name, body_f2)
                    worksheet_tscd.write(row_no, 2, asset_line.code, body_f2)
                    worksheet_tscd.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                    worksheet_tscd.write(row_no, 4, asset_line.quantity, body_f1)
                    worksheet_tscd.write(row_no, 5, asset_line.value, body_f3)
                    worksheet_tscd.write(row_no, 6, asset_line.value_residual, body_f3)
                    worksheet_tscd.write(row_no, 7, '', body_f4)
                    worksheet_tscd.write(row_no, 8, '', body_f4)
                    worksheet_tscd.write(row_no, 9, '', body_f4)
                    worksheet_tscd.write(row_no, 10, '', body_f4)
                    worksheet_tscd.write(row_no, 11, '', body_f4)
                    worksheet_tscd.write(row_no, 12, '', body_f4)
                    worksheet_tscd.write(row_no, 13, '', body_f4)
                    worksheet_tscd.write(row_no, 14, '', body_f4)
                    worksheet_tscd.write(row_no, 15, '', body_f4)
        row_no += 1
        have_not_dept=False
        for asset_line in asset_objects:
            if not asset_line.management_dept:
                have_not_dept=True
                break

        if have_not_dept:
            row_no += 1
            worksheet_tscd.merge_range(row_no, 0, row_no, 15, 'ĐƠN VỊ KHÔNG XÁC ĐỊNH', body_f4)

        for office in offices:

            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office==asset_line.sea_office_id.id:
                        row_no += 1
                        worksheet_tscd.merge_range(row_no, 1, row_no, 15,
                                       asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                        break
            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office == asset_line.sea_office_id.id:
                        row_no += 1
                        line_row += 1
                        worksheet_tscd.write(row_no, 0, line_row, body_f1)
                        worksheet_tscd.write(row_no, 1, asset_line.name, body_f2)
                        worksheet_tscd.write(row_no, 2, asset_line.code, body_f2)
                        worksheet_tscd.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                        worksheet_tscd.write(row_no, 4, asset_line.quantity, body_f1)
                        worksheet_tscd.write(row_no, 5, asset_line.value, body_f3)
                        worksheet_tscd.write(row_no, 6, asset_line.value_residual, body_f3)
                        worksheet_tscd.write(row_no, 7, '', body_f4)
                        worksheet_tscd.write(row_no, 8, '', body_f4)
                        worksheet_tscd.write(row_no, 9, '', body_f4)
                        worksheet_tscd.write(row_no, 10, '', body_f4)
                        worksheet_tscd.write(row_no, 11, '', body_f4)
                        worksheet_tscd.write(row_no, 12, '', body_f4)
                        worksheet_tscd.write(row_no, 13, '', body_f4)
                        worksheet_tscd.write(row_no, 14, '', body_f4)
                        worksheet_tscd.write(row_no, 15, '', body_f4)
        have_no_office = False
        for asset_line in asset_objects:
            if not asset_line.management_dept.id and not asset_line.sea_office_id:
                have_no_office = True
                break
        if have_no_office:
            row_no += 1
            worksheet_tscd.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)
        for asset_line in asset_objects:
            if not asset_line.management_dept and not asset_line.sea_office_id:
                row_no += 1
                line_row += 1
                worksheet_tscd.write(row_no, 0, line_row, body_f1)
                worksheet_tscd.write(row_no, 1, asset_line.name, body_f2)
                worksheet_tscd.write(row_no, 2, asset_line.code, body_f2)
                worksheet_tscd.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                worksheet_tscd.write(row_no, 4, asset_line.quantity, body_f1)
                worksheet_tscd.write(row_no, 5, asset_line.value, body_f3)
                worksheet_tscd.write(row_no, 6, asset_line.value_residual, body_f3)
                worksheet_tscd.write(row_no, 7, '', body_f4)
                worksheet_tscd.write(row_no, 8, '', body_f4)
                worksheet_tscd.write(row_no, 9, '', body_f4)
                worksheet_tscd.write(row_no, 10, '', body_f4)
                worksheet_tscd.write(row_no, 11, '', body_f4)
                worksheet_tscd.write(row_no, 12, '', body_f4)
                worksheet_tscd.write(row_no, 13, '', body_f4)
                worksheet_tscd.write(row_no, 14, '', body_f4)
                worksheet_tscd.write(row_no, 15, '', body_f4)
        x = 0
        row_no+=1
        while x < 16:
            worksheet_tscd.write(row_no, x, '', header_table)
            x += 1
        worksheet_tscd.write(row_no, 1, 'Tổng', header_table)
        row_no += 2
        worksheet_tscd.write(row_no, 13, 'Ngày ... Tháng ... Năm ........', signature_f1)
        row_no += 1
        worksheet_tscd.write(row_no, 1, 'Người lập', signature_f2)
        worksheet_tscd.merge_range(row_no, 2, row_no, 4, 'Đại diện ban kiểm kê', signature_f2)
        worksheet_tscd.write(row_no, 9, 'Kế toán trưởng', signature_f2)
        worksheet_tscd.write(row_no, 13, 'Giám đốc/CEO', signature_f2)

        row_no += 1
        worksheet_tscd.write(row_no, 1, '(Ký, họ tên)', signature_f3)
        worksheet_tscd.merge_range(row_no, 2, row_no, 4, '(Ký, họ tên)', signature_f3)
        worksheet_tscd.write(row_no, 9, '(Ký, họ tên)', signature_f3)
        worksheet_tscd.write(row_no, 13, '(Ký, họ tên và đóng dấu)', signature_f3)

    def generate_xlsx_report_ccdc(self,workbook, data, objects,asset_type):
        # worksheet_ccdc = workbook.add_worksheet('TSCD')
        worksheet_ccdc = workbook.add_worksheet('CCDC')
        # worksheet_ccdccpb = workbook.add_worksheet('CCDCCPB')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        header_f1 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 14, 'font_name': 'Times New Roman'})
        header_f2 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f3 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f4 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f5 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 15, 'font_name': 'Times New Roman'})
        header_f6 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f7 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_table = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f1 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f2 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f3 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'num_format': '#,##0', 'font_name': 'Times New Roman'})
        body_f4 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f1 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        signature_f2 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f3 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})

        text_center = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})
        text_left = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})

        short_date = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mm/yyyy',
             'font_name': 'Tahoma', 'font_size': 10})
        money = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0',
                                     'font_size': 10, 'font_name': 'Tahoma'})
        no_data = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Tahoma'})

        row_no = 0

        # Report Header
        worksheet_ccdc.set_column(0, 0, 7), worksheet_ccdc.set_column(1, 1, 40), worksheet_ccdc.set_column(2, 2, 15)
        worksheet_ccdc.set_column(3, 3, 15), worksheet_ccdc.set_column(4, 4, 6), worksheet_ccdc.set_column(5, 5, 12)
        worksheet_ccdc.set_column(6, 6, 14), worksheet_ccdc.set_column(7, 7, 6), worksheet_ccdc.set_column(8, 8, 12)
        worksheet_ccdc.set_column(9, 9, 16), worksheet_ccdc.set_column(10, 10, 6), worksheet_ccdc.set_column(11, 11, 12)
        worksheet_ccdc.set_column(12, 12, 14), worksheet_ccdc.set_column(13, 13, 50), worksheet_ccdc.set_column(14, 14, 50)
        worksheet_ccdc.set_column(15, 15, 50)

        worksheet_ccdc.merge_range(row_no, 0, row_no, 3, 'Đơn vị: ' + company_name, header_f1)
        worksheet_ccdc.write(row_no, 13, 'Mẫu số 05 - TSCĐ', header_f2)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 3, 'Bộ phận: ', header_f3)
        worksheet_ccdc.merge_range(row_no, 11, row_no, 13, '(Ban hành theo Thông tư số 200/2014/TT-BTC Ngày 22/12/2014 của Bộ Tài chính)', header_f4)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 13, 'BIÊN BẢN KIỂM KÊ CCDC', header_f5)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 13, 'Áp dụng cho CCDC đang được sử dụng chờ phân bổ', header_f6)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, 'Thời gian kiểm kê: … giờ, ngày    tháng    năm 20  ', header_f7)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, 'Ban kiểm kê gồm:', header_f7)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdc.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdc.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdc.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdc.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdc.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdc.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 2
        worksheet_ccdc.merge_range(row_no, 0, row_no, 2, 'Đã kiểm kê CCDC, kết quả như sau:', header_f7)
        row_no += 2
        worksheet_ccdc.merge_range(row_no, 0, row_no + 1, 0, 'STT', header_table)
        worksheet_ccdc.merge_range(row_no, 1, row_no + 1, 1, 'Tên CCDC', header_table)
        worksheet_ccdc.merge_range(row_no, 2, row_no + 1, 2, 'Mã số', header_table)
        worksheet_ccdc.merge_range(row_no, 3, row_no + 1, 3, 'Nơi sử dụng', header_table)
        worksheet_ccdc.merge_range(row_no, 4, row_no, 6, 'Theo số kế toán', header_table)
        worksheet_ccdc.merge_range(row_no, 7, row_no, 9, 'Theo số kiểm kê', header_table)
        worksheet_ccdc.merge_range(row_no, 10, row_no, 12, 'Chênh lệch', header_table)
        worksheet_ccdc.merge_range(row_no, 13, row_no + 1, 13, 'Ghi chú', header_table)
        worksheet_ccdc.merge_range(row_no, 14, row_no + 1, 14, 'Đề xuất xử lý', header_table)
        worksheet_ccdc.merge_range(row_no, 15, row_no + 1, 15, 'Giải trình của đơn vị', header_table)
        row_no += 1
        worksheet_ccdc.write(row_no, 4, 'Số lượng', header_table)
        worksheet_ccdc.write(row_no, 5, 'Nguyên giá', header_table)
        worksheet_ccdc.write(row_no, 6, 'Giá trị còn lại', header_table)
        worksheet_ccdc.write(row_no, 7, 'Số lượng', header_table)
        worksheet_ccdc.write(row_no, 8, 'Nguyên giá', header_table)
        worksheet_ccdc.write(row_no, 9, 'Giá trị còn lại', header_table)
        worksheet_ccdc.write(row_no, 10, 'Số lượng', header_table)
        worksheet_ccdc.write(row_no, 11, 'Nguyên giá', header_table)
        worksheet_ccdc.write(row_no, 12, 'Giá trị còn lại', header_table)
        row_no += 1
        domain = [('company_id', '=', self.env.user.company_id.id)]
        asset_types = self.env['account.asset.type'].sudo().search([('type_template', '=', asset_type)])

        if asset_types:
            domain.append(('asset_type', 'in', asset_types.ids))
        '''Don vi su dung tai san'''
        if data.get('department_id'):
            domain.append(('management_dept', '=', data.get('department_id')))
        if data.get('location_id'):
            domain.append(('sea_office_id', '=', data.get('location_id')))

        asset_objects = self.env['account.asset.asset'].search(domain,order='management_dept')

        line_row = 0
        department_list = []
        for asset in asset_objects:
            if asset.management_dept:
                department_list.append(asset.management_dept.id)

        department_id=[]
        if len(department_list)>0:
            department_id = set(department_list)

        row_no += 1
        offices = []
        for asset_line in asset_objects:
            if asset_line.sea_office_id:
                offices.append((asset_line.sea_office_id.id))
        offices = set(offices)
        for dept in department_id:
            row_no += 1

            department_name = self.env['hr.department'].browse(dept)

            worksheet_ccdc.merge_range(row_no, 0, row_no, 15, department_name.sudo().name if department_name else '', body_f4)




            for office in offices:
                for asset_line in asset_objects:
                    if asset_line.management_dept and asset_line.sea_office_id:
                        if dept == asset_line.management_dept.id and office==asset_line.sea_office_id.id:
                            row_no += 1
                            worksheet_ccdc.merge_range(row_no, 1, row_no, 15,
                                           asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                            break
                for asset_line in asset_objects:
                    if dept == asset_line.management_dept.id and asset_line.sea_office_id:
                        if office==asset_line.sea_office_id.id:
                            row_no += 1
                            line_row += 1
                            worksheet_ccdc.write(row_no, 0, line_row, body_f1)
                            worksheet_ccdc.write(row_no, 1, asset_line.name, body_f2)
                            worksheet_ccdc.write(row_no, 2, asset_line.code, body_f2)
                            worksheet_ccdc.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                            worksheet_ccdc.write(row_no, 4, asset_line.quantity, body_f1)
                            worksheet_ccdc.write(row_no, 5, asset_line.value, body_f3)
                            worksheet_ccdc.write(row_no, 6, asset_line.value_residual, body_f3)
                            worksheet_ccdc.write(row_no, 7, '', body_f4)
                            worksheet_ccdc.write(row_no, 8, '', body_f4)
                            worksheet_ccdc.write(row_no, 9, '', body_f4)
                            worksheet_ccdc.write(row_no, 10, '', body_f4)
                            worksheet_ccdc.write(row_no, 11, '', body_f4)
                            worksheet_ccdc.write(row_no, 12, '', body_f4)
                            worksheet_ccdc.write(row_no, 13, '', body_f4)
                            worksheet_ccdc.write(row_no, 14, '', body_f4)
                            worksheet_ccdc.write(row_no, 15, '', body_f4)

            have_no_office=False
            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    have_no_office = True
                    break
            if have_no_office:
                row_no += 1
                worksheet_ccdc.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)

            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    row_no += 1
                    line_row += 1
                    worksheet_ccdc.write(row_no, 0, line_row, body_f1)
                    worksheet_ccdc.write(row_no, 1, asset_line.name, body_f2)
                    worksheet_ccdc.write(row_no, 2, asset_line.code, body_f2)
                    worksheet_ccdc.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                    worksheet_ccdc.write(row_no, 4, asset_line.quantity, body_f1)
                    worksheet_ccdc.write(row_no, 5, asset_line.value, body_f3)
                    worksheet_ccdc.write(row_no, 6, asset_line.value_residual, body_f3)
                    worksheet_ccdc.write(row_no, 7, '', body_f4)
                    worksheet_ccdc.write(row_no, 8, '', body_f4)
                    worksheet_ccdc.write(row_no, 9, '', body_f4)
                    worksheet_ccdc.write(row_no, 10, '', body_f4)
                    worksheet_ccdc.write(row_no, 11, '', body_f4)
                    worksheet_ccdc.write(row_no, 12, '', body_f4)
                    worksheet_ccdc.write(row_no, 13, '', body_f4)
                    worksheet_ccdc.write(row_no, 14, '', body_f4)
                    worksheet_ccdc.write(row_no, 15, '', body_f4)
        row_no += 1
        have_not_dept=False

        for asset_line in asset_objects:
            if not asset_line.management_dept:
                have_not_dept=True
                break

        if have_not_dept:
            row_no += 1
            worksheet_ccdc.merge_range(row_no, 0, row_no, 15, 'ĐƠN VỊ KHÔNG XÁC ĐỊNH', body_f4)


        for office in offices:

            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office==asset_line.sea_office_id.id:
                        row_no += 1
                        worksheet_ccdc.merge_range(row_no, 1, row_no, 15,
                                       asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                        break
            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office == asset_line.sea_office_id.id:
                        row_no += 1
                        line_row += 1
                        worksheet_ccdc.write(row_no, 0, line_row, body_f1)
                        worksheet_ccdc.write(row_no, 1, asset_line.name, body_f2)
                        worksheet_ccdc.write(row_no, 2, asset_line.code, body_f2)
                        worksheet_ccdc.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                        worksheet_ccdc.write(row_no, 4, asset_line.quantity, body_f1)
                        worksheet_ccdc.write(row_no, 5, asset_line.value, body_f3)
                        worksheet_ccdc.write(row_no, 6, asset_line.value_residual, body_f3)
                        worksheet_ccdc.write(row_no, 7, '', body_f4)
                        worksheet_ccdc.write(row_no, 8, '', body_f4)
                        worksheet_ccdc.write(row_no, 9, '', body_f4)
                        worksheet_ccdc.write(row_no, 10, '', body_f4)
                        worksheet_ccdc.write(row_no, 11, '', body_f4)
                        worksheet_ccdc.write(row_no, 12, '', body_f4)
                        worksheet_ccdc.write(row_no, 13, '', body_f4)
                        worksheet_ccdc.write(row_no, 14, '', body_f4)
                        worksheet_ccdc.write(row_no, 15, '', body_f4)

        have_no_office = False
        for asset_line in asset_objects:
            if not asset_line.management_dept.id and not asset_line.sea_office_id:
                have_no_office = True
                break
        if have_no_office:
            row_no += 1
            worksheet_ccdc.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)
        for asset_line in asset_objects:
            if not asset_line.management_dept and not asset_line.sea_office_id:
                row_no += 1
                line_row += 1
                worksheet_ccdc.write(row_no, 0, line_row, body_f1)
                worksheet_ccdc.write(row_no, 1, asset_line.name, body_f2)
                worksheet_ccdc.write(row_no, 2, asset_line.code, body_f2)
                worksheet_ccdc.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                worksheet_ccdc.write(row_no, 4, asset_line.quantity, body_f1)
                worksheet_ccdc.write(row_no, 5, asset_line.value, body_f3)
                worksheet_ccdc.write(row_no, 6, asset_line.value_residual, body_f3)
                worksheet_ccdc.write(row_no, 7, '', body_f4)
                worksheet_ccdc.write(row_no, 8, '', body_f4)
                worksheet_ccdc.write(row_no, 9, '', body_f4)
                worksheet_ccdc.write(row_no, 10, '', body_f4)
                worksheet_ccdc.write(row_no, 11, '', body_f4)
                worksheet_ccdc.write(row_no, 12, '', body_f4)
                worksheet_ccdc.write(row_no, 13, '', body_f4)
                worksheet_ccdc.write(row_no, 14, '', body_f4)
                worksheet_ccdc.write(row_no, 15, '', body_f4)

        x = 0
        row_no+=1
        while x < 16:
            worksheet_ccdc.write(row_no, x, '', header_table)
            x += 1
        worksheet_ccdc.write(row_no, 1, 'Tổng', header_table)
        row_no += 2
        worksheet_ccdc.write(row_no, 13, 'Ngày ... Tháng ... Năm ........', signature_f1)
        row_no += 1
        worksheet_ccdc.write(row_no, 1, 'Người lập', signature_f2)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 4, 'Đại diện ban kiểm kê', signature_f2)
        worksheet_ccdc.write(row_no, 9, 'Kế toán trưởng', signature_f2)
        worksheet_ccdc.write(row_no, 13, 'Giám đốc/CEO', signature_f2)

        row_no += 1
        worksheet_ccdc.write(row_no, 1, '(Ký, họ tên)', signature_f3)
        worksheet_ccdc.merge_range(row_no, 2, row_no, 4, '(Ký, họ tên)', signature_f3)
        worksheet_ccdc.write(row_no, 9, '(Ký, họ tên)', signature_f3)
        worksheet_ccdc.write(row_no, 13, '(Ký, họ tên và đóng dấu)', signature_f3)

    def generate_xlsx_report_ccdccpb(self,workbook, data, objects,asset_type):
        # worksheet_tscd = workbook.add_worksheet('TSCD')
        # worksheet_ccdc = workbook.add_worksheet('CCDC')
        worksheet_ccdccpb = workbook.add_worksheet('CCDCCPB')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        header_f1 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 14, 'font_name': 'Times New Roman'})
        header_f2 = workbook.add_format(
            {'bold': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f3 = workbook.add_format(
            {'bold': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_f4 = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f5 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 15, 'font_name': 'Times New Roman'})
        header_f6 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        header_f7 = workbook.add_format(
            {'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        header_table = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f1 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f2 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        body_f3 = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'num_format': '#,##0', 'font_name': 'Times New Roman'})
        body_f4 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f1 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})
        signature_f2 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'font_name': 'Times New Roman'})
        signature_f3 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 11, 'italic': True, 'font_name': 'Times New Roman'})

        text_center = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})
        text_left = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
             'font_size': 10})

        short_date = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mm/yyyy',
             'font_name': 'Tahoma', 'font_size': 10})
        money = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0',
                                     'font_size': 10, 'font_name': 'Tahoma'})
        no_data = workbook.add_format(
            {'border': 1, 'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Tahoma'})

        row_no = 0

        # Report Header
        worksheet_ccdccpb.set_column(0, 0, 7), worksheet_ccdccpb.set_column(1, 1, 40), worksheet_ccdccpb.set_column(2, 2, 15)
        worksheet_ccdccpb.set_column(3, 3, 15), worksheet_ccdccpb.set_column(4, 4, 6), worksheet_ccdccpb.set_column(5, 5, 12)
        worksheet_ccdccpb.set_column(6, 6, 14), worksheet_ccdccpb.set_column(7, 7, 6), worksheet_ccdccpb.set_column(8, 8, 12)
        worksheet_ccdccpb.set_column(9, 9, 16), worksheet_ccdccpb.set_column(10, 10, 6), worksheet_ccdccpb.set_column(11, 11, 12)
        worksheet_ccdccpb.set_column(12, 12, 14), worksheet_ccdccpb.set_column(13, 13, 50), worksheet_ccdccpb.set_column(14, 14, 50)
        worksheet_ccdccpb.set_column(15, 15, 50)

        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 3, 'Đơn vị: ' + company_name, header_f1)
        worksheet_ccdccpb.write(row_no, 13, 'Mẫu số 05 - TSCĐ', header_f2)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 3, 'Bộ phận: ', header_f3)
        worksheet_ccdccpb.merge_range(row_no, 11, row_no, 13, '(Ban hành theo Thông tư số 200/2014/TT-BTC Ngày 22/12/2014 của Bộ Tài chính)', header_f4)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 13, 'BIÊN BẢN KIỂM KÊ CCDCCPB', header_f5)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 13, 'Áp dụng cho CCDC đang được sử dụng chờ phân bổ', header_f6)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, 'Thời gian kiểm kê: … giờ, ngày    tháng    năm 20  ', header_f7)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, 'Ban kiểm kê gồm:', header_f7)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdccpb.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdccpb.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdccpb.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 1
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 1, '- Ông/Bà: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 3, 'Chức vụ: ', header_f7)
        worksheet_ccdccpb.merge_range(row_no, 4, row_no, 5, 'Đại diện: ', header_f7)
        worksheet_ccdccpb.write(row_no, 6, 'Trưởng ban', header_f7)
        row_no += 2
        worksheet_ccdccpb.merge_range(row_no, 0, row_no, 2, 'Đã kiểm kê CCDC, kết quả như sau:', header_f7)
        row_no += 2
        worksheet_ccdccpb.merge_range(row_no, 0, row_no + 1, 0, 'STT', header_table)
        worksheet_ccdccpb.merge_range(row_no, 1, row_no + 1, 1, 'Tên CCDC', header_table)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no + 1, 2, 'Mã số', header_table)
        worksheet_ccdccpb.merge_range(row_no, 3, row_no + 1, 3, 'Nơi sử dụng', header_table)
        worksheet_ccdccpb.merge_range(row_no, 4, row_no, 6, 'Theo số kế toán', header_table)
        worksheet_ccdccpb.merge_range(row_no, 7, row_no, 9, 'Theo số kiểm kê', header_table)
        worksheet_ccdccpb.merge_range(row_no, 10, row_no, 12, 'Chênh lệch', header_table)
        worksheet_ccdccpb.merge_range(row_no, 13, row_no + 1, 13, 'Ghi chú', header_table)
        worksheet_ccdccpb.merge_range(row_no, 14, row_no + 1, 14, 'Đề xuất xử lý', header_table)
        worksheet_ccdccpb.merge_range(row_no, 15, row_no + 1, 15, 'Giải trình của đơn vị', header_table)
        row_no += 1
        worksheet_ccdccpb.write(row_no, 4, 'Số lượng', header_table)
        worksheet_ccdccpb.write(row_no, 5, 'Nguyên giá', header_table)
        worksheet_ccdccpb.write(row_no, 6, 'Giá trị còn lại', header_table)
        worksheet_ccdccpb.write(row_no, 7, 'Số lượng', header_table)
        worksheet_ccdccpb.write(row_no, 8, 'Nguyên giá', header_table)
        worksheet_ccdccpb.write(row_no, 9, 'Giá trị còn lại', header_table)
        worksheet_ccdccpb.write(row_no, 10, 'Số lượng', header_table)
        worksheet_ccdccpb.write(row_no, 11, 'Nguyên giá', header_table)
        worksheet_ccdccpb.write(row_no, 12, 'Giá trị còn lại', header_table)
        row_no += 1
        domain = [('company_id', '=', self.env.user.company_id.id)]
        asset_types = self.env['account.asset.type'].sudo().search([('type_template', '=', asset_type)])
        if asset_types:
            domain.append(('asset_type', 'in', asset_types.ids))
        else:
            domain.append(('asset_type', 'in', []))
        '''Don vi su dung tai san'''
        if data.get('department_id'):
            domain.append(('management_dept', '=', data.get('department_id')))
        if data.get('location_id'):
            domain.append(('sea_office_id', '=', data.get('location_id')))

        asset_objects = self.env['account.asset.asset'].search(domain,order='management_dept')

        line_row = 0
        department_list = []
        for asset in asset_objects:
            if asset.management_dept:
                department_list.append(asset.management_dept.id)

        department_id=[]
        if len(department_list)>0:
            department_id = set(department_list)

        row_no += 1
        offices = []
        for asset_line in asset_objects:
            if asset_line.sea_office_id:
                offices.append((asset_line.sea_office_id.id))
        offices = set(offices)
        for dept in department_id:
            row_no += 1

            department_name = self.env['hr.department'].browse(dept)

            worksheet_ccdccpb.merge_range(row_no, 0, row_no, 15, department_name.sudo().name if department_name else '', body_f4)




            for office in offices:
                for asset_line in asset_objects:
                    if asset_line.management_dept and asset_line.sea_office_id:
                        if dept == asset_line.management_dept.id and office==asset_line.sea_office_id.id:
                            row_no += 1
                            worksheet_ccdccpb.merge_range(row_no, 1, row_no, 15,
                                           asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                            break
                for asset_line in asset_objects:
                    if dept == asset_line.management_dept.id and asset_line.sea_office_id:
                        if office==asset_line.sea_office_id.id:
                            row_no += 1
                            line_row += 1
                            worksheet_ccdccpb.write(row_no, 0, line_row, body_f1)
                            worksheet_ccdccpb.write(row_no, 1, asset_line.name, body_f2)
                            worksheet_ccdccpb.write(row_no, 2, asset_line.code, body_f2)
                            worksheet_ccdccpb.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                            worksheet_ccdccpb.write(row_no, 4, asset_line.quantity, body_f1)
                            worksheet_ccdccpb.write(row_no, 5, asset_line.value, body_f3)
                            worksheet_ccdccpb.write(row_no, 6, asset_line.value_residual, body_f3)
                            worksheet_ccdccpb.write(row_no, 7, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 8, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 9, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 10, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 11, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 12, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 13, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 14, '', body_f4)
                            worksheet_ccdccpb.write(row_no, 15, '', body_f4)

            have_no_office=False
            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    have_no_office = True
                    break
            if have_no_office:
                row_no += 1
                worksheet_ccdccpb.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)

            for asset_line in asset_objects:
                if dept == asset_line.management_dept.id and not asset_line.sea_office_id:
                    row_no += 1
                    line_row += 1
                    worksheet_ccdccpb.write(row_no, 0, line_row, body_f1)
                    worksheet_ccdccpb.write(row_no, 1, asset_line.name, body_f2)
                    worksheet_ccdccpb.write(row_no, 2, asset_line.code, body_f2)
                    worksheet_ccdccpb.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                    worksheet_ccdccpb.write(row_no, 4, asset_line.quantity, body_f1)
                    worksheet_ccdccpb.write(row_no, 5, asset_line.value, body_f3)
                    worksheet_ccdccpb.write(row_no, 6, asset_line.value_residual, body_f3)
                    worksheet_ccdccpb.write(row_no, 7, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 8, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 9, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 10, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 11, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 12, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 13, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 14, '', body_f4)
                    worksheet_ccdccpb.write(row_no, 15, '', body_f4)
        row_no += 1
        have_not_dept=False

        for asset_line in asset_objects:
            if not asset_line.management_dept:
                have_not_dept=True
                break

        if have_not_dept:
            row_no += 1
            worksheet_ccdccpb.merge_range(row_no, 0, row_no, 15, 'ĐƠN VỊ KHÔNG XÁC ĐỊNH', body_f4)


        for office in offices:

            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office==asset_line.sea_office_id.id:
                        row_no += 1
                        worksheet_ccdccpb.merge_range(row_no, 1, row_no, 15,
                                       asset_line.sea_office_id.name if asset_line.sea_office_id else '', body_f4)
                        break
            for asset_line in asset_objects:
                if not asset_line.management_dept and asset_line.sea_office_id:
                    if office == asset_line.sea_office_id.id:
                        row_no += 1
                        line_row += 1
                        worksheet_ccdccpb.write(row_no, 0, line_row, body_f1)
                        worksheet_ccdccpb.write(row_no, 1, asset_line.name, body_f2)
                        worksheet_ccdccpb.write(row_no, 2, asset_line.code, body_f2)
                        worksheet_ccdccpb.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                        worksheet_ccdccpb.write(row_no, 4, asset_line.quantity, body_f1)
                        worksheet_ccdccpb.write(row_no, 5, asset_line.value, body_f3)
                        worksheet_ccdccpb.write(row_no, 6, asset_line.value_residual, body_f3)
                        worksheet_ccdccpb.write(row_no, 7, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 8, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 9, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 10, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 11, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 12, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 13, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 14, '', body_f4)
                        worksheet_ccdccpb.write(row_no, 15, '', body_f4)

        have_no_office = False
        for asset_line in asset_objects:
            if not asset_line.management_dept.id and not asset_line.sea_office_id:
                have_no_office = True
                break
        if have_no_office:
            row_no += 1
            worksheet_ccdccpb.merge_range(row_no, 1, row_no, 15, 'ĐỊA ĐIỂM KHÔNG XÁC ĐỊNH', body_f4)
        for asset_line in asset_objects:
            if not asset_line.management_dept and not asset_line.sea_office_id:
                row_no += 1
                line_row += 1
                worksheet_ccdccpb.write(row_no, 0, line_row, body_f1)
                worksheet_ccdccpb.write(row_no, 1, asset_line.name, body_f2)
                worksheet_ccdccpb.write(row_no, 2, asset_line.code, body_f2)
                worksheet_ccdccpb.write(row_no, 3, asset_line.dept_owner.name if asset_line.dept_owner else '', body_f4)
                worksheet_ccdccpb.write(row_no, 4, asset_line.quantity, body_f1)
                worksheet_ccdccpb.write(row_no, 5, asset_line.value, body_f3)
                worksheet_ccdccpb.write(row_no, 6, asset_line.value_residual, body_f3)
                worksheet_ccdccpb.write(row_no, 7, '', body_f4)
                worksheet_ccdccpb.write(row_no, 8, '', body_f4)
                worksheet_ccdccpb.write(row_no, 9, '', body_f4)
                worksheet_ccdccpb.write(row_no, 10, '', body_f4)
                worksheet_ccdccpb.write(row_no, 11, '', body_f4)
                worksheet_ccdccpb.write(row_no, 12, '', body_f4)
                worksheet_ccdccpb.write(row_no, 13, '', body_f4)
                worksheet_ccdccpb.write(row_no, 14, '', body_f4)
                worksheet_ccdccpb.write(row_no, 15, '', body_f4)

        x = 0
        row_no+=1
        while x < 16:
            worksheet_ccdccpb.write(row_no, x, '', header_table)
            x += 1
        worksheet_ccdccpb.write(row_no, 1, 'Tổng', header_table)
        row_no += 2
        worksheet_ccdccpb.write(row_no, 13, 'Ngày ... Tháng ... Năm ........', signature_f1)
        row_no += 1
        worksheet_ccdccpb.write(row_no, 1, 'Người lập', signature_f2)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 4, 'Đại diện ban kiểm kê', signature_f2)
        worksheet_ccdccpb.write(row_no, 9, 'Kế toán trưởng', signature_f2)
        worksheet_ccdccpb.write(row_no, 13, 'Giám đốc/CEO', signature_f2)

        row_no += 1
        worksheet_ccdccpb.write(row_no, 1, '(Ký, họ tên)', signature_f3)
        worksheet_ccdccpb.merge_range(row_no, 2, row_no, 4, '(Ký, họ tên)', signature_f3)
        worksheet_ccdccpb.write(row_no, 9, '(Ký, họ tên)', signature_f3)
        worksheet_ccdccpb.write(row_no, 13, '(Ký, họ tên và đóng dấu)', signature_f3)

