# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from random import choice
from string import digits

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _description = "Employee"

    def _default_random_pin(self):
        return ("".join(choice(digits) for i in range(4)))


    attendance_card_id = fields.Char(string="Attendance Card ID", help="ID used for Balun Attendance Card identification.", copy=False)

    attendance_ids = fields.One2many('balun.attendance', 'employee_id', help='list of attendances for the employee')
    last_attendance_id = fields.Many2one('balun.attendance', compute='_compute_last_attendance_id')

    _sql_constraints = [('attendance_card_id_uniq', 'unique (attendance_card_id)', "The Attendance Card ID must be unique, this one is already assigned to another employee.")]


    @api.depends('attendance_ids')
    def _compute_last_attendance_id(self):
        for employee in self:
            employee.last_attendance_id = employee.attendance_ids and employee.attendance_ids[0] or False


    @api.model
    def attendance_scan(self, attendance_card_id):
        """ Receive a barcode scanned from the Kiosk Mode and change the attendances of corresponding employee.
            Returns either an action or a warning.
        """
        employee = self.search([('attendance_card_id', '=', attendance_card_id)], limit=1)
        return employee

    @api.multi
    def attendance_action(self, next_action):
        """ Changes the attendance of the employee.
            Returns an action to the check in/out message,
            next_action defines which menu the check in/out message should return to. ("My Attendances" or "Kiosk Mode")
        """
        self.ensure_one()
        action_message = self.env.ref('balun_attendance.balun_attendance_action_greeting_message').read()[0]
        action_message['previous_attendance_change_date'] = self.last_attendance_id and (self.last_attendance_id.check_out or self.last_attendance_id.check_in) or False
        if action_message['previous_attendance_change_date']:
            action_message['previous_attendance_change_date'] = \
                fields.Datetime.to_string(fields.Datetime.context_timestamp(self, fields.Datetime.from_string(action_message['previous_attendance_change_date'])))
        action_message['employee_name'] = self.name
        action_message['next_action'] = next_action

        if self.user_id:
            modified_attendance = self.sudo(self.user_id.id).attendance_action_change()
        else:
            modified_attendance = self.sudo().attendance_action_change()
        action_message['attendance'] = modified_attendance.read()[0]
        return {'action': action_message}

    @api.multi
    def attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))
        action_date = fields.Datetime.now()

        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)
        else:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
            if attendance:
                attendance.check_out = action_date
            else:
                raise exceptions.UserError(_('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                    'Your attendances have probably been modified manually by human resources.') % {'empl_name': self.name, })
            return attendance
