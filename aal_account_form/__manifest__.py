{
    'name': 'AAL_Account_Form',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'category': 'Report',
    'depends': [
        'web',
        'account',
    ],
    'data': [
        'data/paper_format.xml',
        'data/report_data.xml',
        'reports/account_style.xml',
        'reports/billing_form.xml',
        'reports/receipt_form.xml',
        'reports/delivery_order_form.xml',
        'reports/delivery_order_tax_invoice_form.xml',
    ],
    'installable': True,
}
