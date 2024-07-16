# -*- coding: utf-8 -*-
{
    "name": "SeaTek Inventory Report 1.0.4",
    "summary": "Báo cáo xuất nhập tồn",
    "description": """
        General report
            + Version 12.0.1.0.3
        12.0.0.2 (Seatek)
            + Remove data "Chi tiết xuất nhập tồn" when other companies use this report
            + update file "inventory_report.xml", "inventory_report.py"
        12.0.0.3 (Seatek)
            + Invisible field "company_id" and "value" 
    """,
    "version": "12.0.0.3",
    "category": "stock",
    "website": "https://seatek.vn",

    "author": "TGL team, ThaiPham",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/inventory_report.xml',
        'reports/report_xlsx.xml',
    ],
    "images": ["static/description/icon.png"],
    "application": False,
    "installable": True,
}
