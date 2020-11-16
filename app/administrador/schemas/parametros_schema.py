from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = (  'idParametros',
                    'Descripcion',
                    'Estado',
                    'FecCrea',
                    'FecModifica',
                    'UsuCrea',
                    'UsuModifica',
                    'Valor')