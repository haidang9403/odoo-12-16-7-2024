{
    "name": "Seatek Vietnam's region",
    "version": "1.0.0",
    "description": """
        Version 1.0.0:
            + Tạo module
    """,
    'license': 'AGPL-3',
    "author": "Seatek, Anh Khoa",
    "website": "https://www.seatek.vn/",
    "category": "Các Miền của Việt Nam",
    "summary": "Các Miền của Việt Nam",
    "depends": ['base', 'contacts', 'sale'],
    "data": [
        "views/region_view.xml",
        "security/ir.model.access.csv",
    ],
    "sequence":10,
    "demo": [],
    'installable': True,
    "application": False,
    "auto_install": True
}
