# -*- coding: utf-8 -*-
{
    'name': "Sea Account Financial Report for Sales",
    'summary': """
        Sea Account Financial Report for Sales
    """,
    'description': """
        Sea Account Financial Report for Sales
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'date_range', 'report_xlsx', 'sale'],

    # always loaded
    'data': [
        'wizard/sea_aged_partner_balance_wizard_view.xml',
    ],
    'installable': True,
}
