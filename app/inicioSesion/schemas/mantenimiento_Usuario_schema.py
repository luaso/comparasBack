from marshmallow import fields
from app.ext import ma

class RolSchemaToken(ma.Schema):
    class Meta:
        fields = ('Rol.idRol',
                  'Rol.nombreRol',
                  'Usuarios.email',
                  'Usuarios.idUsuario')

class UserSchemaToken(ma.Schema):
    class Meta:
        fields = ('Usuarios.nombreUsuario',
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
                  'Usuarios.idUsuario',)

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
                  'Direcciones.referencia',
                  'idRol',
                  'nombreRol')
