from odoo import models, fields, api

class DryerMouth(models.Model):
    _name = 'packing_register.data'
    _description = 'Packing Register'
    sl_no = fields.Integer()
    invoice_number = fields.Char()
    grade = fields.Char()
    weight = fields.Float()
    UniqueInv = fields.Char()
    dispatch_date = fields.Date()
    week = fields.Integer()
    month = fields.Char()
    year = fields.Integer()
    dispatched = fields.Char()