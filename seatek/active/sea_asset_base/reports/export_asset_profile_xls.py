import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class ExportAssetProfileXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.export_asset_profile_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet = workbook.add_worksheet('Thẻ TS')

        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website

        header = workbook.add_format(
            {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Tahoma'})
        so_ngay_phutrach = workbook.add_format(
            {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': False,
             'font_size': 8, 'font_name': 'Tahoma'})
        table_tille = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 8, 'font_name': 'Tahoma'})
        table_data = workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 8, 'font_name': 'Tahoma','num_format': '#,##0'})
        table_data_date = workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 8, 'font_name': 'Tahoma','num_format': 'dd/mm/yyyy'})
        table_data_left = workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 8, 'font_name': 'Tahoma'})
        f1 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Times New Roman'})
        f2 = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Times New Roman'})
        money = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0',
                                     'font_size': 10, 'font_name': 'Times New Roman'})

        short_date = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mm/yyyy',
             'font_name': 'Tahoma', 'font_size': 10})


        row_no = 0
        worksheet.insert_image(0, 0, "company_logo.png",
                               {'image_data': company_logo, 'x_scale': 0.1, 'y_scale': 0.1})

        worksheet.merge_range(row_no, 3, row_no, 10, company_name,header)
        row_no += 1
        worksheet.merge_range(row_no, 3, row_no, 10,
                              'Địa chỉ: ' + company_address,header)
        row_no += 1
        worksheet.merge_range(row_no, 3, row_no, 10,
                              'Điện thoại: ' + str(company_phone) + '     Email: ' + company_email)
        row_no += 2
        # Report Header
        worksheet.set_column(0, 0, 1), worksheet.set_column(1, 1, 4), worksheet.set_column(2, 2, 8)
        worksheet.set_column(3, 3, 10), worksheet.set_column(4, 4, 8), worksheet.set_column(5, 5, 14)
        worksheet.set_column(6, 6, 6), worksheet.set_column(7, 7, 5), worksheet.set_column(8, 8, 7)
        worksheet.set_column(9, 9, 7), worksheet.set_column(10, 10, 9), worksheet.set_column(11, 11, 15)
        worksheet.set_column(12, 12, 20), worksheet.set_column(13, 13, 20), worksheet.set_column(14, 14, 15)
        worksheet.set_column(15, 15, 15), worksheet.set_column(16, 16, 15), worksheet.set_column(17, 17, 15)
        worksheet.set_column(18, 18, 15), worksheet.set_column(119, 19, 15), worksheet.set_column(20, 20, 15)
        worksheet.set_column(21, 21, 15), worksheet.set_column(22, 22, 15), worksheet.set_column(23, 23, 18)
        worksheet.set_column(24, 24, 15), worksheet.set_column(25, 25, 15), worksheet.set_column(26, 26, 15)
        worksheet.set_column(27, 27, 15), worksheet.set_column(28, 28, 12)
        row_no += 3
        worksheet.merge_range(row_no, 3, row_no, 7, 'Số...........................', so_ngay_phutrach)
        row_no+=1
        worksheet.merge_range(row_no, 3, row_no, 7, 'Ngày ...........................', so_ngay_phutrach)
        row_no += 1
        worksheet.merge_range(row_no, 3, row_no, 7, 'NV phụ trách ...........................', so_ngay_phutrach)
        row_no += 1
        worksheet.merge_range(row_no, 1, row_no, 7, 'I. THÔNG TIN CHUNG:', so_ngay_phutrach)
        row_no += 1
        worksheet.merge_range(row_no, 1, row_no, 7, '1. Tài sản:', so_ngay_phutrach)

        row_no += 1
        column=1
        worksheet.merge_range(row_no, column, row_no, column+1, 'BBNT & BG', table_tille)
        worksheet.write(row_no+1, column, 'Số', table_tille)
        worksheet.write(row_no+1, column+1, 'Ngày', table_tille)
        worksheet.write(row_no + 2, column, objects.acceptance_number if objects.acceptance_number else '', table_data)
        worksheet.write(row_no + 2, column + 1, objects.acceptance_date if objects.acceptance_number else '', table_data_date)
        column+=2
        worksheet.merge_range(row_no, column, row_no+1, column, 'MÃ TS', table_tille)
        worksheet.write(row_no+2, column, objects.code, table_data)
        column += 1
        worksheet.merge_range(row_no, column, row_no+1, column+2, 'TÊN TS', table_tille)
        worksheet.merge_range(row_no+2, column, row_no+2, column + 2, objects.name, table_data)
        column += 3
        worksheet.merge_range(row_no, column, row_no + 1, column, 'ĐVT', table_tille)
        worksheet.write(row_no+2, column, objects.alt_unit, table_data)
        column += 1
        worksheet.merge_range(row_no, column, row_no + 1, column, 'SL', table_tille)
        worksheet.write(row_no+2, column, objects.quantity, table_data)
        column += 1
        worksheet.merge_range(row_no, column, row_no + 1, column, 'PHÂN LOẠI', table_tille)
        if objects.asset_type:
            worksheet.write(row_no+2, column, objects.asset_type.sudo().name if objects.asset_type else '', table_data)
        else:
            worksheet.write(row_no + 2, column, '', table_data)
        column += 1
        worksheet.merge_range(row_no, column, row_no + 1, column, 'TIỂU MỤC', table_tille)
        worksheet.write(row_no+2, column, '', table_data)
        row_no+=4
        worksheet.merge_range(row_no, 1, row_no, 7, '1. Phụ tùng thay thế đi kèm:', so_ngay_phutrach)
        column=1
        row_no+=1
        worksheet.write(row_no, column, 'STT', table_tille)
        worksheet.write(row_no+1, column, '', table_data)
        worksheet.write(row_no+2, column, '', table_data)
        column+=1
        worksheet.write(row_no, column, 'MÃ PT', table_tille)
        worksheet.write(row_no + 1, column, '', table_data)
        worksheet.write(row_no + 2, column, '', table_data)
        column+=1
        worksheet.merge_range(row_no, column, row_no, column + 2, 'TÊN PT', table_tille)
        worksheet.merge_range(row_no+1, column, row_no+1, column + 2, '', table_data)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 2, '', table_data)
        column += 3
        worksheet.write(row_no, column, 'ĐVT', table_tille)
        worksheet.write(row_no+1, column, '', table_data)
        worksheet.write(row_no +2, column, '', table_data)
        column += 1
        worksheet.write(row_no, column, 'SL', table_tille)
        worksheet.write(row_no + 1, column, '', table_data)
        worksheet.write(row_no + 2, column, '', table_data)
        column += 1
        worksheet.write(row_no, column, 'GIÁ TRỊ', table_tille)
        worksheet.write(row_no + 1, column, '', table_data)
        worksheet.write(row_no + 2, column, '', table_data)
        column += 1
        worksheet.write(row_no, column, 'PHÂN LOẠI', table_tille)
        worksheet.write(row_no + 1, column, '', table_data)
        worksheet.write(row_no + 2, column, '', table_data)
        column += 1
        worksheet.write(row_no, column, 'TIỂU MỤC', table_tille)
        worksheet.write(row_no + 1, column, '', table_data)
        worksheet.write(row_no + 2, column, '', table_data)
        row_no += 4
        worksheet.merge_range(row_no, 1, row_no, 7, 'II. THÔNG TIN KẾ TOÁN:', so_ngay_phutrach)
        column = 1
        row_no += 1
        worksheet.merge_range(row_no, column, row_no, column + 1, 'NGUYÊN GIÁ', table_tille)
        column+=2
        worksheet.write(row_no, column, 'THỜI GIAN KHẤU HAO', table_tille)
        column += 1
        worksheet.merge_range(row_no, column, row_no , column+1, 'PHƯƠNG PHÁP KHẤU HAO', table_tille)
        column+=2
        worksheet.merge_range(row_no, column, row_no, column + 2, 'HAO MÒN LŨY KẾ', table_tille)
        column += 3
        worksheet.merge_range(row_no, column, row_no, column + 1, 'GIÁ TRỊ CÒN LẠI', table_tille)
        asset_id=objects.id
        depreciations=self.env['account.asset.depreciation.line'].search([('asset_id','=',objects.id)])
        for depreciation in depreciations:
            if depreciation.asset_id.id==objects.id:
                row_no+=1
                column=1
                worksheet.write(row_no, column, objects.value, table_data)
                worksheet.merge_range(row_no, column, row_no, column + 1, objects.value, table_data)
                column+=2
                worksheet.write(row_no, column, depreciation.depreciation_date, table_data_date)
                column += 1
                worksheet.merge_range(row_no, column, row_no , column+1, 'Tuyến tính' if objects.method == 'linear' else 'Giảm dần', table_data)
                column += 2
                worksheet.merge_range(row_no, column, row_no, column + 2, depreciation.depreciated_value, table_data)
                column += 3
                worksheet.merge_range(row_no, column, row_no, column + 1, depreciation.remaining_value, table_data)
        column += 3
        row_no += 2
        worksheet.merge_range(row_no, 1, row_no, 7, 'II. THÔNG TIN GIAO NHẬN:', so_ngay_phutrach)
        column = 1
        row_no += 1
        worksheet.merge_range(row_no, column, row_no, column + 1, 'Tên NCC', table_data_left)
        worksheet.merge_range(row_no+1, column, row_no+1, column + 1, 'Đơn vị sở hữu', table_data_left)
        worksheet.merge_range(row_no+2, column, row_no+2, column + 1, 'Bộ phận sử dụng', table_data_left)
        worksheet.merge_range(row_no+3, column, row_no+3, column + 1, 'Người sử dụng', table_data_left)
        column +=2
        worksheet.merge_range(row_no, column, row_no, column + 2, objects.partner_id.sudo().name if objects.partner_id else '', table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no+1, column + 2, objects.company_id.name if objects.company_id else '', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no+2, column + 2, objects.management_dept.name if objects.management_dept else '', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no+3, column + 2, objects.asset_user_temporary.sudo().name if objects.asset_user_temporary else '' ,
                              table_data_left)
        column += 3
        worksheet.merge_range(row_no, column, row_no, column + 1, 'Bên giao', table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no+1, column + 1, 'Bên nhận', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no+2, column + 1, 'ĐV QLTS', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no+3, column + 1, 'BPMH', table_data_left)

        column += 2
        worksheet.merge_range(row_no, column, row_no, column + 2, objects.handover_party if objects.handover_party else '', table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no + 1, column + 2, objects.receiver_handover_party if objects.receiver_handover_party else '', \
                                                                                                                                             table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 2, objects.asset_management_dept_staff_temporary.sudo().name if
        objects.asset_management_dept_staff_temporary else '', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no + 3, column + 2, objects.procurement_staff_temporary.sudo().name if
        objects.procurement_staff_temporary else
        '' ,
                              table_data_left)
        row_no += 5
        column=1
        worksheet.merge_range(row_no, 1, row_no, 7, 'II. THÔNG TIN SỬ DỤNG - QUẢN LÝ:', so_ngay_phutrach)
        row_no+=1
        worksheet.merge_range(row_no, column, row_no, column + 2, 'Tình trang ban đầu', table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no + 1, column + 2, 'Ngày tạm ngưng sử dụng', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 2, 'Ngày sữa chữa lần 1', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no + 3, column + 2, 'Ngày sữa chữa lần...:', table_data_left)
        worksheet.merge_range(row_no + 4, column, row_no + 4, column + 2, 'Ngày điều chuyển cho ĐV khác', table_data_left)
        worksheet.merge_range(row_no + 5, column, row_no + 5, column + 2, 'Ngày nhận lại từ ĐV khác', table_data_left)
        worksheet.merge_range(row_no + 6, column, row_no + 6, column + 2, 'Ngày nhận điều chuyển từ ĐV khác', table_data_left)
        worksheet.merge_range(row_no + 7, column, row_no + 7, column + 2, 'Ngày trả lại cho ĐV khác', table_data_left)
        worksheet.merge_range(row_no + 8, column, row_no + 8, column + 2, 'Ngày thanh lý TS', table_data_left)
        column+=3
        asset_status_start=''
        if objects.asset_status_start:
            if objects.asset_status_start=='good':
                asset_status_start='Tốt'
            elif objects.asset_status_start=='damaged_waiting_for_repair':
                asset_status_start='Hư hỏng chờ sửa chữa'
            elif objects.asset_status_start=='waiting':
                asset_status_start='Hư hỏng chờ thanh lý'
            elif objects.asset_status_start=='self_destruct':
                asset_status_start='Đã thanh lý'


        worksheet.merge_range(row_no, column, row_no, column + 1, asset_status_start, table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no + 1, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no + 3, column + 1, objects.repair_date if objects.repair_date else '', table_data_date)
        worksheet.merge_range(row_no + 4, column, row_no + 4, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 5, column, row_no + 5, column + 1, objects.asset_receive_date if objects.asset_receive_date else '', table_data_date)
        worksheet.merge_range(row_no + 6, column, row_no + 6, column + 1, objects.latest_asset_transfer_date if objects.latest_asset_transfer_date else '',
                              table_data_date )
        worksheet.merge_range(row_no + 7, column, row_no + 7, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 8, column, row_no + 8, column + 1, objects.liquidation_date if objects.liquidation_date else '', table_data_date)
        column+=2
        worksheet.merge_range(row_no, column, row_no, column + 2, 'Tình trang tại thời điểm KK', table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no + 1, column + 2, 'Ngày sử dụng lại', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 2, 'Lý do', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no + 3, column + 2, 'Lý do', table_data_left)
        worksheet.merge_range(row_no + 4, column, row_no + 5, column + 2, 'ĐV nhận điều chuyển', table_data_left)
        worksheet.merge_range(row_no + 6, column, row_no + 7, column + 2, 'ĐV điều chuyển', table_data_left)
        worksheet.merge_range(row_no + 8, column, row_no + 8, column + 2, 'Người mua', table_data_left)
        column+=3
        latest_inventory_status = ''
        if objects.latest_inventory_status:
            if objects.latest_inventory_status == 'good':
                latest_inventory_status = 'Tốt'
            elif objects.latest_inventory_status == 'damaged_waiting_for_repair':
                latest_inventory_status = 'Hư hỏng chờ sửa chữa'
            elif objects.latest_inventory_status == 'waiting':
                latest_inventory_status = 'Hư hỏng chờ thanh lý'
            elif objects.latest_inventory_status == 'self_destruct':
                latest_inventory_status = 'Đã thanh lý'
        worksheet.merge_range(row_no, column, row_no, column + 1, latest_inventory_status, table_data_left)
        worksheet.merge_range(row_no + 1, column, row_no + 1, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 2, column, row_no + 2, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 3, column, row_no + 3, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 4, column, row_no + 4, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 5, column, row_no + 5, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 6, column, row_no + 6, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 7, column, row_no + 7, column + 1, '', table_data_left)
        worksheet.merge_range(row_no + 8, column, row_no + 8, column + 1, objects.procurement_staff_temporary.name if objects.procurement_staff_temporary else '',table_data_left)