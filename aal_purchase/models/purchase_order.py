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

    # @api.multi
    # def _add_approver(self, invoices):
    #     values = super()._add_approver()
    #     values['approver'] = self.approver
    #     return values
