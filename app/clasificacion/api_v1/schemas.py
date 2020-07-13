from marshmallow import fields
from app.ext import ma


class ClasificacionSchema(ma.Schema):
    idclasificacion = fields.Integer(dump_only=True)
    nombreclasificacion = fields.String()