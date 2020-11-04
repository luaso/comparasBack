from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
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

class Estado(db.Model, BaseModelMixin):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
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
    def get_joins_filter_Subastas_Creadas(self, idUsuarioGet):
        filtro = db.session.query(Subastas, Usuarios, Estado). \
            outerjoin(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
            outerjoin(Estado, Subastas.idEstado == Estado.idEstado). \
            filter(Subastas.idUsuario == idUsuarioGet).all()
        return filtro

    @classmethod
    def get_joins_filter_Detalle_Subasta(self, idSubastaGet):
        filtro = db.session.query(Subastas, Subastas_Productos, Productos, Pujas). \
            outerjoin(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta). \
            outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
            filter(Subastas.idSubasta == idSubastaGet).all()
        return filtro

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




#Ver subastas
#@app.route('/api/listasSubastasCreadas/', methods=['GET'])
#def get_Subastas_Creadas():
#    idUsuarioGet = request.json['idUsuario']

#    filtro = db.session.query(Subastas, Usuarios, Estado). \
#             outerjoin(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
#             outerjoin(Estado, Subastas.idEstado == Estado.idEstado). \
#             filter(Subastas.idUsuario == idUsuarioGet).all()

#@app.route('/api/detalleSubasta/', methods=['GET'])
#def get_Detalle_Subasta():
#    idSubastaGet = request.json['idSubasta']

#    filtro = db.session.query(Subastas, Subastas_Productos, Productos, Pujas). \
#             outerjoin(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta). \
#             outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
#             outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
#             filter(Subastas.idSubasta == idSubastaGet).all()

#@app.route('/api/detalleSubasta/', methods=['PUT'])
#def put_ganador_Subasta():
#    idSubastaGet = request.json['idSubasta']
#    CrearSubasta = Subastas.query.get(idSubastaGet)
#    idUsuarioGanador = request.json['idUsuarioGanador']
#    Subastas.idUsuarioGanador = idUsuarioGanador
#    db.session.commit()
#    return {"respuesta": 'Se guardo el ganador correctamente'}






