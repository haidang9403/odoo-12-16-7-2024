# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Seatek HR Bank Info',
    'version': '12.0.1.0.1',
    'summary' : 'HR Bank Info',
    'description': 'HR Bank Info'
        """
        * Add menu Acounting: OpenSean->Accounting->Bank list
        * Import Bank list from excel
        Verison: 12.0.1.0.1
        """,

    'depends': ['web', 'base', 'hr'],
    'installable': True,
    'auto_install': True,
    'data': [
        'views/seatek_hr_bank_info.xml',
    ],
    'qweb': [
    ],
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
