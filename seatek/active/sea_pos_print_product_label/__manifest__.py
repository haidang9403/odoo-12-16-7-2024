# -*- coding: utf-8 -*-
{
    'name': "Print Product Label POS",

    'summary': """
        Print Product Label POS
    """,

    'description': """
        Print Product Label POS
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'pos_retail'],

    # always loaded
    'data': [
        'views/products_view.xml',
        'views/pos_template.xml',
        'views/pos_config_view.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}