import io, base64, datetime
from odoo import models
import pytz


class DeliveryLogSaleOrderReport(models.AbstractModel):
    _name = 'report.sea_report_delivery_packing_log.packing_log'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        worksheet1 = workbook.add_worksheet('Nhật ký đóng gói')
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street + ', ' + self.env.user.company_id.street2 + ', ' + self.env.user.company_id.state_id.name
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        company_vat = self.env.user.company_id.vat

        header = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Tahoma'})
        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Tahoma'})
        f2 = workbook.add_format(
            {'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma'})
        f3 = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 13,
                                  'font_name': 'Tahoma'})
        f5 = workbook.add_format({'border': 1, 'text_wrap': True, 'valign': 'vcenter'})
        f6 = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0.000'})
        time_report = workbook.add_format(
            {'align': 'right', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9, 'italic': True,
             'font_name': 'Arial'})
        warehouse = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 11,
             'font_name': 'Tahoma'})
        date_search = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
                                           'font_name': 'Tahoma'})
        company = workbook.add_format({'bold': 1, 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
                                       'font_name': 'Tahoma'})
        signature = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 9,
             'font_name': 'Tahoma'})
        text_center = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})

        # header
        worksheet1.set_row(0, 8)
        worksheet1.set_column(0, 0, 4)
        worksheet1.set_column(1, 1, 15)
        worksheet1.set_column(2, 2, 6)
        worksheet1.set_column(3, 3, 20)
        worksheet1.set_column(4, 4, 20)
        worksheet1.set_column(7, 7, 10)
        row_no = 1

        worksheet1.insert_image(0, 1, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.52, 'y_scale': 0.53})
        worksheet1.merge_range(row_no, 2, row_no, 7, company_name, company)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 7, company_address, company)
        row_no += 1
        worksheet1.merge_range(row_no, 2, row_no, 7, 'MST: ' + str(company_vat), company)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 7, 'NHẬT KÝ ĐÓNG GÓI SẢN PHẨM', f1)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 7,
                               'Từ ngày ' + str(objects.start_date.strftime('%d-%m-%Y')) + ' đến ngày ' + str(
                                   objects.end_date.strftime('%d-%m-%Y')), date_search)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 7, str(objects.warehouse_id.name), warehouse)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 7, str(datetime.datetime.now().astimezone(vn_timezone).strftime("%d-%m-%Y  %H:%M:%S")),
                         time_report)
        row_no += 1
        worksheet1.write(row_no, 0, 'STT', header)
        worksheet1.write(row_no, 1, 'SO', header)
        worksheet1.write(row_no, 2, 'Giờ giao', header)
        worksheet1.write(row_no, 3, 'Khách hàng', header)
        worksheet1.write(row_no, 4, 'Sản phẩm', header)
        worksheet1.write(row_no, 5, 'S.lượng tổng', header)
        worksheet1.write(row_no, 6, 'S.lượng thực tế', header)
        worksheet1.write(row_no, 7, 'Ghi chú', header)

        domain = [('commitment_date', '>=', data.get('start_date')),
                  ('commitment_date', '<=', data.get('end_date')),
                  ('warehouse_id', '=', data.get('warehouse_id')),
                  ('state', 'not in', ['draft', 'cancel'])]
        number = 0
        for order in self.env['sale.order'].search(domain):
            for line_order in order.order_line:
                if line_order.product_id:
                    row_no += 1
                    number += 1

                    worksheet1.write(row_no, 0, number, text_center)
                    worksheet1.write(row_no, 1, line_order.order_id.name if line_order.order_id.name else '', text_center)
                    if order.commitment_date:
                        vn_time = order.commitment_date.astimezone(vn_timezone)
                        formatted_time = vn_time.strftime('%H:%M')
                        worksheet1.write(row_no, 2, formatted_time, text_center)
                    else:
                        worksheet1.write(row_no, 2, '', f5)
                    worksheet1.write(row_no, 3,
                                     order.partner_shipping_id.name if order.partner_shipping_id.name else '', f5)
                    worksheet1.write(row_no, 4, line_order.product_id.name if line_order.product_id.name else '', f5)
                    worksheet1.write(row_no, 5, line_order.product_uom_qty - line_order.qty_delivered, f6)
                    worksheet1.write(row_no, 6, '', f5)
                    worksheet1.write(row_no, 7, '', f5)
        row_no += 1
        for col in range(8):
            worksheet1.write(row_no, col, '', f5)

        row_no += 2
        worksheet1.merge_range(row_no, 3, row_no, 4, 'Bộ phận phụ trách đóng gói', signature)
        worksheet1.merge_range(row_no, 5, row_no, 7, 'Người lập', signature)
