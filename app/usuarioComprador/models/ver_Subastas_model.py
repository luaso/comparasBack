from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import distinct
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import func, and_

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
    codEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)

    @classmethod
    def find_by_cod(cls, cod):
        return cls.query.filter_by(codEstado=cod).first()

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
    email = db.Column(db.String)
    password = db.Column(db.String)
    #subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)


class Subastas(db.Model):
    __tablename__= "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    idUsuarioGanador = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    idDireccion = db.Column(db.Integer)
    fechaSubasta = db.Column(db.Date)
    usuario = db.relationship("Usuarios", foreign_keys=[idUsuario])
    usuarioGanador = db.relationship("Usuarios", foreign_keys=[idUsuarioGanador])
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)

    @classmethod
    def get_joins_filter_Subastas_Creadas(self, idUsuarioGet):
        filtro = db.session.query(Subastas, Usuarios, Estado). \
            outerjoin(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
            outerjoin(Estado, Subastas.idEstado == Estado.idEstado). \
            filter(Subastas.idUsuario == idUsuarioGet).all()
        return filtro

    @classmethod
    def find_by_id(cls, id):
        print("entro a find_by_id")
        return cls.query.get(id)

    @classmethod
    def find_by_id2(cls, idSubasta):
        subqueryP = db.session.query(func.min(Pujas.precioPuja), Usuarios.idUsuario). \
            join(Usuarios, Usuarios.idUsuario == Pujas.idUsuario). \
            filter(Pujas.idSubasta == idSubasta).group_by(Pujas.idUsuario, Usuarios.idUsuario).order_by(func.min(Pujas.precioPuja)).all()
        return subqueryP

    @classmethod
    def find_by_id3(cls, idSubasta):
        filtro = db.session.query(Pujas, Subastas, Usuarios). \
            join(Pujas, Pujas.idSubasta == Subastas.idSubasta). \
            join(Usuarios, Usuarios.idUsuario == Pujas.idUsuario). \
            filter(Subastas.idSubasta == idSubasta).all()
        return filtro

    @classmethod
    def get_joins_filter_Detalle_Subasta(cls, idSubasta):

        subqueryP = db.session.query(Pujas). \
            join(Subastas, Subastas.idSubasta == Pujas.idSubasta). \
            filter(Subastas.idSubasta == idSubasta).order_by(Pujas.precioPuja).subquery()
        #print("subquery")
        #print(subqueryP)
        #return

        filtro = db.session.query(subqueryP, Subastas, Usuarios). \
            join(subqueryP, subqueryP.c.idSubasta == Subastas.idSubasta). \
            join(Usuarios, Usuarios.idUsuario == subqueryP.c.idUsuario). \
            filter(Subastas.idSubasta == idSubasta).distinct(subqueryP.c.idUsuario).all()

        return filtro

    @classmethod
    def get_productos_subasta(self, idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos). \
                 join(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
                 filter(Subastas_Productos.idSubasta == idSubasta)
        return filtro

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

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


class Pujas(db.Model, BaseModelMixin):
    __tablename__ = "PUJAS"
    idPuja = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer, db.ForeignKey(Subastas.idSubasta), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    precioPuja = db.Column(db.Float)
    fechaPuja = db.Column(db.DateTime)

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






