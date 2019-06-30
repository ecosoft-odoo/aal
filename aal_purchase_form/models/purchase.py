from openerp import models, api
# from num2words import num2words


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

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
        hide_reports_purchase = [
            'purchase.action_report_purchase_order',
            'purchase.report_purchase_quotation',
        ]
        res = super(PurchaseOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            self.remove_menu_print(res, hide_reports_purchase)
        return res
