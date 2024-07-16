# -*- coding: utf-8 -*-
{
    'name': "Sea Sale Channel",

    'summary': """
        Sea Sale Channel
    """,
    'description': """
       Sea Sale Channel
    """,

    'author': "Seatek",
    'website': "https://home.seacorp.vn",
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sales_team'],
    # always loaded
    'data': [
        'views/sale_channel_view.xml',
        'views/sale_order_extend_view_channel.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}