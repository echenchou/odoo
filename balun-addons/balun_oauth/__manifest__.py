# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Balun OAuth',
    'category': 'Tools',
    'description': """
巴伦域快速登录。
=============================================
""",
    'maintainer': 'Balun IT',
    'depends': ['auth_oauth'],
    'data': [
        'data/auth_oauth_data.xml',
        'data/auth_oauth_data.yml',
    ],
    'application': False,
}
