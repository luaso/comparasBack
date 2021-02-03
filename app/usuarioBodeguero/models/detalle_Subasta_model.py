from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from sqlalchemy.sql.expression import func

db = SQLAlchemy()


class Categorias(db.Model, BaseModelMixin):
    __tablename__ = "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)


class Sub_Categorias(db.Model, BaseModelMixin):
    __tablename__ = "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategoria = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)


class Tipos_Productos(db.Model, BaseModelMixin):
    __tablename__ = "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)
    productos = db.relationship('Productos', backref='Tipos_Productos', lazy=True)

class Rol(db.Model, BaseModelMixin):
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
    pujas = db.relationship('Pujas', backref='Usuarios', lazy=True)


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
    productos = db.relationship('Productos_Supermercados', backref='Productos', lazy=True)

class Estado(db.Model, BaseModelMixin):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)

class Supermercados(db.Model, BaseModelMixin):
    __tablename__ = "SUPERMERCADOS"
    idSupermercado = db.Column(db.Integer, primary_key=True)
    nombreSupermercado = db.Column(db.String)
    imagenSupermercado = db.Column(db.String)
    urlSupermercado = db.Column(db.String)
    productos_supermercados = db.relationship('Productos_Supermercados', backref='Supermercados', lazy=True)

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

class Subastas(db.Model, BaseModelMixin):
    __tablename__ = "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    idDireccion = db.Column(db.Integer)
    fechaSubasta = db.Column(db.Date)
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)



    @classmethod
    def get_joins(self, idSubasta):
        filtro = db.session.query(Subastas, Pujas). \
            outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
            filter(Subastas.idSubasta == idSubasta)
        #print(filtro)
        return filtro

    @classmethod
    def get_detalle_subasta(self,idSubasta):
        filtro = db.session.query(Subastas,Subastas_Productos, Productos, Productos_Supermercados). \
            join(Subastas_Productos, Subastas_Productos.idSubasta == Subastas.idSubasta). \
            join(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            join(Productos_Supermercados, Productos_Supermercados.idProducto == Productos.idProducto). \
            filter(Subastas.idSubasta == idSubasta).all()
        # print(filtro)
        return filtro

    def __init__(self, idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, fechaSubasta):
        self.idUsuario = idUsuario
        self.idEstado = idEstado
        self.tiempoInicial = tiempoInicial
        self.nombreSubasta = nombreSubasta
        self.precioIdeal = precioIdeal
        self.fechaSubasta = fechaSubasta


class Subastas_Productos(db.Model, BaseModelMixin):
    __tablename__ = "SUBASTAS_PRODUCTOS"
    idSubastasProductos = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    Cantidad = db.Column(db.Float)


    def __init__(self,idSubasta, idProducto, Cantidad):

        self.idSubasta = idSubasta
        self.idProducto = idProducto
        self.Cantidad = Cantidad

class Pujas(db.Model, BaseModelMixin):
    __tablename__= "PUJAS"
    idPuja = db.Column(db.Integer, primary_key = True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    precioPuja = db.Column(db.Float)
    fechaPuja = db.Column(db.Date)


    @classmethod
    def get_filter_or(self, idSubastaGet, idUsuarioGet):
        filtro = Pujas.query.filter(or_(Pujas.idSubasta == idSubastaGet, Pujas.idUsuario == idUsuarioGet)).\
                             filter(Pujas.idPuja == db.session.query(func.max(Pujas.idPuja)))
        return filtro
    def __init__(self,idSubasta, idUsuario, precioPuja, fechaPuja):

        self.idSubasta = idSubasta
        self.idUsuario = idUsuario
        self.precioPuja = precioPuja
        self.fechaPuja = fechaPuja



#@app.route('/api/detallePujasSubasta/', methods=['GET'])
#def get_subasta_pujas():
#    idSubasta = request.json['idSubasta']
#    filtro = db.session.query(Subastas, Pujas). \
#             outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
#             filter(Subastas.idSubasta == idSubasta)

#@app.route('/api/miOfertaSubasta/', methods=['GET'])
#def get_mi_oferta():
#    idSubastaGet = request.json['idSubasta']
#    idUsuarioGet = request.json['idUsuarioGet']
#    filtro = Pujas.query.filter(or_(Pujas.idSubasta ==idSubastaGet,Pujas.idUsuario==idUsuarioGet))
