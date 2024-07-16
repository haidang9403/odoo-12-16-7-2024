# -*- coding: utf-8 -*-
{
    'name': "Invoice Consolidation",

    'summary': """
        Invoice Consolidation
    """,

    'description': """
        Invoice Consolidation to issue invoice
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'product', 'mail', 'pos_retail'],

    # always loaded
    'data': [
        'views/invoice_consolidation_views.xml',
        'security/ir.model.access.csv',
        'data/ir_action_push_invoice_to_issue.xml',
        'data/ir_action_invoice_consolidation.xml',
        'views/account_invoice_views.xml',
        'views/res_company_view.xml',
        'security/consolidation_security.xml',
        # 'views/product_product_views.xml',
    ],
    'installable': True,
}
