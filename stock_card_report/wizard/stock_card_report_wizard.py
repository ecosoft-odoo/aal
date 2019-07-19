from odoo import api, fields, models


class StockCardReportWizard(models.TransientModel):
    _name = "stock.card.report.wizard"
    _description = 'Stock Card Report Wizard'

    date_from = fields.Date(
        string="Start Date",
        required=True,
    )
    date_to = fields.Date(
        string="End Date",
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
    )
    stock_location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Location",
        required=True,
    )
    initial_stock = fields.Float(
        string='Initial Stock',
    )
    line_ids = fields.One2many(
        comodel_name='stock.card.report.wizard.line',
        inverse_name='explosion_id',
    )

    # @api.onchange('product_id')
    # def _onchange_product_id(self):
    #     initial_stock = self.env['stock.quant'].search([
    #         ('product_id', '=', self.product_id.id)])
    #     self.initial_stock = initial_stock.quantity

    @api.model
    def _prepare_line(self, stock_card, type, balance, location):
        if type == 'in':
            return {
                'explosion_id': self.id,
                'product_id': stock_card.product_id.id,
                'location_id': stock_card.location_id.id,
                'location_dest_id': stock_card.location_dest_id.id,
                'stock_location_id': location,
                'date': stock_card.date,
                'reference': stock_card.reference,
                'product_in': stock_card.product_uom_qty,
                'product_out': 0.00,
                'product_balance': balance,
            }
        elif type == 'out':
            return {
                'explosion_id': self.id,
                'product_id': stock_card.product_id.id,
                'location_id': stock_card.location_id.id,
                'location_dest_id': stock_card.location_dest_id.id,
                'stock_location_id': location,
                'date': stock_card.date,
                'reference': stock_card.reference,
                'product_in': 0.00,
                'product_out': stock_card.product_uom_qty,
                'product_balance': balance,
            }

    @api.multi
    def do_explode(self):
        self.ensure_one()
        line_obj = self.env['stock.card.report.wizard.line']

        def _create_lines(stock_card, location):
            balance = 0.00
            for line in stock_card:
                if line.location_dest_id.id == location:
                    balance = balance + line.product_uom_qty
                    vals = self._prepare_line(line, 'in', balance, location)
                    line_obj.create(vals)
                elif line.location_id.id == location:
                    balance = balance - line.product_uom_qty
                    vals = self._prepare_line(line, 'out', balance, location)
                    line_obj.create(vals)

        stock_card = self.env['stock.move'].search([
            '|', ('location_id', '=', self.stock_location_id.id),
            ('location_dest_id', '=', self.stock_location_id.id),
            ('product_id', '=', self.product_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to)])
        _create_lines(stock_card, self.stock_location_id.id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Stock Card',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'stock.card.report.wizard',
            'view_id': self.env.ref(
                'stock_card_report.stock_card_report_wizard_view_form2'
            ).id,
            'target': 'new',
            'res_id': self.id,
        }


class StockCardReportWizardLine(models.TransientModel):
    _name = 'stock.card.report.wizard.line'
    _description = 'Stock Card Report Wizard Line'

    explosion_id = fields.Many2one(
        comodel_name='stock.card.report.wizard',
        copy=False,
    )
    date = fields.Date(
        string='Date',
        readonly=True,
    )
    reference = fields.Char(
        string='Reference',
        readonly=True,
    )
    product_in = fields.Float(
        string='Input',
        readonly=True,
    )
    product_out = fields.Float(
        string='Output',
        readonly=True,
    )
    product_balance = fields.Float(
        string='Balance',
        readonly=True,
    )
