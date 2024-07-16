# -*- coding: utf-8 -*-
{
    'name': "Sale Order Extend Discount Line",

    'summary': """
        Sea Sale Order Extend Discount Line
    """,

    'description': """
        Sea Sale Order Extend Discount Line
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sea_account_extend'],

    'data': [
        'security/discount_line_on_customer_security.xml',
        'views/discount_line_on_customer_view.xml',
        'views/transaction_type_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}