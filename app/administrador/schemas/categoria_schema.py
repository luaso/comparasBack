from marshmallow import fields
from app.ext import ma


class CategoriasSchema(ma.Schema):
    idCategoria = fields.Integer(dump_only=True, required=True, error_messages={"required": "idCategoria es obligatorio", "code": 400})
    nombreCategoria = fields.String(required=True, error_messages={"required": "nombreCategoria es obligatorio", "code": 400})
    fechaCreacion = fields.DateTime()