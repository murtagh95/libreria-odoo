# -*- coding: utf-8 -*-
from odoo import models, fields, api


class libreria_categoria(models.Model):
    _name = "libreria.categoria"

    name = fields.Char(string="Nombre", required=True, help="Introduce el nombre de la categoria")
    description = fields.Text(string="Descripción")
    # Debemos informar con que campo se relaciona, tiene que ser el que tiene el Many2one
    libros = fields.One2many("libreria.libro", "categoria", string="Libros")
    disponible = fields.Boolean(string="Disponible", required=True, help="Indicar si esta categoría esta disponible para su uso")


class libreria_libro(models.Model):
    _name = "libreria.libro"

    name = fields.Char(string="Titulo", required=True)
    imagen = fields.Binary(help="Imagen del libro")
    precio = fields.Float(string="Precio")
    ejemplares = fields.Integer(string="Ejemplares")
    fecha = fields.Date(string="Fecha de compra")
    segunMano = fields.Boolean(string="Segunda mano")
    estado = fields.Selection([
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('Malo', 'Malo')
    ], string="Estado", default="Bueno")
    descripcion = fields.Html(string="Descripción", help="Descripción del libro")
    puntuacion = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    ], string="Puntuación", help="Eligue una puntuación del 0 al 5 para definir que tan bueno es el libro")
    country_id = fields.Many2one("res.country", string="País", required=True)

    
    # 1° parametro es el obj al cual se relaciona
    # Con ondalete informamos que al borrar una categoria se borren todos los libros relacionados
    categoria = fields.Many2one("libreria.categoria", string="Categoría", required=True, ondalete="cascade")

    # Creamos un campo calculado, con compute indicamos cual sera la funci{on que relecé el calculo
    # Con store indicamos cuando se realizara el calculo, en este caso cuando cambien los valores
    importeTotal = fields.Float(string="Importe total", compute="_importeTotal", store=True)

    # Informamos cuando el método debe ser llamado,
    # en este caso cuando hay un cambio en precio o ejemplares
    @api.depends('precio', 'ejemplares')
    def _importeTotal(self):
        # Se crea un bucle por las dudas que la función se llame con varios registros
        for r in self:
            r.importeTotal = r.ejemplares * r.precio