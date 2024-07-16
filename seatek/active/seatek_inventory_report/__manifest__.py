# -*- coding: utf-8 -*-
{
    "name": "SeaTek Inventory Report 1.0.0",
    "summary": "Báo cáo xuất nhập tồn tổng quát",
    "description": """
        Version 12.0.0 - 1.0.0:
            + Generate report
    """,
    "version": "12.0.0 - 1.0.0",
    "category": "stock",
    "website": "https://seatek.vn",
    "author": "Seatek, Anh Khoa",
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
    "application": False,
    "installable": True,
}
