from marshmallow import fields
from app.ext import ma


class CategoriasSchema(ma.Schema):
    idCategoria = fields.Integer(dump_only=True, required=True, error_messages={"required": {"message": "idCategoria required", "code": 400}})
    nombreCategoria = fields.String(required=True, error_messages={"required": {"message": "nombreCategoria required", "code": 400}})