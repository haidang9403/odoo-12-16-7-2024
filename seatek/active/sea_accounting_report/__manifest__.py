# -*- coding: utf-8 -*-
{
    'name': "Sea Accounting Report",

    'summary': """
        Sea Accounting Report
    """,

    'description': """
        Sea Accounting Report
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale', 'report_xlsx_helper', 'report_xlsx', 'pos_retail'],

    # always loaded
    'data': [
        'views/account_invoice_view_extend_invoice_finished.xml',
        'reports/accounting_wizard.xml',
        'views/pos_config_view.xml',
    ],
    'installable': True,
}
