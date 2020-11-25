import json
import logging
import requests

from odoo import http, _, exceptions
from odoo.http import request
_logger = logging.getLogger(__name__)

class ProductAPI(http.Controller):
    @http.route('/get_exceptions', type='http', auth='user', methods=['GET'], csrf=False)
    def get_exceptions(self):
        vendor_exceptions = []
        for entry in request.env['x_vendorexceptions'].search([]):
            vendor_exceptions.append({'name': entry.x_name, 'item': entry.x_product, 'rate': entry.x_rate})
        return http.Response(
            json.dumps(vendor_exceptions),
            status=200,
            mimetype='application/json'
        )




'''
self.env['x_vendorexceptions'].search([])
self.env['x_vendorexceptions'].search([('name', '=', 'demo')]).unlink()
self.env['x_vendorexceptions'].create([{'x_name':'Demo STG1', 'x_product':'Green Leaf', 'x_rate':12.0}])
self.env['x_vendorexceptions'].create([{'x_name':'Demo STG2', 'x_product':'Green Leaf', 'x_rate':13.0}])
self.env.cr.commit()

{
    "jsonrpc" : "2.0",
    "params" : {
        "name" : "Demo STG3",
        "item" : "Coal",
        "rate" : 12.0
    }
}
'''