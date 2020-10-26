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


class Categorias(db.Model):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)

class Sub_Categorias(db.Model):
    __tablename__= "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategoria = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)

class Tipos_Productos(db.Model):
    __tablename__= "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)
    productos = db.relationship('Productos', backref='Tipos_Productos', lazy=True)


class Productos(db.Model):
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

    def __init__(self, idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, idDireccion, fechaSubasta):
        self.idUsuario = idUsuario
        self.idEstado = idEstado
        self.tiempoInicial = tiempoInicial
        self.nombreSubasta = nombreSubasta
        self.precioIdeal = precioIdeal
        self.idDireccion = idDireccion
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
                  'Subastas_Productos.Cantidad',
                  'Productos.nombreProducto',
                  'idProducto',
                  'idCategoria',
                  'nombreProducto',
                  'contenidoProducto')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

#Listar subastas de Usuario
@app.route('/api/listasUsuario/', methods=['GET'])
def get_subastas_usuarios():
    idUsuario = request.json['idUsuario']
    idEstado = 1
    filtro = db.session.query(Subastas, Subastas_Productos, Productos).\
             outerjoin(Subastas_Productos, Subastas.idSubasta == Subastas_Productos.idSubasta). \
             outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
             filter(Subastas.idUsuario==idUsuario).\
             filter(Subastas.idEstado==idEstado).all()
    #print(filtro)

    resultado = task_schema.dump(filtro, many=True)
    #print(resultado)
    return {"subastas": resultado}, 200

#Listas direcciones del usuario
@app.route('/api/direccionSubasta/', methods=['GET'])
def get_obtener_direcciones():
    idUsuarioGet = request.json['idUsuario']

    filtro = Usuarios.query.filter(Usuarios.idUsuario.in_((idUsuarioGet)))
    #print(filtro)
    for resultado1 in filtro:
        print(resultado1.direccion)

    resultado = task_schema.dump(filtro, many=True)
    #print(resultado)
    return {"subastas": resultado}, 200


@app.route('/api/crearSubasta/', methods=['PUT'])
def put_Crear_Subuasta():

    idSubastaGet = request.json['idSubasta']

    CrearSubasta = Subastas.query.get(idSubastaGet)

    print(CrearSubasta)

    fechaSubasta = request.json['Fecha'] + ' ' + request.json['Hora']
    print(fechaSubasta)
    idDireccion = request.json['idDireccion']

    CrearSubasta.fechaSubasta = fechaSubasta
    CrearSubasta.idDireccion = idDireccion
    db.session.commit()

    return {"respuesta": 'Se creo la subasta correctamente'}



@app.route('/api/buscarProductos/<string:nombreProducto>', methods=['GET'])
def get_buscar_Productos(nombreProducto):
    producto = Productos.query.filter(or_(Productos.nombreProducto.ilike('%' + nombreProducto + '%'),
                                          Productos.contenidoProducto.ilike('%' + nombreProducto + '%')))

    result = task_schema.dump(producto, many=True)
    print(result)
    print('=================================================')
    return {"producto": result}, 200

# reusar api para crear listas
# reusar api para crear subasta

if __name__ =="__main__":
   app.run(debug=True)
