from odoo import http
from odoo.http import request

class TeacherRatingController(http.Controller):
    
    @http.route('/teacher_rating/form', type='http', auth='public', website=True)
    def rating_form(self, **kwargs):
        teachers = request.env['hr.employee'].sudo().search([('department_id.is_academic', '=', True)])
        return request.render('faculty_review.teacher_rating_form', {'teachers': teachers})

    @http.route('/teacher_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_rating(self, **kwargs):
        try:
            # Create a new teacher rating record
            vals = {
                'teacher_id': int(kwargs.get('teacher_id')),
                'course': kwargs.get('course'),
                'batch': kwargs.get('batch'),
                'listening_rating': float(kwargs.get('listening_rating') or 0.0),
                'speaking_rating': float(kwargs.get('speaking_rating') or 0.0),
                'reading_rating': float(kwargs.get('reading_rating') or 0.0),
                'writing_rating': float(kwargs.get('writing_rating') or 0.0),
                'orientation_rating': float(kwargs.get('orientation_rating') or 0.0),
                'mock_test_rating': float(kwargs.get('mock_test_rating') or 0.0),
                'orientation_feedback': kwargs.get('orientation_feedback'),
                'mock_test_feedback': kwargs.get('mock_test_feedback'),
                'state': 'submitted'
            }
            request.env['teacher.rating'].sudo().create(vals)
            return request.redirect('/teacher_rating/thank_you')
        except Exception as e:
            return request.render('http_routing.http_error', {'status_code': 'Error', 'status_message': str(e)})

    @http.route('/teacher_rating/thank_you', type='http', auth='public', website=True)
    def thank_you(self, **kwargs):
        return request.render('faculty_review.thank_you_template')