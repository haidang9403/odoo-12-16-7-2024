# -*- coding: utf-8 -*-
{
    'name': "Financial Income Account Type",
    'name_vi_VN': "Kiểu tài khoản Doanh thu Tài chính",

    'summary': """
Tạo thêm kiểu tài khoản Doanh thu Tài chính""",
'summary_vi_VN': """
Add Financial Income Account Type""",

    'description': """
* New Account Type

  * Name: Financial Income
  * xml_id: to_account_financial_income.data_account_type_financial_income

    """,
    'description_vi_VN': """
* Kiểu tài khoản mới

  * Tên: Doanh thu Tài chính
  * xml_id: to_account_financial_income.data_account_type_financial_income

    """,

    'author': "T.V.T Marine Automation (aka TVTMA),Viindoo",
    'website': "https://viindoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'data/data_account_type.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': True,
}
