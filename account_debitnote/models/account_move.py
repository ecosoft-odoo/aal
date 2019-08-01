# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
<<<<<<< HEAD
<<<<<<< HEAD
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
=======
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).html)
>>>>>>> 0070992... [12.0][ADD] account debitnote
=======
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
>>>>>>> f98f450... [12.0][ADD] account debitnote

from odoo import models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.multi
    def post(self, invoice=False):
        self = self.with_context(ctx_invoice=invoice)
        return super().post(invoice=invoice)
