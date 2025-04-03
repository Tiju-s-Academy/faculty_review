from odoo import api, fields, models

class TeacherRating(models.Model):
    _name = 'teacher.rating'
    _description = 'Teacher Rating'

    teacher_id = fields.Many2one(
        'hr.employee', string='Teacher',
        domain="[('department_id.is_academic', '=', True)]"
    )

    teacher_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 11)],  # 0 to 10 stars
        string="Rating",
        default='0',
        tracking=True
    )
    teacher_feedback = fields.Text(string='FeedBack')
    student_feedback_id = fields.Many2one('student.feedback', string='Student')
