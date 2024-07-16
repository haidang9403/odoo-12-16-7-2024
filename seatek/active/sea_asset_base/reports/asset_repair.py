import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AssetRepairReportXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.asset_repair_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):

        worksheet = workbook.add_worksheet('PHIẾU SỬA CHỮA')
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
        worksheet.set_column(6, 6, 8), worksheet.set_column(7, 7, 12), worksheet.set_column(8, 8, 12)
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
        worksheet.merge_range(row_no,3,row_no,10,'PHIẾU SỬA CHỮA',title_format)
        row_no += 2
        thong_tin_chung_col=1
        information_format = workbook.add_format(
            {'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        worksheet.merge_range(row_no, thong_tin_chung_col , row_no, thong_tin_chung_col +1, 'Ngày lập phiếu',
                              information_format)
        worksheet.merge_range(row_no, thong_tin_chung_col + 2, row_no, thong_tin_chung_col + 7, objects.repair_date.strftime("%d/%m/%Y") if
        objects.repair_date else '',
                              information_format)
        row_no += 1
        worksheet.set_row(row_no, 18)
        worksheet.merge_range(row_no, thong_tin_chung_col, row_no, thong_tin_chung_col + 1, 'Người bàn giao',
                              information_format)
        worksheet.merge_range(row_no, thong_tin_chung_col + 2, row_no, thong_tin_chung_col + 7,
                              objects.employee_temporary.name if objects.employee_temporary else '',
                              information_format)
        transfer_line_col = 1
        transfer_line_format = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        transfer_line_title_format = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11, 'bold': 1})
        stt = 1
        row_no += 2
        transfer_line_col = 1

        worksheet.write(row_no, transfer_line_col, 'STT', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.merge_range(row_no, transfer_line_col, row_no, transfer_line_col + 3, 'Tên TS',
                              transfer_line_title_format)
        transfer_line_col += 4
        worksheet.write(row_no, transfer_line_col, 'Mã TS', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.write(row_no, transfer_line_col, 'Thời gian bắt đầu', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.write(row_no, transfer_line_col, 'Thời gian kết thúc', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.write(row_no, transfer_line_col, 'Tên Đơn vị', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.write(row_no, transfer_line_col, 'Nơi xảy ra sự cố', transfer_line_title_format)
        transfer_line_col += 1
        worksheet.merge_range(row_no, transfer_line_col, row_no, transfer_line_col + 2, 'Mô tả sự cố',
                              transfer_line_title_format)
        transfer_line_col = 1
        for line in objects.asset_repair_lines:
            row_no += 1
            worksheet.set_row(row_no, 18)
            worksheet.write(row_no, transfer_line_col, stt, transfer_line_format)
            worksheet.merge_range(row_no, transfer_line_col + 1, row_no, transfer_line_col + 4, line.asset_id.name if line.asset_id else '',
                                   transfer_line_format)
            worksheet.write(row_no, transfer_line_col + 5, line.asset_code if line.asset_code else '', transfer_line_format)
            worksheet.write(row_no, transfer_line_col + 6, line.repair_date_start.strftime("%d/%m/%Y") if line.repair_date_start else '0',
                             transfer_line_format)
            worksheet.write(row_no, transfer_line_col + 7, line.repair_date_end.strftime("%d/%m/%Y") if line.repair_date_end else '0',
                        transfer_line_format)
            worksheet.write(row_no, transfer_line_col + 8, line.repair_party if line.repair_party else '',
                             transfer_line_format)
            worksheet.write(row_no, transfer_line_col + 9, line.accident_place if line.accident_place else '',
                            transfer_line_format)
            worksheet.merge_range(row_no, transfer_line_col+10, row_no, transfer_line_col + 12,line.description if line.description else '',
                                  transfer_line_title_format)
            stt+=1
