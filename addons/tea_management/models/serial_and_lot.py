from odoo import fields, models, api, _
from datetime import datetime

class SerialAndLot(models.Model):
    _name = 'tea_management.serial_and_lot'
    entry_date = fields.Datetime(string="Date", default=lambda *a: datetime.now(), required=True)
    serial = fields.Text()
    custom_serial = fields.Text()
    product_name = fields.Text()
    quantity_in_lot = fields.Float()
    status = fields.Text()

