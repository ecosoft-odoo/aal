# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    client_order_ref = fields.Char(
        string='Order Ref.',
        compute='_compute_client_order_ref',
        help="Order Ref computed from sales order "
        "lines related to this invoice line",
    )

    @api.multi
    def _compute_client_order_ref(self):
        for rec in self:
            sales = rec.sale_line_ids.mapped('order_id')
            refs = sales.filtered('client_order_ref').mapped('client_order_ref')
            rec.client_order_ref = ', '.join(refs)
