# -*- coding: utf-8 -*-
{
    'name': "Mi primer modulo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends':[
        'contacts',
        'account',
        ],

    # always loaded
    'data': [
    
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml'
    ],
}
