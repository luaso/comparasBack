from marshmallow import fields
from app.ext import ma


class ProductosBuscarListarSchema(ma.Schema):
    idProducto = fields.Integer(dump_only=True, required=True, error_messages={"required": "idProducto es obligatorio", "code": 400})
    idCategoria = fields.Integer(required=False, error_messages={"no required": "idcategoria no obligatorio", "code": 400})
    nombreProducto = fields.String(required=False, error_messages={"no required": "nombreProducto no obligatorio", "code": 400})
    contenidoProducto = fields.String(required=False, error_messages={"no required": "contenido no obligatorio", "code": 400})
    Imagen = fields.String(required=False, error_messages={"no required": "Imagen no obligatorio", "code": 400})

