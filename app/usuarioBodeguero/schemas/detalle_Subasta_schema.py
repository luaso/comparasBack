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