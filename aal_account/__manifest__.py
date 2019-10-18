{
    'name': 'AAL Account',
    'summary': 'Modify field in account module',
    'version': '12.0.1.0.0',
    'category': 'Account',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'account',
        'account_billing',
        'l10n_th_withholding_tax_cert'
    ],
    'data': [
        'views/account_billing_views.xml',
        'views/withholding_tax_cert.xml',
    ],
}
