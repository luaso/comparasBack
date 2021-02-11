from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('idSubCategorias',
                  'nombreSubCategorias',
                  'idCategoria',
                  'nombreCategoria',
                  'fechaCreacion')

class TaskSchema2(ma.Schema):
    class Meta:
        fields = ('Sub_Categorias.idSubCategorias',
                  'Sub_Categorias.nombreSubCategorias',
                  'Sub_Categorias.idCategoria',
                  'Categorias.nombreCategoria',
                  'Categorias.fechaCreacion')