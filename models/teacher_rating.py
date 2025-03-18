from odoo import api, fields, models

class TeacherRating(models.Model):
    _name = 'teacher.rating'
    _description = 'Teacher Rating'
    _inherit = ['mail.thread']
    
    name = fields.Char(compute='_compute_name', store=True)
    teacher_id = fields.Many2one('hr.employee', string='Teacher', required=True,
        domain="[('department_id.is_academic', '=', True)]")
    course = fields.Char(string='Course', required=True)
    batch = fields.Char(string='Batch', required=True)
    
    listening_rating = fields.Float(string='Listening Rating', required=True, 
        digits=(2,1), default=0.0)
    speaking_rating = fields.Float(string='Speaking Rating', required=True,
        digits=(2,1), default=0.0)
    reading_rating = fields.Float(string='Reading Rating', required=True,
        digits=(2,1), default=0.0)
    writing_rating = fields.Float(string='Writing Rating', required=True,
        digits=(2,1), default=0.0)
    
    orientation_rating = fields.Float(string='Orientation Rating',
        digits=(2,1), default=0.0)
    orientation_feedback = fields.Text(string='Orientation Feedback')
    
    mock_test_rating = fields.Float(string='Mock Test Rating',
        digits=(2,1), default=0.0)
    mock_test_feedback = fields.Text(string='Mock Test Feedback')
    
    overall_rating = fields.Float(string='Overall Rating', compute='_compute_overall_rating',
        store=True, digits=(2,1))
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ], string='Status', default='draft', tracking=True)
    
    @api.depends('teacher_id', 'course', 'batch')
    def _compute_name(self):
        for record in self:
            if record.teacher_id and record.course and record.batch:
                record.name = f"{record.teacher_id.name} - {record.course} ({record.batch})"
            else:
                record.name = "New Rating"
    
    @api.depends('listening_rating', 'speaking_rating', 'reading_rating',
                'writing_rating', 'orientation_rating', 'mock_test_rating')
    def _compute_overall_rating(self):
        for record in self:
            ratings = [
                record.listening_rating,
                record.speaking_rating,
                record.reading_rating,
                record.writing_rating,
                record.orientation_rating,
                record.mock_test_rating
            ]
            valid_ratings = [r for r in ratings if r > 0]
            record.overall_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0