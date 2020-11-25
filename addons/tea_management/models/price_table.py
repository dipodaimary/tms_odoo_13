from odoo import models, fields

class PriceTable(models.Model):
    _name = 'price_table.data'
    _description = 'Manage Price'
    name = fields.Char()
    label = fields.Char()
    item = fields.Char()
    quantity_incentive = fields.Float()
    quality_incentive = fields.Float()
    rate = fields.Float()