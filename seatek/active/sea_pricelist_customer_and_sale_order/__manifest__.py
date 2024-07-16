# -*- coding: utf-8 -*-
{
    'name': "SEA PriceList Customize",

    'summary': """
        SEA PriceList Customize
    """,
    'description': """
       SEA PriceList Customize
    """,

    'author': "Team_SeaTek",
    'website': "https://home.seacorp.vn",
    'category': '',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'sale'],
    # always loaded
    'data': [
        'views/res_partner_view.xml',
        'views/product_pricelist_view.xml',
    ],
    'installable': True,
}