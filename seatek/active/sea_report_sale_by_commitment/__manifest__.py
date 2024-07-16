# -*- coding: utf-8 -*-
{
    'name': "Report Sale Order By Commitment Date",

    'summary': """
        Report Sale Order By Commitment Date
    """,

    'description': """
        Report Sale Order By Commitment Date
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'report_xlsx_helper', 'report_xlsx', 'pos_retail'],

    # always loaded
    'data': [
        'views/account_invoice_view_extend_invoice_finished.xml',
        'reports/sale_wizard.xml',
        'views/sale_channel_view.xml',
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/sales_team_view.xml',
        'security/sale_channel_security.xml',
    ],
    'installable': True,
}
