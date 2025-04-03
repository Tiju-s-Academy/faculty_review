from odoo import fields, models

class AllocationRating(models.Model):
    _name = 'allocation.rating'
    _description = 'Allocation Rating'

    allocation_teacher_id = fields.Many2one(
        'hr.employee',
        string='Teacher',
        domain="[('department_id.name', '=', 'Allocation')]"  # Filter for Allocation department
    )

    teacher_rating = fields.Selection(
        selection=[(str(i), str(i)) for i in range(0, 11)],  # 0 to 10 stars
        string="Rating",
        default='0',
        tracking=True
    )
    teacher_feedback = fields.Text(string='FeedBack')
    student_feedback_id = fields.Many2one('student.feedback', string='Student')