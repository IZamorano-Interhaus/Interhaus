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
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/account_account_type.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/ledger_menu.xml',
        'views/financial_report.xml',
        'views/settings.xml',
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
    'demo': [
        'demo/demo.xml',
    ],
}
