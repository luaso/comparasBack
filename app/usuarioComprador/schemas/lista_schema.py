from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('direccion',
                  'direccionOpcional1',
                  'direccionOpcional2',
                  'Subastas.idSubasta',
                  'Subastas.idUsuario',
                  'Subastas.idEstado',
                  'Subastas.tiempoInicial',
                  'Subastas.nombreSubasta',
                  'Subastas.precioIdeal',
                  'Subastas.fechaSubasta',
                  'Subastas_Productos.idSubasta',
                  'Subastas_Productos.idProducto',
                  'Subastas_Productos.Cantidad',
                  'Productos.nombreProducto',
                  'idProducto',
                  'idCategoria',
                  'Imagen',
                  'unidadMedida',
                  'nombreProducto',
                  'contenidoProducto')

class ProductoSchema(ma.Schema):
    idProducto = fields.Integer(dump_only=True, required=True, error_messages={"required": "idCategoria es obligatorio", "code": 400})
    idTipoProducto = fields.Integer(dump_only=True, required=True, error_messages={"required": "idCategoria es obligatorio", "code": 400})
    nombreProducto = fields.String(dump_only=True, required=True, error_messages={"required": "idCategoria es obligatorio", "code": 400})
    contenidoProducto = fields.String()
    Imagen = fields.String()
    codProducto = fields.String()
    marca = fields.String()
    presentacion = fields.String()
    unidadMedida = fields.String()
    cantidadPaquete = fields.Integer()

class SubastasSchema(ma.Schema):
    idSubasta = fields.Integer(dump_only=True, required=True, error_messages={"required": "idCategoria es obligatorio", "code": 400})
    idUsuario = fields.Integer()
    tiempoInicial = fields.Date()
    nombreSubasta = fields.String()
    precioIdeal = fields.Float()
    idDireccion = fields.Integer()
    fechaSubasta = fields.Date()
