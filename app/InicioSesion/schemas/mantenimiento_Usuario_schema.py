from marshmallow import fields
from app.ext import ma

class RolSchema(ma.Schema):
    class Meta:
        fields = ('Rol.idRol',
                  'Rol.nombreRol',
                  'Usuarios.nombreUsuario',
                  'Usuarios.apellidoPatUsuario',
                  'Usuarios.apellidoMatUsuario',
                  'Usuarios.Ruc',
                  'Usuarios.razonSocial',
                  'Usuarios.nombreComercial',
                  'Usuarios.codigoPostalPais',
                  'Usuarios.telefono',
                  'Usuarios.celular',
                  'Usuarios.email',
                  'Usuarios.imagen',
                  'Usuarios.idUsuario',
                  'Direcciones.idDireccion',
                  'Direcciones.latitud',
                  'Direcciones.longitud',
                  'Direcciones.direccion',
                  'idRol',
                  'nombreRol')
