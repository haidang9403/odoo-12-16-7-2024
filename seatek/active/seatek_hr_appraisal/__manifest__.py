# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Seatek HR Appraisal 1.0.4',
    'version': '12.0.1.0.1',
    'category': 'Survey',
    'author': 'SEATEK',
    'summary': 'Employees KPI',
    'description':
    """
    1.0.4
        * Change interface - Free header of treeview
        * Remove create button.
        * Change security - add  hr_appraisal_user can read hr_appraisal model
    1.0.3
        * Add more colleague
    1.0.2
        * Fix Bug
        * Change Report View
    1.0.1
        * Import KIPS template
        * Tách view đánh giá -> 2 view Đánh giá Seacorp và Đánh giá KPIS
    1.0.0
        * Create hr survey - appraisal    
    """,
    'depends': ['web', 'base','hr','sea_multi_company_employee'],
    'installable': True,
    "application": True,
    'auto_install': False,
    'data': [
        'views/sea_user_notification.xml',
        'data/mail_data.xml',
        'data/ir_module_category_data.xml',
        'security/hr_appraisal_user_security.xml',
        'security/hr_appraisal_rule.xml',
        'reports/seatek_dexuat_sau_dgns_template.xml',
        'reports/seatek_ketqua_sau_dgns_template.xml',
        'reports/seatek_baocao_dgns_template.xml',
        'reports/seatek_export_appraisal_template.xml',
        'views/seatek_dexuat_sau_danhgia_nhansu.xml',
        'views/seatek_ketqua_danhgia_nhansu.xml',
        'views/seatek_hr_appraisal_detail_kpis_report_role.xml',
        'views/seatek_hr_appraisal_detail_seacorp_report_role.xml',
        'views/seatek_hr_appraisal_summary_report_role.xml',
        'views/report_template.xml',
        'reports/hr_appraisal_report_template.xml',
        'reports/pagerformat_hr_appraisal.xml',


        'security/ir.model.access.csv',
        'views/seatek_hr_survey.xml',
        'views/seatek_hr_survey_template.xml',
        'views/seatek_hr_survey_input_line.xml',
        'views/seatek_hr_survey_input.xml',
        'views/seatek_appraisal_hr.xml',
        'views/seatek_hddg.xml',
        'views/survey_kpis_template.xml',
        'views/seatek_assigned_appraisal.xml',
        'views/seatek_hr_appraisal_detail_kpis_report.xml',
        'views/seatek_hr_appraisal_detail_seacorp_report.xml',
        'views/seatek_hr_report_summary.xml',
        'views/seatek_hr_appraisal_period.xml',
        'views/seatek_import_appraisal.xml',
        'views/seatek_hr_appraisal.xml',
        'views/css_loader.xml',
    ],
    'qweb': [
        "static/src/xml/base.xml",
        'static/src/xml/survey_input_notification.xml',
    ],
    'images': ['static/description/iconseatek.png'],
    'website': "https://www.seatek.vn",
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
