{
    'name': 'AAL_Purchase_Form',
    'version': '12.0.1.0.0',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'website': 'https://github.com/ecosoft-odoo/aal',
    'category': 'Report',
    'depends': [
        'web',
        'purchase',
        'aal_purchase',
    ],
    'data': [
        'data/paper_format.xml',
        'data/report_data.xml',
        'reports/purchase_order_form.xml',
        'reports/purchase_style.xml',
    ],
    'installable': True,
}
