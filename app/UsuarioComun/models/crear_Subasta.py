#from flask import Flask, request, jsonify
#from flask_marshmallow import Marshmallow
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import Column, Integer, String
#from datetime import datetime
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
#ma = Marshmallow(app)

from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()
ma = Marshmallow()
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
                  'Subastas_Productos.Cantidad')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


"""@app.route('/api/subastasUsuario', methods=['GET'])
def get_subastas_usuarios():
    idUsuario = request.json['idUsuario']
    idEstado = 1
    filtro = db.session.query(Subastas, Subastas_Productos).outerjoin(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta).filter(Subastas.idUsuario==idUsuario).filter(Subastas.idEstado==idEstado).all()
    #print(filtro)

    resultado = task_schema.dump(filtro, many=True)
    #print(resultado)
    return {"subastas": resultado}, 200

@app.route('/api/direccionSubasta/<idUsuario>', methods=['GET'])
def get_Comparacion_Supermercados_Productos(idUsuario):
    filtro = Usuarios.query.filter(Usuarios.idUsuario.in_((idUsuario)))
    #print(filtro)
    for resultado1 in filtro:
        print(resultado1.direccion)

    resultado = task_schema.dump(filtro, many=True)
    #print(resultado)
    return {"subastas": resultado}, 200

@app.route('/api/subastarLista/<idSubasta>', methods=['PUT'])
def put_Bodeguero(idUsuario):
    usuario = Usuarios.query.get(idUsuario)
    nombreUsuario = request.json['nombreUsuario']
    apellidoPatUsuario = request.json['apellidoPatUsuario']
    apellidoMatUsuario = request.json['apellidoMatUsuario']
    idRol = 3
    Ruc = request.json['Ruc']
    razonSocial = request.json['razonSocial']
    nombreComercial = request.json['nombreComercial']
    codigoPostalPais = request.json['codigoPostalPais']
    telefono = request.json['telefono']
    celular = request.json['celular']
    direccion = request.json['direccion']
    email = request.json['email']
    imagen = request.json['imagen']

    usuario.nombreUsuario = nombreUsuario
    usuario.apellidoPatUsuario = apellidoPatUsuario
    usuario.apellidoMatUsuario = apellidoMatUsuario
    usuario.idRol = idRol
    usuario.Ruc = Ruc
    usuario.razonSocial = razonSocial
    usuario.nombreComercial = nombreComercial
    usuario.codigoPostalPais = codigoPostalPais
    usuario.telefono = telefono
    usuario.celular = celular
    usuario.direccion = direccion
    usuario.email = email
    usuario.imagen = imagen

    db.session.commit()

    return rolSchema.jsonify(usuario)



if __name__ =="__main__":
   app.run(debug=True)"""
