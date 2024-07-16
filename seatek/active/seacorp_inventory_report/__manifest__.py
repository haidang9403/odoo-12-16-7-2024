# -*- coding: utf-8 -*-
{
    "name": "Seacorp Inventory Report 1.0.4",
    "summary": "Báo cáo xuất nhập tồn",
    "description": """
        General report
            + Version 12.0.1.0.3
        12.0.0.3 (Seatek)
            + Remove data "Chi tiết xuất nhập tồn" when other companies use this report
            + update file "inventory_report.xml", "inventory_report.py"
    """,
    "version": "12.0.0.3",
    "category": "stock",
    "website": "https://seatek.vn",
    "author": "TGL team, ThaiPham",
    "license": "AGPL-3",
    "depends": [
        "stock"
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/inventory_report.xml'
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}
