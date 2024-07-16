{
    'name': "Add Contract for Customer",

    'summary': """
       Add Contract for Customer
       """,

    'description': """
        Add Contract for Customer
    """,

    'author': "SeaTek_TEAM",
    'website': "https://www.seacorp.vn",

    'category': 'partner',
    'version': '12.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
}
