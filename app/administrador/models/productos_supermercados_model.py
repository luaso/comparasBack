from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
db = SQLAlchemy()


class Parametros(db.Model, BaseModelMixin):
    __tablename__="PARAMETROS"
    idParametros = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.String)
    Estado = db.Column(db.Integer)
    FecCrea = db.Column(db.Date)
    FecModifica = db.Column(db.Date)
    UsuCrea = db.Column(db.Integer)
    UsuModifica = db.Column(db.Integer)
    Valor = db.Column(db.String)

    @classmethod
    def get(self, idParametros):

       filtro =  db.session.query(Parametros).filter(Parametros.idParametros == idParametros)

       return filtro


class Supermercados(db.Model, BaseModelMixin):
    __tablename__="SUPERMERCADOS"
    idSupermercado = db.Column(db.Integer, primary_key=True)
    nombreSupermercado = db.Column(db.String)
    imagenSupermercado = db.Column(db.String)
    urlSupermercado = db.Column(db.String)
    productos_supermercado = db.relationship('Productos_Supermercados', backref='Supermercados', lazy=True)

    @classmethod
    def get_Supermercado(self, nombreSupermercado):
        filtro = Supermercados.query.filter(Supermercados.nombreSupermercado.ilike('%' + nombreSupermercado + '%'))
        return filtro

class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)

class Sub_Categorias(db.Model, BaseModelMixin):
    __tablename__= "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategorias = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)

class Tipos_Productos(db.Model, BaseModelMixin):
    __tablename__= "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)
    productos = db.relationship('Productos', backref='Tipos_Productos', lazy=True)

    @classmethod
    def get_joins(self):
        filtro = Tipos_Productos.query.all()


        # print(filtro)
        return filtro

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
    productos_supermercado = db.relationship('Productos_Supermercados', backref='Productos', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_pro(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_query(self, idProducto):
        filtro = Productos.query.get(idProducto)
        return filtro

    @classmethod
    def get_joins(self):
        filtro = db.session.query(Categorias, Sub_Categorias, Tipos_Productos, Productos, Productos_Supermercados,Supermercados ). \
                 outerjoin(Sub_Categorias, Categorias.idCategoria == Sub_Categorias.idCategoria). \
                 outerjoin(Tipos_Productos, Sub_Categorias.idSubCategorias == Tipos_Productos.idSubCategorias). \
                 outerjoin(Productos, Tipos_Productos.idTipoProducto == Productos.idTipoProducto). \
                 outerjoin(Productos_Supermercados, Productos.idProducto == Productos_Supermercados.idProducto). \
                 outerjoin(Supermercados, Productos_Supermercados.idSupermercado == Supermercados.idSupermercado)

        # print(filtro)
        return filtro

    @classmethod
    def get(self, idProducto):
        filtro = db.session.query(Productos).filter(Productos.idProducto == idProducto)

        return filtro



    @classmethod
    def get_Max(self):
        filtro = Productos.query.filter(Productos.idProducto == db.session.query(func.max(Productos.idProducto)))
        return filtro

    @classmethod
    def get_productos(self, nombreProducto):
        filtro = Productos.query.filter(or_(Productos.nombreProducto.ilike('%' + nombreProducto + '%'),
                                            Productos.contenidoProducto.ilike('%' + nombreProducto + '%')))
        return filtro


    def __init__(self, idTipoProducto, nombreProducto, contenidoProducto, Imagen, codProducto, marca, presentacion,unidadMedida, cantidadPaquete):
        #self.idProducto = idProducto
        self.idTipoProducto = idTipoProducto
        self.nombreProducto = nombreProducto
        self.contenidoProducto = contenidoProducto
        self.Imagen = Imagen
        self.codProducto = codProducto
        self.marca = marca
        self.presentacion = presentacion
        self.unidadMedida = unidadMedida
        self.cantidadPaquete = cantidadPaquete

class Productos_Supermercados(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS_SUPERMERCADOS"
    idProductoSupermercado = db.Column(db.Integer, primary_key=True)
    idSupermercado = db.Column(db.Integer, db.ForeignKey(Supermercados.idSupermercado), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    fechaProducto = db.Column(db.Date)
    precioRegular = db.Column(db.Float)
    precioOnline = db.Column(db.Float)
    precioTarjeta = db.Column(db.Float)
    nombreTarjeta = db.Column(db.String)

    #Guardar
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    #Eliminar
    def delete_pro(self):
        db.session.delete(self)
        db.session.commit()

    #Filtrar por ID
    @classmethod
    def get_query(self, idProductoSupermercado):
        filtro = Productos_Supermercados.query.get(idProductoSupermercado)
        return filtro

    #Obtener todos los Registros
    @classmethod
    def get(self):
        filtro = db.session.query(Productos_Supermercados, Productos, Supermercados).\
                 join(Productos_Supermercados, Productos.idProducto == Productos_Supermercados.idProducto). \
                 join(Supermercados, Productos_Supermercados.idSupermercado == Supermercados.idSupermercado)
        return filtro

    def __init__(self, idSupermercado, idProducto, fechaProducto, precioRegular, precioOnline, precioTarjeta, nombreTarjeta):
        # self.idProducto = idProducto
        self.idSupermercado = idSupermercado
        self.idProducto = idProducto
        self.fechaProducto = fechaProducto
        self.precioRegular = precioRegular
        self.precioOnline = precioOnline
        self.precioTarjeta = precioTarjeta
        self.nombreTarjeta = nombreTarjeta
