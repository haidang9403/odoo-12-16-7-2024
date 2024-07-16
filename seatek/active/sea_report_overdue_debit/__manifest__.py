# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sea Report Overdue Debit 1.0.0',
    'version': '12.1.0.0',
    'category': 'Account',
    'summary': 'Sea Report Overdue Debit',
    'author': 'SEATEK',
    'description': "",
    'depends': ['hr', 'base', 'account', 'sale', 'pos_retail','sea_contact_employee_extend'],
    'data': [
        'security/accounting_group.xml',
        'security/ir.model.access.csv',
        'security/credit_policy.xml',
        'views/js_template.xml',
        'views/report_overdue_debit.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_move_line.xml',
        'views/credit_policy.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/icon.png'],
    "qweb": [
    ],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
