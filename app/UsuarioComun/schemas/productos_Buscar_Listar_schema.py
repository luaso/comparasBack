from marshmallow import fields
from app.ext import ma


class ProductosBuscarListarSchema(ma.Schema):
    idProducto = fields.Integer(dump_only=True, required=True, error_messages={"required": "idProducto es obligatorio", "code": 400})
    idCategoria = fields.Integer(required=False, error_messages={"no required": "idcategoria es obligatorio", "code": 400})
    nombreProducto = fields.String(required=False, error_messages={"no required": "nombreProducto es obligatorio", "code": 400})
    contenidoProducto = fields.String(required=False, error_messages={"no required": "contenido es obligatorio", "code": 400})

