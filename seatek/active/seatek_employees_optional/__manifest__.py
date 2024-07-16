# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Seatek Employees Optional 1.0.2',
    'version': '12.0.1.0.2',
    'category': 'Employee',
    'author': 'SEATEK',
    'summary': 'Employees Optional',
    'description':
    """
    1.0.2
        * Import Country
        * Translate Vietnames to English
    1.0.1
        * Deny space input to Identity Id, Passport No, Phone, Mobile,MST TTCN, BHXH, BankID
        * Add BHYT
        * Add Permanent City, Permanent District
        * Add Temporary City, Temporary District
        * Add City and District data
        * Import District with template
    """,
    'depends': ['web', 'base', 'hr'],
    'installable': True,
    'auto_install': True,
    'data': [
        'views/employees_optional.xml',
        'views/employees_template.xml',
        'data/district_data.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
