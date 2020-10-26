from marshmallow import fields
from app.ext import ma


class ProductosBuscarListarSchema(ma.Schema):
    idProducto = fields.Integer(dump_only=True, required=True, error_messages={"required": "idProducto es obligatorio", "code": 400})
    idTipoProducto = fields.Integer(required=False, error_messages={"no required": "idTipoProducto no obligatorio", "code": 400})
    nombreProducto = fields.String(required=False, error_messages={"no required": "nombreProducto no obligatorio", "code": 400})
    contenidoProducto = fields.String(required=False, error_messages={"no required": "contenido no obligatorio", "code": 400})
    codProducto = fields.String(required=False, error_messages={"no required": "codProducto no obligatorio", "code": 400})
    Imagen = fields.String(required=False, error_messages={"no required": "Imagen no obligatorio", "code": 400})
    marca = fields.String(required=False, error_messages={"no required": "marca no obligatorio", "code": 400})
    presentacion = fields.String(required=False, error_messages={"no required": "presentacion no obligatorio", "code": 400})
    unidadMedida = fields.String(required=False, error_messages={"no required": "unidadMedida no obligatorio", "code": 400})
    cantidadPaquete = fields.String(required=False, error_messages={"no required": "cantidadPaquete no obligatorio", "code": 400})



