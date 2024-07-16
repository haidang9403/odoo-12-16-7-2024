{
    'name': "Sea Product Extend",

    'summary': """
       Sea Product Extend
       """,

    'description': """
        Sea Product Extend
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': '',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/product_category_view.xml',
        # 'views/product_product_view.xml',
        'views/product_template_view.xml',
    ],
    'installable': True,
}
