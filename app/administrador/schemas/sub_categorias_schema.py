from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('idSubCategorias','nombreSubCategorias','idCategoria','nombreCategoria','fechaCreacion')