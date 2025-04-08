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

        if course == 'PTE':
            request.session['mentor_rating'] = {
                'mentor_id': False,
                'mentor_rating': '0',
            }
            return request.redirect('/institute_rating/form')
        else:
            return request.redirect('/mentor_rating/form')


    @http.route('/mentor_rating/form', type='http', auth='public', website=True)
    def mentor_rating_form(self, **kwargs):
        course = request.session.get('course', '').upper()

        domain = [
            ('department_id.is_academic', '=', True),
        ]

        # Add course filter if available
        if course:
            domain.append(('course_ids.name', '=', course))

        mentors = request.env['hr.employee'].sudo().search(domain)

        return request.render('faculty_review.mentor_rating_form', {
            'mentors': mentors,
            'default_course': course
        })

    @http.route('/mentor_rating/submit', type='http', auth='public', website=True)
    def mentor_rating(self, **kwargs):
        request.session['mentor_rating'] = {
            'mentor_id': kwargs.get('mentor_id'),
            'mentor_rating': kwargs.get('mentor_rating', '0'),
            'mentor_feedback': kwargs.get('mentor_feedback', ''),
        }
        return request.redirect('/institute_rating/form')



    @http.route('/institute_rating/form', type='http', auth='public', website=True)
    def institute_rating_form(self, **kwargs):
        course = request.session.get('course', '').upper()
        return request.render('faculty_review.institute_rating_form', {
            'default_course': course
        })

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
        course = request.session.get('course', '').upper()

        # Only show allocation rating for OET course
        if course != 'OET':
            request.session['allocation_ratings'] = []  # Empty allocation ratings for non-OET
            return request.redirect('/teacher_rating/final_thanks')

        allocation_teacher = request.env['hr.employee'].sudo().search([('name', '=', 'Deepthy Mohandas')])
        return request.render('faculty_review.allocation_rating_form', {
            'allocation_teacher': allocation_teacher,
            'course': course
        })

    @http.route('/allocation_rating/submit', type='http', auth='public', methods=['POST'], csrf=False)
    def allocation_submit_rating(self, **kwargs):
        course = request.session.get('course', '').upper()
        allocation_ratings = []

        # Only process allocation ratings for OET course
        if course == 'OET':
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
        return request.redirect('/teacher_rating/final_thanks')

    @http.route('/teacher_rating/final_thanks', type='http', auth='public', website=True)
    def final_thanks(self, **kwargs):
        teacher_ratings = request.session.get('teacher_ratings', [])
        institute_rating = request.session.get('institute_rating', {})
        allocation_rating = request.session.get('allocation_ratings',[])
        mentor_rating = request.session.get('mentor_rating', {})
        course = request.session.get('course', '')

        if not teacher_ratings or not institute_rating:
            return request.redirect('/teacher_rating/form')

        vals = {
            'name': request.session.get('student_name'),
            'course': course,
            'batch': request.session.get('batch'),
            'orientation_rating': institute_rating.get('orientation_rating', '0'),
            'mock_test_rating': institute_rating.get('mock_test_rating', '0'),
            'orientation_feedback': institute_rating.get('orientation_feedback', ''),
            'mock_test_feedback': institute_rating.get('mock_test_feedback', ''),
        }

        if course != 'PTE':
            vals.update({
                'mentor_id': mentor_rating.get('mentor_id'),
                'mentor_rating': mentor_rating.get('mentor_rating', '0'),
                'mentor_feedback': mentor_rating.get('mentor_feedback', ''),
            })

        feedback_record = request.env['student.feedback'].sudo().create(vals)

        # Create teacher ratings
        for rating in teacher_ratings:
            rating['student_feedback_id'] = feedback_record.id
            request.env['teacher.rating'].sudo().create(rating)

        # Create allocation ratings only for OET course
        if course == 'OET':
            for rating in allocation_rating:
                rating['student_feedback_id'] = feedback_record.id
                request.env['allocation.rating'].sudo().create(rating)

        # Clear session data
        request.session.pop('teacher_ratings', None)
        request.session.pop('institute_rating', None)
        request.session.pop('allocation_ratings', None)
        request.session.pop('mentor_rating', None)
        request.session.pop('student_name', None)
        request.session.pop('course', None)
        request.session.pop('batch', None)

        return request.render('faculty_review.final_thank_you_template')

    # ----------------- CO Worker rating -----------
    @http.route('/coworker_rating/form', type='http', auth="user", website=True)
    def coworker_rating_form(self, **kwargs):
        employee = request.env.user.employee_id
        if not employee:
            return request.redirect('/web/login')
        # Get current employee's coworkers (same department excluding self)
        course = kwargs.get('course', '').upper()
        valid_courses = ['IELTS', 'OET', 'PTE', 'GERMAN']
        if course and course not in valid_courses:
            course = ''

        domain = [
            ('department_id.is_academic', '=', True),
            ('id', '!=', employee.id)  # Exclude current employee
        ]
        if course:
            domain.append(('course_ids.name', '=', course))

        teachers = request.env['hr.employee'].sudo().search(domain)

        return request.render('faculty_review.coworker_rating_form', {
            'teachers': teachers,
            'default_course': course
        })

    @http.route('/coworker_rating/submit', type='http', auth="user", methods=['POST'], website=True, csrf=False)
    def submit_coworker_rating(self, **post):
        employee = request.env.user.employee_id
        print(employee)
        # Create coworker rating record
        rating = request.env['coworker.rating'].sudo().create({
            'rater_id': employee.id,
            'course': post.get('course'),
        })

        for key, value in post.items():
            if key.startswith('rating_'):
                coworker_id = int(key.split('_')[1])
                feedback = post.get(f'feedback_{coworker_id}', '')
                request.env['teacher.rating'].sudo().create({
                    'co_worker_feedback_id': rating.id,
                    'teacher_id': coworker_id,
                    'teacher_rating': value,
                    'teacher_feedback': feedback,
                })
        return request.redirect('/coworker_rating/thanks')

    @http.route('/coworker_rating/thanks', type='http', auth="user", website=True)
    def rating_thanks(self, **kwargs):
        return request.render('faculty_review.final_thank_you_template')

