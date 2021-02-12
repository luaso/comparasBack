from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = (  'idProductoSupermercado',
                    'idSupermercado',
                    'idProducto',
                    'fechaProducto',
                    'precioRegular',
                    'precioOnline',
                    'precioTarjeta',
                    'nombreTarjeta',
                    'idSupermercado',
                    'nombreSupermercado',
                    'imagenSupermercado',
                    'urlSupermercado',
                    'productos_supermercado',
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
                    'productos_supermercado',
                    'Productos_Supermercados.idProductoSupermercado',
                    'Productos_Supermercados.idSupermercado',
                    'Productos_Supermercados.idProducto',
                    'Productos_Supermercados.fechaProducto',
                    'Productos_Supermercados.precioRegular',
                    'Productos_Supermercados.precioOnline',
                    'Productos_Supermercados.precioTarjeta',
                    'Productos_Supermercados.nombreTarjeta',
                    'Productos.nombreProducto',
                    'Supermercados.nombreSupermercado')



class TaskSchema2(ma.Schema):
    class Meta:
        fields = (  'idProductoSupermercado',
                    'idSupermercado',
                    'idProducto',
                    'fechaProducto',
                    'precioRegular',
                    'precioOnline',
                    'precioTarjeta',
                    'nombreTarjeta')