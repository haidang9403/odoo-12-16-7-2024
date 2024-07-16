# -*- coding: utf-8 -*-
{
    'name': "Inventory Reporting Extend Precision",

    'summary': """
       Sea Inventory Reporting Extend Precision""",

    'description': """
        Inventory Reporting Extend Precision
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': '',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock_report_quantity_by_location',
        'stock_analysis',
        'stock',
        'stock_inventory_turnover_report'
    ],

    # always loaded
    'data': [],
    'installable': True,
}
