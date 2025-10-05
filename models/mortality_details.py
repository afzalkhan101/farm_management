from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta
import requests 


class MortalityDetails(models.Model):

    _name = "farm.mortality.details"
    _description = "Mortality Details"
    _inherit =['mail.thread','mail.activity.mixin']
    _order ="date desc"

    name =fields.Char(string="Reference", default="New", readonly=True)
    flock_id = fields.Many2one("farm.layer.flock",string="Flock",required=True,ondelete="cascade")
    date = fields.Date(string ="Date",required=True,default=fields.Date.today)
    state = fields.Selection([('draft', 'Draft'),('done','Done'),], default='draft')

    #Mortality breakdown fields

    normal = fields.Integer(string="Normal", default=0,tracking =True)
    culled = fields.Integer(string="Culled", default=0,tracking=True)
    vaccine = fields.Integer(string="Vaccine Reaction", default=0,tracking =True)
    prolapse = fields.Integer(string="Prolapse", default=0,tracking =True)
    heat_stress = fields.Integer(string="Heat Stress", default=0 ,tracking =True)
    mechanical = fields.Integer(string="Mechanical", default=0,tracking =True)
    injury = fields.Integer(string="Injury", default=0,tracking =True)
    other = fields.Integer(string="Other", default=0 ,tracking =True)

    # Flock related fields . 

    flock_opening_bird = fields.Integer(string="Opening Birds ")
    flock_starting_date = fields.Date(string="Starting Date ")
    flock_ending_date = fields.Date(string="Ending Date ")
    total_mortality = fields.Integer(string="Total Mortality",compute="_compute_total_mortality",store=True)
    updated_Birds =fields.Integer(string="Updated Birds")

    #other's 
    yesterday_date = fields.Date(string="Yesterday Date",default=lambda self: date.today() - timedelta(days=1))

    @api.depends('normal','culled','vaccine','prolapse','heat_stress','mechanical','injury','other')
    
    def _compute_total_mortality(self):
        for record in self:
            record.total_mortality = (record.normal+ record.culled+ record.vaccine+ record.prolapse+ record.heat_stress+ record.mechanical+ record.injury+ record.other)

    @api.model
    def create(self, vals):

        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('farm.mortality.details') or "New"
        return super(MortalityDetails, self).create(vals)
    
    @api.onchange('flock_id')
    def _onchange_get_flock_data(self):
             
        self.flock_opening_bird = self.flock_id.opening_bird_count
        self.flock_ending_date = self.flock_id.end_date 
        self.flock_starting_date = self.flock_id.start_date


    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        if self.state =='done':
            return
        self.state = 'done'
        self.flock_id.opening_bird_count =  self.flock_id.opening_bird_count - self.total_mortality
        self.updated_Birds  = self.flock_id.opening_bird_count 
    
    