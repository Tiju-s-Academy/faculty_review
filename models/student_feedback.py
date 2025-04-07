from odoo import fields, models


class StudentFeedback(models.Model):
    _name = 'student.feedback'
    _description = 'Student Feedback'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name')
    course = fields.Char(string='Course', required=True)
    batch = fields.Char(string='Batch', required=True)
    teacher_rating_ids = fields.One2many('teacher.rating', 'student_feedback_id', string='Teacher Ratings')

    mentor_id = fields.Many2one('hr.employee', string='Mentor',
        domain="[('department_id.is_academic', '=', True)]"
    )
    mentor_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 11)],  # 0 to 10 stars
        string="Rating",
        default='0',
        tracking=True
    )
    mentor_feedback = fields.Text(string='FeedBack')

    allocation_rating_ids = fields.One2many('allocation.rating','student_feedback_id',string='Allocation Rating')

    # Institute ratings
    orientation_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="Orientation rating Test Rating",
        default='0',
        tracking=True
    )
    mock_test_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="Mock Test Rating",
        default='0',
        tracking=True
    )

    # Feedback fields
    orientation_feedback = fields.Text(string='Orientation Feedback')
    mock_test_feedback = fields.Text(string='Mock Test Feedback')


