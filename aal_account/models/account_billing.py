from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class AccountBilling(models.Model):
    _inherit = 'account.billing'

    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_amount',
    )
    amount_diff_name = fields.Char(
        default='Withholding Tax',
        help='change name',
    )
    amount_diff = fields.Float(
        digits=dp.get_precision('Account'),
    )
    amount_total = fields.Float(
        string='Total',
        compute='_compute_amount',
    )

    @api.depends('invoice_ids', 'amount_diff')
    def _compute_amount(self):
        self.subtotal = sum(self.invoice_ids.mapped('amount_total'))
        self.amount_total = self.subtotal + self.amount_diff
