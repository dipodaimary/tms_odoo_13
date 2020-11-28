import logging
from odoo import http
from odoo.http import request
import json
from odoo.fields import Datetime as Dt

_logger = logging.getLogger(__name__)
class GetController(http.Controller):
    @http.route('/create_price', type='json', auth='user')
    def create_price(self, **rec):
        if request.jsonrequest:
            name = rec.get('name', False)
            label = rec.get('label', False)
            item = rec.get('item', False)
            qu_inc = rec.get('qu_inc', False)
            qt_inc = rec.get('qt_inc', False)
            rate = rec.get('rate', False)
            data = request.env['price_table.data'].create([{'name': name, 'label': label, 'item': item, 'quality_incentive': qu_inc, 'quantity_incentive': qt_inc, 'rate': rate}])
            if data:
                message = {'success': True, 'message': 'Success'}
                request.env.cr.commit()
            else:
                message = {'success': False}
        return message

    @http.route('/get_default_stg_price', type='json', auth='user')
    def get_default_stg_price(self, **rec):
        data = request.env['price_table.data'].search([['name', '=', 'DefaultSTG']])
        price = data.rate
        qu_inc = data.quality_incentive
        qt_inc = data.quantity_incentive
        return {"price": price, "qu_inc": qu_inc, "qt_inc": qt_inc}

    @http.route('/update_default_stg_price', type='json', auth='user')
    def update_default_stg_price(self, **rec):
        data = request.env['price_table.data'].search([['label', '=', 'STG']])
        price = rec.get('rate', False)
        qu_inc = rec.get('qu_inc', False)
        qt_inc = rec.get('qt_inc', False)
        data.rate = price
        data.quality_incentive = qu_inc
        data.quantity_incentive = qt_inc
        request.env.cr.commit()
        return {"message": "success"}


    @http.route('/get_special_stg_price', type='json', auth='user')
    def get_special_stg_price(self, **rec):
        name = rec.get('name', False)
        data = request.env['price_table.data'].search([['name', '=', name]])
        price = data.rate
        qu_inc = data.quality_incentive
        qt_inc = data.quantity_incentive
        return {"price": price, "qu_inc": qu_inc, "qt_inc": qt_inc}

    @http.route('/get_stg_price', type='json', auth='user')
    def get_stg_price(self, **rec):
        label = rec.get('label', False)
        data = request.env['price_table.data'].search([['label', '=', label]])
        price = data.rate
        qu_inc = data.quality_incentive
        qt_inc = data.quantity_incentive
        return {"price": price, "qu_inc": qu_inc, "qt_inc": qt_inc}

    def get_price_incentive_dict(self, stg_name='My Company'):
        string_obj = request.env['tea_management.price_incentive'].search([['seller.name', '=', stg_name]])
        q_dict = json.loads(string_obj.Q.replace('\t', '').replace('\n', '').replace("'", '"'))
        k_dict = json.loads(string_obj.K.replace('\t', '').replace('\n', '').replace("'", '"'))
        t_dict = json.loads(string_obj.T.replace('\t', '').replace('\n', '').replace("'", '"'))
        return q_dict, k_dict, t_dict

    def q_incentive(self, stg_name, quality):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            cuts = sorted(list(q_dict['cuts'].keys()))
            if str(quality) not in cuts:
                cuts.append(str(quality))
                cuts = sorted(cuts)
                index = cuts.index(str(quality))
                cut_final = cuts[index-1]
            else:
                cut_final = str(quality)
            return q_dict['cuts'][str(cut_final)]
        except:
            return 0.0

    def k_incentive(self, stg_name, quantity):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            cuts = sorted(list(k_dict['cuts'].keys()))
            if str(quantity) not in cuts:
                cuts.append(str(quantity))
                cuts = sorted(cuts)
                index = cuts.index(str(quantity))
                cut_final = cuts[index - 1]
            else:
                cut_final = str(quantity)
            return k_dict['cuts'][str(cut_final)]
        except:
            return 0.0

    def t_incentive(self, stg_name, distance):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            cuts = sorted(list(t_dict['cuts'].keys()))
            if str(distance) not in cuts:
                cuts.append(str(distance))
                cuts = sorted(cuts)
                index = cuts.index(str(distance))
                cut_final = cuts[index - 1]
            else:
                cut_final = str(distance)
            return t_dict['cuts'][str(cut_final)]
        except:
            return 0.0

    def create_incentive_entry(self, stg_name="My Company", expiry_date='2020-01-01',
                               q_json_str="{'cuts' : {'20' : 1,'30' : 2,'50' : 3}}	",
                               k_json_str="{'cuts' : {'1000' : 1,'1500' : 2,'2000' : 3}}",
                               t_json_str="{'cuts':{'100':10,}}"):
        contact = request.env['res.partner'].search([['name', '=', stg_name]])
        request.env['tea_management.price_incentive'].create({
            'seller': contact,
            'expiry_date': Dt.to_datetime(expiry_date),
            'Q': q_json_str,
            'K': k_json_str,
            'T': t_json_str,
        })
        request.env.cr.commit()

    @http.route('/get_q_incentive', type='json', auth='user')
    def get_q_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        quality = rec.get('quality', False)
        print(stg)
        print(quality)
        try:
            return {"incentive": self.q_incentive(stg, quality)}
        except:
            return {"incentive": 0}

    @http.route('/get_k_incentive', type='json', auth='user')
    def get_k_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        quantity = rec.get('quantity', False)
        try:
            return {"incentive" : self.k_incentive(stg, quantity)}
        except:
            return {"incentive": 0}

    @http.route('/get_t_incentive', type='json', auth='user')
    def get_t_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        distance = rec.get('distance', False)
        try:
            return {"incentive" : self.t_incentive(stg, distance)}
        except:
            return {"incentive": 0}

    @http.route('/create_price_incentive', type='json', auth='user')
    def update_default_stg_price(self, **rec):
        seller = rec.get('seller', False)
        expiry_date = rec.get('expiry_date', False)
        q_json_str = rec.get('q_json_str', False)
        k_json_str = rec.get('k_json_str', False)
        t_json_str = rec.get('t_json_str', False)
        self.create_incentive_entry(stg_name=seller, expiry_date=expiry_date,
                               q_json_str=q_json_str,
                               k_json_str=k_json_str,
                               t_json_str=t_json_str)
        return {"message": "success"}

    def move_lot(self, product_name='BP', lot_name='0000152', partner_name=None, picking_type_str='', location_A_str='', location_B_str=''):
        location_A = request.env['stock.location'].search([['complete_name', '=', location_A_str]])
        location_B = request.env['stock.location'].search([['complete_name', '=', location_B_str]])
        picking_type = request.env['stock.picking.type'].search([('default_location_dest_id', '=', location_B.id), ('code', '=', 'incoming')])
        product_obj = request.env['product.product'].search([['name', '=', product_name]])
        unit = request.env.ref("uom.product_uom_unit")
        picking_in = request.env['stock.picking'].create({
            'picking_type_id': picking_type.id,
            'location_id': location_A.id,
            'location_dest_id': location_B.id
        })
        move = request.env['stock.move'].create({
            'name': 'test',
            'product_id': product_obj.id,
            'product_uom_qty': 1.0,
            'product_uom': unit.id,
            'picking_id': picking_in.id,
            'location_id': location_A.id,
            'location_dest_id': location_B.id
        })
        if partner_name:
            try:
                partner_obj = request.env['res.partner'].search([['name', '=', partner_name]])
                move.partner_id = partner_obj
            except:
                pass
        picking_in.action_confirm()
        if partner_name:
            try:
                partner_obj = request.env['res.partner'].search([['name', '=', partner_name]])
                move.partner_id = partner_obj
                picking_in.partner_id = partner_obj
            except:
                pass
        lot = request.env['stock.production.lot'].search([['name', '=', lot_name]])
        request.env['stock.move.line'].create({
            'move_id': move.id,
            'product_id': product_obj.id,
            'product_uom_id': unit.id,
            'location_id': location_A.id,
            'location_dest_id': location_B.id,
            'qty_done': 1.0,
            'lot_id': lot.id,
        })
        picking_in.action_done()
        self.update_serial_and_lot_entry(serial=lot_name, status=location_B.complete_name)
        request.env.cr.commit()

    def update_serial_and_lot_entry(self, **kwargs):
        print(kwargs['serial'])
        if kwargs['serial']:
            entry_obj = request.env['tea_management.serial_and_lot'].search([['serial', '=', kwargs['serial']]])
        elif kwargs['custom_serial']:
            entry_obj = request.env['tea_management.serial_and_lot'].search(
                [['custom_serial', '=', kwargs['custom_serial']]])
        update_dict = {}
        for k, w in kwargs.items():
            if k in ['custom_serial', 'product_name', 'quantity_in_lot', 'status']:
                update_dict[k] = w
        print(update_dict)
        entry_obj.write(update_dict)
        request.env.cr.commit()

    @http.route('/move_lot', type='json', auth='user')
    def move_lot_api(self, **rec):
        self.move_lot(
            product_name=rec['product_name'],
            lot_name=rec['lot_name'],
            partner_name=rec['partner_name'],
            picking_type_str=rec['picking_type'],
            location_A_str=rec['location_A'],
            location_B_str=rec['location_B']
            )
        return {"message": "success"}

    @http.route('/get_product_list', type='json', auth='user')
    def get_product_list_api(self, **rec):
        products = [x.name for x in request.env['product.product'].search([])]
        return {"products": products}

    @http.route('/get_location_wise_lot_and_quantity', type='json', auth='user')
    def get_location_wise_lot_and_quantity_api(self, **rec):
        product = rec['product']
        location = rec['location']
        quant_available = []
        [quant_available.append({"product" : x.display_name, "location" : x.location_id.complete_name, "lot_id" : x.lot_id.name, "quantity": x.quantity}) for x in request.env['stock.quant'].search([['quantity', '>', 0]])]
        return {"stock" : [x for x in quant_available if x['product']==product and x['location']==location]}

