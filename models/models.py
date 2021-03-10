# -*- coding: utf-8 -*-
from odoo import models, fields, api


class libreria_categoria(models.Model):
    _name = "libreria.categoria"

    name = fields.Char(string="Nombre", required=True, help="Introduce el nombre de la categoria")
    description = fields.Text(string="Descripción")
    # Debemos informar con que campo se relaciona, tiene que ser el que tiene el Many2one
    libros = fields.One2many("libreria.libro", "categoria", string="Libros")


class libreria_libro(models.Model):
    _name = "libreria.libro"

    name = fields.Char(string="Titulo", required=True)
    precio = fields.Float(string="Precio")
    ejemplares = fields.Integer(string="Ejemplares")
    fecha = fields.Date(string="Fecha de compra")
    segunMano = fields.Boolean(string="Segunda mano")
    estado = fields.Selection([
        ('0', 'Bueno'),('1', 'Regular'),('2', 'Malo')
    ], string="Estado", default="0")
    # 1° parametro es el obj al cual se relaciona
    # Con ondalete informamos que al borrar una categoria se borren todos los libros relacionados
    categoria = fields.Many2one("libreria.categoria", string="Categoría", required=True, ondalete="cascade")

    # Creamos un campo calculado, con compute indicamos cual sera la funci{on que relecé el calculo
    # Con store indicamos cuando se realizara el calculo, en este caso cuando cambien los valores
    importeTotal = fields.Float(string="Importe total", compute="_importeTotal", store=True)

    # Informamos cuando el método debe ser llamado
    @api.depends('precio', 'ejemplares')
    def _importeTotal(self):
        # Se crea un bucle por las dudas que la función se llame con varios registros
        for r in self:
            r.importeTotal = r.ejemplares * r.precio