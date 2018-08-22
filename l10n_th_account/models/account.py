# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class AccountTaxTemplate(models.Model):

    _inherit = 'account.tax.template'

    is_undue_tax = fields.Boolean(
        string='Undue Tax',
        default=False,
        help="""This is a undue tax account.
                The tax point will be deferred to the time of payment""",
    )
    is_wht = fields.Boolean(
        string='Withholding Tax',
        help="Tax will be withhold and will be used in Payment",
    )
    threshold_wht = fields.Float(
        string='Threshold Amount',
        help="""Withholding Tax will be applied only if base amount more
                or equal to threshold amount""",
    )
    refer_tax_id = fields.Many2one(
        'account.tax',
        string='Counterpart Tax',
        ondelete='restrict',
        help="Counterpart Tax for payment process",
    )


class AccountTax(models.Model):

    _inherit = 'account.tax'

    # Can't make it required, as it will gen error on first CoA import
    # account_collected_id = fields.Many2one(required=True)
    # base_code_id = fields.Many2one(required=True)
    # tax_code_id = fields.Many2one(required=True)
    # account_paid_id = fields.Many2one(required=True)
    # ref_base_code_id = fields.Many2one(required=True)
    # ref_tax_code_id = fields.Many2one(required=True)
    is_undue_tax = fields.Boolean(
        string='Undue Tax',
        default=False,
        help="""This is a undue tax account.
                The tax point will be deferred to the time of payment""",
    )
    is_wht = fields.Boolean(
        string='Withholding Tax',
        help="Tax will be withhold and will be used in Payment",
    )
    threshold_wht = fields.Float(
        string='Threshold Amount',
        help="""Withholding Tax will be applied only if base amount more
                or equal to threshold amount""",
    )
    refer_tax_id = fields.Many2one(
        'account.tax',
        string='Counterpart Tax',
        ondelete='restrict',
        help="Counterpart Tax for payment process",
    )

    @api.v7
    def compute_all(self, cr, uid, taxes, price_unit, quantity, product=None,
                    partner=None, force_excluded=False, context=None):
        if context is None:
            context = {}
        payment_type = context.get('type', False)
        if payment_type not in ('receipt', 'payment'):  # Invoice
            taxes = taxes.filtered(lambda r: not r.is_wht)  # Remove all WHT
        res = super(AccountTax, self).compute_all(
            cr, uid, taxes, price_unit, quantity, product=None,
            partner=None, force_excluded=False)
        return res

    @api.v8
    def compute_all(self, price_unit, quantity, product=None,
                    partner=None, force_excluded=False):
        return self._model.compute_all(
            self._cr, self._uid, self, price_unit, quantity,
            product=product, partner=partner, force_excluded=force_excluded,
            context=self._context)

    @api.onchange('is_wht')
    def onchange_is_wht(self):
        self.is_undue_tax = False

    @api.onchange('is_undue_tax')
    def onchange_is_undue_tax(self):
        self.is_wht = False


class AccountTaxCode(models.Model):
    _inherit = 'account.tax.code'

    tax_code_type = fields.Selection(
        [('normal', 'Normal'),
         ('undue', 'Undue'),
         ('wht', 'Withholding')],
        string='Tax Code Type',
        compute='_compute_tax_code_type',
        store=True,
        help="Type based on Tax using this Tax Code",
    )
    tax_ids = fields.One2many(
        'account.tax',
        'tax_code_id',
        help="For compute field"
    )
    tax2_ids = fields.One2many(
        'account.tax',
        'ref_tax_code_id',
        help="For compute field"
    )

    @api.one
    @api.depends('tax_ids', 'tax2_ids',
                 'tax_ids.is_wht', 'tax2_ids.is_wht',
                 'tax_ids.is_undue_tax', 'tax2_ids.is_undue_tax',)
    def _compute_tax_code_type(self):
        res_undue = list(set([tax.is_undue_tax for tax in self.tax_ids] +
                             [tax.is_undue_tax for tax in self.tax2_ids]))
        is_undue_tax = False
        if len(res_undue) == 1:
            is_undue_tax = res_undue[0]
        elif len(res_undue) > 1:
            raise ValidationError(
                _('Some tax using the same Tax Code '
                  'is not of the same Due/Undue type!'))
        res_wht = list(set([tax.is_wht for tax in self.tax_ids] +
                           [tax.is_wht for tax in self.tax2_ids]))
        is_wht = False
        if len(res_wht) == 1:
            is_wht = res_wht[0]
        elif len(res_wht) > 1:
            raise ValidationError(
                _('Some tax using the same Tax Code '
                  'is not of the same Withholding type!'))
        self.tax_code_type = 'normal'
        if is_wht:
            self.tax_code_type = 'wht'
        elif is_undue_tax:
            self.tax_code_type = 'undue'


class AccountPeriod(models.Model):
    _inherit = 'account.period'

    wht_sequence_ids = fields.One2many(
        'withholding.tax.sequence',
        'period_id',
        string='WHT Sequence',
    )
