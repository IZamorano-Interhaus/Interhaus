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
            select  b.tipodte codigo_documento,
                    b.tipodtestring tipo_documento,
                    b.rutCliente rut_tributario, 
                    b.folio folio_documento,
                    b.fechaemision date_start,
                    b.fecharecepcion fecha_factura,
                    b.razonsocial razon_social,
                    b.acuserecibo acuseRecibo,
                    ROUND(SUM(b.montoNeto), currency.decimal_places) montoNeto,
                    ROUND(SUM(b.montoivarecuperable), currency.decimal_places) Impuesto
                    b.montototal total,
                    b.trackid
              FROM borradores b
              JOIN account_move move ON move.id = b.id
              JOIN res_company company ON company.id = move.company_id
              JOIN res_currency currency ON currency.id = company.currency_id
             WHERE b.move_id IN %s
          GROUP BY b.move_id, currency.decimal_places
            HAVING ROUND(SUM(b.balance), currency.decimal_places) != 0
        ''', [tuple(contenedor.ids)])

        return self._cr.fetchall()

            # return record
        # function to getting over dues
