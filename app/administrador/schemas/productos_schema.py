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
                  'idTipoProducto',
                  'nombreProducto',
                  'contenidoProducto',
                  'Imagen',
                  'codProducto',
                  'marca',
                  'presentacion',
                  'unidadMedida',
                  'cantidadPaquete',
                  'Valor')


class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('idTipoProducto',
                  'nombreProducto')