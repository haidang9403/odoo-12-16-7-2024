# -*- coding: utf-8 -*-
{
    'name': 'Sea Employee Report 1.0.1',
    'version': '12.0.1.0.0',
    'summary': """""",
    'description':
"""
1.0.0
    * Sea Employee Report
    * Report Biến Động Nhân Sự Seacorp
""",
    'category': 'Employee',
    'author': 'SeaTek',
    'company': 'SeaTek',
    'website': "https://www.seatek.vn",
    'depends': ['base', 'hr', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
    ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
