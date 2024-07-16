{
    'name' : 'E-Invoice S-Invoice Integrator',
    'version': '1.0.3',
    'author' : 'T.V.T Marine Automation (aka TVTMA),Viindoo',
    'website': 'https://viindoo.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'apps.support@viindoo.com',
    'summary': """
Integrates with S-Invoice service to issue legal e-Invoice
    """,
    'summary_vi_VN': """
Tích hợp với dịch vụ hoá đơn điện tử S-Invoice
    """,
    'sequence': 30,
    'category': 'Accounting',
    'description': """
Key Features
============
#. Issue S-Invoices from Odoo Invoices which are either in Open or Paid status
#. Generate Exchange Version of the issued invoice and store it in Odoo for later download
#. Generate Converted Version of the issued invoice and store it in Odoo for later download
#. S-Invoice will be set as Paid automatically upon its corresponding Odoo invoice will be set as Paid
#. S-Invoice will be reopen (from Paid) automatically upon its corresponding Odoo invoice will be reopened from Paid
#. Cancel issued S-Invoices
#. Manage Odoo invoices based on S-Invoice status:

   - Not Issued: Odoo invoices that have no corresponding S-Invoice issued
   - Issued and not Paid: Odoo invoices that have corresponding S-Invoice issued but not set as paid
   - Paid: Odoo invoices that have corresponding S-Invoice issued and paid
   - Issued but Cancelled: Odoo invoices that have corresponding S-Invoice issued but cancelled already

#. Easy to define and manage invoice series, invoice templates, invoices type according to the state rules.
#. Invoice Serial can be set for company (in Accounting > Configuration > Settings) and Account Journal so that you will have

   - Multi-company environment support for different invoice serials
   - Multi-Serial support for the same company: you can issue invoices with different serials that you have registered with
     S-Invoice and accepted by the state authority

#. Invoice template can be set for companies (in Accounting > Configuration > Settings) and account journals so that you will have

   - Multi-company environment support for different invoice templates
   - Multi-Template support for the same company: you can issue invoices with different templates that you have registered with
     S-Invoice and accepted by the state authority

#. Invoice type can be set for companies (in Accounting > Configuration > Settings) and account journals so that you will have 

   - Multi-company environment support for different invoice types
   - Multi-Type support for the same company: you can issue invoices with different types that you have registered with
     S-Invoice and accepted by the state authority

#. Support Odoo's deposit mechanism by issuing S-Invoice with adjustment line. For example,

   - First invoice, consists of a single line for 10% as deposit
   - Second invoice, consists of a single line for 20% as deposit
   - Final invoice, consists of products/services lines and the negative line to compensate the previous deposit.

#. Send Invoice now attaches S-Invoice instead of the default Odoo invoice template
#. Customer Portal

   - Customer can download the display version of S-Invoice in PDF format that is also embed an EU's Factur-X standard compliance attachment so that she/he can import into her/his own Odoo.
   - Customer can print the display version of the S-Invoice
   - Customer can download the zipped XML version of S-Invoice so that she or he can import it any software that support S-Invoice XML

#. Support Sanbox mode for your testing before launching in production
#. Smart enough to avoid you from issuing later invoice that have later date than the one of the earlier invoices that have
   not been issued
#. A large of smart and comprehensive messages that can help you on the context so that you can easily solve any issue with
   the integration by on your own before request help from technicians
#. Multiligual support for issuing to foreign customers according to the state rules: Invoice must be presented in Vietnamese
   and may have another language additionally.

Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,
    'depends': ['to_base', 'l10n_vn_c200', 'to_vietnamese_number2words', 'to_legal_invoice_number'],
    'data': [
        'data/company_data.xml',
        'data/scheduler_data.xml',
        'wizard/account_invoice_sinvoice_cancel_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_journal_views.xml',
        'views/account_journal_dashboard.xml',
        'views/account_invoice_view.xml',
        'views/account_portal_templates.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 99.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
