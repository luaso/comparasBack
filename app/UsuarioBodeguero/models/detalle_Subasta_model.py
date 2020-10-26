from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Estado(db.Model):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)


class Rol(db.Model):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

class Usuarios(db.Model):
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
    direccionOpcional1 = db.Column(db.String)
    direccionOpcional2 = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)
    pujas = db.relationship('Pujas', backref='Usuarios', lazy=True)

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
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    fechaSubasta = db.Column(db.String)
    pujas = db.relationship('Pujas', backref='Subastas', lazy=True)

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

class Pujas(db.Model):
    __tablename__= "PUJAS"
    idPuja = db.Column(db.Integer, primary_key = True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    precioPuja = db.Column(db.Float)

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('direccion',
                  'direccionOpcional1',
                  'direccionOpcional2',
                  'Subastas.idSubasta',
                  'Subastas.idUsuario',
                  'Subastas.idEstado',
                  'Subastas.tiempoInicial',
                  'Subastas.nombreSubasta',
                  'Subastas.precioIdeal',
                  'Subastas.fechaSubasta',
                  'Subastas_Productos.idSubasta',
                  'Subastas_Productos.idProducto',
                  'Subastas_Productos.Cantidad',
                  'Productos.nombreProducto',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'contenidoProducto')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/api/detallePujasSubasta/', methods=['GET'])
def get_subasta_pujas():
    idSubasta = request.json['idSubasta']
    filtro = db.session.query(Subastas, Pujas). \
             outerjoin(Pujas, Subastas.idSubasta == Pujas.idSubasta). \
             filter(Subastas.idSubasta == idSubasta)

@app.route('/api/miOfertaSubasta/', methods=['GET'])
def get_mi_oferta():
    idSubastaGet = request.json['idSubasta']
    idUsuarioGet = request.json['idUsuarioGet']
    filtro = Pujas.query.filter(or_(Pujas.idSubasta ==idSubastaGet,Pujas.idUsuario==idUsuarioGet))
