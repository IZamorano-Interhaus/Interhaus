# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    
   
    @api.depends('value')

    
    def _value_pc(self):
        for record in self:
            record.descuento = float(record.value) * 0.10
        
    documento = fields.One2many('new_module','new_module.list','new_module.new_module')
    """ crossovered_budget_line = fields.One2many('crossovered.budget.lines', 'analytic_account_id', 'Budget Lines')  """
    tipo_documento = fields.One2many('new_module','new_module.list','new_module.new_module')
    
