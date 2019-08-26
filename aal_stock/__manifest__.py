{
    'name': 'AAL Stock',
    'summary': 'Modify field in stock module',
    'version': '12.0.1.0.0',
    'category': 'Stock',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'stock',
    ],
    'data': [
        'report/report_deliveryslip.xml',
    ],
}
