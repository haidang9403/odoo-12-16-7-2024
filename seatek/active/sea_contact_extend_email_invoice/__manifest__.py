# -*- coding: utf-8 -*-
{
    'name': "Contact Extend Email Invoice",

    'summary': """
        Contact Extend Email Invoice
    """,

    'description': """
        Contact Extend Email Invoice
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'product',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
