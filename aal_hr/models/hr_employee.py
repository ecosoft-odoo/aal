from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    address_home_id = fields.Many2one(
        'res.partner', 'Private Address',
        help='Enter here the private address of the employee,'
             'not the one linked to your company.',
        groups="hr.group_hr_user,base.group_private_addresses")
