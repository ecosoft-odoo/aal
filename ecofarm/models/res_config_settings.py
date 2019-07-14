# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Groups
    group_ecofarm_manager = fields.Boolean(
        string='Manage Ecosoft FARM',
        implied_group='ecofarm.group_ecofarm_manager',
    )
    # Modules
    module_l10n_th_vendor_tax_invoice = fields.Boolean(
        string='TH - Vendor Tax Invoice',
    )
    module_l10n_th_withholding_tax_cert = fields.Boolean(
        string='TH - Withholding Tax Certificate',
    )
    module_l10n_th_withholding_tax_cert_form = fields.Boolean(
        string='TH - Print Standard Withholding Tax Certificate ',
    )
