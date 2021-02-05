from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Subastas.idSubasta',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Usuarios.apellidoMatUsuario',
                  'Subastas.fechaSubasta',
                  'Pujas.precioPuja',
                  'Estado.nombreEstado')
