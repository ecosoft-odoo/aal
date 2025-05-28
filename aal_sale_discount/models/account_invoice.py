from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    discount_untaxed = fields.Monetary(
        string='Discount Untaxed',
        compute='_compute_discount',
        store=True,
        readonly=True,
    )
    discount_total = fields.Monetary(
        string='Discount',
        compute='_compute_discount',
        store=True,
        readonly=True,
    )
    amount_untaxed_undiscounted = fields.Float(
        string='Amount Untaxed Before Discount', 
        compute='_compute_undiscounted',
        digits=0,
    )
    amount_total_undiscounted = fields.Float(
        string='Total Before Discount', 
        compute='_compute_undiscounted',
        digits=0,
    )

    @api.one
    def _compute_undiscounted(self):
        total = amount_tax_undiscounted = 0.0
        for line in self.invoice_line_ids.filtered(lambda l: not l.is_discount):
            amount_tax_undiscounted += line.price_tax_undiscounted
            total += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0) * line.quantity 
        self.amount_untaxed_undiscounted = total
        self.amount_total_undiscounted = total + amount_tax_undiscounted

    @api.depends('amount_untaxed')
    def _compute_discount(self):
        for order in self:
            discount_untaxed = order.amount_untaxed_undiscounted - order.amount_untaxed
            discount_total = order.amount_total_undiscounted - order.amount_total
            order.update({
                'discount_untaxed': discount_untaxed,
                'discount_total': discount_total,
            })

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    is_discount = fields.Boolean(
        related='product_id.is_discount',
        store=True,
    )
    price_tax_undiscounted = fields.Float(compute='_compute_price_tax_undiscounted', string='Total Tax Before Discount', readonly=True, store=True)


    @api.depends('quantity', 'discount', 'price_unit', 'invoice_line_tax_ids')
    def _compute_price_tax_undiscounted(self):
        """
        Compute price tax undiscounted of the SO line.
        """
        for line in self:
            taxes_undiscounted = line.invoice_line_tax_ids.compute_all(line.price_unit, line.invoice_id.currency_id, line.quantity, line.product_id, line.invoice_id.partner_id)
            line.update({
                'price_tax_undiscounted': sum(t.get('amount', 0.0) for t in taxes_undiscounted.get('taxes', [])),
            })