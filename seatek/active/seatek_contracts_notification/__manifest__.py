# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Manage Contract status 1.0.2',
    'version': '12.0.1.0.2',
    'category': 'Contracts',
    'author': 'SEATEK',
    'summary': 'Contracts Notification and Manage Contract status',
    'description': """
Add all information on the employee form to manage contracts.
=============================================================

    * v1.0.1: Contract expiration date
    * v1.0.1: Automatically send email notifying Contracts about to expire

Inherit Mail Activity Type, Mail Activity, Contract by tkkhanh
    """,
    'website': 'https://www.odoo.com/page/employees',
    'depends': ['base', 'hr', 'web', 'hr_contract', 'mail', 'hr_contract_operating_unit', 'sea_contract_extend'],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        # 'data/mailbot_data.xml',
        'views/user_mails.xml',
        'views/create_mail_activity_type.xml',
        'views/create_mail_activity.xml',
        'views/database_uuid.xml',
        'views/hr_contract_type.xml',
        'views/view_hr_contract.xml',
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
