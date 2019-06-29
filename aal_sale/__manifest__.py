{
    'name': 'AAL Sale',
    'summary': 'Modify field in sale module',
    'version': '12.0.1.0.0',
    'category': 'Sale',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        'views/sale_order_views.xml',
    ],
}
