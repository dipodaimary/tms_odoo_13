from odoo import models, fields, api

class DryerMouth(models.Model):
    _name = 'dryer_mouth_register.data'
    _description = 'Dryer Mouth Register'
    sl_no = fields.Integer()
    item = fields.Char()
    date = fields.Date()
    amount = fields.Float()
    unit = fields.Char()