from odoo import http
import json
from odoo.http import request, Response

class TeacherRatingController(http.Controller):
    
    @http.route('/teacher_rating/form', type='http', auth='public', website=True)
    def rating_form(self, **kwargs):
        course = kwargs.get('course', '').upper()
        valid_courses = ['IELTS', 'OET', 'PTE', 'GERMAN']
        if course and course not in valid_courses:
            course = ''

        domain = [('department_id.is_academic', '=', True)]
        if course:
            domain.append(('course_ids.name', '=', course))

        teachers = request.env['hr.employee'].sudo().search(domain)
        return request.render('faculty_review.teacher_rating_form', {
        'teachers': teachers,
        'default_course': course  # Pass the course to preselect in the form
    })

    @http.route('/teacher_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_rating(self, **kwargs):
        course = kwargs.get('course')
        batch = kwargs.get('batch')
        student_name = kwargs.get('student_name')
        teacher_ratings = []

        for key, value in kwargs.items():
            if key.startswith('stars_'):
                teacher_id = int(key.split('_')[1])
                rating = value
                feedback = kwargs.get(f'feedback_{teacher_id}', '')
                teacher_ratings.append({
                    'teacher_id': teacher_id,
                    'teacher_rating': rating,
                    'teacher_feedback': feedback,
                })

        request.session['teacher_ratings'] = teacher_ratings
        request.session['course'] = course
        request.session['batch'] = batch
        request.session['student_name'] = student_name
        return request.redirect('/institute_rating/form')


    @http.route('/institute_rating/form', type='http', auth='public', website=True)
    def institute_rating_form(self, **kwargs):
        return request.render('faculty_review.institute_rating_form')

    @http.route('/institute_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_institute_rating(self, **kwargs):
        request.session['institute_rating'] = {
            'orientation_rating': kwargs.get('orientation_rating', '0'),
            'orientation_feedback': kwargs.get('orientation_feedback', ''),
            'mock_test_rating': kwargs.get('mock_test_rating', '0'),
            'mock_test_feedback': kwargs.get('mock_test_feedback', ''),
        }
        return request.redirect('/allocation_rating/form')

    @http.route('/allocation_rating/form', type='http', auth='public', website=True)
    def allocation_rating_form(self, **kwargs):
        allocation_teacher = request.env['hr.employee'].sudo().search([('name', '=', 'Deepthy Mohandas')])
        return request.render('faculty_review.allocation_rating_form',{'allocation_teacher': allocation_teacher})

    @http.route('/allocation_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def allocation_submit_rating(self, **kwargs):

        allocation_ratings = []

        for key, value in kwargs.items():
            if key.startswith('stars_'):
                teacher_id = int(key.split('_')[1])
                rating = value
                feedback = kwargs.get(f'feedback_{teacher_id}', '')
                allocation_ratings.append({
                    'allocation_teacher_id': teacher_id,
                    'teacher_rating': rating,
                    'teacher_feedback': feedback,
                })

        request.session['allocation_ratings'] = allocation_ratings
        return request.redirect('/floor_rating/form')

    @http.route('/floor_rating/form', type='http', auth='public', website=True)
    def floor_rating_form(self, **kwargs):
        return request.render('faculty_review.floor_rating_form')

    @http.route('/floor_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def submit_floor_rating(self, **kwargs):
        # Store floor rating data in session
        request.session['floor_ratings'] = {
            'first_floor_rating': kwargs.get('first_floor_rating', '0'),
            'first_floor_feedback': kwargs.get('first_floor_feedback', ''),
            'second_floor_rating': kwargs.get('second_floor_rating', '0'),
            'second_floor_feedback': kwargs.get('second_floor_feedback', ''),
            'third_floor_rating': kwargs.get('third_floor_rating', '0'),
            'third_floor_feedback': kwargs.get('third_floor_feedback', ''),
            'fourth_floor_rating': kwargs.get('fourth_floor_rating', '0'),
            'forth_floor_feedback': kwargs.get('forth_floor_feedback', ''),
        }
        return request.redirect('/teacher_rating/final_thanks')


    @http.route('/teacher_rating/final_thanks', type='http', auth='public', website=True)
    def final_thanks(self, **kwargs):
        teacher_ratings = request.session.get('teacher_ratings', [])
        institute_rating = request.session.get('institute_rating', {})
        allocation_rating = request.session.get('allocation_ratings',[])
        floor_ratings = request.session.get('floor_ratings', {})

        if not teacher_ratings or not institute_rating or not allocation_rating or not floor_ratings:
            return request.redirect('/teacher_rating/form')

        feedback_record = request.env['student.feedback'].sudo().create({
            'name': request.session.get('student_name'),
            'course': request.session.get('course'),
            'batch': request.session.get('batch'),
            'orientation_rating': institute_rating.get('orientation_rating', '0'),
            'mock_test_rating': institute_rating.get('mock_test_rating', '0'),
            'orientation_feedback': institute_rating.get('orientation_feedback', ''),
            'mock_test_feedback': institute_rating.get('mock_test_feedback', ''),
            'first_floor_rating': floor_ratings.get('first_floor_rating', '0'),
            'second_floor_rating': floor_ratings.get('second_floor_rating', '0'),
            'third_floor_rating': floor_ratings.get('third_floor_rating', '0'),
            'fourth_floor_rating': floor_ratings.get('fourth_floor_rating', '0'),
            'first_floor_feedback': floor_ratings.get('first_floor_feedback', ''),
            'second_floor_feedback': floor_ratings.get('second_floor_feedback', ''),
            'third_floor_feedback': floor_ratings.get('third_floor_feedback', ''),
            'forth_floor_feedback': floor_ratings.get('forth_floor_feedback', ''),
        })

        for rating in teacher_ratings:
            rating['student_feedback_id'] = feedback_record.id
            request.env['teacher.rating'].sudo().create(rating)

        for rating in allocation_rating:
            rating['student_feedback_id'] = feedback_record.id
            request.env['allocation.rating'].sudo().create(rating)

        return request.render('faculty_review.final_thank_you_template')


