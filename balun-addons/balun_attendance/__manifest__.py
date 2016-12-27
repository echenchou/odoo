# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Balun Attendances',
    'version': '1.0',
    'category': 'Human Resources',
    'summary': 'Manage employee attendances',
    'description': """
巴伦考勤模块.
==================================================

显示员工考勤记录，导出考勤报表.
       """,
    'maintainer': 'Balun IT',
    'depends': ['hr'],
    'data': [
        'security/balun_attendance_security.xml',
        'security/ir.model.access.csv',
        'views/web_asset_backend_template.xml',
        'views/balun_attendance_view.xml',
        'views/hr_department_view.xml',
        'views/hr_employee_view.xml',
    ],
    'application': True,
}
