from odoo import models, fields, api
from datetime import date

class LayerFlock(models.Model):
    
    _name = "farm.layer.flock"
    _description = "Layer / Broiler Flock Information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char(string="Flock Name", required=True,tracking =True)

    bird_type = fields.Selection([
        ('layer','Layer'),
        ('broiler','Broiler'),
        ('duck','Duck')],
        string="Bird Type" ,tranking =True,tracking =True)
    
    start_date = fields.Date(string="Start Date",tracking =True)
    end_date = fields.Date(string="End Date",tracking =True)
    opening_bird_count = fields.Integer(string="Opening Brids",tracking =True)
    age_in_days = fields.Integer(string="Age in Days")
    age_in_weeks = fields.Integer(string="Age in Weeks", compute="_compute_age_weeks", store=True,tracking =True)
    age_display = fields.Char(string="Age in Week", compute="_compute_age_display",tracking =True)
    extra_days = fields.Integer(string="Days",compute ="_extra_days",store =True,readonly=True,tracking =True)
    product_id = fields.Many2one('product.product', string="Product",tracking =True)
    total_qty = fields.Float(string="Current Birds",related='product_id.qty_available',tracking =True)
    note_html = fields.Html(string="Notes (HTML)")
    #relation with mortality details 

    mortality_ids = fields.One2many("farm.mortality.details", "flock_id", string="Mortality Details",tracking =True)

    @api.depends('age_in_days')
    def _compute_age_weeks(self):
        for rec in self:
            rec.age_in_weeks = rec.age_in_days /7 
    
    @api.depends("age_in_days")
    def _extra_days(self):

        for rec in self:
            rec.extra_days = rec.age_in_days % 7 

    @api.depends('age_in_weeks', 'extra_days')
    def _compute_age_display(self):
        for rec in self:
            rec.age_display = f"{rec.age_in_weeks}  weeks  {rec.extra_days} days"