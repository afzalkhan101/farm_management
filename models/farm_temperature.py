from odoo import models, fields

class FarmTemperature(models.Model):
    
    _name = "farm.temperature"
    _description = "Temperature Record"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 
    _order = "date desc"

    date = fields.Date(string="Date", required=True, tracking=True)
    time = fields.Float(string="Time (optional)", tracking=True)  
    inside_min = fields.Float(string="Inside Temp Min (°C)", required=True, tracking=True)
    inside_max = fields.Float(string="Inside Temp Max (°C)", required=True, tracking=True)
    outside_min = fields.Float(string="Outside Temp Min (°C)", required=True, tracking=True)
    outside_max = fields.Float(string="Outside Temp Max (°C)", required=True, tracking=True)
    notes = fields.Text(string="Notes", tracking=True)
