{
    "name": "Stock Card Report",
    "summary": "Add stock card report on Inventory Reporting.",
    "version": "12.0.1.0.0",
    "category": "Reporting",
    "website": "https://github.com/ecosoft-odoo/stock-logistics-reporting/tree/12.0",
    "author": "Ecosoft",
    "license": "AGPL-3",
    "depends": [
        "stock",
        "report_xlsx",
    ],
    "data": [
        "data/paper_format.xml",
        "data/report_data.xml",
        "reports/stock_card_report.xml",
        "wizard/stock_card_report_wizard_view.xml",
    ],
}
