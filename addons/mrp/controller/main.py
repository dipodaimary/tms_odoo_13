# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import json
import logging
import requests

from odoo import http, _, exceptions
from odoo.http import request
from odoo.tools.translate import _
from odoo.tests import Form

logger = logging.getLogger(__name__)


class MrpDocumentRoute(http.Controller):

    @http.route('/mrp/upload_attachment', type='http', methods=['POST'], auth="user")
    def upload_document(self, ufile, **kwargs):
        files = request.httprequest.files.getlist('ufile')
        result = {'success': _("All files uploaded")}
        for ufile in files:
            try:
                mimetype = ufile.content_type
                request.env['mrp.document'].create({
                    'name': ufile.filename,
                    'res_model': kwargs.get('res_model'),
                    'res_id': int(kwargs.get('res_id')),
                    'mimetype': mimetype,
                    'datas': base64.encodebytes(ufile.read()),
                })
            except Exception as e:
                logger.exception("Fail to upload document %s" % ufile.filename)
                result = {'error': str(e)}

        return json.dumps(result)
    # Edited From here

    def update_bom(self, bom_quantities={'bulk': 1.0, 'green_leaf': 1.0}):
        bulk = request.env['product.product'].search([['name', '=', 'Bulk']])
        green_leaf = request.env['product.product'].search([['name', '=', 'Green Leaf']])
        unit = request.env.ref("uom.product_uom_unit").id
        bom_bulk = request.env['mrp.bom'].create({
            'product_tmpl_id': bulk.product_tmpl_id.id,
            'product_qty': bom_quantities['bulk'],
            'product_uom_id': unit,
            'bom_line_ids': [(0, 0, {
                'product_id': green_leaf.id,
                'product_qty': bom_quantities['green_leaf'],
                'product_uom_id': unit
            }),]
        })
        request.env.cr.commit()
        return bom_bulk

    def mo_production(self, bom_bulk=None):
        bulk = request.env['product.product'].search([['name', '=', 'Bulk']])
        mo_bulk_form = Form(request.env['mrp.production'])
        mo_bulk_form.product_id = bulk
        mo_bulk_form.bom_id = bom_bulk
        mo_bulk_form.product_qty = bom_bulk.product_qty
        mo_bulk_form.product_uom_id = request.env.ref("uom.product_uom_unit")
        mo_bulk = mo_bulk_form.save()
        mo_bulk.action_confirm()
        mo_bulk.action_assign()
        context = {"active_ids": [mo_bulk.id], "active_id": mo_bulk.id}
        product_form = Form(request.env['mrp.product.produce'].with_context(context))
        product_form.qty_producing = bom_bulk.product_qty
        lot_bulk = request.env['stock.production.lot'].create(
            {'product_id': bulk.id, 'company_id': request.env.company.id})
        product_form.finished_lot_id = lot_bulk
        product_consume = product_form.save()
        product_consume.do_produce()
        mo_bulk.button_mark_done()
        request.env.cr.commit()

    def update_subcontracting(self, vendor, product, quantity):
        picking_form = Form(request.env['stock.picking'])
        picking_form.picking_type_id = request.env.ref('stock.picking_type_in')
        picking_form.partner_id = request.env['res.partner'].search([['name', '=', str(vendor)]])
        with picking_form.move_ids_without_package.new() as move:
            move.product_id = request.env['product.product'].search([['name', '=', str(product)]])
            move.product_uom_qty = quantity
        picking_receipt = picking_form.save()
        picking_receipt.action_confirm()
        wh = picking_receipt.picking_type_id.warehouse_id
        pg1 = request.env['procurement.group'].create({})
        request.env['procurement.group'].run_scheduler()
        picking = request.env['stock.picking'].search([('group_id', '=', pg1.id)])
        picking_receipt.move_lines.quantity_done = quantity
        picking_receipt.button_validate()
        request.env.cr.commit()
        return picking_receipt.id

    @http.route('/auth/', type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **post):
        try:
            login = post["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')
        try:
            password = post["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')
        try:
            db = post["db"]
        except KeyError:
            raise exceptions.AccessDenied(message='`db` is required.')
        url_root = request.httprequest.url_root
        AUTH_URL = f"{url_root}web/session/authenticate/"
        headers = {'Content-type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "params": {
                "login": login,
                "password": password,
                "db": db
            }
        }
        res = requests.post(
            AUTH_URL,
            data=json.dumps(data),
            headers=headers
        )
        try:
            session_id = res.cookies["session_id"]
            user = json.loads(res.text)
            user["result"]["session_id"] = session_id
        except Exception:
            return "Invalid credentials."
        return user["result"]

    @http.route('/create_mo', type='json', auth='user')
    def create_mo(self, **rec):
        if request.jsonrequest:
            if rec['green_leaf']:
                bom_bulk = self.update_bom(bom_quantities={'bulk': rec['bulk'], 'green_leaf': rec['green_leaf']})
                self.mo_production(bom_bulk)
                args = {'success': True, 'message': 'Success'}
        return args

    @http.route('/create_picking', type='json', auth='user')
    def create_picking(self, **rec):
        if request.jsonrequest:
            if rec['quantity']:
                picking_id = self.update_subcontracting(rec['vendor'], rec['product'], rec['quantity'])
                if picking_id:
                    args = {'success': True, 'message': 'Success'}
                else:
                    args = {'success': False}
        return args
