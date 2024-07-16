# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Seatek Manage mail Notification 1.0.0',
    'version': '12.0.1.0.0',
    'category': 'Mail',
    'author': 'SEATEK',
    'summary': 'Manage mail notifications',
    'description': """
Add all information on the employee form to manage contracts.
=============================================================

    * v1.0.1: Prevent email sending if not a 'Production' database,

Inherit Mail Activity Type, Mail Activity by tkkhanh
    """,
    'website': 'https://www.odoo.com/page/employees',
    'depends': ['mail'],
    'data': [
    ],
    'support': 'info@seatek.com',
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
