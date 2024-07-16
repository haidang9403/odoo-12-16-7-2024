# -*- coding: utf-8 -*-
{
    'name': "Sea Manufacturing Account",
    'summary': """
        Sea Manufacturing Account
    """,
    'description': """
        Sea Manufacturing Account
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['mrp', 'account', 'stock', 'stock_account', 'purchase'],

    # always loade
    'data': [
        'views/mrp_workcenter_view.xml',
        'views/mrp_product_costing_parameters.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_product_costing_view.xml',
        'views/mrp_postings_view.xml',
        'data/ir_action_financial_closure.xml'
    ],
    'installable': True,
}
