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
                  'Productos.idTipoProducto',
                  'Productos.Imagen',
                  'Productos.marca',
                  'Productos.presentacion',
                  'Productos.unidadMedida',
                  'Productos.cantidadPaquete',
                  'idProducto',
                  'nombreProducto',
                  'contenidoProducto',
                  'idTipoProducto',
                  'Imagen',
                  'marca',
                  'unidadMedida',
                  'presentacion',
                  'cantidadPaquete',
                  'codProducto',
                  'Valor')


class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('idTipoProducto',
                  'nombreProducto')