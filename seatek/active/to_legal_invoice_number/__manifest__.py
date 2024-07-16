# -*- coding: utf-8 -*-
{
    'name': "Legal Invoice Number",

    'summary': """
An additional number for invoice""",

    'description': """
A new field 'Legal Number' has been added to the invoice model to allow users to:

* Input an additional invoice number for legal purpose
* Search invoice by legal number

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'data/ir_action_server_data.xml',
        'views/account_invoice_views.xml',
    ],
    'price': 9.9,
    'currency': 'EUR',
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
}
