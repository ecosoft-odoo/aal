# -*- coding: utf-8 -*-
{
    'name': 'Adjust all modules for only AAL project',
    'version': '8.0.1.0.0',
    'author': 'Ecosoft Co. Ltd.',
    'license': 'AGPL-3',
    'description': """
    """,
    'category': 'Uncategorized',
    'depends': [
        'purchase',
        'sale_customer_attn',
        'account_billing',
        'l10n_th_account',
        'account_refund_linked_invoice',
    ],
    'data': [
        'views/purchase_view.xml',
        'views/sale_view.xml',
        'views/account_billing.xml',
        'views/account_voucher_view.xml',
    ],
    'js': [],
    'css': [],
    'auto_install': False,
    "installable": True,
    'external_dependencies': {
        'python': [],
    },
}
