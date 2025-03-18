from odoo import api, fields, models
from odoo.exceptions import ValidationError

class TeacherRating(models.Model):
    _name = 'teacher.rating'
    _description = 'Teacher Rating'
    _inherit = ['mail.thread']
    
    name = fields.Char(compute='_compute_name', store=True)
    teacher_id = fields.Many2one('hr.employee', string='Teacher',
        domain="[('department_id.is_academic', '=', True)]",
        required=False)  # Changed from required=True
    course = fields.Char(string='Course', required=True)
    batch = fields.Char(string='Batch', required=True)
    
    # Teacher specific ratings
    listening_rating = fields.Float(string='Listening Rating', required=True, 
        digits=(2,1), default=0.0)
    speaking_rating = fields.Float(string='Speaking Rating', required=True,
        digits=(2,1), default=0.0)
    reading_rating = fields.Float(string='Reading Rating', required=True,
        digits=(2,1), default=0.0)
    writing_rating = fields.Float(string='Writing Rating', required=True,
        digits=(2,1), default=0.0)
    
    # Institute ratings
    orientation_rating = fields.Float(string='Orientation Rating',
        digits=(2,1), default=0.0)
    mock_test_rating = fields.Float(string='Mock Test Rating',
        digits=(2,1), default=0.0)
    
    # Feedback fields
    orientation_feedback = fields.Text(string='Orientation Feedback')
    mock_test_feedback = fields.Text(string='Mock Test Feedback')
    
    # Computed ratings
    teacher_rating = fields.Float(string='Teacher Rating', compute='_compute_teacher_rating',
        store=True, digits=(2,1))
    institute_rating = fields.Float(string='Institute Rating', compute='_compute_institute_rating',
        store=True, digits=(2,1))
    
    overall_rating = fields.Float(string='Overall Rating', compute='_compute_overall_rating',
        store=True, digits=(2,1))
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted')
    ], string='Status', default='draft', tracking=True)
    
    is_institute_rating = fields.Boolean(string='Is Institute Rating', default=False)
    
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
    
    @api.depends('listening_rating', 'speaking_rating', 'reading_rating', 'writing_rating')
    def _compute_teacher_rating(self):
        for record in self:
            ratings = [
                record.listening_rating,
                record.speaking_rating,
                record.reading_rating,
                record.writing_rating
            ]
            valid_ratings = [r for r in ratings if r > 0]
            record.teacher_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0
    
    @api.depends('orientation_rating', 'mock_test_rating')
    def _compute_institute_rating(self):
        for record in self:
            ratings = [
                record.orientation_rating,
                record.mock_test_rating
            ]
            valid_ratings = [r for r in ratings if r > 0]
            record.institute_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0
    
    @api.constrains('teacher_id', 'is_institute_rating')
    def _check_teacher_id(self):
        for record in self:
            if not record.is_institute_rating and not record.teacher_id:
                raise ValidationError("Teacher is required for teacher ratings")
    
    @api.model
    def get_teacher_averages(self):
        ratings = self.search([('is_institute_rating', '=', False)])
        return {
            'average_teacher_rating': sum(r.teacher_rating for r in ratings) / len(ratings) if ratings else 0.0,
            'total_ratings': len(ratings),
            'teachers_rated': len(set(ratings.mapped('teacher_id.id')))
        }
    
    @api.model
    def get_institute_averages(self):
        ratings = self.search([('is_institute_rating', '=', True)])
        return {
            'average_orientation': sum(r.orientation_rating for r in ratings) / len(ratings) if ratings else 0.0,
            'average_mock_test': sum(r.mock_test_rating for r in ratings) / len(ratings) if ratings else 0.0,
            'total_ratings': len(ratings)
        }