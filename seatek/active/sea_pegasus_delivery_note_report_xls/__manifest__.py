# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Delivery Note - XLS",

    'summary': """
       Pegasus Delivery Note XLS""",

    'description': """
        Pegasus Delivery Note XLS
        + Version: 12.0.0.1:
        + Version: 12.0.0.2 - ( 06-Nov-2022) -> Update iso date
        + Version: 12.0.0.3 - ( 20-Nov-2022) -> Edit invoice address and shipping address by sale_id
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'stock',
    'version': '12.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [

        'reports/delivery_note_report.xml',
    ],
}