# -*- coding: utf-8 -*-
{
    'name': "Sea Sale Order With Customer TAX",

    'summary': """
       Sea Sale Order With Customer TAX""",

    'description': """
        Sea Sale Order With Customer TAX
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'Sale Order',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'to_base', 'l10n_vn_c200'],

    # always loaded
    'data': [
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
        'views/account_invoice_view.xml',
    ],
}
