# -*- coding: utf-8 -*-
from openerp import models, api


PURCHASE_TYPE = {
    'quotation': ['aal.request.for.quotation', ],
    'purchase_order': ['aal.purchase.order', ],
}


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(PurchaseOrder, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        toolbar = res.get('toolbar', {})
        action_print = toolbar.get('print', [])
        purchase_type = self._context.get('purchase_type', False)
        if action_print and purchase_type in PURCHASE_TYPE.keys():
            action = []
            for act in action_print:
                if act.get('report_name') not in PURCHASE_TYPE[purchase_type]:
                    continue
                action.append(act)
            res['toolbar']['print'] = action
        return res
