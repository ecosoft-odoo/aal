# -*- coding: utf-8 -*-
from openerp import models, fields


class ResDoctype(models.Model):
    _inherit = 'res.doctype'

    refer_type = fields.Selection(
        selection_add=[
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Supplier Invoice'),
            ('out_refund', 'Customer Refund'),
            ('in_refund', 'Supplier Refund'),
        ],
    )
