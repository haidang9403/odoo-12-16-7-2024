import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AssetTransferReportXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.asset_transfer_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet = workbook.add_worksheet('BIÊN BẢN NHẬN TÀI SẢN')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        header = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Tahoma'})

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

        worksheet.insert_image(0, 2, "company_logo.png",
                               {'image_data': company_logo, 'x_scale': 0.1, 'y_scale': 0.1})

        worksheet.merge_range(row_no, 3, row_no, 13, company_name)
        row_no += 1
        worksheet.merge_range(row_no, 3, row_no, 13,
                              'Địa chỉ: ' + company_address)
        row_no += 1
        worksheet.merge_range(row_no, 3, row_no, 13,
                              'Điện thoại: ' + str(company_phone) + '     Email: ' + company_email)
        row_no += 2
        worksheet.set_column(0, 0, 5), worksheet.set_column(1, 1, 5), worksheet.set_column(2, 2, 18)
        worksheet.set_column(3, 3, 10), worksheet.set_column(4, 4, 8), worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 8), worksheet.set_column(7, 7, 7), worksheet.set_column(8, 8, 8)
        worksheet.set_column(9, 9, 8), worksheet.set_column(10, 10, 18), worksheet.set_column(11, 11, 15)
        worksheet.set_column(12, 12, 20), worksheet.set_column(13, 13, 20), worksheet.set_column(14, 14, 15)
        worksheet.set_column(15, 15, 15), worksheet.set_column(16, 16, 15), worksheet.set_column(17, 17, 15)
        worksheet.set_column(18, 18, 15), worksheet.set_column(119, 19, 15), worksheet.set_column(20, 20, 15)
        worksheet.set_column(21, 21, 15), worksheet.set_column(22, 22, 15), worksheet.set_column(23, 23, 18)
        worksheet.set_column(24, 24, 15), worksheet.set_column(25, 25, 15), worksheet.set_column(26, 26, 15)
        worksheet.set_column(27, 27, 15), worksheet.set_column(28, 28, 12)
        row_no += 2
        title_format = workbook.add_format(
            {'border': 0, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 22,'bold': 1})
        worksheet.merge_range(row_no,3,row_no,10,'BIÊN BẢN BÀN GIAO',title_format)

        information_format = workbook.add_format(
            {'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        row_no += 2
        thong_tin_chung_col=1
        worksheet.merge_range(row_no, thong_tin_chung_col , row_no, thong_tin_chung_col +1, 'Số phiếu',
                              information_format)
        worksheet.merge_range(row_no, thong_tin_chung_col+2, row_no, thong_tin_chung_col+7, objects.acceptance_number if objects.acceptance_number else '',
                              information_format)
        row_no += 1
        worksheet.set_row(row_no, 18)
        worksheet.merge_range(row_no, thong_tin_chung_col, row_no, thong_tin_chung_col + 1, 'Ngày bàn giao',
                              information_format)
        worksheet.merge_range(row_no, thong_tin_chung_col + 2, row_no, thong_tin_chung_col + 7, objects.acceptance_date.strftime("%d-%m-%Y") if objects.acceptance_date else '',
                              information_format)

        row_no += 1
        worksheet.set_row(row_no, 18)
        worksheet.merge_range(row_no, thong_tin_chung_col, row_no, thong_tin_chung_col + 1, 'Công ty nhận',
                              information_format)
        worksheet.merge_range(row_no, thong_tin_chung_col + 2, row_no, thong_tin_chung_col + 7, objects.dest_company_id.name if
        objects.dest_company_id else '', information_format)
        transfer_line_title_format = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11,'bold':1})
        stt = 1
        row_no += 2
        transfer_line_col=1
        worksheet.write(row_no, transfer_line_col, 'STT', transfer_line_title_format)
        transfer_line_col+=1
        worksheet.merge_range(row_no, transfer_line_col, row_no, transfer_line_col + 3, 'Hạng mục',
                              transfer_line_title_format)
        transfer_line_col += 4
        worksheet.write(row_no, transfer_line_col, 'Đơn vị', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.write(row_no, transfer_line_col, 'Số lượng', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.merge_range(row_no, transfer_line_col, row_no, transfer_line_col + 3, 'Ghi chú',
                              transfer_line_title_format)
        transfer_line_col=1
        transfer_line_format = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        for line in objects.asset_transfer_line_ids:
            row_no += 1
            worksheet.set_row(row_no, 18)
            worksheet.write(row_no, transfer_line_col, stt, transfer_line_format)
            worksheet.merge_range(row_no, transfer_line_col + 1, row_no, transfer_line_col + 4, line.asset_id.name if line.asset_id else '',
                                  transfer_line_format)
            worksheet.write(row_no, transfer_line_col+5, line.uom_id.name if line.uom_id else '', transfer_line_format)
            worksheet.write(row_no, transfer_line_col+6, line.quantity_done if line.quantity_done else '0', transfer_line_format)
            worksheet.merge_range(row_no, transfer_line_col + 7, row_no, transfer_line_col + 10, line.note if line.note else '',
                                  transfer_line_format)
            stt+=1
        row_no += 2
        sign_col=1
        sign_top_format = workbook.add_format(
            {'top': 1,'left':1,'right':1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        sign_bottom_format = workbook.add_format(
            {'bottom': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vbottom', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})

        worksheet.set_row(row_no, 18)
        worksheet.merge_range(row_no, sign_col, row_no, sign_col + 2, 'Ngày: .............',sign_top_format)
        worksheet.merge_range(row_no, sign_col+3, row_no, sign_col + 6, 'Ngày: .............', sign_top_format)
        worksheet.merge_range(row_no, sign_col+7, row_no, sign_col + 10, 'Ngày: .............', sign_top_format)
        row_no+=1
        worksheet.merge_range(row_no, sign_col, row_no, sign_col + 2, 'NGƯỜI GIAO', sign_bottom_format)
        worksheet.merge_range(row_no, sign_col + 3, row_no, sign_col + 6, 'BÊN VẬN CHUYỂN', sign_bottom_format)
        worksheet.merge_range(row_no, sign_col + 7, row_no, sign_col + 10, 'NGƯỜI NHẬN', sign_bottom_format)
        row_no += 1
        worksheet.set_row(row_no, 90)
        worksheet.merge_range(row_no, sign_col, row_no, sign_col + 2,'Họ &  tên:'+objects.from_user  if
        objects.from_user else ''+ '\nHọ &  tên:.........', sign_bottom_format)
        worksheet.merge_range(row_no, sign_col + 3, row_no, sign_col + 6,'Họ &  tên:'+objects.shipping_party if
        objects.shipping_party else ''+ 'Họ &  tên:.........', sign_bottom_format)
        worksheet.merge_range(row_no, sign_col + 7, row_no, sign_col + 10,'Họ &  tên:'+ objects.to_user  if
        objects.to_user else ''+ 'Họ &  tên:.........', sign_bottom_format)
        row_no += 2
        handover_top_format = workbook.add_format(
            {'top': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        worksheet.merge_range(row_no, sign_col, row_no, sign_col + 6, 'Phụ trách đơn vị giao',handover_top_format)
        worksheet.merge_range(row_no, sign_col+7, row_no, sign_col + 10, 'Phụ trách đơn vị nhận',handover_top_format)
        row_no += 1
        worksheet.set_row(row_no, 90)
        worksheet.merge_range(row_no, sign_col, row_no, sign_col + 6,'Họ &  tên:'+ objects.handover_party  if
        objects.handover_party else '' + 'Họ &  tên:.........', sign_bottom_format)
        worksheet.merge_range(row_no, sign_col + 7, row_no, sign_col + 10,'Họ &  tên:'+ objects.receiver_handover_party  if
        objects.receiver_handover_party else ''+ 'Họ &  tên:.........', sign_bottom_format)
