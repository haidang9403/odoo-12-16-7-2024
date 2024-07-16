# -*- coding: utf-8 -*-
{
    'name': "Sea Inventory Extend",
    'summary': """
        Sea Inventory Extend
    """,
    'description': """
        + Add group senior_manager_inventory for button unlock/lock
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'views/stock_picking_view.xml',
        'security/senior_manager_inventory.xml',
    ],
    'installable': True,
}
