from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    related_picking_numbers = fields.Char(
        compute='_compute_related_picking_numbers',
        help="Virtual field for printing, sale_line_ids.order_id.picking_ids"
    )

    @api.multi
    def _compute_related_picking_numbers(self):
        for rec in self:
            pickings = rec.mapped('invoice_line_ids').mapped('sale_line_ids').\
                mapped('order_id').mapped('picking_ids').\
                filtered(lambda t: t.state != 'cancel')
            rec.related_picking_numbers = ', '.join(pickings.mapped('name'))
