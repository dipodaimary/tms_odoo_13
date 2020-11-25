import logging
from odoo import http
from odoo.http import request
import json


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
        string_obj = request.env['tea_management.price_incentive'].search([['seller', '=', stg_name]])
        q_dict = json.loads(string_obj.Q.replace('\t', '').replace('\n', '').replace("'", '"'))
        k_dict = json.loads(string_obj.K.replace('\t', '').replace('\n', '').replace("'", '"'))
        t_dict = json.loads(string_obj.T.replace('\t', '').replace('\n', '').replace("'", '"'))
        return q_dict, k_dict, t_dict

    def q_incentive(self, stg_name, quality):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            return q_dict['cuts'][str(quality)]
        except:
            return 0.0

    def k_incentive(self, stg_name, quantity):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            return k_dict['cuts'][str(quantity)]
        except:
            return 0.0

    def t_incentive(self, stg_name, distance):
        q_dict, k_dict, t_dict = self.get_price_incentive_dict(stg_name)
        try:
            return t_dict['cuts'][str(distance)]
        except:
            return 0.0

    @http.route('/get_q_incentive', type='json', auth='user')
    def get_q_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        quality = rec.get('quality', False)
        try:
            return {"incentive" : self.q_incentive(stg, quality)}
        except:
            return {"price": 0}

    @http.route('/get_k_incentive', type='json', auth='user')
    def get_k_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        quantity = rec.get('quantity', False)
        try:
            return {"incentive" : self.k_incentive(stg, quantity)}
        except:
            return {"price": 0}

    @http.route('/get_t_incentive', type='json', auth='user')
    def get_t_incentive_api(self, **rec):
        stg = rec.get('stg', False)
        distance = rec.get('distance', False)
        try:
            return {"incentive" : self.t_incentive(stg, distance)}
        except:
            return {"price": 0}
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
'''