from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    color = fields.Integer(string="Color Index", help="Color index for kanban view.")
    department_color = fields.Integer(related='department_id.color', string="Department Color", store=True)
    academic_department = fields.Boolean(related='department_id.is_academic', string="Academic Department", store=True)
    profile_image = fields.Image("Profile Image", max_width=512, max_height=512)

    course_ids = fields.Many2many(
        'student.course',
        string='Courses Taught',
        help="Courses this teacher is associated with"
    )

    # Add any necessary fields or methods here
    pass


class StudentCourse(models.Model):
    _name = 'student.course'
    _description = 'Student Courses'

    name = fields.Char(required=True)
    code = fields.Char()