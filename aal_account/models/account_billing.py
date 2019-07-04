from odoo import fields, models, api
import odoo.addons.decimal_precision as dp


class AccountBilling(models.Model):
    _inherit = 'account.billing'

    subtotal = fields.Float(
        string='Subtotal',
        readonly=True,
        compute='_compute_subtotal',
    )
    withholding_tax = fields.Float(
        string='Withholding Tax',
        digits=dp.get_precision('Account'),
        required=True,
    )
    amount_total = fields.Float(
        string='Total',
        readonly=True,
        compute='_compute_amount_total',
    )

    @api.depends('invoice_ids')
    def _compute_subtotal(self):
        self.subtotal = sum(self.invoice_ids.mapped('amount_total'))

    @api.depends('invoice_ids', 'withholding_tax')
    def _compute_amount_total(self):
        self.amount_total = sum(self.invoice_ids.mapped('amount_total')) - self.withholding_tax
