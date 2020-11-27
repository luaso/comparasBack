from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Subastas.idSubasta',
                  'Subastas.fechaSubasta',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Estado.nombreEstado')
