# -*- coding: utf-8 -*-
{
    "name": "SeaTek Assigned Order But Not Send",
    "summary": "Báo cáo Danh sách những đơn đang giữ hàng nhưng chưa gửi",
    "description": """
        Version 1.0.0:
    """,
    "version": "1.0.0",
    "category": "stock_move",
    "website": "https://seatek.vn",
    "author": "Seatek",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
    ],
    "data": [
        'views/assign_order.xml',
        'security/ir.model.access.csv',
    ],
    "images": ["static/description/iconseatek.png"],
    "application": False,
    "installable": True,
}