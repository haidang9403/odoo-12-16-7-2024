# -*- coding: utf-8 -*-
###################################################################################
# TKK 14/12/2022
###################################################################################
{
    'name': 'Seatek Employee History 1.0.0',
    'version': '12.0.1.0.0',
    'summary': """History Of Employees In Your Company""",
    'description': 'Track the History of Employees in your Company',
    'category': 'Generic Modules/Human Resources',
    'author': 'SEATEK',
    'depends': ['hr', 'hr_contract', 'oh_employee_creation_from_user', 'sea_multi_company_employee'],
    'installable': True,
    "application": True,
    'auto_install': False,
    'data': ['security/secure.xml',
             'security/ir.model.access.csv',
             'views/employee_history.xml',
             'views/history_views.xml',
             ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}