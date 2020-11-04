from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('idSubastasProductos',
                  'idSubasta',
                  'idProducto',
                  'Cantidad',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'contenidoProducto',
                  'Subastas_Productos.idSubasta',
                  'Productos.idProducto',
                  'Productos.nombreProducto',
                  'Subastas_Productos.Cantidad',
                  'Productos_Supermercados.idSupermercado',
                  'Supermercados.nombreSupermercado',
                  'Productos_Supermercados.precioRegular',
                  'Productos_Supermercados.precioOnline',
                  'Productos_Supermercados.precioTarjeta',
                  'Productos_Supermercados.nombreTarjeta',
                  'anon_1')