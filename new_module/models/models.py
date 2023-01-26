# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class new_module(models.Model):
    _name = 'new_module.new_module'
    _description = 'new_module.new_module'
    name = fields.Char()
    value = fields.Integer()
    descuento = fields.Float(compute="_value_pc", store=True)
    
    """ analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')
    crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'analytic_account_id', 'Budget Lines')
    crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'crossovered_budget_id', 'Budget Lines',
        states={'done': [('readonly', True)]}, copy=True) """



    rut = fields.Char()
    folio = fields.Char()
    """ documento = fields.One2many('new_module',inverse_name='new_module.new_module')
    crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'analytic_account_id', 'Budget Lines')  
    tipo_documento = fields.One2many('new_module',inverse_name='new_module.new_module') """
   
    documento=fields.Char()
    tipo_documento=fields.Integer()
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10


""" class AccountMove(models.Model):
    _inherit = 'account.move'

    edi_document_ids = fields.One2many(
        comodel_name='account.edi.document',
        inverse_name='move_id')
    edi_state = fields.Selection(
        selection=[('to_send', 'To Send'), ('sent', 'Sent'), ('to_cancel', 'To Cancel'), ('cancelled', 'Cancelled')],
        string="Electronic invoicing",
        store=True,
        compute='_compute_edi_state',
        help='The aggregated state of all the EDIs with web-service of this move')
    edi_error_count = fields.Integer(
        compute='_compute_edi_error_count',
        help='How many EDIs are in error for this move ?')
    edi_blocking_level = fields.Selection(
        selection=[('info', 'Info'), ('warning', 'Warning'), ('error', 'Error')],
        compute='_compute_edi_error_message')
    edi_error_message = fields.Html(
        compute='_compute_edi_error_message')
    # Technical field to display the documents that will be processed by the CRON
    edi_web_services_to_process = fields.Text(
        compute='_compute_edi_web_services_to_process')
    edi_show_cancel_button = fields.Boolean(
        compute='_compute_edi_show_cancel_button')
    edi_show_abandon_cancel_button = fields.Boolean(
        compute='_compute_edi_show_abandon_cancel_button') """
        
    
    
