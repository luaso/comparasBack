from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
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
        fields = ('idUsuario', 'idEstado', 'tiempoInicial','nombreSubasta','precioIdeal','fechaSubasta','idSubasta','idProducto','Cantidad')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/api/Subasta', methods=['POST'])
def create_task():

    #if  request.json['idUsuario'] != 1 :
    #    idUsuario = request.json['idUsuario']
    #else:
    #    idUsuario = 1
    idUsuario = 1
    idEstado = 1
    tiempoInicial = datetime.now()
    nombreSubasta = 'Creación de lista'
    precioIdeal = 0.0
    fechaSubasta = 'Por definir'

    crearSubasta = Subastas(idUsuario, idEstado,tiempoInicial,nombreSubasta,precioIdeal,fechaSubasta)
    db.session.add(crearSubasta)

    try:
        db.session.commit()
        print('Crear Subasta')
        intCreacion = 1
    except:
        print('Error al Crear Subasta')

    if  intCreacion == 1:
        idSubasta = request.json['idSubasta']
        idProducto = request.json['idProducto']
        Cantidad = request.json['Cantidad']
        new_task = Subastas_Productos(idSubasta, idProducto, Cantidad)
        db.session.add(new_task)
        db.session.commit()
        #return task_schema.jsonify(new_task)

    return task_schema.jsonify(new_task)

if __name__ =="__main__":
    app.run(debug=True)


