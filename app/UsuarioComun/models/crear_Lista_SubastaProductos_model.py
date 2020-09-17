from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import json


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

class Subastas(db.Model):
    __tablename__= "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    fechaSubasta = db.Column(db.String)
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)

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
        fields = ('idSubastasProductos',
                  'idSubasta',
                  'idProducto',
                  'Cantidad',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'contenidoProducto',
                  'Subastas_Productos.idSubasta',
                  'Productos.idProducto',
                  'Productos.nombreProducto',
                  'Subastas_Productos.Cantidad')



task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class ProductosSchema(ma.Schema):
        class Meta:
            model = Productos


@app.route('/api/SubastaProductos', methods=['POST'])
def post_Subasta_Productos():
    idSubasta = request.json['idSubasta']
    idProducto = request.json['idProducto']
    Cantidad = request.json['Cantidad']
    new_task = Subastas_Productos(idSubasta, idProducto,Cantidad)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)


@app.route('/api/SubastaProductos', methods=['GET'])
def get_Subasta_Productos():
   task =  Subastas_Productos.query.all()
   result = tasks_schema.dump(task)
   return jsonify(result)


# FILTRAR LISTA DE PRODUCTOS DE SUBASTA_PRODUCTOS MEDIANTE LA ID DE SUBASTA
@app.route('/api/SubastaProductos1', methods=['GET'])
def get_get_Subasta_Productos_idSubasta():
    countries = []

    filtro = db.session.query(Subastas_Productos, Productos).outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto).filter(Subastas_Productos.idSubasta==85).all()
    for subastas_Productos, productos in filtro:
        print(productos.idProducto, productos.nombreProducto)


    resultado = task_schema.dump(filtro, many=True)
    print(resultado)
    return {"productos": resultado}, 200



if __name__ =="__main__":
    app.run(debug=True)