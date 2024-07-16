# -*- coding: utf-8 -*-
{
    'name': "Hide Button POS Auto Invoice",

    'summary': """
       Hide Button POS Auto Invoice""",

    'description': """
        Hide Button POS Auto Invoice
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': '',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'pos_restaurant', 'pos_retail'],

    # always loaded
    'data': [
        'views/pos_templates.xml',
    ],
    'installable': True,
}
