# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

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
        'reports/receipt_form.xml',
        'reports/tax_invoice_form.xml',
    ],
    'installable': True,
}
