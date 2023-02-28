# -*- coding: utf-8 -*-
import psycopg2,json,os,sys
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module' 
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Proveedor",
        copy=False,
        index=True,
    )
    rut_tributario = fields.Char(
        string="Rut",
    )   
    tipo_documento=fields.Many2one(
        comodel_name="res.partner",
        string="Tipo de Documento",
        copy=False,
        index=True,
    )
    folio_documento = fields.Many2one(
        comodel_name="account.analytic.account",
        string="Folio",
        copy=False,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        default=lambda l: l.env.company.id
    )
    date_start = fields.Date(
        string="Fecha contable",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
    )
    referencia_pago = fields.Char(
        string="Referencia de pago",
        help="La referencia de pago para establecer en apuntes de diario.",
    )
    fecha_factura = fields.Date(
        string="Fecha factura",
        default=fields.Date.context_today
    )
    terminos_pagos = fields.Many2one(
        comodel_name="account.move",
        string="Términos de Pago",
        copy=False,
        index=True,
    )
    codigo_documento = fields.Char(
        string="Número del documento",
    )
    razon_social = fields.Char(
        string="nombre de la empresa que emite factura o la razon social",
    )
    acuseRecibo = fields.Selection(
        selection=[
            ('not_sent', 'Pendiente de ser enviado'),
            ('accepted','Aceptado'),
            ('ask_for_status', 'Consultar Estado Doc'),
            ('objected','Aceptado con reparos'),
            ('cancelled','Anulado'),
            ('rejected', 'Rechazado'),
            ('manual','Manual ( borrador)'),
        ],
        string='acusoRecibo',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='manual',
    )
    trackId = fields.Integer('Id de seguimiento')
    journal_id = fields.Many2one(
        'account.move', 'Diario',default='Vendor Bills',
    )
    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        'Cuenta Analitica'
    )
    date = fields.Date(
        'Starting Date', 
        required=True, 
        default=date.today()
    )
    state = fields.Selection(
        selection=[('draft', 'Draft'),
        ('running', 'Running')],
        default='draft', string='estado'
    )
    partner_id = fields.Many2one(
        'res.partner', 
        'Partner',
    )
    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )
    assigned_to = fields.Many2one(
        comodel_name="res.users",
        string="Approver",
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("new_module.group_purchase_request_manager").id,
            )
        ],
        index=True,
    )
    # === Payment widget fields === #
    invoice_outstanding_credits_debits_widget = fields.Binary(
        groups="account.group_account_invoice,account.group_account_readonly",
        compute='_compute_payments_widget_to_reconcile_info',
        exportable=False,
    )
    invoice_has_outstanding = fields.Boolean(
        groups="account.group_account_invoice,account.group_account_readonly",
        compute='_compute_payments_widget_to_reconcile_info',
    )
    invoice_payments_widget = fields.Binary(
        groups="account.group_account_invoice,account.group_account_readonly",
        compute='_compute_payments_widget_reconciled_info',
        exportable=False,
    )
    partner_credit_warning = fields.Text(
        compute='_compute_partner_credit_warning',
        groups="account.group_account_invoice,account.group_account_readonly",
    )
    montoNeto = fields.Monetary('monto neto sin iva',
        compute='_compute_amount', currency_field='company_currency_id',store=True, readonly=True,)
    montoIvaRecuperable = fields.Monetary('monto con iva incluido',
        compute='_compute_amount',currency_field='company_currency_id', store=True, readonly=True,)
    monto_Total = fields.Monetary('Monto',compute='_compute_amount',currency_field='company_currency_id', store=True, readonly=True,)

    def _get_invoice_partner_id(self):
        for rec in self:
            rec.invoice_partner_id = rec.partner_id.address_get(
                adr_pref=['invoice']).get('invoice', rec.partner_id.id)
    @api.model
    def cargarDocumentos(self, *post):
        os.system('cls')
        listaRut=[]
        conn = psycopg2.connect(database="testing", user = "postgres", password = "admin", host = "localhost", port = "5432")
        cur = conn.cursor()
        f = open("C:/tools/respaldoBaseDatos/doc_SII_202301", "r")
        archivoJSON = f.read()
        datosJSON = json.loads(archivoJSON)
        for ingreso in (datosJSON["ventas"]["detalleVentas"]):
            lax=[]
            try:
                if ingreso["acuseRecibo"]!=None:
                    acuse=ingreso["acuseRecibo"]
            except:
                acuse=""
            lax= ingreso["tipoDTEString"],str(ingreso["tipoDTE"]),ingreso["tipoCompra"],ingreso["rutCliente"],ingreso["razonSocial"],str(ingreso["folio"]),ingreso["fechaEmision"],ingreso["fechaRecepcion"],str(acuse),str(ingreso["montoExento"]),str(ingreso["montoNeto"]),str(ingreso["montoIvaRecuperable"]),str(ingreso["montoTotal"]),str(ingreso["ivaNoRetenido"]),str(ingreso["totalOtrosImpuestos"]),str(ingreso["valorOtroImpuesto"]),str(ingreso["tasaOtroImpuesto"]), str(ingreso["tipoDocReferencia"]),str(ingreso["trackId"]),ingreso["referencias"],ingreso["referenciado"],ingreso["reparos"],ingreso["otrosImpuestos"],ingreso["estado"]
            listaRut.append(lax)
        query = "select rutCliente,folio from borradores;" 
        cur.execute(query)
        querySelect = cur.fetchall()
        largoQuery=len(querySelect)
        for i in range(len(listaRut)): 
            existe=True
            if largoQuery==0:
                existe=False
            else: 
                existe=True
                for j in range(largoQuery):
                    if str(listaRut[i][3])==str(querySelect[j][0]) and str(listaRut[i][5])==str(querySelect[j][1]):
                        existe=True
                        break
                    else:
                        existe=False
            if existe==False:
                cur.execute("insert into borradores (tipoDTEstring,tipoDTE,tipoCompra,rutCliente,razonSocial,folio,fechaEmision,fechaRecepcion,acuseRecibo,montoExento,montoNeto,montoIvaRecuperable,montoTotal,ivaNoRetenido,totalOtrosImpuestos,valorOtroImpuesto,tasaOtroImpuesto,tipoDocReferencia,trackId,referencias,referenciado,reparos,otrosImpuestos,estado) values('"+str(listaRut[i][0])+"',"+str(listaRut[i][1])+",'"+str(listaRut[i][2])+"','"+str(listaRut[i][3])+"','"+str(listaRut[i][4])+"',"+str(listaRut[i][5])+",'"+str(listaRut[i][6])+"','"+str(listaRut[i][7])+"','"+str(listaRut[i][8])+"','"+str(listaRut[i][9])+"','"+str(listaRut[i][10])+"','"+str(listaRut[i][11])+"','"+str(listaRut[i][12])+"','"+str(listaRut[i][13])+"','"+str(listaRut[i][14])+"','"+str(listaRut[i][15])+"','"+str(listaRut[i][16])+"','"+str(listaRut[i][17])+"','"+str(listaRut[i][18])+"','"+str(listaRut[i][19])+"','"+str(listaRut[i][20])+"','"+str(listaRut[i][21])+"','"+str(listaRut[i][22])+"','"+str(listaRut[i][23])+"');")
                cur.execute(query)
                querySelect = cur.fetchall()
                largoQuery=len(querySelect)
                print("query despues del ciclo parte 2 => "+str(largoQuery))
        

        conn.commit()

        print("script completado")
        conn.close()
    def obtenerDatosVista(self, container):
        contenedor = container['records'].filtered(lambda move: move.line_ids)
        if not contenedor:
            return

        # /!\ As this method is called in create / write, we can't make the assumption the computed stored fields
        # are already done. Then, this query MUST NOT depend on computed stored fields.
        # It happens as the ORM calls create() with the 'no_recompute' statement.
        self.env['borradores'].flush_model(['debit', 'credit', 'balance', 'currency_id', 'move_id'])
        self._cr.execute('''
            select  tipodte codigo_documento,
                    tipodtestring tipo_documento,
                    rutCliente rut_tributario, 
                    folio folio_documento,
                    fechaemision date_start,
                    fecharecepcion fecha_factura,
                    razonsocial razon_social,
                    acuserecibo acuseRecibo,
                    montoNeto montoNeto,
                    montoivarecuperable Impuesto,
                    montototal total,
                    trackid
              FROM borradores 
              ;
        ''', [tuple(contenedor.ids)])

        return self._cr.fetchall()

            # return record
        # function to getting over dues
    def _post(self, soft=True):
        """Post/Validate the documents.

        Posting the documents will give it a number, and check that the document is
        complete (some fields might not be required if not posted but are required
        otherwise).
        If the journal is locked with a hash table, it will be impossible to change
        some fields afterwards.

        :param soft (bool): if True, future documents are not immediately posted,
            but are set to be auto posted automatically at the set accounting date.
            Nothing will be performed on those documents before the accounting date.
        :return Model<account.move>: the documents that have been posted
        """
        if not self.env.su and not self.env.user.has_group('account.group_account_invoice'):
            raise AccessError(_("You don't have the access rights to post an invoice."))

        for invoice in self.filtered(lambda move: move.is_invoice(include_receipts=True)):
            if invoice.quick_edit_mode and invoice.quick_edit_total_amount and invoice.quick_edit_total_amount != invoice.amount_total:
                raise UserError(_(
                    "The current total is %s but the expected total is %s. In order to post the invoice/bill, "
                    "you can adjust its lines or the expected Total (tax inc.).",
                    formatLang(self.env, invoice.amount_total, currency_obj=invoice.currency_id),
                    formatLang(self.env, invoice.quick_edit_total_amount, currency_obj=invoice.currency_id),
                ))
            if invoice.partner_bank_id and not invoice.partner_bank_id.active:
                raise UserError(_(
                    "The recipient bank account linked to this invoice is archived.\n"
                    "So you cannot confirm the invoice."
                ))
            if float_compare(invoice.amount_total, 0.0, precision_rounding=invoice.currency_id.rounding) < 0:
                raise UserError(_(
                    "You cannot validate an invoice with a negative total amount. "
                    "You should create a credit note instead. "
                    "Use the action menu to transform it into a credit note or refund."
                ))

            if not invoice.partner_id:
                if invoice.is_sale_document():
                    raise UserError(_("The field 'Customer' is required, please complete it to validate the Customer Invoice."))
                elif invoice.is_purchase_document():
                    raise UserError(_("The field 'Vendor' is required, please complete it to validate the Vendor Bill."))

            # Handle case when the invoice_date is not set. In that case, the invoice_date is set at today and then,
            # lines are recomputed accordingly.
            if not invoice.invoice_date:
                if invoice.is_sale_document(include_receipts=True):
                    invoice.invoice_date = fields.Date.context_today(self)
                elif invoice.is_purchase_document(include_receipts=True):
                    raise UserError(_("The Bill/Refund date is required to validate this document."))

        if soft:
            future_moves = self.filtered(lambda move: move.date > fields.Date.context_today(self))
            for move in future_moves:
                if move.auto_post == 'no':
                    move.auto_post = 'at_date'
                msg = _('This move will be posted at the accounting date: %(date)s', date=format_date(self.env, move.date))
                move.message_post(body=msg)
            to_post = self - future_moves
        else:
            to_post = self

        for move in to_post:
            if move.state == 'posted':
                raise UserError(_('The entry %s (id %s) is already posted.') % (move.name, move.id))
            if not move.line_ids.filtered(lambda line: line.display_type not in ('line_section', 'line_note')):
                raise UserError(_('You need to add a line before posting.'))
            if move.auto_post != 'no' and move.date > fields.Date.context_today(self):
                date_msg = move.date.strftime(get_lang(self.env).date_format)
                raise UserError(_("This move is configured to be auto-posted on %s", date_msg))
            if not move.journal_id.active:
                raise UserError(_(
                    "You cannot post an entry in an archived journal (%(journal)s)",
                    journal=move.journal_id.display_name,
                ))
            if move.display_inactive_currency_warning:
                raise UserError(_(
                    "You cannot validate a document with an inactive currency: %s",
                    move.currency_id.name
                ))

            if move.line_ids.account_id.filtered(lambda account: account.deprecated):
                raise UserError(_("A line of this move is using a deprecated account, you cannot post it."))

            affects_tax_report = move._affect_tax_report()
            lock_dates = move._get_violated_lock_dates(move.date, affects_tax_report)
            if lock_dates:
                move.date = move._get_accounting_date(move.invoice_date or move.date, affects_tax_report)

        # Create the analytic lines in batch is faster as it leads to less cache invalidation.
        to_post.line_ids._create_analytic_lines()

        # Trigger copying for recurring invoices
        to_post.filtered(lambda m: m.auto_post not in ('no', 'at_date'))._copy_recurring_entries()

        for invoice in to_post:
            # Fix inconsistencies that may occure if the OCR has been editing the invoice at the same time of a user. We force the
            # partner on the lines to be the same as the one on the move, because that's the only one the user can see/edit.
            wrong_lines = invoice.is_invoice() and invoice.line_ids.filtered(lambda aml:
                aml.partner_id != invoice.commercial_partner_id
                and aml.display_type not in ('line_note', 'line_section')
            )
            if wrong_lines:
                wrong_lines.write({'partner_id': invoice.commercial_partner_id.id})

        to_post.write({
            'state': 'posted',
            'posted_before': True,
        })

        for invoice in to_post:
            invoice.message_subscribe([
                p.id
                for p in [invoice.partner_id]
                if p not in invoice.sudo().message_partner_ids
            ])

            # Compute 'ref' for 'out_invoice'.
            if invoice.move_type == 'out_invoice' and not invoice.payment_reference:
                to_write = {
                    'payment_reference': invoice._get_invoice_computed_reference(),
                    'line_ids': []
                }
                for line in invoice.line_ids.filtered(lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable')):
                    to_write['line_ids'].append((1, line.id, {'name': to_write['payment_reference']}))
                invoice.write(to_write)

            if (
                invoice.is_sale_document()
                and invoice.journal_id.sale_activity_type_id
                and (invoice.journal_id.sale_activity_user_id or invoice.invoice_user_id).id not in (self.env.ref('base.user_root').id, False)
            ):
                invoice.activity_schedule(
                    date_deadline=min((date for date in invoice.line_ids.mapped('date_maturity') if date), default=invoice.date),
                    activity_type_id=invoice.journal_id.sale_activity_type_id.id,
                    summary=invoice.journal_id.sale_activity_note,
                    user_id=invoice.journal_id.sale_activity_user_id.id or invoice.invoice_user_id.id,
                )

        customer_count, supplier_count = defaultdict(int), defaultdict(int)
        for invoice in to_post:
            if invoice.is_sale_document():
                customer_count[invoice.partner_id] += 1
            elif invoice.is_purchase_document():
                supplier_count[invoice.partner_id] += 1
        for partner, count in customer_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('customer_rank', count)
        for partner, count in supplier_count.items():
            (partner | partner.commercial_partner_id)._increase_rank('supplier_rank', count)

        # Trigger action for paid invoices if amount is zero
        to_post.filtered(
            lambda m: m.is_invoice(include_receipts=True) and m.currency_id.is_zero(m.amount_total)
        )._invoice_paid_hook()

        return to_post
    def action_invoice_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices could be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})
        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('account.account_invoices').report_action(self)
        else:
            return self.env.ref('account.account_invoices_without_payment').report_action(self)

