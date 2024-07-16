{
    'name': 'Delivery Packing Log Report',
    'summary': 'Sea Delivery Packing Log Report',
    'description': """
        Sea Delivery Packing Log Report
""",
    'author': "SeaTek_Team",
    'website': 'https://seatek.vn',
    'version': '12.0.0.1',

    'depends': ['sale_stock', 'sale_management'],

    'data': [
        'report/action_report.xml',
        'security/ir.model.access.csv'],
    'installable': True,
}
