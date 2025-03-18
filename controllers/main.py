from odoo import http
import json
from odoo.http import request, Response

class TeacherRatingController(http.Controller):
    
    @http.route('/teacher_rating/form', type='http', auth='public', website=True)
    def rating_form(self, **kwargs):
        teachers = request.env['hr.employee'].sudo().search([('department_id.is_academic', '=', True)])
        return request.render('faculty_review.teacher_rating_form', {'teachers': teachers})

    @http.route('/teacher_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_rating(self, **kwargs):
        try:
            vals = {
                'teacher_id': int(kwargs.get('teacher_id')),
                'course': kwargs.get('course'),
                'batch': kwargs.get('batch'),
                'listening_rating': float(kwargs.get('listening_rating', 0.0)),
                'speaking_rating': float(kwargs.get('speaking_rating', 0.0)),
                'reading_rating': float(kwargs.get('reading_rating', 0.0)),
                'writing_rating': float(kwargs.get('writing_rating', 0.0)),
                'state': 'draft'
            }
            rating = request.env['teacher.rating'].sudo().create(vals)
            request.session['last_teacher_rating_id'] = rating.id
            return request.redirect('/institute_rating/form')
        except Exception as e:
            return json.dumps({'success': False, 'error': str(e)})

    @http.route('/teacher_rating/intermediate_thanks', type='http', auth='public', website=True)
    def intermediate_thanks(self, **kwargs):
        return request.render('faculty_review.intermediate_thank_you_template')

    @http.route('/institute_rating/form', type='http', auth='public', website=True)
    def institute_rating_form(self, **kwargs):
        return request.render('faculty_review.institute_rating_form')

    @http.route('/institute_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_institute_rating(self, **kwargs):
        try:
            vals = {
                'is_institute_rating': True,
                'course': kwargs.get('course', 'Institute Rating'),
                'batch': kwargs.get('batch', 'General'),
                'orientation_rating': float(kwargs.get('orientation_rating', 0.0)),
                'mock_test_rating': float(kwargs.get('mock_test_rating', 0.0)),
                'orientation_feedback': kwargs.get('orientation_feedback'),
                'mock_test_feedback': kwargs.get('mock_test_feedback'),
                'state': 'submitted'
            }
            request.env['teacher.rating'].sudo().create(vals)
            return request.redirect('/teacher_rating/final_thanks')
        except Exception as e:
            return Response(json.dumps({'success': False, 'error': str(e)}), 
                          content_type='application/json', status=400)

    @http.route('/teacher_rating/thank_you', type='http', auth='public', website=True)
    def thank_you(self, **kwargs):
        return request.render('faculty_review.thank_you_template')

    @http.route('/teacher_rating/final_submit', type='http', auth='public', methods=['POST'], csrf=True)
    def final_submit(self, **kwargs):
        ratings = request.session.get('teacher_ratings', [])
        institute_rating = request.session.get('institute_rating')
        
        if not ratings or not institute_rating:
            return request.redirect('/teacher_rating/form')
        
        # Create all ratings
        for rating in ratings:
            request.env['teacher.rating'].sudo().create(rating)
        
        # Clear session data
        request.session.pop('teacher_ratings', None)
        request.session.pop('institute_rating', None)
        
        return request.render('faculty_review.thank_you_template')

    @http.route('/teacher_rating/final_thanks', type='http', auth='public', website=True)
    def final_thanks(self, **kwargs):
        return request.render('faculty_review.final_thank_you_template')

    @http.route('/teacher_rating/submit_all', type='json', auth='public', website=True)
    def submit_all_ratings(self, **kwargs):
        data = json.loads(request.httprequest.data)
        
        # Create teacher ratings
        for rating in data['teacher_ratings']:
            rating['is_institute_rating'] = False
            request.env['teacher.rating'].sudo().create(rating)
        
        # Create institute rating
        institute_rating = data['institute_rating']
        institute_rating['is_institute_rating'] = True
        request.env['teacher.rating'].sudo().create(institute_rating)
        
        return {'success': True}