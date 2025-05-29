from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

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
        for line in self.order_line.filtered(lambda l: not l.is_discount):
            amount_tax_undiscounted += line.price_tax_undiscounted
            total += line.price_subtotal + line.price_unit * ((line.discount or 0.0) / 100.0) * line.product_uom_qty 
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