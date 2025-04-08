from odoo import models, fields, api

class CoworkerRating(models.Model):
    _name = 'coworker.rating'
    _description = 'Employee Coworker Ratings'
    _rec_name = 'rater_id'

    rater_id = fields.Many2one('hr.employee', string="Rater", default=lambda self: self.env.user.employee_id,
                               readonly=True)

    course = fields.Char(string='Course', required=True,readonly=True)
    teacher_rating_ids = fields.One2many('teacher.rating', 'co_worker_feedback_id', string='Co-workers Ratings')

