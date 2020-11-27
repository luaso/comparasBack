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
                  'nombreProducto',
                  'contenidoProducto',
                  'Pujas.idPuja',
                  'Pujas.precioPuja',
                  'Pujas.fechaPuja',
                  'Subastas_Productos.cantidad',
                  'Productos.nombreProducto',
                  'Productos.marca',
                  'Productos.unidadMedida',
                  'Productos.cantidadPaquete')
