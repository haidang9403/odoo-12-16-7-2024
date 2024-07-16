# -*- coding: utf-8 -*-
{
    'name': "SEA PO REPORT",
    'summary': """
        Sea Purchase Order Report
    """,
    'description': """
        Sea Purchase Order Report
    """,
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'reports/action_report.xml',
        'reports/paper_format.xml',
        'reports/dannygreen_po_template.xml',
    ],
    'installable': True,
}
