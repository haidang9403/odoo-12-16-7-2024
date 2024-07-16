import logging
from odoo import models

_logger = logging.getLogger(__name__)


class AccountingReportXLS(models.AbstractModel):
    _name = 'report.sea_accounting_report.accounting_report_by_date'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        worksheet2 = workbook.add_worksheet('Báo cáo bán hàng')
        worksheet3 = workbook.add_worksheet('Báo cáo xuất kho bán hàng')

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
        worksheet2.set_column(0, 0, 5), worksheet2.set_column(1, 1, 7), worksheet2.set_column(2, 2, 7),
        worksheet2.set_column(3, 3, 7), worksheet2.set_column(4, 4, 7), worksheet2.set_column(5, 5, 7),
        worksheet2.set_column(6, 6, 7), worksheet2.set_column(7, 7, 7), worksheet2.set_column(8, 8, 7),
        worksheet2.set_column(9, 9, 7), worksheet2.set_column(10, 10, 14), worksheet2.set_column(11, 11, 12),
        worksheet2.set_column(12, 12, 8), worksheet2.set_column(13, 13, 60), worksheet2.set_column(14, 14, 30),
        worksheet2.set_column(15, 15, 7), worksheet2.set_column(16, 16, 7), worksheet2.set_column(17, 17, 7),
        worksheet2.set_column(18, 18, 7), worksheet2.set_column(19, 19, 7), worksheet2.set_column(20, 20, 7),
        worksheet2.set_column(21, 21, 7), worksheet2.set_column(22, 22, 7), worksheet2.set_column(23, 23, 7),
        worksheet2.set_column(24, 24, 7), worksheet2.set_column(25, 25, 7), worksheet2.set_column(26, 26, 7),
        worksheet2.set_column(27, 27, 12), worksheet2.set_column(28, 28, 7), worksheet2.set_column(29, 29, 16),
        worksheet2.set_column(30, 30, 14), worksheet2.set_column(31, 31, 20), worksheet2.set_column(32, 32, 10),
        worksheet2.set_column(33, 33, 18), worksheet2.set_column(34, 34, 40), worksheet2.set_column(35, 35, 14),
        worksheet2.set_column(36, 36, 12), worksheet2.set_column(37, 37, 15), worksheet2.set_column(38, 38, 14),
        worksheet2.set_column(39, 39, 10), worksheet2.set_column(40, 40, 7), worksheet2.set_column(41, 41, 7),
        worksheet2.freeze_panes(1, 0)

        worksheet3.set_column(0, 0, 5)
        worksheet3.set_column(1, 1, 15)
        worksheet3.set_column(2, 2, 40)
        worksheet3.set_column(3, 3, 10)
        worksheet3.set_column(4, 4, 10)
        worksheet3.set_column(5, 5, 20)
        worksheet3.freeze_panes(1, 0)

        sheet2_row_no = 0
        sheet3_row_no = 0

        worksheet2.write(sheet2_row_no, 0, 'STT', header)
        worksheet2.write(sheet2_row_no, 1, 'CTGS', header)
        worksheet2.write(sheet2_row_no, 2, 'Ngày GS', header)
        worksheet2.write(sheet2_row_no, 3, 'Số Phiếu', header)
        worksheet2.write(sheet2_row_no, 4, 'TK Nợ', header)
        worksheet2.write(sheet2_row_no, 5, 'C.Tiết Nợ', header)
        worksheet2.write(sheet2_row_no, 6, 'Kho Nợ', header)
        worksheet2.write(sheet2_row_no, 7, 'TK Có', header)
        worksheet2.write(sheet2_row_no, 8, 'C.Tiết Có', header)
        worksheet2.write(sheet2_row_no, 9, 'Kho Có', header)
        worksheet2.write(sheet2_row_no, 10, 'Số Tiền', header)
        worksheet2.write(sheet2_row_no, 11, 'Doanh Thu', header)
        worksheet2.write(sheet2_row_no, 12, 'S.Lượng', header)
        worksheet2.write(sheet2_row_no, 13, 'Đối Tượng (Ghi chú)', header)
        worksheet2.write(sheet2_row_no, 14, 'Diễn giải', header)
        worksheet2.write(sheet2_row_no, 15, 'Ký Hiệu', header)
        worksheet2.write(sheet2_row_no, 16, 'Số HĐ', header)
        worksheet2.write(sheet2_row_no, 17, 'Ngày HĐ', header)
        worksheet2.write(sheet2_row_no, 18, 'Mã Thuế', header)
        worksheet2.write(sheet2_row_no, 19, 'TS %', header)
        worksheet2.write(sheet2_row_no, 20, 'Loại', header)
        worksheet2.write(sheet2_row_no, 21, 'Ngoại Tệ', header)
        worksheet2.write(sheet2_row_no, 22, 'Tỷ Giá', header)
        worksheet2.write(sheet2_row_no, 23, 'Nợ/Có', header)
        worksheet2.write(sheet2_row_no, 24, 'TK Ngoài', header)
        worksheet2.write(sheet2_row_no, 25, 'Số Tiền Ngoài', header)
        worksheet2.write(sheet2_row_no, 26, 'Mã QL', header)
        worksheet2.write(sheet2_row_no, 27, 'VAT', header)
        worksheet2.write(sheet2_row_no, 28, 'Chứng Từ Đề Xuất', header)
        worksheet2.write(sheet2_row_no, 29, 'Mã Chứng Từ', header)
        worksheet2.write(sheet2_row_no, 30, 'Ngày Chứng Từ Đề Xuất', header)
        worksheet2.write(sheet2_row_no, 31, 'Bộ Phận Đề Xuất', header)
        worksheet2.write(sheet2_row_no, 32, 'Mã Sản Phẩm', header)
        worksheet2.write(sheet2_row_no, 33, 'Mã Sản Phẩm Kế Toán', header)
        worksheet2.write(sheet2_row_no, 34, 'Cây Nhóm Sản Phẩm', header)
        worksheet2.write(sheet2_row_no, 35, 'Số Tiền Dự Kiến', header)
        worksheet2.write(sheet2_row_no, 36, 'Doanh Thu/ Chi Phí Dự Kiến', header)
        worksheet2.write(sheet2_row_no, 37, 'Thuế GTGT Dự Kiến', header)
        worksheet2.write(sheet2_row_no, 38, 'Điều Kiện 1', header)
        worksheet2.write(sheet2_row_no, 39, 'Điều Kiện 2', header)
        worksheet2.write(sheet2_row_no, 40, 'Điều Kiện 3', header)
        worksheet2.write(sheet2_row_no, 41, 'Điều Kiện 4', header)
        sheet2_row_no += 1

        worksheet3.write(sheet3_row_no, 0, 'STT', header)
        worksheet3.write(sheet3_row_no, 1, 'Mã Sản Phẩm', header)
        worksheet3.write(sheet3_row_no, 2, 'Tên Sản Phẩm', header)
        worksheet3.write(sheet3_row_no, 3, 'ĐVT', header)
        worksheet3.write(sheet3_row_no, 4, 'Số Lượng Xuất', header)
        worksheet3.write(sheet3_row_no, 5, 'Doanh Thu (VNĐ)', header)

        domain_sale = []
        domain_pos = []
        domain_invoice = []
        domain_picking_out = []
        domain_picking_in = []

        # GET DOMAIN FOR SALE.ORDER WITH COMMITMENT DATE
        if data.get('start_date'):
            if objects.type == 'by_commitment':
                domain_sale.append(('commitment_date', '>=', data.get('start_date')))
                domain_sale.append(('state', 'not in', ['draft', 'sent', 'cancel', 'booked']))
        if data.get('end_date'):
            if objects.type == 'by_commitment':
                domain_sale.append(('commitment_date', '<=', data.get('end_date')))

        # GET DOMAIN FOR ACCOUNT.INVOICE WITH DATE INVOICE
        if data.get('start_date'):
            if objects.type == 'by_invoice':
                domain_invoice.append(('date_invoice', '>=', data.get('start_date')))
                domain_invoice.append(('state', 'not in', ['draft', 'cancel']))
        if data.get('end_date'):
            if objects.type == 'by_invoice':
                domain_invoice.append(('date_invoice', '<=', data.get('end_date')))

        # GET DOMAIN FOR POS
        if data.get('start_date'):
            domain_pos.append(('date_order', '>=', data.get('start_date')))
        if data.get('end_date'):
            domain_pos.append(('date_order', '<=', data.get('end_date')))

        # GET DOMAIN FOR STOCK.PICKING EXPORT
        if data.get('start_date'):
            domain_picking_out.append(('date_done', '>=', data.get('start_date')))
            domain_picking_out.append(('location_dest_id.usage', '=', 'inventory'))
            domain_picking_out.append(('location_id.usage', 'in', ['view', 'internal']))
            domain_picking_out.append(('state', '=', 'done'))
        if data.get('end_date'):
            domain_picking_out.append(('date_done', '<=', data.get('end_date')))

        # GET DOMAIN FOR STOCK.PICKING IMPORT
        if data.get('start_date'):
            domain_picking_in.append(('date_done', '>=', data.get('start_date')))
            domain_picking_in.append(('location_id.usage', '=', 'inventory'))
            domain_picking_in.append(('location_dest_id.usage', 'in', ['view', 'internal']))
            domain_picking_in.append(('state', '=', 'done'))
        if data.get('end_date'):
            domain_picking_in.append(('date_done', '<=', data.get('end_date')))

        # GET LIST MODEL
        list_sale_order = self.env['sale.order'].search(domain_sale)
        list_invoices = self.env['account.invoice'].search(domain_invoice)
        list_pos_order = self.env['pos.order'].search(domain_pos)
        list_picking_out = self.env['stock.picking'].search(domain_picking_out)
        list_picking_in = self.env['stock.picking'].search(domain_picking_in)

        order_line_no = 0
        list_product_ids = []
        list_invoice_ids = []
        list_order_sale_to_invoice = []
        if objects.type == 'by_commitment':
            for order in list_sale_order:
                search_invoice = self.env['account.invoice'].search([('origin', '=', order.name),
                                                                     ('state', 'not in', ['draft', 'cancel'])])
                for line in order.order_line:
                    if line.product_id:
                        if line.qty_invoiced > 0:
                            list_order_sale_to_invoice.append(order.name)
                        list_product_ids.append(line.product_id.id)
                        order_line_no += 1
                        worksheet2.write(sheet2_row_no, 0, order_line_no, text_center)
                        worksheet2.write(sheet2_row_no, 1, '', no_data)
                        worksheet2.write(sheet2_row_no, 2, '', no_data)
                        worksheet2.write(sheet2_row_no, 3, '', no_data)
                        worksheet2.write(sheet2_row_no, 4, '', no_data)
                        worksheet2.write(sheet2_row_no, 5, '', no_data)
                        worksheet2.write(sheet2_row_no, 6, '', no_data)
                        worksheet2.write(sheet2_row_no, 7, '', no_data)
                        worksheet2.write(sheet2_row_no, 8, '', no_data)
                        worksheet2.write(sheet2_row_no, 9, '', no_data)
                        if search_invoice:
                            qty_out_invoice_invoice = 0
                            qty_out_invoice_refund = 0
                            subtotal_out_invoice = 0
                            subtotal_out_refund = 0
                            total_out_invoice_invoice = 0
                            total_out_refund_invoice = 0
                            sea_invoice_finished = False
                            for invoice in search_invoice:
                                if invoice.sea_invoice_finished:
                                    sea_invoice_finished = True
                                else:
                                    sea_invoice_finished = False
                                for invoice_line in invoice.invoice_line_ids:
                                    if invoice_line.product_id.id == line.product_id.id and \
                                            invoice_line.invoice_id.type == 'out_invoice':
                                        qty_out_invoice_invoice += invoice_line.quantity
                                        total_out_invoice_invoice += invoice_line.price_total
                                        subtotal_out_invoice += invoice_line.price_subtotal
                                    elif invoice_line.product_id.id == line.product_id.id and \
                                            invoice_line.invoice_id.type == 'out_refund':
                                        qty_out_invoice_refund += invoice_line.quantity
                                        total_out_refund_invoice += invoice_line.price_total
                                        subtotal_out_refund += invoice_line.price_subtotal
                            amount_tax_out_invoice = total_out_invoice_invoice - subtotal_out_invoice
                            amount_tax_refund_invoice = total_out_refund_invoice - subtotal_out_refund
                            if sea_invoice_finished:
                                worksheet2.write(sheet2_row_no, 10,
                                                 total_out_invoice_invoice - total_out_refund_invoice,
                                                 money)
                                worksheet2.write(sheet2_row_no, 11, subtotal_out_invoice - subtotal_out_refund, money)
                                worksheet2.write(sheet2_row_no, 12, qty_out_invoice_invoice - qty_out_invoice_refund,
                                                 text_center)
                                worksheet2.write(sheet2_row_no, 27, amount_tax_out_invoice - amount_tax_refund_invoice,
                                                 money)
                                worksheet2.write(sheet2_row_no, 35, '', money)
                                worksheet2.write(sheet2_row_no, 36, '', money)
                                worksheet2.write(sheet2_row_no, 37, '', money)
                            else:
                                worksheet2.write(sheet2_row_no, 10, '', money)
                                worksheet2.write(sheet2_row_no, 11, '', money)
                                worksheet2.write(sheet2_row_no, 12, '', text_center)
                                worksheet2.write(sheet2_row_no, 27, '', text_center)
                                worksheet2.write(sheet2_row_no, 35, line.price_total, money)
                                worksheet2.write(sheet2_row_no, 36, line.price_subtotal, money)
                                worksheet2.write(sheet2_row_no, 37, line.price_tax, money)
                        else:
                            worksheet2.write(sheet2_row_no, 10, '', money)
                            worksheet2.write(sheet2_row_no, 11, '', money)
                            worksheet2.write(sheet2_row_no, 12, '', text_center)
                            worksheet2.write(sheet2_row_no, 27, '', text_center)
                            worksheet2.write(sheet2_row_no, 35, line.price_total, money)
                            worksheet2.write(sheet2_row_no, 36, line.price_subtotal, money)
                            worksheet2.write(sheet2_row_no, 37, line.price_tax, money)
                        worksheet2.write(sheet2_row_no, 13, line.order_partner_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 14, line.product_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 15, '', no_data)
                        worksheet2.write(sheet2_row_no, 16, '', no_data)
                        worksheet2.write(sheet2_row_no, 17, '', no_data)
                        worksheet2.write(sheet2_row_no, 18, '', no_data)
                        worksheet2.write(sheet2_row_no, 19, line.tax_id.amount, text_center)
                        worksheet2.write(sheet2_row_no, 20, '', no_data)
                        worksheet2.write(sheet2_row_no, 21, '', no_data)
                        worksheet2.write(sheet2_row_no, 22, '', no_data)
                        worksheet2.write(sheet2_row_no, 23, '', no_data)
                        worksheet2.write(sheet2_row_no, 24, '', no_data)
                        worksheet2.write(sheet2_row_no, 25, '', no_data)
                        worksheet2.write(sheet2_row_no, 26, '', no_data)
                        worksheet2.write(sheet2_row_no, 28, 'SO', text_center)
                        worksheet2.write(sheet2_row_no, 29, line.order_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 30, line.order_id.confirmation_date, short_date)
                        worksheet2.write(sheet2_row_no, 31, line.order_id.team_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 32, line.product_id.product_tmpl_id.default_code, text_left)
                        if line.product_id.accounting_code:
                            worksheet2.write(sheet2_row_no, 33, line.product_id.accounting_code, text_left)
                        else:
                            worksheet2.write(sheet2_row_no, 33, '', text_left)
                        worksheet2.write(sheet2_row_no, 34, line.product_id.product_tmpl_id.categ_id.complete_name,
                                         text_left)
                        if line.order_id.sea_sale_channel_item:
                            worksheet2.write(sheet2_row_no, 38, line.order_id.sea_sale_channel_item.complete_name,
                                             text_left)
                        else:
                            if line.order_id.sea_sale_channel:
                                worksheet2.write(sheet2_row_no, 38, line.order_id.sea_sale_channel.name, text_left)
                            else:
                                worksheet2.write(sheet2_row_no, 38, '', text_left)
                        if line.order_id.partner_shipping_id.state_id:
                            if line.order_id.partner_shipping_id.region_name:
                                worksheet2.write(sheet2_row_no, 39, line.order_id.partner_shipping_id.region_name,
                                                 text_left)
                            else:
                                worksheet2.write(sheet2_row_no, 39, '', text_left)
                        else:
                            worksheet2.write(sheet2_row_no, 39, '', text_left)
                        worksheet2.write(sheet2_row_no, 40, '', no_data)
                        worksheet2.write(sheet2_row_no, 41, '', no_data)
                        sheet2_row_no += 1
            for i in self.env['account.invoice'].search([('origin', 'in', list_order_sale_to_invoice)]):
                list_invoice_ids.append(i.id)

            pos_line_no = order_line_no
            for pos in list_pos_order:
                if pos.invoice_id:
                    list_invoice_ids.append(pos.invoice_id.id)
                for pos_line in pos.lines:
                    list_product_ids.append(pos_line.product_id.id)
                    pos_line_no += 1
                    worksheet2.write(sheet2_row_no, 0, pos_line_no, text_center)
                    worksheet2.write(sheet2_row_no, 1, '', no_data)
                    worksheet2.write(sheet2_row_no, 2, '', no_data)
                    worksheet2.write(sheet2_row_no, 3, '', no_data)
                    worksheet2.write(sheet2_row_no, 4, '', no_data)
                    worksheet2.write(sheet2_row_no, 5, '', no_data)
                    worksheet2.write(sheet2_row_no, 6, '', no_data)
                    worksheet2.write(sheet2_row_no, 7, '', no_data)
                    worksheet2.write(sheet2_row_no, 8, '', no_data)
                    worksheet2.write(sheet2_row_no, 9, '', no_data)
                    worksheet2.write(sheet2_row_no, 10, pos_line.price_subtotal_incl, money)
                    worksheet2.write(sheet2_row_no, 11, pos_line.price_subtotal, money)
                    worksheet2.write(sheet2_row_no, 12, pos_line.qty, text_center)
                    worksheet2.write(sheet2_row_no, 13, pos_line.order_id.partner_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 14, pos_line.product_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 15, '', no_data)
                    worksheet2.write(sheet2_row_no, 16, '', no_data)
                    worksheet2.write(sheet2_row_no, 17, '', no_data)
                    worksheet2.write(sheet2_row_no, 18, '', no_data)
                    worksheet2.write(sheet2_row_no, 19, pos_line.tax_ids.amount, text_center)
                    worksheet2.write(sheet2_row_no, 20, '', no_data)
                    worksheet2.write(sheet2_row_no, 21, '', no_data)
                    worksheet2.write(sheet2_row_no, 22, '', no_data)
                    worksheet2.write(sheet2_row_no, 23, '', no_data)
                    worksheet2.write(sheet2_row_no, 24, '', no_data)
                    worksheet2.write(sheet2_row_no, 25, '', no_data)
                    worksheet2.write(sheet2_row_no, 26, '', no_data)
                    worksheet2.write(sheet2_row_no, 27, pos_line.price_subtotal_incl - pos_line.price_subtotal, money)
                    worksheet2.write(sheet2_row_no, 28, 'POS', text_center)
                    worksheet2.write(sheet2_row_no, 29, pos_line.order_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 30, pos_line.order_id.date_order, short_date)
                    worksheet2.write(sheet2_row_no, 31, 'Bán lẻ', text_left)
                    worksheet2.write(sheet2_row_no, 32, pos_line.product_id.product_tmpl_id.default_code, text_left)
                    if pos_line.product_id.accounting_code:
                        worksheet2.write(sheet2_row_no, 33, pos_line.product_id.accounting_code, text_left)
                    else:
                        worksheet2.write(sheet2_row_no, 33, '', text_left)
                    worksheet2.write(sheet2_row_no, 34, pos_line.product_id.product_tmpl_id.categ_id.complete_name,
                                     text_left)
                    worksheet2.write(sheet2_row_no, 35, '', money)
                    worksheet2.write(sheet2_row_no, 36, '', money)
                    worksheet2.write(sheet2_row_no, 37, '', money)
                    worksheet2.write(sheet2_row_no, 38, 'Bán lẻ / ' + str(pos_line.order_id.config_id.name), text_left)
                    if pos_line.order_id.config_id.sea_pos_region_name:
                        pos_region_name = pos_line.order_id.config_id.sea_pos_region_name
                        if pos_region_name == 'mien_bac':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Bắc', text_left)
                        elif pos_region_name == 'mien_trung':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Trung', text_left)
                        elif pos_region_name == 'mien_nam':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Nam', text_left)
                    else:
                        worksheet2.write(sheet2_row_no, 39, '', text_left)
                    worksheet2.write(sheet2_row_no, 40, '', no_data)
                    worksheet2.write(sheet2_row_no, 41, '', no_data)
                    sheet2_row_no += 1

            list_picking_out_ids = []
            list_picking_in_ids = []
            for s_o in list_picking_out:
                list_picking_out_ids.append(s_o.id)
            for s_i in list_picking_in:
                list_picking_in_ids.append(s_i.id)
            move_out_objs = self.env['stock.move'].search([('picking_id', 'in', list_picking_out_ids)])
            for move_out in move_out_objs:
                list_product_ids.append(move_out.product_id.id)
            move_in_objs = self.env['stock.move'].search([('picking_id', 'in', list_picking_in_ids)])
            for move_in in move_in_objs:
                list_product_ids.append(move_in.product_id.id)
            invoice_objs = self.env['account.invoice'].browse(list_invoice_ids)
            product_objs = self.env['product.product'].browse(set(list_product_ids))

            line_no = 0
            for prod in product_objs:
                if prod.id:
                    line_no += 1
                    product_amount_out_invoice = 0
                    product_amount_out_refund = 0
                    product_qty_invoice = 0
                    product_qty_refund = 0
                    product_qty_loss_out = 0
                    product_qty_loss_in = 0
                    for invoice in invoice_objs:
                        if invoice.state != 'draft' and invoice.state != 'cancel' and invoice.type == 'out_invoice':
                            for inv in invoice.invoice_line_ids:
                                if inv.product_id.id == prod.id:
                                    product_amount_out_invoice += inv.price_total
                                    product_qty_invoice += inv.quantity
                        elif invoice.state != 'draft' and invoice.type == 'out_refund':
                            for inv in invoice.invoice_line_ids:
                                if inv.product_id.id == prod.id:
                                    product_amount_out_refund += inv.price_total
                                    product_qty_refund += inv.quantity
                    for move in move_out_objs:
                        for mo in move.move_line_ids:
                            if mo.product_id.id == prod.id:
                                product_qty_loss_out += mo.qty_done
                    for move in move_in_objs:
                        for mo in move.move_line_ids:
                            if mo.product_id.id == prod.id:
                                product_qty_loss_in += mo.qty_done
                    worksheet3.write(line_no, 0, line_no, text_center)
                    worksheet3.write(line_no, 1, prod.default_code, text_left)
                    worksheet3.write(line_no, 2, prod.name, text_left)
                    worksheet3.write(line_no, 3, prod.sea_unit_of_measure.name, text_center)
                    worksheet3.write(line_no, 4,
                                     (product_qty_invoice - product_qty_refund) + (
                                             product_qty_loss_out - product_qty_loss_in),
                                     text_center)
                    worksheet3.write(line_no, 5, product_amount_out_invoice - product_amount_out_refund, money)
                    sheet3_row_no += 1
        else:
            list_order_ref_ids = []
            list_pos_ref_ids = []
            list_product_inv_ids = []
            for invoice in list_invoices:
                for order in self.env['sale.order'].search([('name', '=', invoice.origin)]):
                    list_order_ref_ids.append(order.id)
                for pos in self.env['pos.order'].search([('name', '=', invoice.origin)]):
                    list_pos_ref_ids.append(pos.id)
                for inv_line in invoice.invoice_line_ids:
                    list_product_inv_ids.append(inv_line.product_id.id)

            list_picking_out_ids = []
            list_picking_in_ids = []
            for s_o in list_picking_out:
                list_picking_out_ids.append(s_o.id)
            for s_i in list_picking_in:
                list_picking_in_ids.append(s_i.id)
            move_out_objs = self.env['stock.move'].search([('picking_id', 'in', list_picking_out_ids)])
            for move_out in move_out_objs:
                list_product_inv_ids.append(move_out.product_id.id)
            move_in_objs = self.env['stock.move'].search([('picking_id', 'in', list_picking_in_ids)])
            for move_in in move_in_objs:
                list_product_inv_ids.append(move_in.product_id.id)
            product_inv_objs = self.env['product.product'].browse(set(list_product_inv_ids))
            line_no = 0
            for prod in product_inv_objs:
                if prod.id:
                    line_no += 1
                    product_amount_out_invoice = 0
                    product_amount_out_refund = 0
                    product_qty_invoice = 0
                    product_qty_refund = 0
                    product_qty_loss_out = 0
                    product_qty_loss_in = 0
                    for invoice in list_invoices:
                        if invoice.state != 'draft' and invoice.state != 'cancel' and invoice.type == 'out_invoice':
                            for inv in invoice.invoice_line_ids:
                                if inv.product_id.id == prod.id:
                                    product_amount_out_invoice += inv.price_total
                                    product_qty_invoice += inv.quantity
                        elif invoice.state != 'draft' and invoice.type == 'out_refund':
                            for inv in invoice.invoice_line_ids:
                                if inv.product_id.id == prod.id:
                                    product_amount_out_refund += inv.price_total
                                    product_qty_refund += inv.quantity
                    for move in move_out_objs:
                        for mo in move.move_line_ids:
                            if mo.product_id.id == prod.id:
                                product_qty_loss_out += mo.qty_done
                    for move in move_in_objs:
                        for mo in move.move_line_ids:
                            if mo.product_id.id == prod.id:
                                product_qty_loss_in += mo.qty_done
                    worksheet3.write(line_no, 0, line_no, text_center)
                    worksheet3.write(line_no, 1, prod.default_code, text_left)
                    worksheet3.write(line_no, 2, prod.name, text_left)
                    worksheet3.write(line_no, 3, prod.sea_unit_of_measure.name, text_center)
                    worksheet3.write(line_no, 4,
                                     (product_qty_invoice - product_qty_refund) + (
                                             product_qty_loss_out - product_qty_loss_in),
                                     text_center)
                    worksheet3.write(line_no, 5, product_amount_out_invoice - product_amount_out_refund, money)
                    sheet3_row_no += 1

            order_objs = self.env['sale.order'].browse(set(list_order_ref_ids))
            for order in order_objs:
                search_invoice = self.env['account.invoice'].search([('origin', '=', order.name),
                                                                     ('state', 'not in', ['draft', 'cancel'])])
                for line in order.order_line:
                    if line.product_id:
                        list_product_ids.append(line.product_id.id)
                        order_line_no += 1
                        worksheet2.write(sheet2_row_no, 0, order_line_no, text_center)
                        worksheet2.write(sheet2_row_no, 1, '', no_data)
                        worksheet2.write(sheet2_row_no, 2, '', no_data)
                        worksheet2.write(sheet2_row_no, 3, '', no_data)
                        worksheet2.write(sheet2_row_no, 4, '', no_data)
                        worksheet2.write(sheet2_row_no, 5, '', no_data)
                        worksheet2.write(sheet2_row_no, 6, '', no_data)
                        worksheet2.write(sheet2_row_no, 7, '', no_data)
                        worksheet2.write(sheet2_row_no, 8, '', no_data)
                        worksheet2.write(sheet2_row_no, 9, '', no_data)
                        if search_invoice:
                            qty_out_invoice_invoice = 0
                            qty_out_invoice_refund = 0
                            subtotal_out_invoice = 0
                            subtotal_out_refund = 0
                            total_out_invoice_invoice = 0
                            total_out_refund_invoice = 0
                            sea_invoice_finished = False
                            for invoice in search_invoice:
                                if invoice.sea_invoice_finished:
                                    sea_invoice_finished = True
                                else:
                                    sea_invoice_finished = False
                                for invoice_line in invoice.invoice_line_ids:
                                    if invoice_line.product_id.id == line.product_id.id and \
                                            invoice_line.invoice_id.type == 'out_invoice':
                                        qty_out_invoice_invoice += invoice_line.quantity
                                        total_out_invoice_invoice += invoice_line.price_total
                                        subtotal_out_invoice += invoice_line.price_subtotal
                                    elif invoice_line.product_id.id == line.product_id.id and \
                                            invoice_line.invoice_id.type == 'out_refund':
                                        qty_out_invoice_refund += invoice_line.quantity
                                        total_out_refund_invoice += invoice_line.price_total
                                        subtotal_out_refund += invoice_line.quantity
                            amount_tax_out_invoice = total_out_invoice_invoice - subtotal_out_invoice
                            amount_tax_refund_invoice = total_out_refund_invoice - subtotal_out_refund
                            if sea_invoice_finished:
                                worksheet2.write(sheet2_row_no, 10,
                                                 total_out_invoice_invoice - total_out_refund_invoice,
                                                 money)
                                worksheet2.write(sheet2_row_no, 11, subtotal_out_invoice - subtotal_out_refund, money)
                                worksheet2.write(sheet2_row_no, 12, qty_out_invoice_invoice - qty_out_invoice_refund,
                                                 text_center)
                                worksheet2.write(sheet2_row_no, 27, amount_tax_out_invoice - amount_tax_refund_invoice,
                                                 money)
                                worksheet2.write(sheet2_row_no, 35, '', money)
                                worksheet2.write(sheet2_row_no, 36, '', money)
                                worksheet2.write(sheet2_row_no, 37, '', money)
                            else:
                                worksheet2.write(sheet2_row_no, 10, '', money)
                                worksheet2.write(sheet2_row_no, 11, '', money)
                                worksheet2.write(sheet2_row_no, 12, '', text_center)
                                worksheet2.write(sheet2_row_no, 27, '', text_center)
                                worksheet2.write(sheet2_row_no, 35, line.price_total, money)
                                worksheet2.write(sheet2_row_no, 36, line.price_subtotal, money)
                                worksheet2.write(sheet2_row_no, 37, line.price_tax, money)
                        else:
                            worksheet2.write(sheet2_row_no, 10, '', money)
                            worksheet2.write(sheet2_row_no, 11, '', money)
                            worksheet2.write(sheet2_row_no, 12, '', text_center)
                            worksheet2.write(sheet2_row_no, 27, '', text_center)
                            worksheet2.write(sheet2_row_no, 35, line.price_total, money)
                            worksheet2.write(sheet2_row_no, 36, line.price_subtotal, money)
                            worksheet2.write(sheet2_row_no, 37, line.price_tax, money)
                        worksheet2.write(sheet2_row_no, 13, line.order_partner_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 14, line.product_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 15, '', no_data)
                        worksheet2.write(sheet2_row_no, 16, '', no_data)
                        worksheet2.write(sheet2_row_no, 17, '', no_data)
                        worksheet2.write(sheet2_row_no, 18, '', no_data)
                        worksheet2.write(sheet2_row_no, 19, line.tax_id.amount, text_center)
                        worksheet2.write(sheet2_row_no, 20, '', no_data)
                        worksheet2.write(sheet2_row_no, 21, '', no_data)
                        worksheet2.write(sheet2_row_no, 22, '', no_data)
                        worksheet2.write(sheet2_row_no, 23, '', no_data)
                        worksheet2.write(sheet2_row_no, 24, '', no_data)
                        worksheet2.write(sheet2_row_no, 25, '', no_data)
                        worksheet2.write(sheet2_row_no, 26, '', no_data)
                        worksheet2.write(sheet2_row_no, 28, 'SO', text_center)
                        worksheet2.write(sheet2_row_no, 29, line.order_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 30, line.order_id.confirmation_date, short_date)
                        worksheet2.write(sheet2_row_no, 31, line.order_id.team_id.name, text_left)
                        worksheet2.write(sheet2_row_no, 32, line.product_id.default_code, text_left)
                        if line.product_id.accounting_code:
                            worksheet2.write(sheet2_row_no, 33, line.product_id.accounting_code, text_left)
                        else:
                            worksheet2.write(sheet2_row_no, 33, '', text_left)
                        worksheet2.write(sheet2_row_no, 34, line.product_id.product_tmpl_id.categ_id.complete_name,
                                         text_left)
                        if line.order_id.sea_sale_channel_item:
                            worksheet2.write(sheet2_row_no, 38, line.order_id.sea_sale_channel_item.complete_name,
                                             text_left)
                        else:
                            if line.order_id.sea_sale_channel:
                                worksheet2.write(sheet2_row_no, 38, line.order_id.sea_sale_channel.name, text_left)
                            else:
                                worksheet2.write(sheet2_row_no, 38, '', text_left)
                        if line.order_id.partner_shipping_id.state_id:
                            if line.order_id.partner_shipping_id.region_name:
                                worksheet2.write(sheet2_row_no, 39, line.order_id.partner_shipping_id.region_name,
                                                 text_left)
                            else:
                                worksheet2.write(sheet2_row_no, 39, '', text_left)
                        else:
                            worksheet2.write(sheet2_row_no, 39, '', text_left)
                        worksheet2.write(sheet2_row_no, 40, '', no_data)
                        worksheet2.write(sheet2_row_no, 41, '', no_data)
                        sheet2_row_no += 1
            pos_objs = self.env['pos.order'].browse(set(list_pos_ref_ids))
            pos_line_no = order_line_no
            for pos in pos_objs:
                for pos_line in pos.lines:
                    list_product_ids.append(pos_line.product_id.id)
                    pos_line_no += 1
                    worksheet2.write(sheet2_row_no, 0, pos_line_no, text_center)
                    worksheet2.write(sheet2_row_no, 1, '', no_data)
                    worksheet2.write(sheet2_row_no, 2, '', no_data)
                    worksheet2.write(sheet2_row_no, 3, '', no_data)
                    worksheet2.write(sheet2_row_no, 4, '', no_data)
                    worksheet2.write(sheet2_row_no, 5, '', no_data)
                    worksheet2.write(sheet2_row_no, 6, '', no_data)
                    worksheet2.write(sheet2_row_no, 7, '', no_data)
                    worksheet2.write(sheet2_row_no, 8, '', no_data)
                    worksheet2.write(sheet2_row_no, 9, '', no_data)
                    worksheet2.write(sheet2_row_no, 10, pos_line.price_subtotal_incl, money)
                    worksheet2.write(sheet2_row_no, 11, pos_line.price_subtotal, money)
                    worksheet2.write(sheet2_row_no, 12, pos_line.qty, text_center)
                    worksheet2.write(sheet2_row_no, 13, pos_line.order_id.partner_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 14, pos_line.product_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 15, '', no_data)
                    worksheet2.write(sheet2_row_no, 16, '', no_data)
                    worksheet2.write(sheet2_row_no, 17, '', no_data)
                    worksheet2.write(sheet2_row_no, 18, '', no_data)
                    worksheet2.write(sheet2_row_no, 19, pos_line.tax_ids.amount, text_center)
                    worksheet2.write(sheet2_row_no, 20, '', no_data)
                    worksheet2.write(sheet2_row_no, 21, '', no_data)
                    worksheet2.write(sheet2_row_no, 22, '', no_data)
                    worksheet2.write(sheet2_row_no, 23, '', no_data)
                    worksheet2.write(sheet2_row_no, 24, '', no_data)
                    worksheet2.write(sheet2_row_no, 25, '', no_data)
                    worksheet2.write(sheet2_row_no, 26, '', no_data)
                    worksheet2.write(sheet2_row_no, 27, pos_line.price_subtotal_incl - pos_line.price_subtotal, money)
                    worksheet2.write(sheet2_row_no, 28, 'POS', text_center)
                    worksheet2.write(sheet2_row_no, 29, pos_line.order_id.name, text_left)
                    worksheet2.write(sheet2_row_no, 30, pos_line.order_id.date_order, short_date)
                    worksheet2.write(sheet2_row_no, 31, 'Bán lẻ', text_left)
                    worksheet2.write(sheet2_row_no, 32, pos_line.product_id.product_tmpl_id.default_code, text_left)
                    if pos_line.product_id.accounting_code:
                        worksheet2.write(sheet2_row_no, 33, pos_line.product_id.accounting_code, text_left)
                    else:
                        worksheet2.write(sheet2_row_no, 33, '', text_left)
                    worksheet2.write(sheet2_row_no, 34, pos_line.product_id.product_tmpl_id.categ_id.complete_name,
                                     text_left)
                    worksheet2.write(sheet2_row_no, 35, '', money)
                    worksheet2.write(sheet2_row_no, 36, '', money)
                    worksheet2.write(sheet2_row_no, 37, '', money)
                    worksheet2.write(sheet2_row_no, 38, 'Bán lẻ / ' + str(pos_line.order_id.config_id.name), text_left)
                    if pos_line.order_id.config_id.sea_pos_region_name:
                        pos_region_name = pos_line.order_id.config_id.sea_pos_region_name
                        if pos_region_name == 'mien_bac':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Bắc', text_left)
                        elif pos_region_name == 'mien_trung':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Trung', text_left)
                        elif pos_region_name == 'mien_nam':
                            worksheet2.write(sheet2_row_no, 39, 'Miền Nam', text_left)
                    else:
                        worksheet2.write(sheet2_row_no, 39, '', text_left)
                    worksheet2.write(sheet2_row_no, 40, '', no_data)
                    worksheet2.write(sheet2_row_no, 41, '', no_data)
                    sheet2_row_no += 1
