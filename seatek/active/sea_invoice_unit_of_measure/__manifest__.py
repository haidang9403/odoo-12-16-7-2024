{
    'name': "Invoice Unit Of Measure",

    'summary': """
       Invoice Unit Of Measure
       """,

    'description': """
        - Create a list of units of measure for an invoice.
        - Add field when creating product.
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': 'accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/invoice_unit_of_measure_view.xml',
        'views/product_product_view.xml',
        # 'views/product_template_view.xml',
        # 'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
