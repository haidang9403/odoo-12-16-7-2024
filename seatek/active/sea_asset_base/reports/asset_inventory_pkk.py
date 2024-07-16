import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AssetInvntoryPKKReportXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.asset_inventory_pkk_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):

        worksheet = workbook.add_worksheet('PHIẾU KIỂM KÊ')
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
        worksheet.set_column(6, 6, 8), worksheet.set_column(7, 7, 7), worksheet.set_column(8, 8, 13)
        worksheet.set_column(9, 9, 13), worksheet.set_column(10, 10, 13), worksheet.set_column(11, 11, 15)
        worksheet.set_column(12, 12, 12), worksheet.set_column(13, 13, 20), worksheet.set_column(14, 14, 20)
        worksheet.set_column(15, 15, 20), worksheet.set_column(16, 16, 20), worksheet.set_column(17, 17, 20)
        worksheet.set_column(18, 18, 15), worksheet.set_column(119, 19, 15), worksheet.set_column(20, 20, 15)
        worksheet.set_column(21, 21, 15), worksheet.set_column(22, 22, 15), worksheet.set_column(23, 23, 18)
        worksheet.set_column(24, 24, 15), worksheet.set_column(25, 25, 15), worksheet.set_column(26, 26, 15)
        worksheet.set_column(27, 27, 15), worksheet.set_column(28, 28, 12)
        row_no += 2
        title_format = workbook.add_format(
            {'border': 0, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 22,'bold': 1})
        worksheet.merge_range(row_no,3,row_no,10,'PHIẾU KIỂM KÊ',title_format)

        information_format = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        inventory_line_col = 1
        row_no+=2
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Đơn vị:', information_format)
        worksheet.merge_range(row_no, inventory_line_col+2,row_no,inventory_line_col+8, objects.company_id.name if objects.company_id else '',
                              information_format)
        row_no += 1
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Đối tượng:', information_format)
        worksheet.merge_range(row_no, inventory_line_col + 2, row_no, inventory_line_col + 8, objects.sea_office_id.name if objects.sea_office_id else '',
                              information_format)
        row_no += 1
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Bộ phận:', information_format)
        worksheet.merge_range(row_no, inventory_line_col + 2, row_no, inventory_line_col + 8, objects.department.name if objects.department else '',
                              information_format)
        # row_no += 1
        # worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Khu vục (nếu có):', information_format)
        # worksheet.merge_range(row_no, inventory_line_col + 2, row_no, inventory_line_col + 8, objects.department.name if objects.department else '',
        #                       information_format)
        row_no += 1
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Thời gian bắt đầu:', information_format)
        worksheet.merge_range(row_no, inventory_line_col + 2, row_no, inventory_line_col + 8, objects.start_time.strftime("%d-%m-%Y") if objects.start_time
        else '' ,information_format)
        row_no += 1
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, 'Thời gian kết thúc:', information_format)
        worksheet.merge_range(row_no, inventory_line_col + 2, row_no, inventory_line_col + 8, objects.end_time.strftime("%d-%m-%Y") if objects.end_time
        else '',information_format)
        row_no += 2
        information_format = workbook.add_format(
            {'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        worksheet.merge_range(row_no, inventory_line_col,row_no,inventory_line_col+1, '- Thành viên Ban kiểm kê:', information_format)
        stt=0
        inventory_line_col=1
        for member in objects.member_of_inventory:
            row_no += 1
            col_no=1
            stt+=1
            worksheet.write(row_no, col_no,str(stt)+'.',information_format)
            worksheet.merge_range(row_no, col_no +1, row_no, col_no + 2, member.employee_id_temp.name if member.employee_id_temp
            else '',information_format)
            worksheet.merge_range(row_no, col_no + 3, row_no, col_no + 4,'Chức vụ: '+ member.position.name if member.position else ''
            ,information_format)
        row_no += 2
        worksheet.merge_range(row_no, inventory_line_col, row_no, inventory_line_col + 1, '- Đại diện Đơn vị được kiểm kê:', information_format)
        stt = 0
        for member in objects.inventoried_department:
            row_no += 1
            stt += 1
            worksheet.write(row_no, col_no, str(stt)+'.' , information_format)
            worksheet.merge_range(row_no, col_no, row_no, col_no + 2, member.employee_id_temp.name if member.employee_id_temp
            else ''
                                  , information_format)
            worksheet.merge_range(row_no, col_no + 3, row_no, col_no + 4,'Chức vụ: '+ member.job_id.sudo().name if member.job_id else ''
                                  , information_format)
        row_no += 2
        inventory_line_title_format = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11, 'bold': 1})

        row_no += 2
        inventory_line_col = 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'STT',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col + 3, 'Tên nhãn hiệu, quy cách',
                              inventory_line_title_format)
        inventory_line_col += 4
        worksheet.merge_range(row_no, inventory_line_col, row_no + 1, inventory_line_col , 'Mã số',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no + 1, inventory_line_col, 'ĐVT',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.write(row_no,  inventory_line_col, 'Theo sổ sách',inventory_line_title_format)
        worksheet.write(row_no+1, inventory_line_col, 'Số lượng',inventory_line_title_format)
        inventory_line_col += 1
        worksheet.write(row_no,  inventory_line_col, 'Kiểm kê thực tế',
                              inventory_line_title_format)
        worksheet.write(row_no+1,  inventory_line_col, 'Số lượng',inventory_line_title_format)
        inventory_line_col += 1
        worksheet.write(row_no,  inventory_line_col, 'Chênh lệch',inventory_line_title_format)
        worksheet.write (row_no + 1, inventory_line_col,'Số lượng',inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'Thực trạng',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'Đã dán tem mới',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'Người/BP sử dụng',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'Ghi chú',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no+1, inventory_line_col, 'Đề xuất xử lý',
                              inventory_line_title_format)
        inventory_line_col += 1
        worksheet.merge_range(row_no, inventory_line_col, row_no + 1, inventory_line_col, 'Giải trình của đơn vị',
                              inventory_line_title_format)
        inventory_line_col = 1
        inventory_line_format = workbook.add_format(
            {'border': 0, 'align': 'left', 'valign': 'vcenter', 'text_wrap': False,
             'font_name': 'Tahoma', 'font_size': 11,'bold':1})
        stt = 1
        row_no += 3
        worksheet.merge_range(row_no,  1, row_no, 7, '- Đã kiểm kê và ghi nhận số lượng thực tế, chi tiết như sau : ',
                              inventory_line_format)
        inventory_line_left_format = workbook.add_format(
            {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        inventory_line_format = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11})
        for line in objects.asset_inventory_lines:
            row_no += 1
            col_no=1
            worksheet.set_row(row_no, 50)
            worksheet.write(row_no, inventory_line_col, stt, inventory_line_format)
            worksheet.merge_range(row_no, col_no+1, row_no , col_no + 4, line.asset_id.name if line.asset_id else '',
                                  inventory_line_left_format)
            col_no+=5
            worksheet.write(row_no, inventory_line_col+5, line.asset_id.code if line.asset_id else '',
                                  inventory_line_format)
            col_no +=1
            worksheet.write(row_no, col_no,  line.asset_uom.name if line.asset_uom else '',
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no, line.quantity_so_sach ,
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no,  line.quantity_thuc_te ,
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no,  line.quantity_chenh_lech ,
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no,  'Đang sử dụng' if line.status=='dang_su_dung'
            else 'Hư hỏng' , inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no, 'Đã dán tem' if line.da_dan_tem else 'Chưa dán tem',
                            inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no, line.asset_user_temporary.name if line.asset_user_temporary
            else '', inventory_line_format)

            col_no += 1
            worksheet.write(row_no, col_no,   line.note if line.note else '',
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no,   line.de_xuat_xu_ly if line.de_xuat_xu_ly else '',
                                  inventory_line_format)
            col_no += 1
            worksheet.write(row_no, col_no,   line.giai_trinh if line.giai_trinh else '',
                                  inventory_line_format)

            stt+=1

        row_no += 2
        sign_format = workbook.add_format(
            {'border': 0, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_name': 'Tahoma', 'font_size': 11,'bold':1})
        worksheet.merge_range(row_no, 2, row_no, 8, 'THÀNH VIÊN BAN KIỂM KÊ',
                              sign_format)
        worksheet.merge_range(row_no, 10, row_no, 14, 'ĐẠI DIỆN ĐƠN VỊ',
                              sign_format)
        row_no += 1
        col_no=1
        worksheet.merge_range(row_no, col_no+1, row_no, col_no+2, 'Trưởng nhóm',
                              sign_format)
        worksheet.merge_range(row_no, col_no+3, row_no, col_no+4, 'Thành viên',
                              sign_format)
        worksheet.merge_range(row_no, col_no+5, row_no, col_no+6, 'Kế toán',
                              sign_format)
        worksheet.merge_range(row_no, col_no+10, row_no, col_no+11, 'Quản lý trực tiếp',
                              sign_format)
        worksheet.merge_range(row_no, col_no+12, row_no, col_no+13, 'Nhân viên',
                              sign_format)