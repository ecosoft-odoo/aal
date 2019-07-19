import logging
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class ReportStockCardReportXlsx(models.AbstractModel):
    _name = 'report.stock_card_report.report_stock_card_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    @staticmethod
    def _print_bom_children(ch, sheet, row):
        i = row
        sheet.write(i, 0, str(ch.date) or '')
        sheet.write(i, 1, ch.reference or '')
        sheet.write(i, 2, ch.product_in or 0.00)
        sheet.write(i, 3, ch.product_out or 0.00)
        sheet.write(i, 4, ch.product_balance or 0.00)
        i += 1
        return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 11.0'})
        sheet = workbook.add_worksheet(_('Stock Card Report'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 4, 24)

        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('Date'),
                       _('Reference'),
                       _('Input'),
                       _('Output'),
                       _('Balance'),
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(4, 0, sheet_title, title_style)

        for o in objects:
            # Write header
            sheet.write_row(0, 0, [_('Product'), (o.product_id.name)])
            sheet.write_row(1, 0, [_('Location'), (o.stock_location_id.name)])
            sheet.write_row(2, 0, [_('Date from'), str(o.date_from)])
            sheet.write_row(3, 0, [_('Date to'), str(o.date_to)])
            i = 5
            for ch in o.line_ids:
                i = self._print_bom_children(ch, sheet, i)
