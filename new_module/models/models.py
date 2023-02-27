from collections import defaultdict
from contextlib import ExitStack, contextmanager
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from hashlib import sha256
from json import dumps
import re
from textwrap import shorten
from unittest.mock import patch
import psycopg2,json,os,sys
from odoo import api, fields, models, _, Command
from odoo.addons.base.models.decimal_precision import DecimalPrecision
from odoo.addons.account.tools import format_rf_reference
from odoo.exceptions import UserError, ValidationError, AccessError, RedirectWarning
from odoo.tools import (
    date_utils,
    email_re,
    email_split,
    float_compare,
    float_is_zero,
    format_amount,
    format_date,
    formatLang,
    frozendict,
    get_lang,
    is_html_empty,
    sql
)


#forbidden fields
INTEGRITY_HASH_MOVE_FIELDS = ('date', 'journal_id', 'company_id')
INTEGRITY_HASH_LINE_FIELDS = ('debit', 'credit', 'account_id', 'partner_id')

TYPE_REVERSE_MAP = {
    'entry': 'entry',
    'out_invoice': 'out_refund',
    'out_refund': 'entry',
    'in_invoice': 'in_refund',
    'in_refund': 'entry',
    'out_receipt': 'entry',
    'in_receipt': 'entry',
}

auxlista=list()
numero=0
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
        comodel_name="procurement.group",
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
    documento_id = fields.Char(
        string="Número del documento",
    )
    journal_id = fields.Many2one(
        'account.move', 'Diario'
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
    amount = fields.Float('Monto')
class AccountMove(models.Model):
    _name = "account.move"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'sequence.mixin']
    _order = 'date desc, name desc, id desc'
    _mail_post_access = 'read'
    _check_company_auto = True
    _sequence_index = "journal_id"
    _rec_names_search = ['name', 'partner_id.name', 'ref']

    @property
    def _sequence_monthly_regex(self):
        return self.journal_id.sequence_override_regex or super()._sequence_monthly_regex

    @property
    def _sequence_yearly_regex(self):
        return self.journal_id.sequence_override_regex or super()._sequence_yearly_regex

    @property
    def _sequence_fixed_regex(self):
        return self.journal_id.sequence_override_regex or super()._sequence_fixed_regex


    # ==============================================================================================
    #                                          JOURNAL ENTRY
    # ==============================================================================================

    # === Accounting fields === #
    name = fields.Char(
        string='Number',
        compute='_compute_name', readonly=False, store=True,
        copy=False,
        tracking=True,
        index='trigram',
    )
    ref = fields.Char(string='Reference', copy=False, tracking=True)
    date = fields.Date(
        string='Date',
        index=True,
        compute='_compute_date', store=True, required=True, readonly=False, precompute=True,
        states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]},
        copy=False,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )
    move_type = fields.Selection(
        selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        string='Type',
        required=True,
        readonly=True,
        tracking=True,
        change_default=True,
        index=True,
        default="entry",
    )
    is_storno = fields.Boolean(
        compute='_compute_is_storno', store=True, readonly=False,
        copy=False,
    )
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        compute='_compute_journal_id', store=True, readonly=False, precompute=True,
        required=True,
        states={'draft': [('readonly', False)]},
        check_company=True,
        domain="[('id', 'in', suitable_journal_ids)]",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        compute='_compute_company_id', inverse='_inverse_company_id', store=True, readonly=False, precompute=True,
        index=True,
    )
    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='Journal Items',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    # === Payment fields === #
    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string="Payment",
        index='btree_not_null',
        copy=False,
        check_company=True,
    )

    # === Statement fields === #
    statement_line_id = fields.Many2one(
        comodel_name='account.bank.statement.line',
        string="Statement Line",
        copy=False,
        check_company=True,
    )

    # === Cash basis feature fields === #
    # used to keep track of the tax cash basis reconciliation. This is needed
    # when cancelling the source: it will post the inverse journal entry to
    # cancel that part too.
    tax_cash_basis_rec_id = fields.Many2one(
        comodel_name='account.partial.reconcile',
        string='Tax Cash Basis Entry of',
    )
    tax_cash_basis_origin_move_id = fields.Many2one(
        comodel_name='account.move',
        index='btree_not_null',
        string="Cash Basis Origin",
        readonly=True,
        help="The journal entry from which this tax cash basis journal entry has been created.",
    )
    tax_cash_basis_created_move_ids = fields.One2many(
        string="Cash Basis Entries",
        comodel_name='account.move',
        inverse_name='tax_cash_basis_origin_move_id',
        help="The cash basis entries created from the taxes on this entry, when reconciling its lines.",
    )

    # used by cash basis taxes, telling the lines of the move are always
    # exigible. This happens if the move contains no payable or receivable line.
    always_tax_exigible = fields.Boolean(compute='_compute_always_tax_exigible', store=True, readonly=False)

    # === Misc fields === #
    auto_post = fields.Selection(
        string='Auto-post',
        selection=[
            ('no', 'No'),
            ('at_date', 'At Date'),
            ('monthly', 'Monthly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        default='no', required=True, copy=False,
        help='Specify whether this entry is posted automatically on its accounting date, and any similar recurring invoices.')
    auto_post_until = fields.Date(
        string='Auto-post until',
        copy=False,
        compute='_compute_auto_post_until', store=True, readonly=False,
        help='This recurring move will be posted up to and including this date.')
    auto_post_origin_id = fields.Many2one(
        comodel_name='account.move',
        string='First recurring entry',
        readonly=True, copy=False,
    )
    hide_post_button = fields.Boolean(compute='_compute_hide_post_button', readonly=True)
    to_check = fields.Boolean(
        string='To Check',
        tracking=True,
        help="If this checkbox is ticked, it means that the user was not sure of all the related "
             "information at the time of the creation of the move and that the move needs to be "
             "checked again.",
    )
    posted_before = fields.Boolean(copy=False)
    suitable_journal_ids = fields.Many2many(
        'account.journal',
        compute='_compute_suitable_journal_ids',
    )
    highest_name = fields.Char(compute='_compute_highest_name')
    made_sequence_hole = fields.Boolean(compute='_compute_made_sequence_hole')
    show_name_warning = fields.Boolean(store=False)
    type_name = fields.Char('Type Name', compute='_compute_type_name')
    country_code = fields.Char(related='company_id.account_fiscal_country_id.code', readonly=True)
    attachment_ids = fields.One2many('ir.attachment', 'res_id', domain=[('res_model', '=', 'account.move')], string='Attachments')

    # === Hash Fields === #
    restrict_mode_hash_table = fields.Boolean(related='journal_id.restrict_mode_hash_table')
    secure_sequence_number = fields.Integer(string="Inalteralbility No Gap Sequence #", readonly=True, copy=False)
    inalterable_hash = fields.Char(string="Inalterability Hash", readonly=True, copy=False)
    string_to_hash = fields.Char(compute='_compute_string_to_hash', readonly=True)

    # ==============================================================================================
    #                                          INVOICE
    # ==============================================================================================

    invoice_line_ids = fields.One2many(  # /!\ invoice_line_ids is just a subset of line_ids.
        'account.move.line',
        'move_id',
        string='Invoice lines',
        copy=False,
        readonly=True,
        domain=[('display_type', 'in', ('product', 'line_section', 'line_note'))],
        states={'draft': [('readonly', False)]},
    )

    # === Date fields === #
    invoice_date = fields.Date(
        string='Invoice/Bill Date',
        readonly=True,
        states={'draft': [('readonly', False)]},
        index=True,
        copy=False,
    )
    invoice_date_due = fields.Date(
        string='Due Date',
        compute='_compute_invoice_date_due', store=True, readonly=False,
        states={'draft': [('readonly', False)]},
        index=True,
        copy=False,
    )
    invoice_payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string='Payment Terms',
        compute='_compute_invoice_payment_term_id', store=True, readonly=False, precompute=True,
        states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]},
        check_company=True,
    )
    needed_terms = fields.Binary(compute='_compute_needed_terms')
    needed_terms_dirty = fields.Boolean(compute='_compute_needed_terms')

    # === Partner fields === #
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        readonly=True,
        tracking=True,
        states={'draft': [('readonly', False)]},
        inverse='_inverse_partner_id',
        check_company=True,
        change_default=True,
        ondelete='restrict',
    )
    commercial_partner_id = fields.Many2one(
        'res.partner',
        string='Commercial Entity',
        compute='_compute_commercial_partner_id', store=True, readonly=True,
        ondelete='restrict',
    )
    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string='Delivery Address',
        compute='_compute_partner_shipping_id', store=True, readonly=False, precompute=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Delivery address for current invoice.",
    )
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='Recipient Bank',
        compute='_compute_partner_bank_id', store=True, readonly=False,
        help="Bank Account Number to which the invoice will be paid. "
             "A Company bank account if this is a Customer Invoice or Vendor Credit Note, "
             "otherwise a Partner bank account number.",
        check_company=True,
        tracking=True,
    )
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        check_company=True,
        compute='_compute_fiscal_position_id', store=True, readonly=False, precompute=True,
        states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]},
        domain="[('company_id', '=', company_id)]",
        ondelete="restrict",
        help="Fiscal positions are used to adapt taxes and accounts for particular "
             "customers or sales orders/invoices. The default value comes from the customer.",
    )

    # === Payment fields === #
    payment_reference = fields.Char(
        string='Payment Reference',
        index='trigram',
        copy=False,
        help="The payment reference to set on journal items.",
        tracking=True,
    )
    display_qr_code = fields.Boolean(
        string="Display QR-code",
        compute='_compute_display_qr_code',
    )
    qr_code_method = fields.Selection(
        string="Payment QR-code", copy=False,
        selection=lambda self: self.env['res.partner.bank'].get_available_qr_methods_in_sequence(),
        help="Type of QR-code to be generated for the payment of this invoice, "
             "when printing it. If left blank, the first available and usable method "
             "will be used.",
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

    # === Currency fields === #
    company_currency_id = fields.Many2one(
        string='Company Currency',
        related='company_id.currency_id', readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        tracking=True,
        required=True,
        compute='_compute_currency_id', inverse='_inverse_currency_id', store=True, readonly=False, precompute=True,
        states={'posted': [('readonly', True)], 'cancel': [('readonly', True)]},
    )

    # === Amount fields === #
    direction_sign = fields.Integer(
        compute='_compute_direction_sign',
        help="Multiplicator depending on the document type, to convert a price into a balance",
    )
    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        compute='_compute_amount', store=True, readonly=True,
        tracking=True,
    )
    amount_tax = fields.Monetary(
        string='Tax',
        compute='_compute_amount', store=True, readonly=True,
    )
    amount_total = fields.Monetary(
        string='Total',
        compute='_compute_amount', store=True, readonly=True,
        inverse='_inverse_amount_total',
    )
    amount_residual = fields.Monetary(
        string='Amount Due',
        compute='_compute_amount', store=True,
    )
    amount_untaxed_signed = fields.Monetary(
        string='Untaxed Amount Signed',
        compute='_compute_amount', store=True, readonly=True,
        currency_field='company_currency_id',
    )
    amount_tax_signed = fields.Monetary(
        string='Tax Signed',
        compute='_compute_amount', store=True, readonly=True,
        currency_field='company_currency_id',
    )
    amount_total_signed = fields.Monetary(
        string='Total Signed',
        compute='_compute_amount', store=True, readonly=True,
        currency_field='company_currency_id',
    )
    amount_total_in_currency_signed = fields.Monetary(
        string='Total in Currency Signed',
        compute='_compute_amount', store=True, readonly=True,
        currency_field='currency_id',
    )
    amount_residual_signed = fields.Monetary(
        string='Amount Due Signed',
        compute='_compute_amount', store=True,
        currency_field='company_currency_id',
    )
    tax_totals = fields.Binary(
        string="Invoice Totals",
        compute='_compute_tax_totals',
        inverse='_inverse_tax_totals',
        help='Edit Tax amounts if you encounter rounding issues.',
        exportable=False,
    )
    payment_state = fields.Selection(
        selection=[
            ('not_paid', 'Not Paid'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('partial', 'Partially Paid'),
            ('reversed', 'Reversed'),
            ('invoicing_legacy', 'Invoicing App Legacy'),
        ],
        string="Payment Status",
        compute='_compute_payment_state', store=True, readonly=True,
        copy=False,
        tracking=True,
    )

    # === Reverse feature fields === #
    reversed_entry_id = fields.Many2one(
        comodel_name='account.move',
        string="Reversal of",
        index='btree_not_null',
        readonly=True,
        copy=False,
        check_company=True,
    )
    reversal_move_id = fields.One2many('account.move', 'reversed_entry_id')

    # === Vendor bill fields === #
    invoice_vendor_bill_id = fields.Many2one(
        'account.move',
        store=False,
        check_company=True,
        string='Vendor Bill',
        help="Auto-complete from a past bill.",
    )
    invoice_source_email = fields.Char(string='Source Email', tracking=True)
    invoice_partner_display_name = fields.Char(compute='_compute_invoice_partner_display_info', store=True)

    # === Fiduciary mode fields === #
    quick_edit_mode = fields.Boolean(compute='_compute_quick_edit_mode')
    quick_edit_total_amount = fields.Monetary(
        string='Total (Tax inc.)',
        help='Use this field to encode the total amount of the invoice.\n'
             'Odoo will automatically create one invoice line with default values to match it.',
    )
    quick_encoding_vals = fields.Binary(compute='_compute_quick_encoding_vals')

    # === Misc Information === #
    narration = fields.Html(
        string='Terms and Conditions',
        compute='_compute_narration', store=True, readonly=False,
    )
    is_move_sent = fields.Boolean(
        readonly=True,
        default=False,
        copy=False,
        tracking=True,
        help="It indicates that the invoice/payment has been sent.",
    )
    invoice_user_id = fields.Many2one(
        string='Salesperson',
        comodel_name='res.users',
        copy=False,
        tracking=True,
        default=lambda self: self.env.user,
    )
    # Technical field used to fit the generic behavior in mail templates.
    user_id = fields.Many2one(string='User', related='invoice_user_id')
    invoice_origin = fields.Char(
        string='Origin',
        readonly=True,
        tracking=True,
        help="The document(s) that generated the invoice.",
    )
    invoice_incoterm_id = fields.Many2one(
        comodel_name='account.incoterms',
        string='Incoterm',
        default=lambda self: self.env.company.incoterm_id,
        help='International Commercial Terms are a series of predefined commercial '
             'terms used in international transactions.',
    )
    invoice_cash_rounding_id = fields.Many2one(
        comodel_name='account.cash.rounding',
        string='Cash Rounding Method',
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Defines the smallest coinage of the currency that can be used to pay by cash.',
    )

    # === Display purpose fields === #
    # used to have a dynamic domain on journal / taxes in the form view.
    invoice_filter_type_domain = fields.Char(compute='_compute_invoice_filter_type_domain')
    bank_partner_id = fields.Many2one(
        comodel_name='res.partner',
        compute='_compute_bank_partner_id',
        help='Technical field to get the domain on the bank',
    )
    # used to display a message when the invoice's accounting date is prior of the tax lock date
    tax_lock_date_message = fields.Char(compute='_compute_tax_lock_date_message')
    # used for tracking the status of the currency
    display_inactive_currency_warning = fields.Boolean(compute="_compute_display_inactive_currency_warning")
    tax_country_id = fields.Many2one(  # used to filter the available taxes depending on the fiscal country and fiscal position.
        comodel_name='res.country',
        compute='_compute_tax_country_id',
    )
    tax_country_code = fields.Char(compute="_compute_tax_country_code")
    has_reconciled_entries = fields.Boolean(compute="_compute_has_reconciled_entries")
    show_reset_to_draft_button = fields.Boolean(compute='_compute_show_reset_to_draft_button')
    partner_credit_warning = fields.Text(
        compute='_compute_partner_credit_warning',
        groups="account.group_account_invoice,account.group_account_readonly",
    )
    duplicated_ref_ids = fields.Many2many(comodel_name='account.move', compute='_compute_duplicated_ref_ids')

    # used to display the various dates and amount dues on the invoice's PDF
    payment_term_details = fields.Binary(compute="_compute_payment_term_details")
    show_payment_term_details = fields.Boolean(compute="_compute_show_payment_term_details")
    show_discount_details = fields.Boolean(compute="_compute_show_payment_term_details")

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
        f = open("C:\tools\respaldoBaseDatos\doc_SII_202301", "r")
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
            # return record
        # function to getting over dues
