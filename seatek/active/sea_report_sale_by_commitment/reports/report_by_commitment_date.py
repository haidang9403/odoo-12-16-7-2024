import logging
from odoo import models
import pytz

_logger = logging.getLogger(__name__)


class AccountingReportXLS(models.AbstractModel):
    _name = 'report.sea_report_sale_by_commitment.report_by_commitment_date'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        worksheet1 = workbook.add_worksheet('Báo cáo bán hàng (Commitment Date)')
        worksheet2 = workbook.add_worksheet('Báo cáo xuất kho bán hàng')

        header = workbook.add_format(
            {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
             'font_size': 10, 'font_name': 'Tahoma'})

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

        # Header
        worksheet1.set_column(0, 0, 5)
        worksheet1.set_column(1, 1, 10)
        worksheet1.set_column(2, 2, 10)
        worksheet1.set_column(3, 3, 8)
        worksheet1.set_column(4, 4, 10)
        worksheet1.set_column(5, 5, 10)
        worksheet1.set_column(6, 6, 10)
        worksheet1.set_column(7, 7, 8)
        worksheet1.set_column(8, 8, 10)
        worksheet1.set_column(9, 9, 10)
        worksheet1.set_column(10, 10, 10)
        worksheet1.set_column(11, 11, 8)
        worksheet1.set_column(12, 12, 10)
        worksheet1.set_column(13, 13, 35)
        worksheet1.set_column(14, 14, 35)
        worksheet1.set_column(15, 15, 6)
        worksheet1.set_column(16, 16, 10)
        worksheet1.set_column(17, 17, 8)
        worksheet1.set_column(18, 18, 15)
        worksheet1.set_column(19, 19, 15)
        worksheet1.set_column(20, 20, 10)
        worksheet1.set_column(21, 21, 10)
        worksheet1.set_column(22, 22, 13)
        worksheet1.set_column(23, 23, 25)
        worksheet1.set_column(24, 24, 10)
        worksheet1.set_column(25, 25, 10)
        worksheet1.set_column(26, 26, 8)
        worksheet1.set_column(27, 27, 10)
        worksheet1.set_column(28, 28, 10)
        worksheet1.set_column(29, 29, 10)
        worksheet1.set_column(30, 30, 10)
        worksheet1.set_column(31, 31, 10)

        worksheet1.freeze_panes(1, 0)

        worksheet2.set_column(0, 0, 5)
        worksheet2.set_column(1, 1, 10)
        worksheet2.set_column(2, 2, 35)
        worksheet2.set_column(3, 3, 5)
        worksheet2.set_column(4, 4, 5)
        worksheet2.set_column(5, 5, 10)
        worksheet2.set_column(6, 6, 10)
        worksheet2.set_column(7, 7, 10)
        worksheet2.set_column(8, 8, 10)

        worksheet2.freeze_panes(1, 0)

        sheet1_row_no = 0
        sheet1_col_no = 0
        sheet2_row_no = 0

        worksheet1.write(sheet1_row_no, sheet1_col_no, 'STT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh Thu', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'S.Lượng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Thuế GTGT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền Dự kiến', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh thu/Chi Phí Dự Kiến', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'S.Lượng Dự Kiến', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Thuế GTGT Dự Kiến', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Tổng Số Tiền', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Tổng Doanh Thu', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Tổng S.Lượng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Tổng Thuế GTGT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Đối Tượng (Ghi CHú)', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Diễn Giải', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'TS %', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'VAT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Chứng Từ Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Chứng Từ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày CHứng Từ Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Bọ Phận Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Sản Phẩm', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã sản Phẩm Kế Toán', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Cây Nhóm Sản Phẩm', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền Theo Đơn Đặt Hàng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh Thu Theo Đơn Đặt Hàng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'S.Lượng Theo Đơn Đặt Hàng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Thuế Theo Đơn Đặt Hàng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 1', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 2', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 3', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 4', header)
        sheet1_row_no += 1

        worksheet2.write(sheet2_row_no, 0, 'STT', header)
        worksheet2.write(sheet2_row_no, 1, 'Mã Sản Phẩm', header)
        worksheet2.write(sheet2_row_no, 2, 'Tên Sản Phẩm', header)
        worksheet2.write(sheet2_row_no, 3, 'ĐVT', header)
        worksheet2.write(sheet2_row_no, 4, 'Số Lượng Xuất', header)
        worksheet2.write(sheet2_row_no, 5, 'Doanh Thu (VNĐ)', header)
        worksheet2.write(sheet2_row_no, 6, 'Doanh Thu Dự Kiến (VNĐ)', header)
        worksheet2.write(sheet2_row_no, 7, 'Tổng (DT + DT dự kiến)', header)
        worksheet2.write(sheet2_row_no, 8, 'Doanh Thu theo SO', header)

        list_product_ids = []
        list_sale_order_line_ids = []
        list_move_ids = []
        list_invoice_line_ids = []
        list_invoice_not_finished = []
        domain = [('commitment_date', '>=', data.get('start_date')),
                  ('commitment_date', '<=', data.get('end_date')),
                  ('state', 'not in', ['draft', 'cancel'])]
        line_no = 0
        for order in self.env['sale.order'].search(domain):
            for line_order in order.order_line:
                if line_order.product_id:
                    delivery = False
                    for move_ids in self.env['stock.move'].search(
                            [('sale_line_id', '=', line_order.id), ('state', '=', 'done')]):
                        if len(move_ids) > 0:
                            delivery = True
                    if delivery == True and line_order.qty_delivered <= 0:
                        continue
                    list_sale_order_line_ids.append(line_order)
                    list_product_ids.append(line_order.product_id.id)
                    for move_ids in self.env['stock.move'].search([('sale_line_id', '=', line_order.id)]):
                        list_move_ids.append(move_ids.id)
                    line_no += 1
                    invoice_finished = False
                    inv_qty = 0
                    inv_subtotal = 0
                    inv_total = 0
                    inv_qty_refund = 0
                    inv_subtotal_refund = 0
                    inv_total_refund = 0
                    inv_tax_id = 0
                    inv_price_tax = 0
                    inv_price_tax_refund = 0
                    for invoice_line in self.env['account.invoice.line'].search(
                            [('sale_line_ids', '=', line_order.id),
                             ('invoice_id.state', '!=', 'cancel')]):
                        if invoice_line.invoice_id.sea_invoice_finished:
                            list_invoice_line_ids.append(invoice_line)
                            invoice_finished = True
                            if line_order.id == invoice_line.sale_line_ids.id:
                                inv_tax_id = invoice_line.invoice_line_tax_ids.amount
                                if invoice_line.invoice_id.type == 'out_invoice':
                                    inv_qty += invoice_line.quantity
                                    inv_total += invoice_line.price_total
                                    inv_subtotal += invoice_line.price_subtotal
                                    inv_price_tax += invoice_line.price_tax
                                else:
                                    inv_qty_refund = invoice_line.quantity
                                    inv_total_refund = invoice_line.price_total
                                    inv_subtotal_refund = invoice_line.price_subtotal
                                    inv_price_tax_refund = invoice_line.price_tax
                        # else:
                        #     list_invoice_not_finished.append(invoice_line)
                    inv_tax = (inv_total - inv_total_refund) - (inv_subtotal - inv_subtotal_refund)
                    worksheet1.write(sheet1_row_no, 0, line_no, text_center)
                    if invoice_finished:
                        worksheet1.write(sheet1_row_no, 1, inv_total - inv_total_refund, money)
                        worksheet1.write(sheet1_row_no, 2, inv_subtotal - inv_subtotal_refund, money)
                        worksheet1.write(sheet1_row_no, 3, inv_qty - inv_qty_refund, text_center)
                        worksheet1.write(sheet1_row_no, 4, inv_price_tax - inv_price_tax_refund, money)
                        worksheet1.write(sheet1_row_no, 15, inv_tax_id, text_center)
                    else:
                        worksheet1.write(sheet1_row_no, 1, '', money)
                        worksheet1.write(sheet1_row_no, 2, '', money)
                        worksheet1.write(sheet1_row_no, 3, '', text_center)
                        worksheet1.write(sheet1_row_no, 4, '', money)
                        worksheet1.write(sheet1_row_no, 15, '', text_center)
                    worksheet1.write(sheet1_row_no, 13, line_order.order_id.partner_id.name, text_left)
                    worksheet1.write(sheet1_row_no, 14, line_order.product_id.name, text_left)
                    if invoice_finished:
                        worksheet1.write(sheet1_row_no, 16, inv_tax, money)
                    else:
                        worksheet1.write(sheet1_row_no, 16, '', money)
                    worksheet1.write(sheet1_row_no, 17, 'SO', text_center)
                    worksheet1.write(sheet1_row_no, 18, line_order.order_id.name, text_left)
                    worksheet1.write(sheet1_row_no, 19, line_order.order_id.confirmation_date, short_date)
                    worksheet1.write(sheet1_row_no, 20, line_order.order_id.team_id.name, text_left)
                    worksheet1.write(sheet1_row_no, 21, line_order.product_id.product_tmpl_id.default_code,
                                     text_center)
                    if line_order.product_id.accounting_code:
                        worksheet1.write(sheet1_row_no, 22, line_order.product_id.accounting_code, text_left)
                    else:
                        worksheet1.write(sheet1_row_no, 22, '', text_left)
                    worksheet1.write(sheet1_row_no, 23,
                                     line_order.product_id.product_tmpl_id.categ_id.complete_name,
                                     text_left)
                    if invoice_finished == True and delivery == True:
                        worksheet1.write(sheet1_row_no, 5, '', money)
                        worksheet1.write(sheet1_row_no, 6, '', money)
                        worksheet1.write(sheet1_row_no, 7, '', text_center)
                        worksheet1.write(sheet1_row_no, 8, '', money)
                        worksheet1.write(sheet1_row_no, 9, (inv_total - inv_total_refund), money)
                        worksheet1.write(sheet1_row_no, 10, (inv_subtotal - inv_subtotal_refund), money)
                        worksheet1.write(sheet1_row_no, 11, (inv_qty - inv_qty_refund), text_center)
                        worksheet1.write(sheet1_row_no, 12, (inv_price_tax - inv_price_tax_refund), money)
                    elif invoice_finished == False and delivery == True:
                        list_invoice_not_finished.append(line_order)
                        worksheet1.write(sheet1_row_no, 5, line_order.price_total * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                        worksheet1.write(sheet1_row_no, 6, line_order.price_subtotal * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                        worksheet1.write(sheet1_row_no, 7, line_order.qty_delivered, text_center)
                        worksheet1.write(sheet1_row_no, 8, line_order.price_tax * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                        worksheet1.write(sheet1_row_no, 9, line_order.price_total * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                        worksheet1.write(sheet1_row_no, 10, line_order.price_subtotal * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                        worksheet1.write(sheet1_row_no, 11, line_order.qty_delivered, text_center)
                        worksheet1.write(sheet1_row_no, 12, line_order.price_tax * (
                                line_order.qty_delivered / line_order.product_uom_qty), money)
                    else:
                        worksheet1.write(sheet1_row_no, 5, '', money)
                        worksheet1.write(sheet1_row_no, 6, '', money)
                        worksheet1.write(sheet1_row_no, 7, '', text_center)
                        worksheet1.write(sheet1_row_no, 8, '', money)
                        worksheet1.write(sheet1_row_no, 9, '', money)
                        worksheet1.write(sheet1_row_no, 10, '', money)
                        worksheet1.write(sheet1_row_no, 11, '', text_center)
                        worksheet1.write(sheet1_row_no, 12, '', money)
                    worksheet1.write(sheet1_row_no, 24, line_order.price_total, money)
                    worksheet1.write(sheet1_row_no, 25, line_order.price_subtotal, money)
                    worksheet1.write(sheet1_row_no, 26, line_order.product_uom_qty, text_center)
                    worksheet1.write(sheet1_row_no, 27, line_order.price_tax, money)
                    if line_order.order_id.sea_sale_department and line_order.order_id.sea_sale_channel_id:
                        worksheet1.write(sheet1_row_no, 28,
                                         dict(line_order.order_id._fields['sea_sale_department'].selection).get(
                                             line_order.order_id.sea_sale_department) + ' / ' + line_order.order_id.sea_sale_channel_id.complete_name,
                                         text_left)
                    else:
                        worksheet1.write(sheet1_row_no, 28, '', text_left)
                    if line_order.order_id.partner_shipping_id.state_id:
                        if line_order.order_id.partner_shipping_id.region_name:
                            worksheet1.write(sheet1_row_no, 29, line_order.order_id.partner_shipping_id.region_name,
                                             text_left)
                        else:
                            worksheet1.write(sheet1_row_no, 29, '', text_left)
                    else:
                        worksheet1.write(sheet1_row_no, 29, '', text_left)
                    worksheet1.write(sheet1_row_no, 30, '', no_data)
                    worksheet1.write(sheet1_row_no, 31, '', no_data)
                    sheet1_row_no += 1
        row_no = 0
        for products in self.env['product.product'].browse(set(list_product_ids)):
            row_no += 1
            quantity = 0
            subtotal = 0
            subtotal_so = 0
            subtotal_expected = 0

            for line in list_sale_order_line_ids:
                if line.product_id.id == products.id:
                    quantity += line.qty_delivered
                    subtotal_so += line.price_subtotal
            for inv_line in list_invoice_line_ids:
                if inv_line.product_id.id == products.id:
                    subtotal += inv_line.price_subtotal_signed
            for inv_line_temp in list_invoice_not_finished:
                if inv_line_temp.product_id.id == products.id:
                    subtotal_expected += inv_line_temp.price_subtotal * (
                            inv_line_temp.qty_delivered / inv_line_temp.product_uom_qty)
            worksheet2.write(row_no, 0, row_no, text_center)
            worksheet2.write(row_no, 1, products.default_code, text_left)
            worksheet2.write(row_no, 2, products.name, text_left)
            worksheet2.write(row_no, 3, products.sea_unit_of_measure.name, text_center)
            worksheet2.write(row_no, 4, quantity, text_center)
            worksheet2.write(row_no, 5, subtotal, money)
            worksheet2.write(row_no, 6, subtotal_expected, money)
            worksheet2.write(row_no, 7, subtotal + subtotal_expected, money)
            worksheet2.write(row_no, 8, subtotal_so, money)
            sheet2_row_no += 1

    # def generate_xlsx_report(self, workbook, data, objects):
    #     worksheet1 = workbook.add_worksheet('Báo cáo bán hàng (Commitment Date)')
    #     worksheet2 = workbook.add_worksheet('Báo cáo xuất kho bán hàng')
    #
    #     header = workbook.add_format(
    #         {'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True,
    #          'font_size': 10, 'font_name': 'Tahoma'})
    #
    #     text_center = workbook.add_format(
    #         {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
    #          'font_size': 10})
    #     text_left = workbook.add_format(
    #         {'border': 1, 'align': 'left', 'valign': 'vcenter', 'text_wrap': True, 'font_name': 'Tahoma',
    #          'font_size': 10})
    #
    #     short_date = workbook.add_format(
    #         {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': 'dd/mm/yyyy',
    #          'font_name': 'Tahoma', 'font_size': 10})
    #     money = workbook.add_format({'border': 1, 'align': 'right', 'valign': 'vcenter', 'num_format': '#,##0',
    #                                  'font_size': 10, 'font_name': 'Tahoma'})
    #     no_data = workbook.add_format(
    #         {'border': 1, 'align': 'right', 'valign': 'vcenter', 'font_size': 10, 'font_name': 'Tahoma'})
    #
    #     # Report Header
    #     worksheet1.set_column(0, 0, 5)
    #     worksheet1.set_column(1, 1, 10)
    #     worksheet1.set_column(2, 2, 10)
    #     worksheet1.set_column(3, 3, 10)
    #     worksheet1.set_column(4, 4, 30)
    #     worksheet1.set_column(5, 5, 30)
    #     worksheet1.set_column(6, 6, 8)
    #     worksheet1.set_column(7, 7, 10)
    #     worksheet1.set_column(8, 8, 8)
    #     worksheet1.set_column(9, 9, 15)
    #     worksheet1.set_column(10, 10, 12)
    #     worksheet1.set_column(11, 11, 8)
    #     worksheet1.set_column(12, 12, 10)
    #     worksheet1.set_column(13, 13, 15)
    #     worksheet1.set_column(14, 14, 22)
    #     worksheet1.set_column(15, 15, 12)
    #     worksheet1.set_column(16, 16, 11)
    #     worksheet1.set_column(17, 17, 10)
    #     worksheet1.set_column(18, 18, 11)
    #     worksheet1.set_column(19, 19, 11)
    #     worksheet1.set_column(20, 20, 11)
    #     worksheet1.set_column(21, 21, 11)
    #     worksheet1.freeze_panes(1, 0)
    #
    #     worksheet2.set_column(0, 0, 5)
    #     worksheet2.set_column(1, 1, 15)
    #     worksheet2.set_column(2, 2, 40)
    #     worksheet2.set_column(3, 3, 10)
    #     worksheet2.set_column(4, 4, 10)
    #     worksheet2.set_column(5, 5, 20)
    #     worksheet2.set_column(6, 6, 20)
    #     worksheet2.freeze_panes(1, 0)
    #
    #     sheet1_row_no = 0
    #     sheet1_col_no = 0
    #     sheet2_row_no = 0
    #
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'STT', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh Thu', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'S.Lượng', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Đối Tượng (Ghi chú)', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Diễn giải', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'TS %', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'VAT', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Chứng Từ Đề Xuất', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Chứng Từ', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày Chứng Từ Đề Xuất', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Bộ Phận Đề Xuất', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Sản Phẩm', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Sản Phẩm Kế Toán', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Cây Nhóm Sản Phẩm', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền Dự Kiến', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh Thu/ Chi Phí Dự Kiến', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Thuế GTGT Dự Kiến', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 1', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 2', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 3', header)
    #     sheet1_col_no += 1
    #     worksheet1.write(sheet1_row_no, sheet1_col_no, 'Điều Kiện 4', header)
    #     sheet1_row_no += 1
    #
    #     worksheet2.write(sheet2_row_no, 0, 'STT', header)
    #     worksheet2.write(sheet2_row_no, 1, 'Mã Sản Phẩm', header)
    #     worksheet2.write(sheet2_row_no, 2, 'Tên Sản Phẩm', header)
    #     worksheet2.write(sheet2_row_no, 3, 'ĐVT', header)
    #     worksheet2.write(sheet2_row_no, 4, 'Số Lượng Xuất', header)
    #     worksheet2.write(sheet2_row_no, 5, 'Doanh Thu (VNĐ)', header)
    #     worksheet2.write(sheet2_row_no, 6, 'Doanh Thu Dự Kiến (VNĐ)', header)
    #
    #     list_product_ids = []
    #     list_sale_order_line_ids = []
    #     list_move_ids = []
    #     list_invoice_line_ids = []
    #     list_invoice_not_finished = []
    #     domain = [('company_id', '=', objects.company_id.id),
    #               ('commitment_date', '!=', False),
    #               ('commitment_date', '>=', data.get('start_date')),
    #               ('commitment_date', '<=', data.get('end_date')),
    #               ('state', 'not in', ['draft', 'sent', 'cancel', 'booked'])]
    #     line_no = 0
    #     for order in self.env['sale.order'].search(domain):
    #         for line_order in order.order_line:
    #             if line_order.product_id:
    #                 list_sale_order_line_ids.append(line_order)
    #                 list_product_ids.append(line_order.product_id.id)
    #                 for move_ids in self.env['stock.move'].search([('sale_line_id', '=', line_order.id)]):
    #                     list_move_ids.append(move_ids.id)
    #                 line_no += 1
    #                 invoice_finished = False
    #                 inv_qty = 0
    #                 inv_subtotal = 0
    #                 inv_total = 0
    #                 inv_qty_refund = 0
    #                 inv_subtotal_refund = 0
    #                 inv_total_refund = 0
    #                 inv_tax_id = 0
    #                 for invoice_line in self.env['account.invoice.line'].search([('sale_line_ids', '=', line_order.id),
    #                                                                              ('invoice_id.state', '!=', 'cancel')]):
    #                     if invoice_line.invoice_id.sea_invoice_finished:
    #                         list_invoice_line_ids.append(invoice_line)
    #                         invoice_finished = True
    #                         if line_order.id == invoice_line.sale_line_ids.id:
    #                             inv_tax_id = invoice_line.invoice_line_tax_ids.amount
    #                             if invoice_line.invoice_id.type == 'out_invoice':
    #                                 inv_qty += invoice_line.quantity
    #                                 inv_total += invoice_line.price_total
    #                                 inv_subtotal += invoice_line.price_subtotal
    #                             else:
    #                                 inv_qty_refund = invoice_line.quantity
    #                                 inv_total_refund = invoice_line.price_total
    #                                 inv_subtotal_refund = invoice_line.price_subtotal
    #                     else:
    #                         list_invoice_not_finished.append(invoice_line)
    #                 inv_tax = (inv_total - inv_total_refund) - (inv_subtotal - inv_subtotal_refund)
    #                 worksheet1.write(sheet1_row_no, 0, line_no, text_center)
    #                 if invoice_finished:
    #                     worksheet1.write(sheet1_row_no, 1, inv_total - inv_total_refund, money)
    #                     worksheet1.write(sheet1_row_no, 2, inv_subtotal - inv_subtotal_refund, money)
    #                     worksheet1.write(sheet1_row_no, 3, inv_qty - inv_qty_refund, text_center)
    #                     worksheet1.write(sheet1_row_no, 6, inv_tax_id, text_center)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 1, '', money)
    #                     worksheet1.write(sheet1_row_no, 2, '', money)
    #                     worksheet1.write(sheet1_row_no, 3, '', text_center)
    #                     worksheet1.write(sheet1_row_no, 6, '', text_center)
    #                 worksheet1.write(sheet1_row_no, 4, line_order.order_id.partner_id.name, text_left)
    #                 worksheet1.write(sheet1_row_no, 5, line_order.product_id.name, text_left)
    #                 if invoice_finished:
    #                     worksheet1.write(sheet1_row_no, 7, inv_tax, money)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 7, '', money)
    #                 worksheet1.write(sheet1_row_no, 8, 'SO', text_center)
    #                 worksheet1.write(sheet1_row_no, 9, line_order.order_id.name, text_left)
    #                 worksheet1.write(sheet1_row_no, 10, line_order.order_id.confirmation_date, short_date)
    #                 worksheet1.write(sheet1_row_no, 11, line_order.order_id.team_id.name, text_left)
    #                 worksheet1.write(sheet1_row_no, 12, line_order.product_id.product_tmpl_id.default_code, text_center)
    #                 if line_order.product_id.accounting_code:
    #                     worksheet1.write(sheet1_row_no, 13, line_order.product_id.accounting_code, text_left)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 13, '', text_left)
    #                 worksheet1.write(sheet1_row_no, 14, line_order.product_id.product_tmpl_id.categ_id.complete_name,
    #                                  text_left)
    #                 if invoice_finished:
    #                     worksheet1.write(sheet1_row_no, 15, '', money)
    #                     worksheet1.write(sheet1_row_no, 16, '', money)
    #                     worksheet1.write(sheet1_row_no, 17, '', money)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 15, line_order.price_total, money)
    #                     worksheet1.write(sheet1_row_no, 16, line_order.price_subtotal, money)
    #                     worksheet1.write(sheet1_row_no, 17, line_order.price_tax, money)
    #                 if line_order.order_id.sea_sale_department and line_order.order_id.sea_sale_channel_id:
    #                     worksheet1.write(sheet1_row_no, 18,
    #                                      dict(line_order.order_id._fields['sea_sale_department'].selection).get(
    #                                          line_order.order_id.sea_sale_department) + ' / ' + line_order.order_id.sea_sale_channel_id.complete_name,
    #                                      text_left)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 18, '', text_left)
    #                 if line_order.order_id.partner_shipping_id.state_id:
    #                     if line_order.order_id.partner_shipping_id.region_name:
    #                         worksheet1.write(sheet1_row_no, 19, line_order.order_id.partner_shipping_id.region_name,
    #                                          text_left)
    #                     else:
    #                         worksheet1.write(sheet1_row_no, 19, '', text_left)
    #                 else:
    #                     worksheet1.write(sheet1_row_no, 19, '', text_left)
    #                 worksheet1.write(sheet1_row_no, 20, '', no_data)
    #                 worksheet1.write(sheet1_row_no, 21, '', no_data)
    #                 sheet1_row_no += 1
    #
    #     row_no = 0
    #     for products in self.env['product.product'].browse(set(list_product_ids)):
    #         row_no += 1
    #         quantity = 0
    #         subtotal = 0
    #         subtotal_expected = 0
    #
    #         for line in list_sale_order_line_ids:
    #             if line.product_id.id == products.id:
    #                 quantity += line.qty_delivered
    #         for inv_line in list_invoice_line_ids:
    #             if inv_line.product_id.id == products.id:
    #                 subtotal += inv_line.price_subtotal_signed
    #         for inv_line_temp in list_invoice_not_finished:
    #             if inv_line_temp.product_id.id == products.id:
    #                 subtotal_expected += inv_line_temp.price_subtotal_signed
    #         worksheet2.write(row_no, 0, row_no, text_center)
    #         worksheet2.write(row_no, 1, products.default_code, text_left)
    #         worksheet2.write(row_no, 2, products.name, text_left)
    #         worksheet2.write(row_no, 3, products.sea_unit_of_measure.name, text_center)
    #         worksheet2.write(row_no, 4, quantity, text_center)
    #         worksheet2.write(row_no, 5, subtotal, money)
    #         worksheet2.write(row_no, 6, subtotal_expected, money)
    #         sheet2_row_no += 1
