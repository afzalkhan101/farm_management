from odoo import models, fields, api 

class EggLine(models.Model):
    _name = "farm.egg.line"
    _description = "Egg Line"

    production_id = fields.Many2one("farm.production.details", string="Production", ondelete="cascade")
    
    small = fields.Integer(string="Small")
    medium = fields.Integer(string="Medium")
    high_medium = fields.Integer(string="High Medium")
    high = fields.Integer(string="High")
    double_yolk = fields.Integer(string="Double Yolk")
    broken = fields.Integer(string="Broken")
    white = fields.Integer(string="White")
    damage = fields.Integer(string="Damage")


class ProductionDetails(models.Model):
    _name = "farm.production.details"
    _description = "Production Details"
    _order = "id asc"

    egg_line_ids = fields.One2many("farm.egg.line", "production_id", string="Egg Categories")

    # Calculated totals
    total_egg = fields.Integer(string="Total Egg", compute="_compute_total_egg", store=True)
    percentage = fields.Float(string="%")
    cumulative_egg = fields.Integer(string="Cumulative Egg")
    egg_weight = fields.Float(string="Egg Weight (gm)")
    act = fields.Integer(string="Act")  

    # Extra fields for linking
    date = fields.Date(string="Production Date", default=fields.Date.context_today)
    flock_id = fields.Many2one("farm.layer.flock", string="Flock")

    @api.depends('egg_line_ids.small','egg_line_ids.medium','egg_line_ids.high_medium',
                 'egg_line_ids.high','egg_line_ids.double_yolk',
                 'egg_line_ids.broken','egg_line_ids.white','egg_line_ids.damage')
    def _compute_total_egg(self):
        for rec in self:
            rec.total_egg = sum(
                line.small + line.medium + line.high_medium +
                line.high + line.double_yolk + line.broken +
                line.white + line.damage
                for line in rec.egg_line_ids
            )
