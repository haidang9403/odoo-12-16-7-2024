{
    "name": "Seatek Product Report (by location) 1.0.1",
    "summary": "Báo cáo tình trạng tồn kho theo lô",
    "description": """
        Version 1.0.0:
            + Tạo module
    """,
    "version": "1.0.0",
    "category": "stock",
    "website": "https://seatek.vn",
    "author": "Seatek, Anh Khoa",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
        "pos_retail",
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/product_report_view.xml',
        'views/product_cost_lot.xml',
        'report/templates/template_product_cost_lot.xml',
    ],
    "images": ["static/description/iconseatek.png"],
    "application": False,
    "installable": True,
}
