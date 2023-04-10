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
        'account'
    ],

    # always loaded
    'data': [
    
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menu.xml',
        'views/ledger_menu.xml',
        'views/financial_report.xml',
        'views/settings.xml',
        'views/templates.xml',
        'wizard/account_report_common_view.xml',
        'wizard/partner_ledger.xml',
        'wizard/general_ledger.xml',
        'wizard/trial_balance.xml',
        'wizard/balance_sheet.xml',
        'wizard/profit_and_loss.xml',
        'wizard/tax_report.xml',
        'wizard/aged_partner.xml',
        'wizard/journal_audit.xml',
        'report/report.xml',
        'report/report_partner_ledger.xml',
        'report/report_general_ledger.xml',
        'report/report_trial_balance.xml',
        'report/report_financial.xml',
        'report/report_tax.xml',
        'report/report_aged_partner.xml',
        'report/report_journal_audit.xml',
        'report/report_journal_entries.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
