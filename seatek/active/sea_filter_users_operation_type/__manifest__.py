# -*- coding: utf-8 -*-
{
    'name': "Filter Users Operation Type",

    'summary': """
        Sea Filter Users Operation Type
    """,
    'description': """
       Sea Filter Users Operation Type
    """,

    'author': "Seatek",
    'website': "https://home.seacorp.vn",
    'category': '',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'purchase', 'sale', 'consignment_management_ept'],
    # always loaded
    'data': [
        'views/res_users_view.xml',
        'views/stock_picking_view.xml',
        'views/purchase_order_view.xml',
        'views/sale_order_view.xml',
        'views/consignment_process_ept_view.xml',
        'security/operation_type_security.xml',
        'security/users_security.xml',
    ],
    'installable': True,
}