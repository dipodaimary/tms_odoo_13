from odoo import fields, models, api, _
from datetime import datetime

class PriceIncentives(models.Model):
    _name = 'tea_management.price_incentive'
    entry_date = fields.Datetime(string="Date", default=lambda *a: datetime.now(), required=True)
    seller = fields.Many2many('res.partner')
    expiry_date = fields.Date()
    Q = fields.Text()
    K = fields.Text()
    T = fields.Text()

