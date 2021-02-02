from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from config.configuration import AdditionalConfig
import math
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from geopy.distance import geodesic
db = SQLAlchemy()

class Estado(db.Model):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    codEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)


class Rol(db.Model):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

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
    password = db.Column(db.String)
    imagen = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)



class Direcciones(db.Model):
    __tablename__ = "DIRECCIONES"
    idDireccion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    direccion = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Direcciones', lazy=True)

    @classmethod
    def get(self, idUsuario):
        filtro = db.session.query(Direcciones).filter(Direcciones.idUsuario == idUsuario)
        return filtro


class Categorias(db.Model):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    productos = db.relationship('Productos', backref='Categorias', lazy=True)


class Productos(db.Model):
    __tablename__ = "PRODUCTOS"
    idProducto = db.Column(db.Integer, primary_key=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    nombreProducto = db.Column(db.String)
    contenidoProducto = db.Column(db.String)
    subastas_productos = db.relationship('Subastas_Productos', backref='Productos', lazy=True)

class Subastas(db.Model):
    __tablename__= "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    idDireccion = db.Column(db.Integer, db.ForeignKey(Direcciones.idDireccion), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    fechaSubasta = db.Column(db.String)

    @classmethod
    def get_join_filter(self):
        filtro = db.session.query(Subastas, Usuarios, Estado). \
                 outerjoin(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
                 outerjoin(Estado, Subastas.idEstado == Estado.idEstado). \
                 filter(Estado.idEstado.in_((1, 2)))
        return filtro

    @classmethod
    def get_subastas(self):

        filtro =  db.session.query(Subastas, Direcciones, Estado, Usuarios). \
                  join(Direcciones, Subastas.idDireccion == Direcciones.idDireccion). \
                  join(Estado, Estado.idEstado == Subastas.idEstado). \
                  join(Usuarios,Subastas.idUsuario == Usuarios.idUsuario). \
                  filter(Estado.codEstado == "Cod2").all()
        return filtro

    @classmethod
    def get_direccion_usuario_2km(self, idUsuario, direcciones):
        i = 0
        codRadio = AdditionalConfig.RADIOBUSQUEDASUBASTA
        parametroRadio = db.session.query(Parametros).filter(Parametros.idParametros == codRadio).first()
        radioInt = int(parametroRadio.Valor)
        print(type(radioInt))

        direccionesMenores = []
        latlongBodeguero = db.session.query(Direcciones).filter(Direcciones.idUsuario == idUsuario)
        for data in latlongBodeguero:
            coordenada = ((data.latitud, data.longitud))
            print("coordenada")
            print(coordenada)

        for direccion in direcciones:

            coordenadadaBus = ((direccion["Direcciones.latitud"],direccion["Direcciones.longitud"]))
            print("coordenada")
            print(coordenada)
            print("coordenada busqueda")
            print(coordenadadaBus)
            dist = geodesic(coordenada,coordenadadaBus).km
            print("distancia")
            print(dist)
            if dist <= radioInt:

                print("entro al  if")
                direccionesMenores.append(direccion)

        return direccionesMenores

    def __init__(self, idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, fechaSubasta):
        self.idUsuario = idUsuario
        self.idEstado = idEstado
        self.tiempoInicial = tiempoInicial
        self.nombreSubasta = nombreSubasta
        self.precioIdeal = precioIdeal
        self.fechaSubasta = fechaSubasta


class Subastas_Productos(db.Model):
    __tablename__= "SUBASTAS_PRODUCTOS"
    idSubastasProductos = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    Cantidad = db.Column(db.Float)

    def __init__(self,idSubasta, idProducto, Cantidad):

        self.idSubasta = idSubasta
        self.idProducto = idProducto
        self.Cantidad = Cantidad


class Parametros(db.Model):
    __tablename__= "PARAMETROS"
    idParametros = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.Text)
    Estado = db.Column(db.Integer)
    FecCrea = db.Column(db.Date)
    FecModifica = db.Column(db.Date)
    UsuCrea = db.Column(db.Integer)
    UsuModifica = db.Column(db.Integer)
    Valor = db.Column(db.String)

    def __init__(self,idParametros, Descripcion, Estado, FecCrea, FecModifica, UsuCrea, UsuModifica, Valor):

        self.idParametros = idParametros
        self.Descripcion = Descripcion
        self.Estado = Estado
        self.FecCrea = FecCrea
        self.FecModifica = FecModifica
        self.UsuCrea = UsuCrea
        self.UsuModifica = UsuModifica
        self.Valor = Valor


#Listar subastas de Usuario que podria escoger el bodeguero
#@app.route('/api/listasUsuario/', methods=['GET'])
#def get_subastas():
#    idUsuario = request.json['idUsuario']
#    filtro = db.session.query(Subastas, Usuarios, Estado). \
#             outerjoin(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
#             outerjoin(Estado, Subastas.idEstado == Estado.idEstado). \
#             filter(Estado.idEstado.in_((1,2)))





