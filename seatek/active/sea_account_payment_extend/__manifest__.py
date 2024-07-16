# -*- coding: utf-8 -*-
{
    'name': 'Sea Account Payment Extend 1.0.1',
    'version': '12.0.1.0.1',
    'category': 'base',
    'summary': 'Extend Employee Model and Extend Contact Model',
    'description': """
        01. Create table account.payment.res.file
        02. Add advance_file_id
        0.0.0.2 : Inherit Account Payment by tkkhanh 
    """,
    'depends': ['account', 'payment', 'base'],
    'author': 'SEATEK',
    'website': 'https://seatek.com',
    'support': 'info@seatek.com',
    'data': [
        'security/ir.model.access.csv',
        'views/account_payment_res_file_view.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
