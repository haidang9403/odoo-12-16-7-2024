# -*- coding: utf-8 -*-
{
    'name': "Issue Multiple Invoices",

    'summary': """
        SeaCorp Issue Multiple Invoices
    """,

    'description': """
        Select multiple invoices to issue
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'data/ir_action_server_data.xml',
        'views/account_invoice_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
