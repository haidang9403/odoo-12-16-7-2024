# -*- coding: utf-8 -*-
{
    'name': "Sea Company Extend",

    'summary': """
        Thêm 1 field thể hiện tên nước ngoài của Công ty""",
    'category': 'sale',
    'version': '1.0.0.1',

    'description': """
       Thêm 1 field thể hiện tên nước ngoài của Công ty
    """,

    'author': "Seatek",
    'website': "https://home.seacorp.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list


    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/company_view.xml',
    ],
    # only loaded in demonstration mode
}