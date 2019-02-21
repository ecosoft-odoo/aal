# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2014-Today BrowseInfo (<http://www.browseinfo.in>)>
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

from openerp import models, fields, api
from openerp.osv import osv, fields

class product_item(osv.osv):
    _name = "product.item"
    _description = "Product Item for Bundle products"
    _columns = {
        'sequence':   fields.integer('Sequence'),
        'product_id': fields.many2one('product.product', 'Bundle Product', required=True),
        'item_id':    fields.many2one('product.product', 'Item', required=True),
        'uom_id':     fields.many2one('product.uom', 'UoM', required=True),
        'qty_uom':    fields.integer('Quantity', required=True),
    }

    def onchange_item_id(self, cr, uid, ids, item_id, context=None):
        context = context or {}
        result = {}
        if item_id:
            item = self.pool.get('product.product').browse(cr, uid, item_id, context=context)
            if item:
                result.update({'uom_id': item.uom_id.id})
        return {'value': result}

product_item()

class product_product(osv.osv):
    _inherit = "product.product"

    _columns = {
        'items_ids': fields.one2many('product.item', 'product_id', 'Item sets'),
    }

product_product()
