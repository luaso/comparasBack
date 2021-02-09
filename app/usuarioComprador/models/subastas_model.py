from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import or_

from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()
ma = Marshmallow()


class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)

class Sub_Categorias(db.Model, BaseModelMixin):
    __tablename__= "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategoria = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)

class Tipos_Productos(db.Model, BaseModelMixin):
    __tablename__= "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)
    productos = db.relationship('Productos', backref='Tipos_Productos', lazy=True)


class Productos(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS"
    idProducto = db.Column(db.Integer, primary_key=True)
    idTipoProducto = db.Column(db.Integer, db.ForeignKey(Tipos_Productos.idTipoProducto), nullable=False)
    nombreProducto = db.Column(db.String)
    contenidoProducto = db.Column(db.String)
    Imagen = db.Column(db.String)
    codProducto = db.Column(db.String)
    marca = db.Column(db.String)
    presentacion = db.Column(db.String)
    unidadMedida = db.Column(db.String)
    cantidadPaquete = db.Column(db.Integer)
    subastas_productos = db.relationship('Subastas_Productos', backref='Productos', lazy=True)

    @classmethod
    def get_filter_buscar_Productos(self, nombreProducto):
        filtro = Productos.query.filter(or_(Productos.nombreProducto.ilike('%' + nombreProducto + '%'),
                                            Productos.contenidoProducto.ilike('%' + nombreProducto + '%')))
        return filtro


class Estado(db.Model, BaseModelMixin):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    codEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)


class Rol(db.Model, BaseModelMixin):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

class Usuarios(db.Model, BaseModelMixin):
    __tablename__ = "USUARIOS"
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String)
    idRol = db.Column(db.Integer,db.ForeignKey(Rol.idRol), nullable=False)
    Ruc = db.Column(db.String)
    razonSocial = db.Column(db.String)
    nombreComercial = db.Column(db.String)
    codigoPostalPais = db.Column(db.String)
    telefono = db.Column(db.String)
    celular = db.Column(db.String)
    direccion = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)

    @classmethod
    def get_joins_filter_obtener_direcciones(self, idUsuarioGet):
        filtro = Usuarios.query.filter(Usuarios.idUsuario.in_((idUsuarioGet)))
        return filtro

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
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)

    @classmethod
    def get_list_user(self, idUsuario, codEstado):
        filtro = db.session.query(Subastas, Estado). \
                 join(Estado, Subastas.idEstado == Estado.idEstado). \
                 filter(Estado.codEstado == codEstado). \
                 filter(Subastas.idUsuario == idUsuario).all()

        return filtro

    @classmethod
    def get_list_for_id(self, idUsuario, idList):
        filtro = db.session.query(Productos). \
            join(Subastas_Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            join(Subastas, Subastas.idSubasta == Subastas_Productos.idSubasta). \
            join(Estado, Estado.idEstado == Subastas.idEstado). \
            filter(Estado.nombreEstado == "Lista"). \
            filter(Subastas.idUsuario == idUsuario). \
            filter(Subastas.idSubasta == idList).all()

        return filtro

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_idd(cls, id):
        return cls.query.filter_by(idSubasta=id).first()

    @classmethod
    def find_by_id(cls, id):
        print("entro a find_by_id")
        return cls.query.get(id)

    def __init__(self, idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, idDireccion, fechaSubasta):
        self.idUsuario = idUsuario
        self.idEstado = idEstado
        self.tiempoInicial = tiempoInicial
        self.nombreSubasta = nombreSubasta
        self.precioIdeal = precioIdeal
        self.idDireccion = idDireccion
        self.fechaSubasta = fechaSubasta

class Subastas_Productos(db.Model, BaseModelMixin):
    __tablename__= "SUBASTAS_PRODUCTOS"
    idSubastasProductos = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    Cantidad = db.Column(db.Float)

    def __init__(self,idSubasta, idProducto, Cantidad):

        self.idSubasta = idSubasta
        self.idProducto = idProducto
        self.Cantidad = Cantidad

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(nombreCategoria=name).first()

    @classmethod
    def find_by_id(cls, id):
        print("entro a find_by_id")
        return cls.query.get(id)

    @classmethod
    def delete_Subastas(cls, id):
        delete_q = Subastas_Productos.__table__.delete().where(Subastas_Productos.idSubasta == id)
        db.session.execute(delete_q)
        delete_s = Subastas.__table__.delete().where(Subastas.idSubasta == id)
        db.session.execute(delete_s)
        db.session.commit()

    @classmethod
    def delete_rows_for_id(cls, id):
        delete_q = Subastas_Productos.__table__.delete().where(Subastas_Productos.idSubasta == id)
        db.session.execute(delete_q)
        #delete_s = Subastas.__table__.delete().where(Subastas.idSubasta == id)
        #db.session.execute(delete_s)
        db.session.commit()