# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo import tools

class importData(models.Model):
    _name = "import.data"
    _description="obtener datos por el rut presente en odoo"


    def _get_data_by_folio(self):
        for x in self:
            x.folio = x.partner_id.address_get(
                adr_pref=['invoice']).get('invoice', x.partner_id.id)
    
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    primera_fecha = fields.Date('First move', readonly=True)
    ultima_fecha = fields.Date('Last move', readonly=True)
    fecha_seguimiento = fields.Date('Latest follow-up', readonly=True)
    max_followup_id = fields.Many2one('followup.line', 'Max Follow Up Level', readonly=True, ondelete="cascade")
    balance = fields.Float('Balance', readonly=True)
    rutTributario = fields.Many2one('res.company', 'Company', readonly=True)
    folio = fields.Many2one('res.partner', compute='_get_data_by_folio', string='Invoice Address')

    @api.model

    def _get_account_move_entry(self, accounts, form_data, date):
        cr = self.env.cr
        MoveLine = self.env['account.move.line']
        init_wheres = [""]

        init_tables, init_where_clause, init_where_params =MoveLine._query_get()
        if init_where_clause.strip():
            init_wheres.append(init_where_clause.strip())
        if form_data['target_move'] == 'posted':
            target_move = "AND m.state = 'posted'"
        else:
            target_move = ''

        sql = (
            "aqui ira la sintaxis sql para traer los datos"
            """ SELECT 0 AS lid, 
                          l.account_id AS account_id, l.date AS ldate, j.code AS lcode, 
                          l.amount_currency AS amount_currency,l.ref AS lref,l.name AS lname, 
                          COALESCE(SUM(l.credit),0.0) AS credit,COALESCE(l.debit,0) AS debit,COALESCE(SUM(l.debit),0) - COALESCE(SUM(l.credit),0) as balance, 
                              m.name AS move_name, 
                              c.symbol AS currency_code, 
                              p.name AS lpartner_id, 
                              m.id AS mmove_id 
                            FROM 
                              account_move_line l 
                              LEFT JOIN account_move m ON (l.move_id = m.id) 
                              LEFT JOIN res_currency c ON (l.currency_id = c.id) 
                              LEFT JOIN res_partner p ON (l.partner_id = p.id) 
                              JOIN account_journal j ON (l.journal_id = j.id) 
                              JOIN account_account acc ON (l.account_id = acc.id) 
                            WHERE 
                              l.account_id IN %s 
                              AND l.journal_id IN %s """ + target_move + """ 
                              AND l.date = %s 
                            GROUP BY 
                              l.id, 
                              l.account_id, 
                              l.date, 
                              m.name, 
                              m.id, 
                              p.name, 
                              c.symbol, 
                              j.code, 
                              l.ref 
                            ORDER BY 
                              l.date DESC """
        )
        where_params = (tuple(accounts.ids), tuple(form_data['journal_ids']), date)
        cr.execute(sql, where_params)
        data = cr.dictfetchall()
        res = {}
        debit = credit = balance = 0.00
        for line in data:
            debit += line['debit']
            credit += line['credit']
            balance += line['balance']
        res['debit'] = debit
        res['credit'] = credit
        res['balance'] = balance
        res['lines'] = data
        return res