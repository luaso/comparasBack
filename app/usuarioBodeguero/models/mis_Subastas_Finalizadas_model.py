from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from config.configuration import AdditionalConfig
from sqlalchemy.sql.expression import func

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
    pujas = db.relationship('Pujas', backref='Usuarios', lazy=True)

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

class Direcciones(db.Model, BaseModelMixin):
    __tablename__="DIRECCIONES"
    idDireccion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    direccion = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Direcciones', lazy=True)

class Subastas(db.Model):
    __tablename__ = "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    idUsuarioGanador = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    idDireccion = db.Column(db.Integer,db.ForeignKey(Direcciones.idDireccion), nullable=False)
    fechaSubasta = db.Column(db.Date)
    direccionFinal = db.Column(db.String)
    usuario = db.relationship("Usuarios", foreign_keys=[idUsuario])
    usuarioGanador = db.relationship("Usuarios", foreign_keys=[idUsuarioGanador])
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)


    @classmethod
    def get_join_filter(self, idUsuario):
        filtro = db.session.query(Subastas, Subastas_Productos, Productos, Pujas, Estado, Usuarios). \
            join(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta). \
            join(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            join(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
            join(Estado, Subastas.idEstado == Estado.idEstado). \
            join(Usuarios, Subastas.idUsuario == Usuarios.idUsuario). \
            filter(Pujas.idUsuario == idUsuario).all()
            #filter(Pujas.idSubasta== Subastas.idSubasta).all()
        # filtro = Pujas.query.filter(or_(Pujas.idSubasta == idSubastaGet, Pujas.idUsuario == idUsuarioGet)).\
        # filter(Pujas.idPuja == db.session.query(func.max(Pujas.idPuja)))
        return filtro

    @classmethod
    def get_mis_subastas_finalizadas(self, idUsuario):

        misOfertasMin = db.session.query(func.min(Pujas.precioPuja).label("miMinOferta"), Subastas.idSubasta).\
            join(Subastas, Subastas.idSubasta == Pujas.idSubasta).\
            join(Estado, Estado.idEstado == Subastas.idEstado).\
            join(Usuarios, Usuarios.idUsuario == Pujas.idUsuario).\
            filter(Pujas.idUsuario == idUsuario).\
            filter(Estado.codEstado == AdditionalConfig.ESTADO4). \
            filter(Subastas.idUsuarioGanador == idUsuario). \
            group_by(Pujas.idSubasta, Subastas.idSubasta).all()

        print("misOfertasMin")
        print(misOfertasMin)

        misSubastasP = db.session.query(Subastas.idSubasta, Usuarios.nombreUsuario, Usuarios.apellidoPatUsuario,
                                        Subastas.fechaSubasta, Estado.nombreEstado). \
            join(Usuarios, Usuarios.idUsuario == Subastas.idUsuario). \
            join(Estado, Estado.idEstado == Subastas.idEstado).\
            filter(Estado.codEstado == AdditionalConfig.ESTADO4). \
            filter(Subastas.idUsuarioGanador == idUsuario).all()

        print("misSubastasP")
        print(misSubastasP)

        arr = []

        for data in misOfertasMin:
            dicc = {}
            miOfertaMinima = data[0]
            idSubasta = data[1]
            ofertaMinimaSubasta = data[0]


            for subasta in misSubastasP:
                if subasta[0] == idSubasta:
                    nombreUsuario = subasta[1]
                    apellidoPatUsuario = subasta[2]
                    fechaSubasta = subasta[3].strftime("%Y-%m-%d %H:%M:%S")
                    estadoSubasta = subasta[4]

            dicc = {"Subastas.idSubasta":idSubasta,
                    "Usuarios.nombreUsuario":nombreUsuario,
                    "Usuarios.apellidoPatUsuario":apellidoPatUsuario,
                    "Subastas.fechaSubasta":fechaSubasta,
                    "Pujas.miOferta":miOfertaMinima,
                    "Pujas.ofertaMinimaSubasta":ofertaMinimaSubasta,
                    "Estado.nombreEstado":estadoSubasta}

            arr.append(dicc)
        return arr

    @classmethod
    def get_usuario_ganador(self, idSubasta, idUsuario):
        filtro = db.session.query(Usuarios, Direcciones,Subastas). \
            join(Subastas, Subastas.idUsuario == Usuarios.idUsuario). \
            join(Direcciones, Direcciones.idDireccion == Subastas.idDireccion).\
            filter(Subastas.idSubasta == idSubasta).\
            filter(Subastas.idUsuarioGanador == idUsuario).all()
        return filtro


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

class Pujas(db.Model, BaseModelMixin):
    __tablename__ = "PUJAS"
    idPuja = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer, db.ForeignKey(Subastas.idSubasta), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey(Usuarios.idUsuario), nullable=False)
    precioPuja = db.Column(db.Float)
    fechaPuja = db.Column(db.DateTime)

    def __init__(self,idSubasta, idUsuario, precioPuja, fechaPuja):

        self.idSubasta = idSubasta
        self.idUsuario = idUsuario
        self.precioPuja = precioPuja
        self.fechaPuja = fechaPuja



#@app.route('/api/misSubastasBodeguero/', methods=['GET'])
#def get_Subastas():
#    idUsuario = request.json['idUsuario']

#    filtro = db.session.query(Subastas, Subastas_Productos, Productos, Pujas). \
#             outerjoin(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta). \
#             outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
#             outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
#             filter(Subastas.idUsuario == idUsuario).all()

