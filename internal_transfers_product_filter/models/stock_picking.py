# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __manifest__.py file at the root folder of this module.                  #
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.onchange('product_id')
    def stock_product_availability(self):
        result ={}
        product_ids_list = []
        context = dict(self._context or {})
        picking_type = self.env['stock.picking.type'].search([('id','=',self._context.get('default_picking_type_id'))])
        product_obj = self.env['product.product']
        if picking_type.code == 'internal':
            if self._context.get('default_location_id'):
                stock_quant  =  self.env["stock.quant"].search([('qty','>',0),('location_id','=',self._context.get('default_location_id'))])                
                for product_id in stock_quant:
                    product_ids_list.append(product_id.product_id.id)
            result['domain'] = {'product_id': [('id','in',product_ids_list)]}
            return result
        else:
            result['domain'] = {'product_id': [('type', 'in', ['product', 'consu'])]}
            return result

    product_id = fields.Many2one(
        'product.product', 'Product',
        index=True, required=True,
        states={'done': [('readonly', True)]})