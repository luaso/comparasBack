from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Pujas.idPuja',
                  'Pujas.fechaPuja',
                  'Pujas.precioPuja',
                  'Pujas.idSubasta',
                  'idPuja',
                  'precioPuja')

class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('Productos.idProducto',
                  'Productos.nombreProducto',
                  'Productos.idProducto',
                  'Pujas.idSubasta',
                  'idPuja',
                  'precioPuja')

class TaskSchema3(ma.Schema):
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
                  'Productos_Supermercados.precioOnline')