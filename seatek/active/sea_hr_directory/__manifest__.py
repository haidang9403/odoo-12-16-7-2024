# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sea HR Directory',
    'version': '12.1.0.0',
    'category': 'Employee',
    'summary': 'Sea HR Directory',
    'author': 'SEATEK',
    'description': "",
    'depends': ['hr', 'base', 'account'],
    'data': [
        'views/view_company_extends.xml',
        'views/view_hr_directory.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
