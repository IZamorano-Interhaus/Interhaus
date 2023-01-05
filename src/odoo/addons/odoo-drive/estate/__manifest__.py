{
    'name': "odoo-drive",
    'version': '1.0',
    'depends': ['web'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'views/webclient_templates.xml',
        'views/report_templates.xml',
        
        'views/speedscope_template.xml',
        'views/lazy_assets.xml',
        'views/neutralize_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/demo_data.xml',
    ],
}