from odoo.tests.common import TransactionCase, Form
from odoo.exceptions import ValidationError
from datetime import date


class TestAccountDebitNote(TransactionCase):

    def setUp(self):
        super(TestAccountDebitNote, self).setUp()
        self.AccountInvoice = self.env['account.invoice']
        self.Wizard = self.env['account.invoice.debitnote']
        self.test_partner = self.env.ref('base.res_partner_12')
        self.test_product = self.env.ref('product.product_product_7')
        #  Create Invoice

    def call_invoice_debit_note(self, invoice):
        ctx = {'active_id': invoice.id, 'active_ids': [invoice.id]}
        view_id = 'account_debitnote.view_account_invoice_debitnote'
        with Form(self.Wizard.with_context(ctx), view=view_id) as f:
            f.date = date.today()
            f.description = 'Test'
        wizard = f.save()
        wizard.invoice_debitnote()

    def test_1_account_debitnote(self):
        """I create invoice, validate it, and create debit note. I expect,
        - Invoice is open
        - Debit note is created
        """
        with Form(self.AccountInvoice) as f:
            f.partner_id = self.test_partner
            f.type = 'out_invoice'
            with f.invoice_line_ids.new() as line:
                line.product_id = self.test_product
        invoice = f.save()
        invoice.action_invoice_open()
        self.assertEqual(invoice.state, 'open')
        # Create Debit Note
        self.call_invoice_debit_note(invoice)

    def test_2_ValidationError(self):
        """Create debit note in Credit note and Refund. I expect,
        - ValidationError
        """

        with Form(self.AccountInvoice) as f:
            f.partner_id = self.test_partner
            f.type = 'out_invoice'
            with f.invoice_line_ids.new() as line:
                line.product_id = self.test_product
        invoice = f.save()
        with self.assertRaises(ValidationError):
            self.call_invoice_debit_note(invoice)

        with Form(self.AccountInvoice) as f:
            f.partner_id = self.test_partner
            f.type = 'out_refund'
            with f.invoice_line_ids.new() as line:
                line.product_id = self.test_product
        creditnote = f.save()
        creditnote.action_invoice_open()
        with self.assertRaises(ValidationError):
            self.call_invoice_debit_note(creditnote)
