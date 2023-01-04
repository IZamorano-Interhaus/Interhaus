# -*- coding: utf-8 -*-
# from odoo import http


# class Cambio-ventas(http.Controller):
#     @http.route('/cambio-ventas/cambio-ventas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cambio-ventas/cambio-ventas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cambio-ventas.listing', {
#             'root': '/cambio-ventas/cambio-ventas',
#             'objects': http.request.env['cambio-ventas.cambio-ventas'].search([]),
#         })

#     @http.route('/cambio-ventas/cambio-ventas/objects/<model("cambio-ventas.cambio-ventas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cambio-ventas.object', {
#             'object': obj
#         })
