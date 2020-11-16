
from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()
ma = Marshmallow()

class Rol(db.Model):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

    def __init__(self, idRol, nombreRol):
        self.idRol = idRol
        self.nombreRol = nombreRol



class Usuarios(db.Model, BaseModelMixin):
    __tablename__ = "USUARIOS"
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String)
    apellidoPatUsuario = db.Column(db.String)
    apellidoMatUsuario = db.Column(db.String)
    idRol = db.Column(db.Integer,db.ForeignKey(Rol.idRol), nullable=False)
    Ruc = db.Column(db.String)
    razonSocial = db.Column(db.String)
    nombreComercial = db.Column(db.String)
    codigoPostalPais = db.Column(db.String)
    telefono = db.Column(db.String)
    celular = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.Text)
    imagen = db.Column(db.String)
    direcciones = db.relationship('Direcciones', backref='Usuarios', lazy=True)



    def __init__(self, nombreUsuario,apellidoPatUsuario,apellidoMatUsuario,idRol,Ruc,razonSocial,nombreComercial,codigoPostalPais,telefono,celular,email,password,imagen):
        self.nombreUsuario = nombreUsuario
        self.apellidoPatUsuario = apellidoPatUsuario
        self.apellidoMatUsuario = apellidoMatUsuario
        self.idRol = idRol
        self.Ruc = Ruc
        self.razonSocial = razonSocial
        self.nombreComercial = nombreComercial
        self.codigoPostalPais = codigoPostalPais
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.password = password
        self.imagen = imagen

    def get_dato(email):
        filtro = db.session.query(Usuarios).filter(Usuarios.email == email)

        return filtro
class Direcciones(db.Model):
    __tablename__="DIRECCIONES"
    idDireccion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    direccion = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    def __init__(self, idUsuario,direccion,latitud,longitud):
        #self.idDireccion=idDireccion
        self.idUsuario =idUsuario
        self.direccion= direccion
        self.latitud = latitud
        self.longitud = longitud


class RolSchema(ma.Schema):
    class Meta:
        fields = ('idRol', 'nombreRol','Usuarios.nombreUsuario','Usuarios.apellidoPatUsuario','Usuarios.apellidoMatUsuario','Usuarios.Ruc','Usuarios.razonSocial','Usuarios.nombreComercial','Usuarios.codigoPostalPais','Usuarios.telefono','Usuarios.celular','Usuarios.email','Usuarios.imagen','Usuarios.idUsuario','Direcciones.idDireccion','Direcciones.latitud','Direcciones.longitud', 'Direcciones.direccion')

rolSchema = RolSchema()