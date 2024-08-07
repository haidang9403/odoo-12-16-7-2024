# -*- coding: utf-8 -*-
{
    'name': "Sea Pegasus Purchase Report - PDF",

    'summary': """
        Sea Pegasus Purchase Report PDF""",

    'description': """
        Sea Pegasus Purchase Report PDF
        + Version: 12.0.0.1
        + Version: 12.0.0.2 -> Edit ISO number
        + Version: 12.0.0.3 - (06-Nov-2022) -> Update iso date
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'purchase',
    'version': '12.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/pegasus_action_report.xml',
        'report/pegasus_purchase_order_report.xml',
    ],
    'installable': True,
    'application': False,
}