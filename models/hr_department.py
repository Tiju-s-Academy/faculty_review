from odoo import models, fields, api

class HrDepartment(models.Model):
    _inherit = 'hr.department'
    
    is_academic = fields.Boolean(string='Is Academic Department', default=False)
    total_employee = fields.Integer(string='Total Employees', compute='_compute_total_employee', store=True)

    @api.depends('child_ids')
    def _compute_total_employee(self):
        for department in self:
            employee_domain = [('department_id', '=', department.id)]
            department.total_employee = self.env['hr.employee'].search_count(employee_domain)