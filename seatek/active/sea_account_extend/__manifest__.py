# -*- coding: utf-8 -*-
{
    'name': "Sea Account Extend 1.0.1",
    'summary': """
        Sea Account Extend
    """,
    'description': """
        Sea Account Extend
    """,
    'sequence': 16,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'om_account_asset', 'sale_stock'],

    # always loaded
    'data': [
        'views/transaction_type_view.xml',
        'security/ir.model.access.csv',
        'security/transaction_type_security.xml',
        'views/stock_view.xml',
        'views/account_move_view.xml',
    ],
    'qweb':['views/reconcile_template.xml'],
    'installable': True,
}
