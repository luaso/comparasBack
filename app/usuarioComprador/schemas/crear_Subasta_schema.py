from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('idDireccion',
                  'direccion',
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
                  'Productos.marca',
                  'Productos.cantidadPaquete',
                  'Productos.unidadMedida',
                  'Productos.presentacion',
                  'Productos.Imagen',
                  'marca',
                  'cantidadPaquete',
                  'unidadMedida',
                  'presentacion',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'Imagen',
                  'contenidoProducto')