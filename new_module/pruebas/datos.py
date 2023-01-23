from odoo import api, fields, models,pruebas, tools
class tablaDatos(pruebas.datos):
    _name="obtencion de datos"
    _description="esta clase usa metodo get para obtener datos del odoo"

    nombre= fields.Char()
    rut = fields.Char()
    folio = fields.Integer()

    @api.model
    def ObtenerDatos(self):
        print("inicio de actividades")
        tools.drop_view_if_exists(self._cr, 'followup_stat_by_partner')
        self._cr.execute("""
            create view followup_stat_by_partner as (
                SELECT
                    l.partner_id * 10000::bigint + l.company_id as id,
                    l.partner_id AS partner_id,
                    min(l.date) AS date_move,
                    max(l.date) AS date_move_last,
                    max(l.followup_date) AS date_followup,
                    max(l.followup_line_id) AS max_followup_id,
                    sum(l.debit - l.credit) AS balance,
                    l.company_id as company_id
                FROM
                    account_move_line l
                    LEFT JOIN account_account a ON (l.account_id = a.id)
                WHERE
                    a.account_type = 'asset_receivable' AND
                    l.full_reconcile_id is NULL AND
                    l.partner_id IS NOT NULL
                    GROUP BY
                    l.partner_id, l.company_id
            )""")