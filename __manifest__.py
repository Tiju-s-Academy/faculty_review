{
    'name': 'Teacher Rating',
    'version': '17.0.1.0.0',
    'category': 'Education',
    'summary': 'Allow students to rate teachers',
    'description': """
        This module allows public users (students) to rate teachers based on:
        - Listening skills
        - Speaking skills
        - Reading skills
        - Orientation
        - Mock tests
        - Overall experience
    """,
    'author': 'Odoo Admin',
    'website': 'https://www.example.com',
    'depends': ['base', 'hr', 'website'],
    'data': [
        'security/teacher_rating_security.xml',
        'security/ir.model.access.csv',
        'views/hr_department_views.xml',
        'views/hr_employee_views.xml',
        'views/teacher_rating_views.xml',
        'views/teacher_rating_templates.xml',
        'views/student_feedback_views.xml',
        'views/teacher_rating_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/faculty_review/static/src/css/rating.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
