# -*- coding: utf-8 -*-
{
    'name': "Sea Poss Extend",
    'summary': """
        Extend function of POS """,

    'description': """
        12.0.0.1 : Initial
        
    """,
    'author': "KhoaHt",
    'website': "https://seacorp.vn",
    'category': 'POS',
    'version': '12.0.0.1.0',
    'depends': [
        'base',
        'sale_stock',
        'account',
        'account_cancel',
        'pos_restaurant',
        'bus',
        'stock',
        'purchase',
        'product',
        'product_expiry',
    ],

    'data': [
        'views/pos_config.xml',
    ],
}