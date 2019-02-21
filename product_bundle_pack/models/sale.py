# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp import api, models
from openerp import netsvc
from openerp.tools.translate import _
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta

class sale_order(osv.osv):
    _inherit = "sale.order"

    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        date_planned = self._get_date_planned(cr, uid, order, line, order.date_order, context=context)
        res = []
        if line.product_id.items_ids:
            for item in line.product_id.items_ids:
                res.append({
                    'name': line.name,
                    'origin': order.name,
                    'date_planned': date_planned,
                    'product_id': item.item_id.id,
                    'product_qty': item.qty_uom * line.product_uom_qty or 0.00,
                    'product_uom': item.uom_id and item.uom_id.id or False,
                    'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
                    'product_uos': (line.product_uos and line.product_uos.id) or line.product_uom.id,
                    'company_id': order.company_id.id,
                    'group_id': group_id,
                    'invoice_state': (order.order_policy == 'picking') and '2binvoiced' or 'none',
                    'sale_line_id': line.id,
                    'warehouse_id' : line.order_id.warehouse_id and line.order_id.warehouse_id.id,
                    'location_id': line.order_id.partner_shipping_id.property_stock_customer.id,
                    'route_ids': line.route_id and [(4, line.route_id.id)] or [],
                    'partner_dest_id': line.order_id.partner_shipping_id.id,
                })
        else:
            res.append({
                'name': line.name,
                'origin': order.name,
                'date_planned': date_planned,
                'product_id': line.product_id.id,
                'product_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'product_uos_qty': (line.product_uos and line.product_uos_qty) or line.product_uom_qty,
                'product_uos': (line.product_uos and line.product_uos.id) or line.product_uom.id,
                'company_id': order.company_id.id,
                'group_id': group_id,
                'invoice_state': (order.order_policy == 'picking') and '2binvoiced' or 'none',
                'sale_line_id': line.id,
                'warehouse_id' : line.order_id.warehouse_id and line.order_id.warehouse_id.id,
                'location_id': line.order_id.partner_shipping_id.property_stock_customer.id,
                'route_ids': line.route_id and [(4, line.route_id.id)] or [],
                'partner_dest_id': line.order_id.partner_shipping_id.id,
            })
        return res

    def action_ship_create(self, cr, uid, ids, context=None):
        context = context or {}
        context['lang'] = self.pool['res.users'].browse(cr, uid, uid).lang
        procurement_obj = self.pool.get('procurement.order')
        sale_line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context=context):
            proc_ids = []
            vals = self._prepare_procurement_group(cr, uid, order, context=context)
            if not order.procurement_group_id:
                group_id = self.pool.get("procurement.group").create(cr, uid, vals, context=context)
                order.write({'procurement_group_id': group_id})

            for line in order.order_line:
                if line.state == 'cancel':
                    continue
                if line.procurement_ids:
                    procurement_obj.check(cr, uid, [x.id for x in line.procurement_ids if x.state not in ['cancel', 'done']])
                    line.refresh()
                    except_proc_ids = [x.id for x in line.procurement_ids if x.state in ('exception', 'cancel')]
                    procurement_obj.reset_to_confirmed(cr, uid, except_proc_ids, context=context)
                    proc_ids += except_proc_ids
                elif sale_line_obj.need_procurement(cr, uid, [line.id], context=context):
                    if (line.state == 'done') or not line.product_id:
                        continue
                    vals = self._prepare_order_line_procurement(cr, uid, order, line, group_id=order.procurement_group_id.id, context=context)
                    ctx = context.copy()
                    ctx['procurement_autorun_defer'] = True
                    for val in vals:
                        proc_id = procurement_obj.create(cr, uid, val, context=ctx)
                        proc_ids.append(proc_id)
            procurement_obj.run(cr, uid, proc_ids, context=context)

            if order.state == 'shipping_except':
                val = {'state': 'progress', 'shipped': False}

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
                order.write(val)
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        self.ensure_one()
        res = []
        if self.product_id.items_ids:
            for item in self.product_id.items_ids:
                res.append({
                    'name': self.product_id.items_ids.item_id.name,
                    'origin': self.order_id.name,
                    'date_planned': datetime.strptime(self.order_id.date_order, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(days=self.customer_lead),
                    'product_id': item.item_id.id,
                    'product_qty': item.qty_uom * self.product_uom_qty,
                    'product_uom': item.uom_id and item.uom_id.id,
                    'company_id': self.order_id.company_id.id,
                    'group_id': group_id,
                    'sale_line_id': self.id,
                    'warehouse_id' : self.order_id.warehouse_id and self.order_id.warehouse_id.id,
                    'location_id': self.order_id.partner_shipping_id.property_stock_customer.id,
                    'route_ids': self.route_id and [(4, self.route_id.id)] or [],
                    'partner_dest_id': self.order_id.partner_shipping_id.id,
                })
        else:
            res.append({
                'name': self.name,
                'origin': self.order_id.name,
                'date_planned': datetime.strptime(self.order_id.date_order, DEFAULT_SERVER_DATETIME_FORMAT) + timedelta(days=self.customer_lead),
                'product_id': self.product_id.id,
                'product_qty': self.product_uom_qty,
                'product_uom': self.product_uom.id,
                'company_id': self.order_id.company_id.id,
                'group_id': group_id,
                'sale_line_id': self.id,
                'warehouse_id' : self.order_id.warehouse_id and self.order_id.warehouse_id.id,
                'location_id': self.order_id.partner_shipping_id.property_stock_customer.id,
                'route_ids': self.route_id and [(4, self.route_id.id)] or [],
                'partner_dest_id': self.order_id.partner_shipping_id.id,
            })
        return res

    @api.multi
    def _action_procurement_create(self):
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        new_procs = self.env['procurement.order']
        for line in self:
            if line.state != 'sale' or not line.product_id._need_procurement():
                continue
            qty = 0.0
            for proc in line.procurement_ids:
                qty += proc.product_qty
            if float_compare(qty, line.product_uom_qty, precision_digits=precision) >= 0:
                return False

            if not line.order_id.procurement_group_id:
                vals = line.order_id._prepare_procurement_group()
                line.order_id.procurement_group_id = self.env["procurement.group"].create(vals)

            vals = line._prepare_order_line_procurement(group_id=line.order_id.procurement_group_id.id)
            for val in vals:
                val['product_qty'] = line.product_uom_qty - qty
                new_proc = self.env["procurement.order"].create(val)
                new_procs += new_proc
        new_procs.run()
        return new_procs
