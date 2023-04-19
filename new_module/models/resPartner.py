from odoo import fields,models,api,_
from datetime import  date

class res_partner(models.Model):
    _name="res.partner"
    _inherit="res.partner"

    property_payment_method_id = fields.Many2one(
        comodel_name='account.payment.method',
        string='Payment Method',
        company_dependent=True,
        domain="[('payment_type', '=', 'outbound')]",
        help="Preferred payment method when paying this vendor. This is used to filter vendor bills"
             " by preferred payment method to register payments in mass. Use cases: create bank"
             " files for batch wires, check runs.",
    )
class factura(models.Model):
    _inherit="account.move"

    name = fields.Char(
        string='Numero o nombre, no se que es',
        compute='_compute_name', readonly=False, store=True,
        copy=False,
        tracking=True,
        index='trigram',
    )
    ref = fields.Char(string='Referencia', copy=False, tracking=True)
    date = fields.Date(
        string='Fecha de emision',
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
        string='Estado',
        required=True,
        readonly=True,
        copy=False,
        tracking=True,
        default='draft',
    )
    move_type = fields.Selection(
        selection=[
            ('entry', 'Entrada Registro'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Credit Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        string='Tipazo',
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
        string='Diario contable',
        compute='_compute_journal_id', store=True, readonly=False, precompute=True,
        required=True,
        states={'draft': [('readonly', False)]},
        check_company=True,
        domain="[('id', 'in', suitable_journal_ids)]",
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Compañia',
        compute='_compute_company_id', inverse='_inverse_company_id', store=True, readonly=False, precompute=True,
        index=True,
    )
    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='Items de diarios',
        copy=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    # === Payment fields === #
    payment_id = fields.Many2one(
        comodel_name='account.payment',
        string="Pago genialo",
        index='btree_not_null',
        copy=False,
        check_company=True,
    )

    # === Statement fields === #
    statement_line_id = fields.Many2one(
        comodel_name='account.bank.statement.line',
        string="Linea de tu testamento",
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
        string='Auto-posteo',
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
        string='fecha de la factura emitida como dios manda',
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
        string='Proveedor genialo',
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
        string='direccion de entrega',
        compute='_compute_partner_shipping_id', store=True, readonly=False, precompute=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Delivery address for current invoice.",
    )
    partner_bank_id = fields.Many2one(
        'res.partner.bank',
        string='lugar del banco',
        compute='_compute_partner_bank_id', store=True, readonly=False,
        help="Bank Account Number to which the invoice will be paid. "
             "A Company bank account if this is a Customer Invoice or Vendor Credit Note, "
             "otherwise a Partner bank account number.",
        check_company=True,
        tracking=True,
    )
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Posicion Fiscal UVE',
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

    def _auto_init(self):
        super()._auto_init()
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS account_move_to_check_idx
            ON account_move(journal_id) WHERE to_check = true;
            CREATE INDEX IF NOT EXISTS account_move_payment_idx
            ON account_move(journal_id, state, payment_state, move_type, date);
        """)