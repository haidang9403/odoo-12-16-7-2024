# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Sale Quotation - XLS",

    'summary': """
       Pegasus Sale Quotation Report XLS""",

    'description': """
        Pegasus Sale Quotation Report XLS
        + Version: 12.0.0.1
        + Version: 12.0.0.2 - ( 06-Nov-2022) -> Update iso date
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'sale',
    'version': '12.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [

        'reports/sale_quotation_report.xml',
    ],
}