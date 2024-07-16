# -*- coding: utf-8 -*-
{
    'name': "Seacorp Sale Customer Partner Field",

    'summary': """
        Seacorp Sale Customer Partner Field""",

    'description': """
<<<<<<< HEAD:seatek/active/sc_sale_customer_partner_id_field/__manifest__.py
       Seacorp Sale Customer Partner Field
=======
       Seacorp Sale Customer Partner Field -> Merge to sea_sale_order_extend
       Old : 
>>>>>>> 8b5e6376818945ee379ea76920d0bb300793a0f7:seatek/inactive/sc_sale_customer_partner_id_field/__manifest__.py
    """,

    'author': "Seatek",
    'website': "https://www.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sale',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/sale_view.xml',
    ],
    # only loaded in demonstration mode
}