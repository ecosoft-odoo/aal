from openerp import models, api, fields


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
                mapped('order_id').mapped('picking_ids')
            rec.related_picking_numbers = ', '.join(pickings.mapped('name'))

    @api.multi
    def remove_menu_print(self, res, reports):
        # Remove reports menu
        for report in reports:
            reports = self.env.ref(report, raise_if_not_found=False)
            for rec in res.get('toolbar', {}).get('print', []):
                if rec.get('id', False) in reports.ids:
                    del res['toolbar']['print'][
                        res.get('toolbar', {}).get('print').index(rec)]
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        hide_reports_sale = [
            # 'sale.action_report_saleorder',
        ]
        res = super(AccountInvoice, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_sale)
        return res
