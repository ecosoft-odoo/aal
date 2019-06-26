{
    'name': 'AAL Purchase',
    'summary': 'Modify field in purchase module',
    'version': '12.0.1.0.0',
    'category': 'Purchases',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order_views.xml',
    ],
}
