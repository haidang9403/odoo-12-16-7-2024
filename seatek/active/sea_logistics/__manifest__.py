{
    'name': "Sea Logistics",

    'summary': """
       Sea Logistics
       """,

    'description': """
        Sea Logistics
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': 'stock',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sea_order_view_customer_received'],

    # always loaded
    'data': [
        'security/logistic_security.xml',
        'security/ir.model.access.csv',
        'views/logistic_menu_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
