from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Productos.idProducto',
                  'Productos.nombreProducto',
                  'Productos.codProducto',
                  'Productos_Supermercados.precioRegular',
                  'Categorias.nombreCategoria',
                  'Supermercados.nombreSupermercado',
                  'nombreProducto',
                  'idProducto',
                  'Productos.idTipoProducto',
                  'nombreProducto',
                  'contenidoProducto',
                  'Productos.Imagen',
                  'codProducto',
                  'Productos.marca',
                  'Productos.presentacion',
                  'Productos.unidadMedida',
                  'Productos.cantidadPaquete',
                  'Valor')


class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('idTipoProducto',
                  'nombreProducto')