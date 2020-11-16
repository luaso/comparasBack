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
                    'productos_supermercado')