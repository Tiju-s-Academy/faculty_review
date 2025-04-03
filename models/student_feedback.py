from odoo import fields, models


class StudentFeedback(models.Model):
    _name = 'student.feedback'
    _description = 'Student Feedback'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name')
    course = fields.Char(string='Course', required=True)
    batch = fields.Char(string='Batch', required=True)
    teacher_rating_ids = fields.One2many('teacher.rating', 'student_feedback_id', string='Teacher Ratings')
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

    first_floor_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="1st Floor Rating",
        default='0',
        tracking=True
    )
    second_floor_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="2nd Floor Rating",
        default='0',
        tracking=True
    )
    third_floor_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="3rd Floor Rating",
        default='0',
        tracking=True
    )
    fourth_floor_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 6)],
        string="4th Floor Rating",
        default='0',
        tracking=True
    )

    first_floor_feedback = fields.Text(string='1st Floor Feedback')
    second_floor_feedback = fields.Text(string='2nd Floor Feedback')
    third_floor_feedback = fields.Text(string='3rd Floor Feedback')
    forth_floor_feedback = fields.Text(string='4th Floor Feedback')
