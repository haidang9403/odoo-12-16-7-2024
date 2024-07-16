import io, base64, datetime
import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AssetReportXLS(models.AbstractModel):
    _name = 'report.sea_asset_base.asset_report_xls'
    _inherit = 'report.report_xlsx.abstract'
    def generate_work_sheet(self,workbook,worksheet,data,asset_type):
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street
        company_phone = self.env.user.company_id.phone
        company_email = self.env.user.company_id.catchall
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        website = self.env.user.company_id.website
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
        # Report Header
        worksheet.set_column(0, 0, 5), worksheet.set_column(1, 1, 15), worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 10), worksheet.set_column(4, 4, 8), worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 8), worksheet.set_column(7, 7, 7), worksheet.set_column(8, 8, 8)
        worksheet.set_column(9, 9, 8), worksheet.set_column(10, 10, 18), worksheet.set_column(11, 11, 15)
        worksheet.set_column(12, 12, 20), worksheet.set_column(13, 13, 20), worksheet.set_column(14, 14, 15)
        worksheet.set_column(15, 15, 15), worksheet.set_column(16, 16, 15), worksheet.set_column(17, 17, 15)
        worksheet.set_column(18, 18, 15), worksheet.set_column(119, 19, 15), worksheet.set_column(20, 20, 15)
        worksheet.set_column(21, 21, 15), worksheet.set_column(22, 22, 15), worksheet.set_column(23, 23, 18)
        worksheet.set_column(24, 24, 15), worksheet.set_column(25, 25, 15), worksheet.set_column(26, 26, 15)
        worksheet.set_column(27, 27, 15), worksheet.set_column(28, 28, 12)

        worksheet.merge_range(row_no, 0, row_no, 7, 'Thông tin chung', header)
        worksheet.merge_range(row_no, 8, row_no, 13, 'Thông tin kế toán', header)
        worksheet.merge_range(row_no, 14, row_no, 21, 'Thông tin giao nhận', header)
        worksheet.merge_range(row_no, 22, row_no, 28, 'Thông tin quản lý nội bộ', header)
        row_no += 1
        worksheet.write(row_no, 0, 'STT', header)
        worksheet.write(row_no, 1, 'Ngày Biên bản nghiệm thu', header)
        worksheet.write(row_no, 2, 'Số Biên bản nghiệm thu', header)
        worksheet.write(row_no, 3, 'Tên TS', header)
        worksheet.write(row_no, 4, 'Mã TS', header)
        worksheet.write(row_no, 5, 'Mô tả (nếu có)', header)
        worksheet.write(row_no, 6, 'Số lượng', header)
        worksheet.write(row_no, 7, 'Đơn vị tính', header)
        worksheet.write(row_no, 8, 'Phân loại', header)
        worksheet.write(row_no, 9, 'Nguyên giá', header)
        worksheet.write(row_no, 10, 'Số tháng khấu hao', header)
        worksheet.write(row_no, 11, 'Phương pháp khấu hao', header)
        worksheet.write(row_no, 12, 'Hao mòn lũy kế (tại thời điểm truy xuất thông tin)', header)
        worksheet.write(row_no, 13, 'Giá trị còn lại (tại thời điểm truy xuất thông tin)', header)
        worksheet.write(row_no, 14, 'Tên nhà cung cấp)', header)
        worksheet.write(row_no, 15, 'TS thuộc sở hữu của Công ty:)', header)
        worksheet.write(row_no, 16, 'Bộ phận quản lý sử dụng', header)
        worksheet.write(row_no, 17, 'Người sử dụng', header)
        worksheet.write(row_no, 18, 'Bên giao', header)
        worksheet.write(row_no, 19, 'Bên nhận', header)
        worksheet.write(row_no, 20, 'NV P.SX&QLTS phụ trách', header)
        worksheet.write(row_no, 21, 'NV BPMH phụ trách mua TS', header)
        worksheet.write(row_no, 22, 'Tình trạng TS tại thời điểm ban đầu', header)
        worksheet.write(row_no, 23, 'Tình trạng TS tại thời điểm kiểm kê gần nhất', header)
        worksheet.write(row_no, 24, 'Ngày tạm ngưng sử dụng TS', header)
        worksheet.write(row_no, 25, 'Ngày sửa chữa lần 1, lần 2,…', header)
        worksheet.write(row_no, 26, 'Ngày điều chuyển TS cho Đơn vị khác', header)
        worksheet.write(row_no, 27, 'Ngày nhận lại TS từ Đơn vị khác', header)
        worksheet.write(row_no, 28, 'Ngày thanh lý TS', header)
        row_no += 1
        domain = []
        asset_types = self.env['account.asset.type'].sudo().search([('type_template', '=', asset_type)])
        if asset_types:
            domain.append(('asset_type', 'in', asset_types.ids))
        domain.append(('state', '=', 'open'))
        domain.append(('company_id', '=', data.get('company_id')))
        if data.get('department_id'):
            domain.append(('dept_owner', '=', data.get('department_id')))
        if data.get('asset_type'):
            domain.append(('asset_type', '=', data.get('asset_type')))
        if data.get('category_id'):
            domain.append(('category_id', '=', data.get('category_id')))
        if data.get('sea_office_id'):
            domain.append(('sea_office_id', '=', data.get('sea_office_id')))
        if data.get('latest_inventory_status'):
            domain.append(('latest_inventory_status', '=', data.get('latest_inventory_status')))
        if data.get('latest_asset_transfer_date_from'):
            domain.append(('latest_asset_transfer_date', '>=', data.get('latest_asset_transfer_date_from')))
        if data.get('latest_asset_transfer_date_to'):
            domain.append(('latest_asset_transfer_date', '<=', data.get('latest_asset_transfer_date_to')))
        if data.get('asset_receive_date_from'):
            domain.append(('asset_receive_date', '>=', data.get('asset_receive_date_from')))
        if data.get('asset_receive_date_to'):
            domain.append(('asset_receive_date', '<=', data.get('asset_receive_date_to')))
        asset_objects = False
        try:
            asset_objects = self.env['account.asset.asset'].search(domain)
        except Exception as e:
            print('exception', e)
        line_row = 0
        for asset in asset_objects:
            line_row += 1
            worksheet.write(row_no, 0, line_row, f1)
            worksheet.write(row_no, 1, asset.acceptance_date if asset.acceptance_date else '', short_date)
            worksheet.write(row_no, 2, asset.acceptance_number if asset.acceptance_number else '', f2)

            worksheet.write(row_no, 3, asset.name, f2)
            worksheet.write(row_no, 4, asset.code if asset.code else '', f2)
            worksheet.write(row_no, 5, asset.description if asset.description else '', f2)

            worksheet.write(row_no, 6, asset.quantity, f1)
            worksheet.write(row_no, 7, asset.asset_uom.name if asset.asset_uom else '', f1)
            worksheet.write(row_no, 8, asset.category_id.sudo().name if asset.sudo().category_id else '', f2)
            worksheet.write(row_no, 9, asset.value, money)
            worksheet.write(row_no, 10, asset.method_period, f1)
            worksheet.write(row_no, 11, 'Tuyến tính' if asset.method == 'linear' else 'Giảm dần', f2)
            worksheet.write(row_no, 12, asset.salvage_value, money)
            worksheet.write(row_no, 13, asset.value_residual, money)
            worksheet.write(row_no, 14, asset.partner_id.name if asset.partner_id else '', f2)
            worksheet.write(row_no, 15, asset.company_id.name, f2)
            worksheet.write(row_no, 16, asset.management_dept.sudo().name if asset.management_dept else '', f2)
            worksheet.write(row_no, 17, asset.asset_user_temporary.name if asset.asset_user_temporary else '', f2)
            worksheet.write(row_no, 18, asset.handover_party if asset.handover_party else '', f2)
            worksheet.write(row_no, 19, asset.receiver_handover_party if asset.receiver_handover_party else '', f2)
            worksheet.write(row_no, 20, asset.asset_management_dept_staff_temporary.sudo().name if asset.asset_management_dept_staff_temporary else '', f2)
            worksheet.write(row_no, 21, asset.procurement_staff_temporary.sudo().name if asset.procurement_staff_temporary else '', f2)
            asset_status_start = ''
            if asset.asset_status_start == 'good':
                asset_status_start = 'Tốt'
            elif asset.asset_status_start == 'damaged_waiting_for_repair':
                asset_status_start = 'Hư hỏng chờ sửa chữa'
            elif asset.asset_status_start == 'damaged_waiting_for_liquidation':
                asset_status_start = 'Hư hỏng chờ thanh lý'
            elif asset.asset_status_start == 'self_destruct':
                asset_status_start = 'Thanh lý'
            worksheet.write(row_no, 22, asset_status_start, f2)
            latest_inventory_status = ''
            if asset.latest_inventory_status == 'good':
                latest_inventory_status = 'Tốt'

            elif asset.latest_inventory_status == 'damaged_waiting_for_repair':
                latest_inventory_status = 'Damaged waiting for repair'
            elif asset.latest_inventory_status == 'damaged_waiting_for_liquidation':
                latest_inventory_status = 'Damaged waiting for liquidation'
            elif asset.latest_inventory_status == 'self_destruct':
                latest_inventory_status = 'Self destruct'
            worksheet.write(row_no, 23, latest_inventory_status, f2)
            worksheet.write(row_no, 25, asset.repair_date if asset.repair_date else '', short_date)
            worksheet.write(row_no, 26, asset.latest_asset_transfer_date if asset.latest_asset_transfer_date else '', short_date)
            worksheet.write(row_no, 27, asset.asset_receive_date if asset.asset_receive_date else '', short_date)
            worksheet.write(row_no, 28, asset.liquidation_date if asset.liquidation_date else '', short_date)
            row_no += 1
    def generate_xlsx_report(self, workbook, data, objects):
        worksheet_tscd = workbook.add_worksheet('TSCD')
        worksheet_ccdc = workbook.add_worksheet('CCDC')
        worksheet_ccdccpb = workbook.add_worksheet('CCDCCPB')
        self.generate_work_sheet(workbook,worksheet_tscd,data,'tscd')
        self.generate_work_sheet(workbook,worksheet_ccdc,data,'ccdc')
        self.generate_work_sheet(workbook,worksheet_ccdccpb,data,'ccdccpb')
