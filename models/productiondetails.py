from odoo import models, fields, api
from odoo.exceptions import UserError 

class ProductionDetails(models.Model):
    _name = "farm.production.details"
    _description = "Production Details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id asc"

    egg_line_ids = fields.One2many("farm.egg.line", "production_id", string="Egg Categories",default=lambda self: [])
    total_small = fields.Integer(string="Total Small", compute="_compute_egg_totals", store=True, tracking=True)
    total_medium = fields.Integer(string="Total Medium", compute="_compute_egg_totals", store=True, tracking=True)
    total_high_medium = fields.Integer(string="Total High Medium", compute="_compute_egg_totals", store=True, tracking=True)
    total_high = fields.Integer(string="Total High", compute="_compute_egg_totals", store=True, tracking=True)
    total_double_yolk = fields.Integer(string="Total Double Yolk", compute="_compute_egg_totals", store=True, tracking=True)
    total_broken = fields.Integer(string="Total Broken", compute="_compute_egg_totals", store=True, tracking=True)
    total_white = fields.Integer(string="Total White", compute="_compute_egg_totals", store=True, tracking=True)
    total_damage = fields.Integer(string="Total Damage", compute="_compute_egg_totals", store=True, tracking=True)
    total_egg = fields.Integer(string="Total Egg", compute="_compute_egg_totals", store=True, tracking=True)
    percentage = fields.Float(string="%", compute="_compute_percentage", store=True, tracking=True)
    cumulative_egg = fields.Integer(string="Cumulative Egg", tracking=True)
    egg_weight = fields.Float(string="Egg Weight (gm)", tracking=True)
    act = fields.Integer(string="Act", tracking=True)
    date = fields.Date(string="Production Date", default=fields.Date.context_today, tracking=True)
    flock_id = fields.Many2one("farm.layer.flock", string="Flock", tracking=True)
    total_hens = fields.Integer(string="Total Hens", tracking=True)

    @api.onchange("flock_id")
    def _onchange_get_flock_data(self):
        self.total_hens = self.flock_id.opening_bird_count

    @api.depends("egg_line_ids.egg_type", "egg_line_ids.value")
    def _compute_egg_totals(self):
        for rec in self:
            rec.total_small = sum(line.value for line in rec.egg_line_ids if line.egg_type == "small")
            rec.total_medium = sum(line.value for line in rec.egg_line_ids if line.egg_type == "medium")
            rec.total_high_medium = sum(line.value for line in rec.egg_line_ids if line.egg_type == "high_medium")
            rec.total_high = sum(line.value for line in rec.egg_line_ids if line.egg_type == "high")
            rec.total_double_yolk = sum(line.value for line in rec.egg_line_ids if line.egg_type == "double_yolk")
            rec.total_broken = sum(line.value for line in rec.egg_line_ids if line.egg_type == "broken")
            rec.total_white = sum(line.value for line in rec.egg_line_ids if line.egg_type == "white")
            rec.total_damage = sum(line.value for line in rec.egg_line_ids if line.egg_type == "damage")

            rec.total_egg = (
                rec.total_small
                + rec.total_medium
                + rec.total_high_medium
                + rec.total_high
                + rec.total_double_yolk
                + rec.total_broken
                + rec.total_white
                + rec.total_damage
            )

    @api.depends("total_egg", "total_hens")
    def _compute_percentage(self):
        for record in self:
            record.percentage = (record.total_egg / record.total_hens) * 100 if record.total_hens else 0.0


class EggLine(models.Model):
    _name = "farm.egg.line"
    _description = "Egg Line"
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    production_id = fields.Many2one(
        "farm.production.details",
        string="Production",
        ondelete="cascade",
        tracking=True
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        tracking=True
    )

    egg_type = fields.Selection([
        ("small", "Small"),
        ("medium", "Medium"),
        ("high_medium", "High Medium"),
        ("high", "High"),
        ("double_yolk", "Double Yolk"),
        ("broken", "Broken"),
        ("white", "White"),
        ("damage", "Damage"),
    ], string="Egg Type", required=True, tracking=True)

    value = fields.Integer(string="Value", required=True, tracking=True)
    short_description = fields.Char(string="Short Description", tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string="Status", default="draft", readonly=True, tracking=True)
    
    def action_done(self):
        for line in self:
            line.state = 'done'

    def unlink(self):
        if any(line.state == 'done' for line in self):
            raise UserError("You cannot delete a record marked as Done!")
        return super(EggLine, self).unlink()
