# -*- coding: utf-8 -*-
{
    'name': "Tax Is VAT",

    'summary': """Add VAT indicator on tax groups and taxes""",

    'description': """
In some cases, we need to know if a tax is a value added tax. This module adds new field 'Is VAT' to the model account.tax.group and the model account.tax for that purpose

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': 'T.V.T Marine Automation (aka TVTMA),Viindoo',
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/account_tax_views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 9.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
