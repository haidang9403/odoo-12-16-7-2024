{
    'name': "Customer Received",

    'summary': """
       Delivery date while customer received
       """,

    'description': """
        Delivery date while customer received
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': 'stock',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale'],

    # always loaded
    'data': [
        'views/stock_picking_views.xml',
        'views/sale_order_views.xml',
        'views/sale_order_templates.xml',
    ],
    'installable': True,
}
