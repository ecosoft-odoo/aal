# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
{
    'name': 'Ecosoft FARM',
    'summary': 'Ecosoft - Featured Addons Resource Management',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'website': 'https://github.com/ecosoft-odoo/addons',
    'author': 'Ecosoft',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale',
    ],
    'data': [
        'security/res_groups.xml',
        'views/res_config_settings.xml',
    ],
}
