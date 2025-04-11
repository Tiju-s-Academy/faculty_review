from odoo import models, fields, api, tools

class TeacherRatingDashboard(models.Model):
    _name = 'teacher.rating.dashboard'
    _description = 'Teacher Rating Dashboard'
    _auto = False

    teacher_id = fields.Many2one('hr.employee', string='Teacher')
    course_id = fields.Many2one('student.course', string='Course')

    rating_10 = fields.Integer(string='10 Stars Count')
    rating_9 = fields.Integer(string='9 Stars Count')
    rating_8 = fields.Integer(string='8 Stars Count')
    rating_7 = fields.Integer(string='7 Stars Count')
    rating_6 = fields.Integer(string='6 Stars Count')
    rating_5 = fields.Integer(string='5 Stars Count')
    rating_4 = fields.Integer(string='4 Stars Count')
    rating_3 = fields.Integer(string='3 Stars Count')
    rating_2 = fields.Integer(string='2 Stars Count')
    rating_1 = fields.Integer(string='1 Stars Count')
    rating_0 = fields.Integer(string='0 Stars Count')
    total_ratings = fields.Integer(string='Total Ratings')
    average_rating = fields.Float(string='Average Rating', digits=(3, 2))

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW teacher_rating_dashboard AS (
                SELECT 
                    row_number() OVER () AS id,
                    tr.teacher_id,
                    sc.id AS course_id,  -- Changed from course_name to course_id
                    COUNT(CASE WHEN tr.teacher_rating = '10' THEN 1 END) AS rating_10,
                    COUNT(CASE WHEN tr.teacher_rating = '9' THEN 1 END) AS rating_9,
                    COUNT(CASE WHEN tr.teacher_rating = '8' THEN 1 END) AS rating_8,
                    COUNT(CASE WHEN tr.teacher_rating = '7' THEN 1 END) AS rating_7,
                    COUNT(CASE WHEN tr.teacher_rating = '6' THEN 1 END) AS rating_6,
                    COUNT(CASE WHEN tr.teacher_rating = '5' THEN 1 END) AS rating_5,
                    COUNT(CASE WHEN tr.teacher_rating = '4' THEN 1 END) AS rating_4,
                    COUNT(CASE WHEN tr.teacher_rating = '3' THEN 1 END) AS rating_3,
                    COUNT(CASE WHEN tr.teacher_rating = '2' THEN 1 END) AS rating_2,
                    COUNT(CASE WHEN tr.teacher_rating = '1' THEN 1 END) AS rating_1,
                    COUNT(CASE WHEN tr.teacher_rating = '0' THEN 1 END) AS rating_0,
                    COUNT(*) AS total_ratings,
                    AVG(CAST(tr.teacher_rating AS INTEGER)) AS average_rating
                FROM 
                    teacher_rating tr
                JOIN 
                    student_feedback sf ON tr.student_feedback_id = sf.id
                JOIN
                    student_course sc ON sc.name = sf.course  -- Join with course table
                GROUP BY 
                    tr.teacher_id, sc.id  -- Group by course_id instead of course_name
            )
        """)

