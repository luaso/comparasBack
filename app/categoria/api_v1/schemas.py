from marshmallow import fields
from app.ext import ma


class CategoriasSchema(ma.Schema):
    idCategoria = fields.Integer(dump_only=True)
    nombreCategoria = fields.String()