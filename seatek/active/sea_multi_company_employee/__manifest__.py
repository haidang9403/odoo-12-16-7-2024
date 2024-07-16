# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sea Multi Company Employee 1.0.2',
    'version': '12.0.1.0.7',
    'category': 'Employee',
    'summary': 'Employee Company Information',
    'author': 'SEATEK',
    'description': "",
    'depends': ['hr', 'base', 'hr_contract', 'sea_employee_extend', 'hr_org_chart'],
    'data': [
        # 'data/ir_module_category_data.xml',
        'security/security_multi_company.xml',
        'security/ir.model.access.csv',
        'views/view_base_group.xml',
        # 'views/group_view_edit_view.xml',
        'views/create_multi_company_employee.xml',
        'views/multi_company_employee_view.xml',
        'views/multi_company_employee_template.xml',
        'views/private_information.xml',
        'views/work_information.xml',
        'views/hr_settings.xml',
        'views/seagroup.xml',
        'views/create_employee_button_view.xml',
        'views/hr_department_view.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [
        'views/create_button_template.xml',
    ],
    'images': ['static/description/icon.png'],
    'website': "https://www.seatek.vn",
    'license': 'LGPL-3',
}
