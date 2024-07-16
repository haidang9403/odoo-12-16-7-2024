# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Seatek Attendances 1.0.5',
    'version': '12.0.1.0.5',
    'author': 'SEATEK',
    'category': 'Human Resources',
    'summary': 'Track employee attendance',
    'description': """
This module aims to manage employee's attendances.
==================================================

Keeps account of the attendances of the employees on the basis of the
actions(Check in/Check out) performed by them.
0.0.0.2 : Inherit Contact Type by tkkhanh
       """,
    'depends': ['hr', 'barcodes', 'report_xlsx', 'sea_multi_company_employee'],
    'inherit_id': 'web.assets_frontend',
    'data': [
        'data/ir_module_category_data.xml',
        'security/hr_attendance_security.xml',
        'security/ir.model.access.csv',
        'data/timesheet_symbol_data.xml',
        'views/attendance_js_template.xml',
        'views/timekeeper.xml',
        'views/sea_hr_calendar_view.xml',
        'views/sea_hr_attendance_view.xml',
        'views/sea_hr_attendance_month_view.xml',
        'views/sea_hr_calendar_employee_view.xml',
        'views/sea_hr_attendance_realtime.xml',
        'views/sea_hr_attendance_config.xml',
        'views/report.xml',
        'views/menu.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'qweb': [],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'support': 'info@seatek.com',
    'bootstrap': True,
    'license': 'LGPL-3',
}