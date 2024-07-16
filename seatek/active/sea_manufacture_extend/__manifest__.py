# -*- coding: utf-8 -*-
{
    'name': "Sea Manufacture Extend",
    'summary': """
        Sea Manufacture Extend
    """,
    'description': """
        + Modify print report Production Order
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp'],

    # always loaded
    'data': [
        'reports/sea_mrp_report_menu.xml',
        'reports/report_production_order.xml',
        'reports/report_finished_product.xml',
    ],
    'installable': True,
}
