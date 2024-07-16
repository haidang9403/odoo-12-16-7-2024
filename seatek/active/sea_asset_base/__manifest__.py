# -*- coding: utf-8 -*-
{
    'name': "Sea Asset Base 1.0.2",

    'summary': """
        Sea Asset Base
        
    """,

    'description': """
        Sea Asset Base
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'category': 'Asset',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['web','base', 'product', 'om_account_asset', 'mail','hr','sea_multi_company_employee','stock'],

    'data': [
        'security/asset_security.xml',
        'security/asset_rules.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/account_asset_asset_view.xml',
        'views/sea_office_view.xml',
        'reports/asset_wizard.xml',
        'views/asset_print_qrcode.xml',
        'reports/export_inventory_asset_wizard.xml',
        'reports/export_asset_transfer_wizard.xml',
        'reports/export_asset_repair_wizard.xml',
        'reports/export_asset_inventory_pkk_wizard.xml',
        'reports/asset_print_qrcode_pdf.xml',
        'reports/asset_inventory_report_wizard.xml',
        'reports/export_asset_profile.xml',
        'views/asset_transfer_view.xml',
        'views/asset_repair_view.xml',
        'views/asset_inventory_view.xml',
        'views/asset_adjustment.xml',
        'views/hr_employee_temporary.xml',
        'views/asset_category_view.xml',

        # 'views/fixed_asset_card.xml',
    ],
    'installable': True,
    'website': "https://www.seatek.vn",
    'bootstrap': True,  # load translations for login screen,
    'license': 'LGPL-3',
}
