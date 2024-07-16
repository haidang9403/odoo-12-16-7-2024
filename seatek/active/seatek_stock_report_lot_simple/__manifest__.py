# -*- coding: utf-8 -*-
{
    "name": "SeaTek Inventory Report (simple) 1.0.1",
    "summary": "Báo cáo tồn kho",
    "description": """
        Version 1.0.0:
            + Generate report
    """,
    "version": "1.0.0",
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
    "images": ["static/description/iconseatek.png"],
    "application": False,
    "installable": True,
}
