# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Purchase Report - XLS",

    'summary': """
       Pegasus Purchase Order XLS""",

    'description': """
        Pegasus Purchase Order XLS
        + Version: 12.0.0.1
        + Version: 12.0.0.2 -> Edit ISO number
        + Version: 12.0.0.3 - ( 06-Nov-2022) -> Update iso date
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'purchase',
    'version': '12.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [

        'reports/purchase_order_report.xml',
    ],
}