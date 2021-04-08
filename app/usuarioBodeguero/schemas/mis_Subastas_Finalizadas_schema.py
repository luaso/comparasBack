from marshmallow import fields
from app.ext import ma

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('Subastas.idSubasta',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Usuarios.apellidoMatUsuario',
                  'Usuarios.telefono',
                  'Usuarios.celular',
                  'Usuarios.email',
                  'Direcciones.direccion',
                  "Subastas.direccionFinal")
