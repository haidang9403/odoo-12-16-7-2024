# -*- coding: utf-8 -*-
{
    'name': "Delivery Info Report",
    'summary': """
        Sea Sale Delivery Report
    """,
    'description': """
        Sea Sale Delivery Report
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['sale_stock', 'sale_management'],

    # always loaded
    'data': [
        'views/stock_request_order_view.xml',
        'report/action_report.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}