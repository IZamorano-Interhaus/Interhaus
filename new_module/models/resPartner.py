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