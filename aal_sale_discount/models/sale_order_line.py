# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_discount = fields.Boolean(
        related='product_id.is_discount',
        store=True,
    )
    price_tax_undiscounted = fields.Float(compute='_compute_price_tax_undiscounted', string='Total Tax Before Discount', readonly=True, store=True)


    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_price_tax_undiscounted(self):
        """
        Compute price tax undiscounted of the SO line.
        """
        for line in self:
            taxes_undiscounted = line.tax_id.compute_all(line.price_unit, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax_undiscounted': sum(t.get('amount', 0.0) for t in taxes_undiscounted.get('taxes', [])),
            })

