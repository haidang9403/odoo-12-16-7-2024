# -*- coding: utf-8 -*-
{
    'name': "Invoice View Search Commitment Date",

    'summary': """
        Invoice View Search Commitment Date
    """,

    'description': """
        Search input for Commitment Date in Invoice screen
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        'views/account_invoice_view.xml',
    ],
    'installable': True,
}
