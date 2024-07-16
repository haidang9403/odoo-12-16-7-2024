import io, base64, datetime
from odoo import models
import pytz
from collections import defaultdict
import datetime


class SaleOrderReportSCS(models.AbstractModel):
    _name = 'report.sea_report_delivery_info.delivery_info_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        vn_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        worksheet1 = workbook.add_worksheet('Delivery ' + str(objects.date.strftime('%d-%m-%Y')))
        company_name = self.env.user.company_id.display_name
        company_address = self.env.user.company_id.street + ', ' + self.env.user.company_id.street2 + ', ' + self.env.user.company_id.state_id.name
        company_logo = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))
        company_vat = self.env.user.company_id.vat

        f1 = workbook.add_format(
            {'bold': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 12,
             'font_name': 'Tahoma'})
        text_center = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        f2 = workbook.add_format(
            {'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma'})
        f3 = workbook.add_format(
            {'border': 1, 'align': 'center', 'valign': 'vcenter', 'bold': True, 'text_wrap': True, 'font_size': 10,
             'font_name': 'Tahoma', 'bg_color': '#669966'})
        f4 = workbook.add_format(
            {'border': 1, 'valign': 'vcenter', 'text_wrap': True})
        f5 = workbook.add_format(
            {'border': 1, 'valign': 'vcenter', 'bg_color': '#669966'})
        footer = workbook.add_format(
            {'bold': 1, 'valign': 'left', 'text_wrap': True})

        row_no = 0
        # Report Header
        worksheet1.set_column(0, 0, 5)
        worksheet1.set_column(1, 1, 15)
        worksheet1.set_column(2, 2, 8)
        worksheet1.set_column(3, 3, 35)
        worksheet1.set_column(4, 4, 40)

        worksheet1.insert_image(1, 1, "company_logo.png",
                                {'image_data': company_logo, 'x_scale': 0.60, 'y_scale': 0.55})
        worksheet1.merge_range(row_no, 0, row_no, 13, company_name, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 13, company_address, f2)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 13, 'MST: ' + str(company_vat), f2)
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 13, ' ')
        row_no += 1
        worksheet1.merge_range(row_no, 0, row_no, 13,
                               'THÔNG TIN LỊCH GIAO HÀNG NGÀY ' + str(objects.date.strftime('%d/%m/%Y')), f1)
        row_no += 2
        worksheet1.write(row_no, 0, 'STT', f3)
        worksheet1.write(row_no, 1, 'SO', f3)
        worksheet1.write(row_no, 2, 'Giờ giao', f3)
        worksheet1.write(row_no, 3, 'Khách hàng', f3)
        worksheet1.write(row_no, 4, 'Địa chỉ', f3)

        worksheet1.write(row_no + 1, 0, '', f5)
        worksheet1.write(row_no + 1, 1, '', f5)
        worksheet1.write(row_no + 1, 2, '', f5)
        worksheet1.write(row_no + 1, 3, '', f5)
        worksheet1.write(row_no + 1, 4, '', f5)
        worksheet1.write(row_no + 2, 0, '', f5)
        worksheet1.write(row_no + 2, 1, '', f5)
        worksheet1.write(row_no + 2, 2, '', f5)
        worksheet1.write(row_no + 2, 3, '', f5)
        worksheet1.write(row_no + 2, 4, '', f5)
        worksheet1.freeze_panes(9, 0)

        orders = self.env['sale.order'].search([
            ('state', 'in', ['done', 'sale']),
            ('commitment_date', '>=', data.get('start_date')),
            ('commitment_date', '<=', data.get('end_date'))
        ])

        consignments = self.env['consignment.process.ept'].search([
            ('state', 'in', ['processed', 'delivered']),
            ('consignment_type', '=', 'transfer'),
            ('date', '>=', data.get('start_date')),
            ('date', '<=', data.get('end_date'))
        ])

        stocks = self.env['stock.request.order'].search([
            ('state', 'in', ['open', 'done']),
            ('expected_date', '>=', data.get('start_date')),
            ('expected_date', '<=', data.get('end_date'))])

        # Initialize a set to store the names of all products
        all_product_names = set()
        product_quantities = defaultdict(int)
        product_quantities_by_stock = defaultdict(lambda: defaultdict(int))

        for order in orders:
            for line in order.order_line:
                product_name = line.product_id.name
                if product_name:
                    all_product_names.add(product_name)
                    product_quantities[product_name] += line.product_uom_qty
                    product_quantities_by_stock[order.warehouse_id.name][product_name] += line.product_uom_qty
        for consignment in consignments:
            for line in consignment.consignment_process_line_ids:
                product_name = line.product_id.name
                if product_name:
                    all_product_names.add(product_name)
                    product_quantities[product_name] += line.quantity
                    product_quantities_by_stock[consignment.warehouse_id.name][product_name] += line.quantity
        for stock in stocks:
            for line in stock.stock_request_ids:
                product_name = line.product_id.name
                if product_name:
                    all_product_names.add(product_name)
                    product_quantities[product_name] += line.product_uom_qty
                    product_quantities_by_stock[stock.warehouse_id.name][product_name] += line.product_uom_qty

        # Convert the collection into a list for use or printing
        unique_product_names = list(all_product_names)
        if len(unique_product_names) == 1:
            worksheet1.write(row_no, 5, 'Bán', f3)
        else:
            worksheet1.merge_range(row_no, 5, row_no, 5 + len(unique_product_names) - 1, "Bán", f3)
        row_no += 1
        col = 4
        col_default = col

        # List all products sold during the day
        for product in unique_product_names:
            col += 1
            worksheet1.write(row_no, col, product, f5)
            worksheet1.write(row_no + 1, col, product_quantities[product], f5)
        worksheet1.write(row_no, col + 1, '', f5)
        worksheet1.write(row_no + 1, col + 1, '', f5)
        worksheet1.write(row_no, col + 2, '', f5)
        worksheet1.write(row_no + 1, col + 2, '', f5)
        row_no += 1
        unique_warehouse_ids = set()

        worksheet1.write(6, col + 1, 'Thanh Toán', f3)
        worksheet1.write(6, col + 2, 'Ghi Chú', f3)
        worksheet1.set_column(col + 2, col + 2, 50)

        # Browse through each order in the order list
        for order in orders:
            unique_warehouse_ids.add(order.warehouse_id.name)
        for consignment in consignments:
            unique_warehouse_ids.add(consignment.warehouse_id.name)
        for stock in stocks:
            unique_warehouse_ids.add(stock.warehouse_id.name)

        number = 0
        col_default_warehouse = 0
        # Browse through each unique warehouse_id
        for warehouse_id in unique_warehouse_ids:
            # Write the name warehouse_id into the Excel file
            row_no += 1
            col_default_warehouse = col_default

            worksheet1.write(row_no, 0, warehouse_id, f5)
            worksheet1.write(row_no, 1, '', f5)
            worksheet1.write(row_no, 2, '', f5)
            worksheet1.write(row_no, 3, '', f5)
            worksheet1.write(row_no, 4, '', f5)
            worksheet1.write(row_no, col + 1, '', f5)
            worksheet1.write(row_no, col + 2, '', f5)

            for product in unique_product_names:
                col_default_warehouse += 1
                worksheet1.write(row_no, col_default_warehouse, product_quantities_by_stock[warehouse_id][product], f5)
            # Filter orders belonging to the same warehouse_id and sort them by order name
            warehouse_order_list = orders.filtered(
                lambda o: o.warehouse_id.name == warehouse_id).sorted(
                key=lambda o: o.name)
            warehouse_order_list_consignment = consignments.filtered(
                lambda o: o.warehouse_id.name == warehouse_id).sorted(
                key=lambda o: o.name)
            warehouse_order_list_stock = stocks.filtered(
                lambda o: o.warehouse_id.name == warehouse_id).sorted(
                key=lambda o: o.name)

            # Record information for each order in the corresponding order list
            for order in warehouse_order_list:
                row_no += 1
                number += 1
                worksheet1.write(row_no, 0, number, text_center)
                worksheet1.write(row_no, 1, order.name if order.name else '', f4)
                if order.commitment_date:
                    vn_time = order.commitment_date.astimezone(vn_timezone)
                    formatted_time = vn_time.strftime('%H:%M')
                    worksheet1.write(row_no, 2, formatted_time, text_center)
                else:
                    worksheet1.write(row_no, 2, '', f4)
                address = ''
                if order.partner_shipping_id.street:
                    address += order.partner_shipping_id.street
                if order.partner_shipping_id.street2:
                    address += ', '
                    address += order.partner_shipping_id.street2
                if order.partner_shipping_id.city:
                    address += ', '
                    address += order.partner_shipping_id.city
                if order.partner_shipping_id.state_id:
                    address += ', '
                    address += order.partner_shipping_id.state_id.name
                worksheet1.write(row_no, 3, order.partner_shipping_id.name if order.partner_shipping_id.name else '',
                                 f4)
                worksheet1.write(row_no, 4, address if address else '', f4)
                worksheet1.write(row_no, col + 1, dict(order._fields['sea_payment_method'].selection).get(
                    order.sea_payment_method) if order.sea_payment_method else '', f4)
                worksheet1.write(row_no, col + 2, order.note if order.note else '', f4)

                # Count the number of products for each product and record in the corresponding column
                product_count = {}
                for line in order.order_line:
                    product_name = line.product_id.name
                    quantity = line.product_uom_qty

                    # Thêm số lượng sản phẩm vào từ điển
                    if product_name in product_count:
                        product_count[product_name] += quantity
                    else:
                        product_count[product_name] = quantity

                for idx, product in enumerate(unique_product_names):
                    quantity = product_count.get(product, '')
                    worksheet1.write(row_no, idx + 5, quantity, f4)

            for order in warehouse_order_list_consignment:
                row_no += 1
                number += 1
                worksheet1.write(row_no, 0, number, text_center)
                worksheet1.write(row_no, 1, order.name if order.name else '', f4)
                if order.date:
                    vn_time = order.date.astimezone(vn_timezone)
                    formatted_time = vn_time.strftime('%H:%M')
                    worksheet1.write(row_no, 2, formatted_time, text_center)
                else:
                    worksheet1.write(row_no, 2, '', f4)
                worksheet1.write(row_no, 3,
                                 order.consignment_delivery_address.name if order.consignment_delivery_address.name else '',
                                 f4)
                address = ''
                if order.consignment_delivery_address.street:
                    address += order.consignment_delivery_address.street
                if order.consignment_delivery_address.street2:
                    address += ', '
                    address += order.consignment_delivery_address.street2
                if order.consignment_delivery_address.city:
                    address += ', '
                    address += order.consignment_delivery_address.city
                if order.consignment_delivery_address.state_id:
                    address += ', '
                    address += order.consignment_delivery_address.state_id.name
                worksheet1.write(row_no, 4, address if address else '',
                                 f4)
                worksheet1.write(row_no, col + 1, '', f4)
                worksheet1.write(row_no, col + 2, order.delivery_address_note if order.delivery_address_note else '',
                                 f4)

                product_count = {}
                for line in order.consignment_process_line_ids:
                    product_name = line.product_id.name
                    quantity = line.quantity

                    # Thêm số lượng sản phẩm vào từ điển
                    if product_name in product_count:
                        product_count[product_name] += quantity
                    else:
                        product_count[product_name] = quantity

                for idx, product in enumerate(unique_product_names):
                    quantity = product_count.get(product, '')
                    worksheet1.write(row_no, idx + 5, quantity, f4)

            for order in warehouse_order_list_stock:
                row_no += 1
                number += 1
                worksheet1.write(row_no, 0, number, text_center)
                worksheet1.write(row_no, 1, order.name if order.name else '', f4)
                if order.expected_date:
                    vn_time = order.expected_date.astimezone(vn_timezone)
                    formatted_time = vn_time.strftime('%H:%M')
                    worksheet1.write(row_no, 2, formatted_time, text_center)
                else:
                    worksheet1.write(row_no, 2, '', f4)
                worksheet1.write(row_no, 3, order.location_id.name if order.location_id.name else '', f4)
                worksheet1.write(row_no, 4, '', f4)
                worksheet1.write(row_no, col + 1, '', f4)
                worksheet1.write(row_no, col + 2, order.note if order.note else '', f4)

                product_count = {}
                for line in order.stock_request_ids:
                    product_name = line.product_id.name
                    quantity = line.product_uom_qty

                    # Thêm số lượng sản phẩm vào từ điển
                    if product_name in product_count:
                        product_count[product_name] += quantity
                    else:
                        product_count[product_name] = quantity

                for idx, product in enumerate(unique_product_names):
                    quantity = product_count.get(product, '')
                    worksheet1.write(row_no, idx + 5, quantity, f4)
        row_no += 2
        date_now = datetime.datetime.now(vn_timezone)
        worksheet1.merge_range(row_no, col_default_warehouse, row_no, col_default_warehouse + 2,
                               'Xuất báo cáo lúc  ' + date_now.strftime('%H:%M') + ' Ngày ' + date_now.strftime(
                                   '%d/%m/%Y'), footer)
        row_no += 1
        worksheet1.merge_range(row_no, col_default_warehouse, row_no, col_default_warehouse + 2,
                               'Người thực hiện :  ' + self.env.user.name, footer)
