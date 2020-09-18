from marshmallow import fields
from app.ext import ma


class SupermercadosSchema(ma.Schema):
    idSupermercado = fields.Integer(dump_only=True, required=True, error_messages={"required": "idSupermercado es obligatorio", "code": 400})
    nombreSupermercado = fields.String(required=True, error_messages={"required": "nombreSupermercado es obligatorio", "code": 400})
    imagenSupermercado = fields.String(required=True, error_messages={"required": "imagenSupermercado es obligatorio", "code": 400})
    urlSupermercado = fields.String(required=True, error_messages={"required": "urlSupermercado es obligatorio", "code": 400})