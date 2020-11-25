import logging
from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)
class GetController(http.Controller):
    @http.route('/user_name', type='json',  auth='user', methods=['POST'], csrf=False)
    def user_name(self, **rec):
        pos = rec.get('function', False)
        data = request.env['res.partner'].search([['function', '=', pos]])
        names = []
        for i in range(len(data)):
            names.append(data[i].name)
            i += 1
        if len(names) > 0:
            return {"names": names}
        else:
            return {"name": None}

    @http.route('/insert_stg', type='json', auth='user', methods=['POST'], csrf=False)
    def insert_stg(self, **rec):
        name = rec.get('name', False)
        try:
            data = request.env['res.partner'].create([{'name': name, 'function': 'STG'}])
            if data:
                return {"message": "Success"}
            else:
                return {"message": "Not Inserted"}
        except Exception as e:
            return {"message": "Not Inserted"}

    @http.route('/insert_labour', type='json', auth='user', methods=['POST'], csrf=False)
    def insert_labour(self, **rec):
        name = rec.get('name', False)
        try:
            data = request.env['res.partner'].create([{'name': name, 'function': 'Labour'}])
            if data:
                return {"message": "Success"}
            else:
                return {"message": "Not Inserted"}
        except Exception as e:
            return {"message": "Not Inserted"}
'''
http://localhost:8069/user_name
{
    "jsonrpc": "2.0",
    "params" : {
        "function": "Labour"
    } 
}
http://localhost:8069/insert_stg
{
    "jsonrpc": "2.0",
    "params" : {
        "name": "STG 4"
    } 
}
http://localhost:8069/insert_labour
{
    "jsonrpc": "2.0",
    "params" : {
        "name": "STG 4"
    } 
}
'''