# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import models, fields, api, _


class WithholdingTaxCert(models.Model):
    _inherit = 'withholding.tax.cert'

    base_amount_total = fields.Float(
        compute='_compute_amount_total',
    )
    tax_amount_total = fields.Float(
        compute='_compute_amount_total',
    )
    book_number = fields.Integer()
    number = fields.Integer()
    sequence = fields.Integer()

    @api.depends('wt_line')
    def _compute_amount_total(self):
        for rec in self:
            rec.base_amount_total = sum(rec.wt_line.mapped('base'))
            rec.tax_amount_total = sum(rec.wt_line.mapped('amount'))
