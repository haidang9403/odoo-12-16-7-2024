# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sea Employee Multi Company Extend',
    'version': '12.1.0.0',
    'category': 'Employee',
    'summary': 'Employee Company Information',
    'author': 'SEATEK',
    'description': "",
    'depends': ['hr', 'base', 'sea_multi_company_employee'],
    'data': [
        'view/view_employee_working_status.xml',
        'view/view_tree_super_manager.xml'
        # 'view/view_send_mail.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
