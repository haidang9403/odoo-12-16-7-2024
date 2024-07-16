# -*- coding: utf-8 -*-
{
    'name': "Report Data Accounting",

    'summary': """
        Sea Report Data Accounting
    """,

    'description': """
        Sea Report Data Accounting
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'report_xlsx_helper', 'report_xlsx'],

    # always loaded
    'data': [
        'views/account_invoice_view.xml',
        'reports/accounting_wizard.xml',
    ],
    'installable': True,
}
