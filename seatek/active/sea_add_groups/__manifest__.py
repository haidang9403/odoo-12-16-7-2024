# -*- coding: utf-8 -*-
{
    'name': "Sea Add Groups",

    'summary': """
        Sea Add Groups
    """,

    'description': """
        Sea Add Groups
    """,

    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',

    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['web'],

    'data': [
        'security/groups_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
