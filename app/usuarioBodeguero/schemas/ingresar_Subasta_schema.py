from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Subastas.idSubasta',
                  'Subastas.nombreSubasta',
                  'Subastas.idUsuarioGanador',
                  'Usuarios.idUsuario',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Usuarios.apellidoMatUsuario',
                  'Subastas.fechaSubasta',
                  'Estado.nombreEstado',
                  'Estado.idEstado',
                  'Direcciones.idDireccion',
                  'Direcciones.latitud',
                  'Direcciones.longitud',)