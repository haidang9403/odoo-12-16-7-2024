# -*- coding: utf-8 -*-
{
    'name': "Sea Sales Department",

    'summary': """
        Sea Sales Department
    """,

    'description': """
        Sea Sales Department
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sea_filter_users_operation_type'],

    'data': [
        'views/sales_department_view.xml',
        'views/sale_order_view.xml',
        'views/res_users_view.xml',
        'views/crm_team_view.xml',
        'security/ir.model.access.csv',
        'security/sales_department_security.xml',
    ],
    'installable': True,
}
