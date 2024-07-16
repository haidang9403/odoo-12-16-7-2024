# -*- coding: utf-8 -*-
{
    'name': 'OpenSea Employee Extend 1.0.10',
    'version': '12.0.1.0.6',
    'summary': """Extend Employee OpenSea""",
    'description':

"""
1.0.10
    * SeaCode must have 'SC' if not write or create will return false
    * Auto SeaCode will not working.
1.0.9
    * Sort tree view hr_employee
    * Add filter and default filter tree view hr_employee
1.0.8
    * Add Sort Name in hr_department
    * Add Sequence int hr_job
"""

"""
1.0.7
    * Add bank, acc_number, acc_holder_name' 06052022
    * Invisible bank_account_id
    * Translate Vietnamese to English
1.0.6
    * Extend Employee OpenSea 1.0.6 | 07dec2020 by htkhoa.
""",
    'category': 'Employee',
    'author': 'SeaTek',
    'company': 'SeaTek',
    'website': "https://www.seatek.vn",
    'depends': ['base', 'hr', 'sea_menu_base', 'report_xlsx','website_hr_recruitment'],
    'data': [
        'views/hr_employee_bank_view.xml',
        'views/hr_department_extend_view.xml',
        'views/hr_employee_view.xml',
        'views/sea_employee_level.xml',
        'views/hr_employee_family_view.xml',
        'views/hr_notification.xml',
        'security/ir.model.access.csv',

    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
