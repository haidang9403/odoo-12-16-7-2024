# -*- coding: utf-8 -*-
{
    'name': "Seacorp Pos Report for VivoCity",

    'summary': """
       Seacorp Pos Report for VivoCity""",

    'description': """
        Seacorp Pos Report for VivoCity
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'Point of Sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'pos_retail', 'point_of_sale', 'report_xlsx_helper', 'report_xlsx'],

    # always loaded
    'data': [
        'views/pos_sale_wizard.xml',
        'data/scheduler_data.xml',
    ],
}
