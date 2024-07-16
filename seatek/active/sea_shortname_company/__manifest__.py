# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Seatek Short Name Company 1.0.0',
    'version': '1.0.0',
    'category': 'Company',
    'summary': 'Company Information',
    'description': "",
    'depends': ['base', 'sea_company_extended'],
    'data': [
        'views/company_order_by.xml',
        'views/sea_shortname_company_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    'website': "",
    'license': 'LGPL-3',
}
