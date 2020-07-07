from marshmallow import fields
from app.ext import ma


class ClasificacionSchema(ma.Schema):
    idClasificacion = fields.Integer(dump_only=True)
    nombreClasificacion = fields.String()