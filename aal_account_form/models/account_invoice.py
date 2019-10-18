from openerp import models, api, fields


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def remove_menu_print(self, res, reports):
        # Remove reports menu
        for report in reports:
            print(report)
            reports = self.env.ref(report, raise_if_not_found=False)
            for rec in res.get('toolbar', {}).get('print', []):
                if rec.get('id', False) in reports.ids:
                    del res['toolbar']['print'][
                        res.get('toolbar', {}).get('print').index(rec)]
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        hide_reports_base = [
            'account.account_invoices',
            'account.account_invoices_without_payment',
        ]
        hide_reports_vendor = [
            'aal_account_form.aal_credit_note_tax_invoice_form_pdf_report',
            'aal_account_form.aal_debit_note_tax_invoice_form_pdf_report',
            'aal_account_form.aal_delivery_order_form_pdf_report',
            'aal_account_form.aal_delivery_order_tax_invoice_A_form_pdf_report',
            'aal_account_form.aal_delivery_order_tax_invoice_B_form_pdf_report',
        ]
        hide_reports_customer_invoice = [
            'aal_account_form.aal_credit_note_tax_invoice_form_pdf_report',
        ]
        hide_reports_customer_refund = [
            'aal_account_form.aal_debit_note_tax_invoice_form_pdf_report',
            'aal_account_form.aal_delivery_order_form_pdf_report',
            'aal_account_form.aal_delivery_order_tax_invoice_A_form_pdf_report',
            'aal_account_form.aal_delivery_order_tax_invoice_B_form_pdf_report',
        ]
        type = self._context.get('type')
        res = super(AccountInvoice, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        if res and view_type in ['tree', 'form']:
            # del menu report customer and vendor
            self.remove_menu_print(res, hide_reports_base)
            # del menu report vendor
            if type and type not in ['out_invoice', 'out_refund']:
                self.remove_menu_print(res, hide_reports_vendor)
            # del menu report customer invoice
            if type and type != 'out_refund':
                self.remove_menu_print(res, hide_reports_customer_invoice)
            # del menu report customer refund
            if type and type != 'out_invoice':
                self.remove_menu_print(res, hide_reports_customer_refund)
        return res

    def _get_invoice_origin(self):
        invoice_id = self.env['account.invoice'].search([
            ('number', '=', self.origin)
        ])
        return invoice_id
