# -*- coding: utf-8 -*-
{
    "name": "Seatek Inventory Period 1.0.0",
    "summary": "Quản lý các kỳ",
    "description": """
        General report
            + Version 12.0.0.1
    """,
    "version": "12.0.0.1",
    "category": "stock",
    "website": "https://seatek.vn",
    "author": "Seatek, Anh Khoa",
    "license": "AGPL-3",
    "depends": [
        "stock", "seacorp_inventory_report"
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/seatek_inventory_security.xml',
        'views/seatek_inventory_period.xml',
        'views/seatek_inventory_period_management.xml',
        'views/seatek_inventory_stock_closing.xml',
    ],
    'images': ['static/description/iconseatek.png'],
    "application": False,
    "installable": True,
}
