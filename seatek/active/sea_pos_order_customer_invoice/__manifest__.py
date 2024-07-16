# -*- coding: utf-8 -*-
{
    'name': "Sea Pos Order Customer Invoice",

    'summary': """
       Sea Pos Order Customer Invoice""",

    'description': """
        Sea Pos Order Customer Invoice
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    'category': 'Pos Order',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'pos_retail', 'sea_invoice_consolidation', 'sea_issue_invoice_with_ts24'],

    # always loaded
    'data': [
        'views/pos_config_view.xml',
        'views/pos_templates.xml',
        'views/invoice_consolidation_view.xml',
        'views/pos_order_view.xml',
        'data/scheduler_data.xml',
    ],
    # 'qweb': ['static/src/xml/customer_get_invoice.xml'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
