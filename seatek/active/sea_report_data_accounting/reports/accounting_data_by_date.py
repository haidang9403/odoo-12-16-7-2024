import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AccountingDataByDate(models.AbstractModel):
    _name = 'report.sea_report_data_accounting.accounting_data_by_date'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet1 = workbook.add_worksheet('Báo cáo bán hàng (Accounting Date)')

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

        # Report Header
        worksheet1.set_column(0, 0, 5), worksheet1.set_column(1, 1, 7), worksheet1.set_column(2, 2, 7),
        worksheet1.set_column(3, 3, 7), worksheet1.set_column(4, 4, 7), worksheet1.set_column(5, 5, 7),
        worksheet1.set_column(6, 6, 7), worksheet1.set_column(7, 7, 7), worksheet1.set_column(8, 8, 7),
        worksheet1.set_column(9, 9, 7), worksheet1.set_column(10, 10, 14), worksheet1.set_column(11, 11, 12),
        worksheet1.set_column(12, 12, 8), worksheet1.set_column(13, 13, 50), worksheet1.set_column(14, 14, 40),
        worksheet1.set_column(15, 15, 12), worksheet1.set_column(16, 16, 12), worksheet1.set_column(17, 17, 12),
        worksheet1.set_column(18, 18, 12), worksheet1.set_column(19, 19, 7), worksheet1.set_column(20, 20, 7),
        worksheet1.set_column(21, 21, 7), worksheet1.set_column(22, 22, 7), worksheet1.set_column(23, 23, 7),
        worksheet1.set_column(24, 24, 7), worksheet1.set_column(25, 25, 7), worksheet1.set_column(26, 26, 7),
        worksheet1.set_column(27, 27, 12), worksheet1.set_column(28, 28, 17), worksheet1.set_column(29, 29, 25),
        worksheet1.set_column(30, 30, 18), worksheet1.set_column(31, 31, 20), worksheet1.set_column(32, 32, 20),
        worksheet1.set_column(33, 33, 18), worksheet1.set_column(34, 34, 14), worksheet1.set_column(35, 35, 14),
        worksheet1.set_column(36, 36, 25), worksheet1.set_column(37, 37, 40), worksheet1.set_column(38, 38, 14),
        worksheet1.set_column(39, 39, 10), worksheet1.set_column(40, 40, 7), worksheet1.set_column(41, 41, 7),
        worksheet1.freeze_panes(1, 0)

        sheet1_row_no = 0
        sheet1_col_no = 0

        worksheet1.write(sheet1_row_no, sheet1_col_no, 'STT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'CTGS', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày GS', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Phiếu', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'TK Nợ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'C.Tiết Nợ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Kho Nợ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'TK Có', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'C.Tiết Có', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Kho Có', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Doanh Thu/ Chi Phí', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'S.Lượng', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Đối Tượng (Ghi chú)', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Diễn giải', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ký Hiệu', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số HĐ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày HĐ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Thuế', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'TS %', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Loại', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngoại Tệ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Tỷ Giá', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Nợ/Có', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'TK Ngoài', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Số Tiền Ngoài', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã QL', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'VAT', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Chứng Từ Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Kho', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Chứng Từ', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày Chứng Từ Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Ngày Hoạnh Toán/ Ghi Sổ (Accounting Date)', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Bộ Phận Đề Xuất', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Sản Phẩm', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Mã Sản Phẩm Kế Toán', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Cây Nhóm Sản Phẩm', header)
        sheet1_col_no += 1
        worksheet1.write(sheet1_row_no, sheet1_col_no, 'Nguồn Giao Dịch', header)
        sheet1_row_no += 1

        domain_account = [('company_id', '=', objects.company_id.id),
                          ('move_type', '!=', 'liquidity')]
        domain_account = []
        if data.get('start_date'):
            domain_account.append(('date', '>=', data.get('start_date')))
        if data.get('end_date'):
            domain_account.append(('date', '<=', data.get('end_date')))

        line_no = 0
        for line in self.env['account.move.line'].search(domain_account):
            if line.product_id:
                stock_move = line.move_id.stock_move_id
                if stock_move.picking_id.pos_order_id and line.user_type_id.id == 5 \
                        or stock_move.sale_line_id and line.user_type_id.id == 5\
                        or stock_move.purchase_line_id and line.user_type_id.id == 5\
                        or line.invoice_id and line.user_type_id.id == 14\
                        or line.invoice_id and line.user_type_id.id == 9\
                        or stock_move.location_dest_id.usage == 'inventory' and line.user_type_id.id == 16\
                        or stock_move.location_id.usage == 'inventory' and line.user_type_id.id == 16 \
                        or stock_move.location_dest_id.usage == 'inventory' and line.account_id.id == 206 and line.user_type_id.id == 5 \
                        or stock_move.location_id.usage == 'inventory' and line.user_type_id.id == 9:
                    line_no += 1
                    worksheet1.write(line_no, 0, line_no, text_center)
                    worksheet1.write(line_no, 1, '', text_center)
                    worksheet1.write(line_no, 2, '', text_center)
                    worksheet1.write(line_no, 3, '', text_center)
                    worksheet1.write(line_no, 4, '', text_center)
                    worksheet1.write(line_no, 5, '', text_center)
                    worksheet1.write(line_no, 6, '', text_center)
                    worksheet1.write(line_no, 7, '', text_center)
                    worksheet1.write(line_no, 8, '', text_center)
                    worksheet1.write(line_no, 9, '', text_center)
                    worksheet1.write(line_no, 10, '', text_center)
                    worksheet1.write(line_no, 13, line.partner_id.name, text_left)
                    worksheet1.write(line_no, 14, line.product_id.name, text_left)
                    if line.invoice_id.symbol_invoice:
                        worksheet1.write(line_no, 15, line.invoice_id.symbol_invoice, text_center)
                    else:
                        worksheet1.write(line_no, 15, '', text_center)
                    if line.invoice_id.supplier_invoice_number:
                        worksheet1.write(line_no, 16, line.invoice_id.supplier_invoice_number, text_center)
                    else:
                        worksheet1.write(line_no, 16, '', text_center)
                    if line.invoice_id.supplier_invoice_date:
                        worksheet1.write(line_no, 17, line.invoice_id.supplier_invoice_date, short_date)
                    else:
                        worksheet1.write(line_no, 17, '', text_center)
                    if line.invoice_id.supplier_vat:
                        worksheet1.write(line_no, 18, line.invoice_id.supplier_vat, text_center)
                    else:
                        worksheet1.write(line_no, 18, '', text_center)
                    worksheet1.write(line_no, 19, '', text_center)
                    worksheet1.write(line_no, 20, '', text_center)
                    worksheet1.write(line_no, 21, '', text_center)
                    worksheet1.write(line_no, 22, '', text_center)
                    worksheet1.write(line_no, 23, '', text_center)
                    worksheet1.write(line_no, 24, '', text_center)
                    worksheet1.write(line_no, 25, '', text_center)
                    worksheet1.write(line_no, 26, '', text_center)
                    worksheet1.write(line_no, 27, '', text_center)

                    if line.move_id.stock_move_id:
                        move = line.move_id.stock_move_id
                        if move.sale_line_id:
                            if line.product_id.id == move.product_id.id:
                                worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                                worksheet1.write(line_no, 12, move.product_qty, text_center)
                                worksheet1.write(line_no, 28, 'SO', text_center)
                                location = ''
                                for move_line in move.move_line_ids:
                                    if line.product_id.id == move_line.product_id.id:
                                        if move.picking_id.location_id.usage == 'customer':
                                            location += move_line.location_dest_id.name + ', '
                                        else:
                                            location += move_line.location_id.name + ', '
                                worksheet1.write(line_no, 29, location[:-2], text_center)
                                worksheet1.write(line_no, 30, move.origin, text_left)
                                worksheet1.write(line_no, 31, move.date, short_date)
                                worksheet1.write(line_no, 32, line.date, short_date)
                                worksheet1.write(line_no, 33, move.sale_line_id.order_id.team_id.name, text_center)
                                worksheet1.write(line_no, 34, move.product_id.default_code, text_center)
                                if move.picking_id.location_id.usage == 'customer':
                                    worksheet1.write(line_no, 37, 'Khách trả hàng theo sales Order', text_left)
                                else:
                                    worksheet1.write(line_no, 37, 'Xuất bán theo Sales Order', text_left)
                        if move.picking_id.pos_order_id:
                            worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                            worksheet1.write(line_no, 12, move.product_qty, text_center)
                            worksheet1.write(line_no, 28, 'POS', text_center)
                            location = ''
                            for move_line in move.move_line_ids:
                                if line.product_id.id == move_line.product_id.id:
                                    if move.picking_id.location_id.usage == 'customer':
                                        location += move_line.location_dest_id.name + ', '
                                    else:
                                        location += move_line.location_id.name + ', '
                            worksheet1.write(line_no, 29, location[:-2], text_center)
                            worksheet1.write(line_no, 30, move.picking_id.origin, text_left)
                            worksheet1.write(line_no, 31, move.date, short_date)
                            worksheet1.write(line_no, 32, line.date, short_date)
                            worksheet1.write(line_no, 33, move.picking_id.create_uid.name, text_center)
                            if move.picking_id.location_id.usage == 'customer':
                                worksheet1.write(line_no, 37, 'Khách trả hàng theo POS', text_left)
                            else:
                                worksheet1.write(line_no, 37, 'Xuất bán theo POS', text_left)
                        if move.purchase_line_id:
                            if move.picking_id.location_id.usage == 'supplier':
                                worksheet1.write(line_no, 11, move.purchase_line_id.price_subtotal, money)
                            else:
                                worksheet1.write(line_no, 11, -move.purchase_line_id.price_unit * move.product_qty,
                                                 money)
                            worksheet1.write(line_no, 12, move.product_qty, text_center)
                            worksheet1.write(line_no, 28, 'PO', text_center)
                            location = ''
                            for move_line in move.move_line_ids:
                                if line.product_id.id == move_line.product_id.id:
                                    if move.picking_id.location_id.usage == 'supplier':
                                        location += move_line.location_dest_id.name + ', '
                                    else:
                                        location += move_line.location_id.name + ', '
                            worksheet1.write(line_no, 29, location[:-2], text_center)
                            worksheet1.write(line_no, 30, move.origin, text_left)
                            worksheet1.write(line_no, 31, move.date, short_date)
                            worksheet1.write(line_no, 32, line.date, short_date)
                            worksheet1.write(line_no, 33, move.purchase_line_id.order_id.user_id.name, text_center)
                            if move.picking_id.location_id.usage == 'supplier':
                                worksheet1.write(line_no, 37, 'Nhập kho từ PO', text_left)
                            else:
                                worksheet1.write(line_no, 37, 'Trả hàng từ PO', text_left)

                        if move.location_id.usage == 'internal' and move.location_dest_id.usage == 'inventory':
                            if move.inventory_id:
                                worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                                worksheet1.write(line_no, 12, move.product_qty, text_center)
                                worksheet1.write(line_no, 13, '', text_left)
                                worksheet1.write(line_no, 28, 'Kiểm kê', text_center)
                                worksheet1.write(line_no, 29, move.inventory_id.location_id.name, text_center)
                                worksheet1.write(line_no, 30, move.inventory_id.name, text_left)
                                worksheet1.write(line_no, 31, move.date, short_date)
                                worksheet1.write(line_no, 32, line.date, short_date)
                                worksheet1.write(line_no, 33, move.create_uid.name, text_center)
                                worksheet1.write(line_no, 37, 'Kiểm kê thiếu', text_left)
                            else:
                                worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                                worksheet1.write(line_no, 12, move.product_qty, text_center)
                                worksheet1.write(line_no, 13, '', text_left)
                                worksheet1.write(line_no, 28, 'Kho chi phí', text_center)
                                worksheet1.write(line_no, 29, move.location_id.name, text_center)
                                worksheet1.write(line_no, 30, move.picking_id.name, text_left)
                                worksheet1.write(line_no, 31, move.date, short_date)
                                worksheet1.write(line_no, 32, line.date, short_date)
                                # worksheet1.write(line_no, 32, move.picking_id.date_done, short_date)
                                worksheet1.write(line_no, 33, move.create_uid.name, text_center)
                                worksheet1.write(line_no, 37, 'Xuất đến kho chi phí', text_left)
                        if move.location_id.usage == 'inventory' and move.location_dest_id.usage == 'internal':
                            if move.inventory_id:
                                worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                                worksheet1.write(line_no, 12, move.product_qty, text_center)
                                worksheet1.write(line_no, 13, '', text_left)
                                worksheet1.write(line_no, 28, 'Kiểm kê', text_center)
                                worksheet1.write(line_no, 29, move.inventory_id.location_id.name, text_center)
                                worksheet1.write(line_no, 30, move.inventory_id.name, text_left)
                                worksheet1.write(line_no, 31, move.date, short_date)
                                worksheet1.write(line_no, 32, line.date, short_date)
                                worksheet1.write(line_no, 33, move.create_uid.name, text_center)
                                worksheet1.write(line_no, 37, 'Kiểm kê thừa', text_left)
                            else:
                                worksheet1.write(line_no, 11, move.price_unit * move.product_qty, money)
                                worksheet1.write(line_no, 12, move.product_qty, text_center)
                                worksheet1.write(line_no, 13, '', text_left)
                                worksheet1.write(line_no, 28, 'Kho chi phí', text_center)
                                worksheet1.write(line_no, 29, move.location_dest_id.name, text_center)
                                worksheet1.write(line_no, 30, move.picking_id.name, text_left)
                                worksheet1.write(line_no, 31, move.date, short_date)
                                worksheet1.write(line_no, 32, line.date, short_date)
                                worksheet1.write(line_no, 33, move.create_uid.name, text_center)
                                worksheet1.write(line_no, 37, 'Trả lại từ kho chi phí', text_left)

                    if line.invoice_id:
                        invoice = line.invoice_id
                        for invoice_line in invoice.invoice_line_ids:
                            if invoice_line.invoice_id.invoice_consolidation_id:
                                worksheet1.write(line_no, 15, invoice.invoice_consolidation_id.symbol_code, text_center)
                                worksheet1.write(line_no, 16, invoice.invoice_consolidation_id.legal_number, text_center)
                                worksheet1.write(line_no, 17, invoice.invoice_consolidation_id.invoice_issued_date, short_date)
                            if not invoice_line.pos_line_id and not invoice_line.purchase_line_id:
                                if line.product_id.id == invoice_line.product_id.id:
                                    # print(invoice.invoice_consolidation_id.invoice_issued_date)
                                    worksheet1.write(line_no, 11, invoice_line.price_subtotal_signed, money)
                                    worksheet1.write(line_no, 12, invoice_line.quantity, text_center)
                                    worksheet1.write(line_no, 19, invoice_line.invoice_line_tax_ids.amount, text_center)
                                    worksheet1.write(line_no, 28, 'SO', text_center)
                                    worksheet1.write(line_no, 29, '', text_center)
                                    worksheet1.write(line_no, 30, invoice_line.origin, text_left)
                                    worksheet1.write(line_no, 31, invoice_line.invoice_id.date_invoice, short_date)
                                    worksheet1.write(line_no, 32, invoice_line.invoice_id.move_id.date, short_date)
                                    worksheet1.write(line_no, 33, invoice_line.invoice_id.team_id.name, text_center)
                                    if invoice_line.invoice_id.type == 'out_invoice':
                                        worksheet1.write(line_no, 27, invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed + invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Hóa đơn công nợ phải thu của Sale Order',
                                                         text_left)

                                    else:
                                        worksheet1.write(line_no, 27, -invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed - invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Giảm trừ công nợ phải thu của Sales Order',
                                                         text_left)
                            if invoice_line.pos_line_id:
                                if line.product_id.id == invoice_line.product_id.id:
                                    worksheet1.write(line_no, 11, invoice_line.price_subtotal_signed, money)
                                    worksheet1.write(line_no, 12, invoice_line.quantity, text_center)
                                    worksheet1.write(line_no, 19, invoice_line.invoice_line_tax_ids.amount, text_center)
                                    worksheet1.write(line_no, 28, 'POS', text_center)
                                    worksheet1.write(line_no, 29, '', text_center)
                                    worksheet1.write(line_no, 30, invoice_line.invoice_id.origin, text_left)
                                    worksheet1.write(line_no, 31, invoice_line.invoice_id.date_invoice, short_date)
                                    worksheet1.write(line_no, 32, invoice_line.invoice_id.move_id.date, short_date)
                                    worksheet1.write(line_no, 33, invoice_line.invoice_id.team_id.name, text_center)
                                    if invoice_line.invoice_id.type == 'out_invoice':
                                        worksheet1.write(line_no, 27, invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed + invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Hóa đơn công nợ phải thu của POS', text_left)
                                    else:
                                        worksheet1.write(line_no, 27, -invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed - invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Giảm trừ công nợ phải thu của POS', text_left)
                            if invoice_line.purchase_line_id:
                                if line.product_id.id == invoice_line.product_id.id:
                                    worksheet1.write(line_no, 11, invoice_line.price_subtotal_signed, money)
                                    worksheet1.write(line_no, 12, invoice_line.quantity, text_center)
                                    worksheet1.write(line_no, 19, invoice_line.invoice_line_tax_ids.amount, text_center)
                                    worksheet1.write(line_no, 28, 'PO', text_center)
                                    worksheet1.write(line_no, 29, '', text_center)
                                    worksheet1.write(line_no, 30, invoice_line.purchase_line_id.order_id.name, text_left)
                                    worksheet1.write(line_no, 31, invoice_line.invoice_id.date_invoice, short_date)
                                    worksheet1.write(line_no, 32, invoice_line.invoice_id.move_id.date, short_date)
                                    worksheet1.write(line_no, 33, invoice_line.invoice_id.team_id.name, text_center)
                                    if invoice_line.invoice_id.type == 'in_invoice':
                                        worksheet1.write(line_no, 27, invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed + invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Hóa đơn phải trả', text_left)
                                    else:
                                        worksheet1.write(line_no, 27, -invoice_line.price_tax, money)
                                        worksheet1.write(line_no, 10,
                                                         invoice_line.price_subtotal_signed - invoice_line.price_tax,
                                                         money)
                                        worksheet1.write(line_no, 37, 'Giảm trừ công nợ phải trả', text_left)

                    worksheet1.write(line_no, 34, line.product_id.default_code, text_center)
                    if line.product_id.accounting_code:
                        worksheet1.write(line_no, 35, line.product_id.accounting_code, text_center)
                    else:
                        worksheet1.write(line_no, 35, '', text_center)
                    worksheet1.write(line_no, 36, line.product_id.product_tmpl_id.categ_id.complete_name, text_left)

                # print(line.ref)
                # print(line.product_id.name)
                # if line:
                #     print(line.ref)
                #     print(line.product_id.name)
                #     for move in self.env['stock.move.line'].search([('reference', '=', line.ref),
                #                                                     ('product_id', '=', line.product_id.id)]):
                #         print(move)
                #         print(move.move_id.picking_id.origin)
                #         print(move.move_id.picking_id.name)
                #     print('-----------------')
        # # Get account_move list
        # domain_account = [('company_id', '=', objects.company_id.id),
        #                   ('move_type', '!=', 'liquidity')]
        # if data.get('start_date'):
        #     domain_account.append(('date', '>=', data.get('start_date')))
        # if data.get('end_date'):
        #     domain_account.append(('date', '<=', data.get('end_date')))
        #
        # line_no = 0
        # for account in self.env['account.move'].search(domain_account):
        #     if account.move_type == 'receivable' or account.move_type == 'receivable_refund' \
        #             or account.move_type == 'payable' or account.move_type == 'payable_refund':
        #         for line in self.env['account.invoice'].search([('move_id', '=', account.name)]).invoice_line_ids:
        #             line_no += 1
        #             worksheet1.write(line_no, 0, line_no, text_center)
        #             worksheet1.write(line_no, 1, '', text_center)
        #             worksheet1.write(line_no, 2, '', text_center)
        #             worksheet1.write(line_no, 3, '', text_center)
        #             worksheet1.write(line_no, 4, '', text_center)
        #             worksheet1.write(line_no, 5, '', text_center)
        #             worksheet1.write(line_no, 6, '', text_center)
        #             worksheet1.write(line_no, 7, '', text_center)
        #             worksheet1.write(line_no, 8, '', text_center)
        #             worksheet1.write(line_no, 9, '', text_center)
        #             if line.invoice_id.type == 'out_refund' or line.invoice_id.type == 'in_refund':
        #                 if line.purchase_line_id:
        #                     worksheet1.write(line_no, 10, -line.price_total, money)
        #                     worksheet1.write(line_no, 11, -line.price_subtotal, money)
        #                     worksheet1.write(line_no, 12, -line.quantity, text_center)
        #                 else:
        #                     worksheet1.write(line_no, 10, '', money)
        #                     worksheet1.write(line_no, 11, line.quantity * line.move_line_ids.price_unit, money)
        #                     worksheet1.write(line_no, 12, line.quantity, text_center)
        #             else:
        #                 if line.purchase_line_id:
        #                     worksheet1.write(line_no, 10, line.price_total, money)
        #                     worksheet1.write(line_no, 11, line.price_subtotal, money)
        #                     worksheet1.write(line_no, 12, line.quantity, text_center)
        #                 else:
        #                     worksheet1.write(line_no, 10, '', money)
        #                     if line.pos_line_id:
        #                         picking_ids = self.env['stock.picking'].search([('pos_order_id', '=', line.pos_line_id.order_id.id)])
        #                         for move_pos in self.env['stock.move'].search([('picking_id', '=', picking_ids.id)]):
        #                             if line.product_id.id == move_pos.product_id.id:
        #                                 worksheet1.write(line_no, 11, line.quantity * move_pos.price_unit, money)
        #                     else:
        #                         worksheet1.write(line_no, 11, line.quantity * line.move_line_ids.price_unit, money)
        #                     worksheet1.write(line_no, 12, -line.quantity, text_center)
        #             worksheet1.write(line_no, 13, line.invoice_id.partner_id.name, text_left)
        #             worksheet1.write(line_no, 14, line.product_id.name, text_left)
        #             if line.invoice_id.symbol_invoice:
        #                 worksheet1.write(line_no, 15, line.invoice_id.symbol_invoice, text_center)
        #             else:
        #                 worksheet1.write(line_no, 15, '', text_center)
        #             if line.invoice_id.supplier_invoice_number:
        #                 worksheet1.write(line_no, 16, line.invoice_id.supplier_invoice_number, text_center)
        #             else:
        #                 worksheet1.write(line_no, 16, '', text_center)
        #             if line.invoice_id.supplier_invoice_date:
        #                 worksheet1.write(line_no, 17, line.invoice_id.supplier_invoice_date, short_date)
        #             else:
        #                 worksheet1.write(line_no, 17, '', text_center)
        #             if line.invoice_id.supplier_vat:
        #                 worksheet1.write(line_no, 18, line.invoice_id.supplier_vat, text_center)
        #             else:
        #                 worksheet1.write(line_no, 18, '', text_center)
        #             if line.purchase_line_id:
        #                 worksheet1.write(line_no, 19, line.invoice_line_tax_ids.amount, text_center)
        #             else:
        #                 worksheet1.write(line_no, 19, '', text_center)
        #             worksheet1.write(line_no, 20, '', text_center)
        #             worksheet1.write(line_no, 21, '', text_center)
        #             worksheet1.write(line_no, 22, '', text_center)
        #             worksheet1.write(line_no, 23, '', text_center)
        #             worksheet1.write(line_no, 24, '', text_center)
        #             worksheet1.write(line_no, 25, '', text_center)
        #             worksheet1.write(line_no, 26, '', text_center)
        #             if line.purchase_line_id:
        #                 if line.invoice_id.type == 'out_refund' or line.invoice_id.type == 'in_refund':
        #                     worksheet1.write(line_no, 27, -(line.price_total - line.price_subtotal), money)
        #                 else:
        #                     worksheet1.write(line_no, 27, (line.price_total - line.price_subtotal), money)
        #             else:
        #                 worksheet1.write(line_no, 27, '', money)
        #             if line.pos_line_id:
        #                 worksheet1.write(line_no, 28, 'POS', text_center)
        #                 worksheet1.write(line_no, 29, line.pos_line_id.order_id.location_id.name, text_center)
        #             elif line.purchase_line_id:
        #                 worksheet1.write(line_no, 28, 'PO', text_center)
        #                 for i in line.purchase_line_id.move_ids:
        #                     if i.location_dest_id.usage == 'internal':
        #                         worksheet1.write(line_no, 29, i.location_dest_id.name,
        #                                          text_center)
        #             else:
        #                 worksheet1.write(line_no, 28, 'SO', text_center)
        #                 if line.invoice_id.type == 'out_refund':
        #                     worksheet1.write(line_no, 29, line.move_line_ids.move_line_ids.location_dest_id.name, text_center)
        #                 else:
        #                     worksheet1.write(line_no, 29, line.move_line_ids.move_line_ids.location_id.name, text_center)
        #             worksheet1.write(line_no, 30, line.invoice_id.origin, text_left)
        #             worksheet1.write(line_no, 31, line.invoice_id.date_invoice, short_date)
        #             worksheet1.write(line_no, 32, line.invoice_id.team_id.name, text_left)
        #             worksheet1.write(line_no, 33, line.product_id.default_code, text_center)
        #             if line.product_id.accounting_code:
        #                 worksheet1.write(line_no, 34, line.product_id.accounting_code, text_center)
        #             else:
        #                 worksheet1.write(line_no, 34, '', text_center)
        #             worksheet1.write(line_no, 35, line.product_id.product_tmpl_id.categ_id.complete_name, text_left)
        #     else:
        #         for line in account.stock_move_id.move_line_ids:
        #             if line.location_dest_id.usage == 'inventory' or line.location_id.usage == 'inventory':
        #                 line_no += 1
        #                 worksheet1.write(line_no, 0, line_no, text_center)
        #                 worksheet1.write(line_no, 1, '', text_center)
        #                 worksheet1.write(line_no, 2, '', text_center)
        #                 worksheet1.write(line_no, 3, '', text_center)
        #                 worksheet1.write(line_no, 4, '', text_center)
        #                 worksheet1.write(line_no, 5, '', text_center)
        #                 worksheet1.write(line_no, 6, '', text_center)
        #                 worksheet1.write(line_no, 7, '', text_center)
        #                 worksheet1.write(line_no, 8, '', text_center)
        #                 worksheet1.write(line_no, 9, '', text_center)
        #                 worksheet1.write(line_no, 10, '', money)
        #                 worksheet1.write(line_no, 11, line.qty_done * line.move_id.price_unit, money)
        #                 if line.location_dest_id.usage == 'inventory':
        #                     worksheet1.write(line_no, 12, -line.qty_done, text_center)
        #                 elif line.location_id.usage == 'inventory':
        #                     worksheet1.write(line_no, 12, line.qty_done, text_center)
        #                 else:
        #                     worksheet1.write(line_no, 12, line.qty_done, text_center)
        #                 worksheet1.write(line_no, 13, '', text_left)
        #                 worksheet1.write(line_no, 14, line.product_id.name, text_left)
        #                 worksheet1.write(line_no, 15, '', text_center)
        #                 worksheet1.write(line_no, 16, '', text_center)
        #                 worksheet1.write(line_no, 17, '', text_center)
        #                 worksheet1.write(line_no, 18, '', text_center)
        #                 worksheet1.write(line_no, 19, '', text_center)
        #                 worksheet1.write(line_no, 20, '', text_center)
        #                 worksheet1.write(line_no, 21, '', text_center)
        #                 worksheet1.write(line_no, 22, '', text_center)
        #                 worksheet1.write(line_no, 23, '', text_center)
        #                 worksheet1.write(line_no, 24, '', text_center)
        #                 worksheet1.write(line_no, 25, '', text_center)
        #                 worksheet1.write(line_no, 26, '', text_center)
        #                 worksheet1.write(line_no, 27, '', money)
        #                 if line.location_dest_id.usage == 'inventory':
        #                     worksheet1.write(line_no, 29, line.location_id.name, text_center)
        #                 elif line.location_id.usage == 'inventory':
        #                     worksheet1.write(line_no, 29, line.location_dest_id.name, text_center)
        #                 if line.move_id.inventory_id:
        #                     worksheet1.write(line_no, 28, 'Kiểm kê', text_center)
        #                     worksheet1.write(line_no, 30, line.move_id.inventory_id.name, text_left)
        #                     worksheet1.write(line_no, 31, line.move_id.inventory_id.date, short_date)
        #                 else:
        #                     worksheet1.write(line_no, 28, 'Xuất chi phí', text_center)
        #                     worksheet1.write(line_no, 30, line.picking_id.name, text_left)
        #                     worksheet1.write(line_no, 31, line.picking_id.date_done, short_date)
        #                 worksheet1.write(line_no, 32, line.write_uid.name, text_left)
        #                 worksheet1.write(line_no, 33, line.product_id.default_code, text_center)
        #                 if line.product_id.accounting_code:
        #                     worksheet1.write(line_no, 34, line.product_id.accounting_code, text_center)
        #                 else:
        #                     worksheet1.write(line_no, 34, '', text_center)
        #                 worksheet1.write(line_no, 35, line.product_id.product_tmpl_id.categ_id.complete_name,
        #                                  tex
