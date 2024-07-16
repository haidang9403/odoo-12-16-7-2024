# -*- coding: utf-8 -*-
{
    'name': "Issue Invoices with TS24",

    'summary': """
        Issue Invoices With TS24
    """,

    'description': """
        Issue Invoices With TS24
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sea_invoice_consolidation', 'to_vietnamese_number2words'],

    # always loaded
    'data': [
        # 'data/ir_action_server_data.xml',
        # 'views/issue_invoice_views.xml',
        # 'security/ir.model.access.csv',
        # 'data/ir_action_send_to_issue_invoice.xml',
        'data/ir_action_switch_cron_job.xml',
        'data/ir_action_issue_invoice.xml',
        'data/ir_action_sign_invoice.xml',
        'views/res_config_settings_views.xml',
        'views/invoice_consolidation_views.xml',
    ],
    'installable': True,
}
