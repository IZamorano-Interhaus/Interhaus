from odoo import models,fields
class TestModel(models.Model):
    _name="test.model"
    _description="una pequeña descripcion"

    name= fields.Char()