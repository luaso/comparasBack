from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import func, and_
from config.configuration import AdditionalConfig

db = SQLAlchemy()
ma = Marshmallow()

class Usuarios(db.Model, BaseModelMixin):
    __tablename__ = "USUARIOS"
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String)
    idRol = db.Column(db.Integer)
    Ruc = db.Column(db.String)
    razonSocial = db.Column(db.String)
    nombreComercial = db.Column(db.String)
    apellidoPatUsuario = db.Column(db.String)
    codigoPostalPais = db.Column(db.String)
    telefono = db.Column(db.String)
    celular = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)

class Estado(db.Model):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    codEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)

class Subastas(db.Model, BaseModelMixin):
    __tablename__= "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    idDireccion = db.Column(db.Integer)
    fechaSubasta = db.Column(db.Date)
    idUsuarioGanador = db.Column(db.Integer)
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)

    @classmethod
    def get_compras(cls, idUsuario):

        filtro = db.session.query(Subastas, Usuarios). \
            join(Estado, Estado.idEstado == Subastas.idEstado). \
            join(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
            filter(Subastas.idUsuario == idUsuario). \
            filter(Estado.codEstado == AdditionalConfig.ESTADO4).\
            filter(Subastas.idUsuarioGanador.isnot(None)).all()

        print(filtro)


        arr = []
        for data in filtro:
            dicc = {}
            idSubasta = data[0].idSubasta
            idUsuarioGanador = data[0].idUsuarioGanador
            fechaSubasta = data[0].fechaSubasta
            print(idSubasta)
            print(data[0].idUsuarioGanador)
            filtro2 = db.session.query(func.min(Pujas.precioPuja).label("miMinOferta"), Usuarios.nombreUsuario, Usuarios.apellidoPatUsuario). \
                join(Subastas, Subastas.idUsuarioGanador == Pujas.idUsuario). \
                join(Usuarios, Usuarios.idUsuario == Subastas.idUsuarioGanador). \
                filter(Pujas.idSubasta == idSubasta).\
                filter(Pujas.idUsuario == idUsuarioGanador).group_by(Pujas.idUsuario, Usuarios.idUsuario).all()

            precioGanador = filtro2[0][0]
            nombreGanador = filtro2[0][1]
            apellidoPatGanador = filtro2[0][2]
            dicc = {
                "Usuarios.nombreUsuario": nombreGanador,
                "Usuarios.apellidoPatUsuario": apellidoPatGanador,
                "Pujas.precioPuja": precioGanador,
                "Pujas.idSubasta": idSubasta,
                "Subastas.idSubasta": idSubasta,
                "Pujas.fechaPuja": fechaSubasta,
                "Subastas.fechaSubasta": fechaSubasta
            }

            arr.append(dicc)
            print(arr)
        print("fin")
        return arr

    def get_compraSeleccionada(idSubasta):
        filtro = db.session.query(Pujas, Usuarios). \
                join(Usuarios, Pujas.idUsuario == Usuarios.idUsuario). \
                filter(Pujas.idSubasta == idSubasta)
        return filtro

    def get_productosSubasta(idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos). \
                join(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
                filter(Subastas_Productos.idSubasta == idSubasta)
        return filtro

    def get_bodegueroGanador(idSubasta):
        filtro = db.session.query(Subastas, Usuarios, Pujas). \
                join(Usuarios, Subastas.idUsuarioGanador == Usuarios.idUsuario). \
                join(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
                filter(Subastas.idSubasta == idSubasta). \
                filter(Subastas.idUsuarioGanador == Pujas.idUsuario)

        return filtro


class Pujas(db.Model, BaseModelMixin):
    __tablename__ = "PUJAS"
    idPuja = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer, db.ForeignKey(Subastas.idSubasta), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    precioPuja = db.Column(db.Float)
    fechaPuja = db.Column(db.DateTime)

class Productos(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS"
    idProducto = db.Column(db.Integer, primary_key=True)
    idTipoProducto = db.Column(db.Integer, nullable=False)
    nombreProducto = db.Column(db.String)
    contenidoProducto = db.Column(db.String)
    Imagen = db.Column(db.String)
    codProducto = db.Column(db.String)
    marca = db.Column(db.String)
    presentacion = db.Column(db.String)
    unidadMedida = db.Column(db.String)
    cantidadPaquete = db.Column(db.Integer)
    subastas_productos = db.relationship('Subastas_Productos', backref='Productos', lazy=True)

class Subastas_Productos(db.Model):
    __tablename__= "SUBASTAS_PRODUCTOS"
    idSubastasProductos = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    Cantidad = db.Column(db.Float)