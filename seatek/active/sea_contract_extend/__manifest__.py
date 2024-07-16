# -*- coding: utf-8 -*-
{
    'name': 'Open Sea Contract Extend 0.0.5',
    'version': '12.0.0.0.5',
    'summary': """Open Sea Contract Extend""",
    'description': 'Open Sea Contract Extend.'
'''
* Version = 12.0.0.0.5 -dkh 30112022
* Change tree view
* Change Group By Default
* Add color state='close' or 'cancel
-------------------------------------
* Version = 12.0.0.0.4 - dkh 15082022
* Add Menu Contract Period
------------------------------------- 
* Vesrion = 12.0.0.0.3 - dkh 12082022
* Add End Days 
''',
    'category': 'Open Sea Contract Extend',
    'author': 'Nam',
    'company': 'Seacorp',
    'website': "https://www.seacorp.com",
    'depends': ['base', 'hr', 'mail', 'hr_gamification', 'hr_contract', 'note'],
    'data': [
        'security/ir.model.access.csv',
        'views/sea_contract_extend.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