'''
/create_price
{
    "jsonrpc" : "2.0",
    "params" : {
        "name" : "Demo STG3",
        "label" : "STG",
        "item" : "Green Leaf",
        "qu_inc" : 0.0,
        "qt_inc" : 0.0,
        "rate" : 12.0
    }
}

{
    "params" : {
        "stg" : "My Company",
        "quantity" : "1000"
    }
}

{
    "jsonrpc" : "2.0",
    "params" : {
        "seller" : "My Company",
        "expiry_date" : "2019-01-01",
        "q_json_str" : "{'cuts' : {'20' : 1,'30' : 2,'50' : 3}}	",
        "k_json_str" : "{'cuts' : {'1000' : 1,'1500' : 2,'2000' : 3}}"
        "t_json_str" : "{'cuts':{'100':10,}}",
    }
}

#get incentive apis

{
    "jsonrpc" : "2.0",
    "params" : {
        "stg":"Test",
        "distance" : "100"
    }
}

{
    "jsonrpc": "2.0",
    "params" : {
        "product_name" : "BP",
        "lot_name" : "0000003",
        "partner_name" : "Test",
        "picking_type" : "My Company: TSPT_RECEPITS",
        "location_A" : "WH/Stock",
        "location_B" : "TSPT"
    }
}

{
    "jsonrpc": "2.0",
    "params" : {
        "product_name" : "BP",
        "lot_name" : "0000004",
        "partner_name" : "Test",
        "picking_type" : "My Company: DSPT_RECEIPT",
        "location_A" : "TSPT",
        "location_B" : "DSPT"
    }
}

'''