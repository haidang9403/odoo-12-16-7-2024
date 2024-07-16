# -*- coding: utf-8 -*-
{
    'name': 'Sea Contact, Employee, User Extend 1.0.1',
    'version': '12.0.1.0.1',
    'category': 'base',
    'summary': 'Extend Employee Model and Extend Contact Model',
    'description': """
        01. Add employee_id
        02. Auto create Contact for Employee
        03. Auto create User for Employee
        0.0.0.2 : Inherit Contact and EmployeeType by tkkhanh 
    """,
    'depends': ['base', 'account',  'contacts', 'hr', 'seacorp_pos_search_unaccent','pos_retail'],
    'author': 'SEATEK',
    'website': 'https://seatek.com',
    'support': 'info@seatek.com',
    'data': [
        'security/accounting_group.xml',
        'views/sea_contact.xml',
        'views/create_contract_of_employee.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
