# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus PRO-FORMA Invoice - XLS",

    'summary': """
       Pegasus PROFORMA Invoice Report - XLS""",

    'description': """
        Pegasus PROFORMA Invoice Report - XLS
        + Version: 12.0.0.1
        + Version: 12.0.0.2 -> Edit signature table 
        + Version: 12.0.0.3 - (06-Nov-2022 ) -> Update iso date
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'sale',
    'version': '12.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [

        'reports/proforma_invoice_report.xml',
    ],
}
