from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # partner_attn_id = fields.Many2one(
    #     'res.partner',
    #     string='ATTN.',
    #     readonly=True,
    #     states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}
    # )

    # pricelist_id = fields.Many2one(
    #     'product.pricelist',
    #     'Pricelist',
    #     required=False,
    #     help="The pricelist sets the currency used for this purchase order. It also computes the supplier price for the selected products/quantities."
    # )
