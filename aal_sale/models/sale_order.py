from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    attention_id = fields.Many2one(
        string='Attention:',
        comodel_name='res.partner',
        domain="[('parent_id', '!=', False),"
        "('parent_id', '=', partner_id)]",
    )
