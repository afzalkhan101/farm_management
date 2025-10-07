from odoo import models, fields

class Medicine(models.Model):
    _name = "farm.medicine"
    _description = "Medicine Information"
    _rec_name = "name"

    name = fields.Char(string="Medicine Name", required=True)
    quantity = fields.Float(string="Quantity (Kg/Lit/Pcs)")
    unit = fields.Selection([
        ('kg', 'Kg'),
        ('lit', 'Liter'),
        ('pc', 'Piece')
    ], string="Unit", default='pc')
    description = fields.Text(string="Description")
