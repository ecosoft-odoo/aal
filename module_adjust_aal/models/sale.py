from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form',
    #                     toolbar=False, submenu=False):
    #     res = super(SaleOrder, self).fields_view_get(
    #         view_id, view_type, toolbar=toolbar, submenu=submenu)
    #     print "==================================="
    #     x=1/0
    #     return res
