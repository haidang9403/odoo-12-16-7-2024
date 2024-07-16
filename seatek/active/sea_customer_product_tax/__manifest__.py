# -*- coding: utf-8 -*-
{
    'name': "Sea Customer Product TAX",

    'summary': """
       Sea Customer Product TAX""",

    'description': """
        Sea Customer Product TAX
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': 'accounting',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'to_base', 'l10n_vn_c200'],

    # always loaded
    'data': [
        'views/customer_product_tax_view.xml',
        'views/customer_category_tax_view.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
        'security/customer_product_tax_security.xml',
    ],
    'installable': True,
}