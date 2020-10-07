from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime

#import crypt

#import os
#import binascii
#from Crypto.PublicKey import RSA
#from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Rol(db.Model):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

    def __init__(self, idRol, nombreRol):
        self.idRol = idRol
        self.nombreRol = nombreRol



class Usuarios(db.Model):
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
    direcciones = db.relationship('Direcciones', backref='Usuarios', lazy=True)

    def __init__(self, nombreUsuario,apellidoPatUsuario,apellidoMatUsuario,idRol,Ruc,razonSocial,nombreComercial,codigoPostalPais,telefono,celular,email,password,imagen):
        self.nombreUsuario = nombreUsuario
        self.apellidoPatUsuario = apellidoPatUsuario
        self.apellidoMatUsuario = apellidoMatUsuario
        self.idRol = idRol
        self.Ruc = Ruc
        self.razonSocial = razonSocial
        self.nombreComercial = nombreComercial
        self.codigoPostalPais = codigoPostalPais
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.password = password
        self.imagen = imagen

class Direcciones(db.Model):
    __tablename__="DIRECCIONES"
    idDireccion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    direccion = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    def __init__(self, idUsuario,direccion,latitud,longitud):
        #self.idDireccion=idDireccion
        self.idUsuario =idUsuario
        self.direccion= direccion
        self.latitud = latitud
        self.longitud = longitud


class RolSchema(ma.Schema):
    class Meta:
        fields = ('idRol', 'nombreRol','nombreUsuario','apellidoPatUsuario','apellidoMatUsuario','Ruc','razonSocial','nombreComercial','codigoPostalPais','telefono','celular','email','imagen','imagen','idUsuario','direccion','latitud','longitud')

rolSchema = RolSchema()


#db.create_all()
#rolsSchema = rolSchema(many=True)


@app.route('/api/ObtenerRol/', methods=['GET'])
def get1():
    print('22222')
    filtro=Rol.query.filter(Rol.idRol.in_((3,4)))


    print(filtro)

    resultado = rolSchema.dump(filtro, many=True)
    print(resultado)
    return {"rol": resultado}, 200

@app.route('/api/direcciones/', methods=['GET'])
def get():
    print('Estoy aqui')
    producto = Direcciones.query.filter(Direcciones.direccion.ilike('%1%'))
    print('Error al jalar')

    print(producto)
    result = rolSchema.dump(producto, many=True)
    return {"productos": result}, 200

@app.route('/api/agregarDireccion/', methods=['POST'])
def get2():
    #idDireccion=4
    idUsuario = 35
    direccion = '123123'
    latitud = '1231231232'
    longitud = '123123213'
    CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
    print(CrearDireccion)
    db.session.add(CrearDireccion)
    db.session.commit()
    return ('POR FIN UN RESULTADO BUENO CON ESA TABLA DE MIERDA')

@app.route('/api/GuardarUsuario/', methods=['POST'])
def post():
    print('ingresando a guardarusuario')
    data = request.get_json()

    for usuarios in data['usuarios']:
        print('ingresando a seccion usuarios')
        nombreUsuario = usuarios['nombreUsuario']
        apellidoPatUsuario = usuarios['apellidoPatUsuario']
        apellidoMatUsuario = usuarios['apellidoMatUsuario']
        idRol = usuarios['idRol']
        Ruc = usuarios['Ruc']
        razonSocial = usuarios['razonSocial']
        nombreComercial = usuarios['nombreComercial']
        codigoPostalPais = usuarios['codigoPostalPais']
        telefono = usuarios['telefono']
        celular = usuarios['celular']
        email = usuarios['email']
        password = usuarios['password']
        imagen = usuarios['imagen']

        CrearUsuario = Usuarios(nombreUsuario, apellidoPatUsuario, apellidoMatUsuario, idRol, Ruc, razonSocial,
                                nombreComercial, codigoPostalPais, telefono, celular, email, password,imagen)
        print(CrearUsuario)
        db.session.add(CrearUsuario)
        try:
            db.session.commit()
            idUsuarioFK = CrearUsuario.idUsuario
            print('Usuario agregado correctamente')
        except:
            print('Error al agregar usuario')

    for direcciones in data['direcciones']:
        idUsuario = idUsuarioFK
        print(idUsuario)
        direccion = direcciones['direccion']
        print(direccion)
        latitud = direcciones['latitud']
        print(latitud)
        longitud = direcciones['longitud']
        print(longitud)


        print('entrando al try')
        try:
            CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
            print(CrearDireccion)
            db.session.add(CrearDireccion)
            db.session.commit()
            print('Direcciones agregadas correctamente')
        except:
            print('Error al agregar direccion')

    return ('Usuario registrado correctamente')

@app.route('/api/BuscarUsuario/<idUsuario>', methods=['GET'])
def get_usuario(idUsuario):
  task = Usuarios.query.get(idUsuario)
  return rolSchema.jsonify(task)

@app.route('/api/EditarUsuarioComprador/', methods=['PUT'])
def put_Comprador():
    data = request.get_json()
    for direcciones in data['direcciones']:


        idUsuario = direcciones['idUsuario']
        print(idUsuario)
        direccion = direcciones['direccion']
        print(direccion)
        latitud = direcciones['latitud']
        print(latitud)
        longitud = direcciones['longitud']
        print(longitud)

        print('entrando al try')
        try:
            CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
            print(CrearDireccion)
            db.session.add(CrearDireccion)
            db.session.commit()
            print('Direcciones agregadas correctamente')
        except:
            print('Error al agregar direccion')

    return ('Usuario registrado correctamente')


@app.route('/api/EditarUsuarioBodeguero/<idUsuario>', methods=['PUT'])
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


#LOGIN

@app.route('/api/LoginUsuario/', methods=['GET'])
def get_email():
    print('prueba entrada get')
    email = request.json['email']
    password = request.json['password']
    try:

        task = db.session.query(Usuarios).filter_by(email=email).first()
        print(task.idUsuario)
        print(task.password)
        repuesta = '0'

        if task.password == password:
           print('Correcto')
           repuesta = 'ok'
           print(task.idUsuario)
           idusuario = task.idUsuario
        else:
            print('incorrecto')
            repuesta = 'nok'
            idusuario = 'Usuario no encontrado'

        return {"respuesta": repuesta, "idUsuario": idusuario}
    except:
        return {"respuesta": "Correo no encontrado"}


if __name__ =="__main__":
   app.run(debug=True)

