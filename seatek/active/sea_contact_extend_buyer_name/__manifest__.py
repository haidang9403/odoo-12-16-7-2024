# -*- coding: utf-8 -*-
{
    'name': 'Contact Extend Buyer Name',
    'version': '12.0.0.1',
    'category': '',
    'summary': 'Extend Contact Model',
    'description': """
        Add Buyer's name in shipping address 
    """,
    'depends': ['base', 'contacts', 'sale'],
    'author': 'Seatek Team',
    'website': 'https://seatek.com',
    'support': 'info@seatek.com',
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
