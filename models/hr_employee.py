from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    color = fields.Integer(string="Color Index", help="Color index for kanban view.")
    department_color = fields.Integer(related='department_id.color', string="Department Color", store=True)
    academic_department = fields.Boolean(related='department_id.is_academic', string="Academic Department", store=True)
    # Add any necessary fields or methods here
    pass