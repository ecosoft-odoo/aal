from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    notes = fields.Text(
        default="1) Shipping Method: \n2) Payment Term: \n3) Delivery date: ")
    approver_id = fields.Many2one(
        string='Approver',
        comodel_name='res.users',
        states={'draft': [('readonly', False)]},
        readonly=True,
    )
    attention_id = fields.Many2one(
        string='Attention:',
        comodel_name='res.partner',
        domain="[('parent_id', '!=', False),"
        "('parent_id', '=', partner_id)]",
    )
