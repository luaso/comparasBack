from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('idTipoProducto','nombreProducto','idSubCategorias','nombreSubCategorias')