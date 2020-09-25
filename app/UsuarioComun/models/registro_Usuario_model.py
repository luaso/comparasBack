from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
#import Crypto
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
    direccion = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    imagen = db.Column(db.String)


    def __init__(self, nombreUsuario,apellidoPatUsuario,apellidoMatUsuario,idRol,Ruc,razonSocial,nombreComercial,codigoPostalPais,telefono,celular,direccion,email,password,imagen):
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
        self.direccion = direccion
        self.email = email
        self.password = password
        self.imagen = imagen


class RolSchema(ma.Schema):
    class Meta:
        fields = ('idRol', 'nombreRol','nombreUsuario','apellidoPatUsuario','apellidoMatUsuario','Ruc','razonSocial','nombreComercial','codigoPostalPais','telefono','celular','direccion','email','imagen','imagen')



rolSchema = RolSchema()
#rolsSchema = rolSchema(many=True)


@app.route('/api/ObtenerRol/', methods=['GET'])
def get():
    print('22222')
    filtro = db.session.query(Rol.nombreRol).all()
    filtro = Rol.query.filter_by(idRol=1).first()

    print(filtro)

    resultado = rolSchema.dump(filtro, many=True)
    print(resultado)
    return {"productos": filtro}, 200


@app.route('/api/GuardarUsuario/', methods=['POST'])
def post():
    data = request.get_json()
    for usuarios in data['usuarios']:
        nombreUsuario = usuarios['nombreUsuario']
        idRol = usuarios['idRol']
        Ruc = usuarios['Ruc']
        razonSocial = usuarios['razonSocial']
        nombreComercial = usuarios['nombreComercial']
        codigoPostalPais = usuarios['codigoPostalPais']
        telefono = usuarios['telefono']
        celular = usuarios['celular']
        direccion = usuarios['direccion']
        email = usuarios['email']
        password = usuarios['password']

        new_task = Usuarios(nombreUsuario, idRol, Ruc, razonSocial, nombreComercial, codigoPostalPais, telefono, celular, direccion, email, password)
        print(new_task)
        db.session.add(new_task)
        try:
            db.session.commit()
            print('Productos Agregados a la subasta con exito')
        except:
            print('Error al agregar productos')
    return ('Usuario registrado correctamente')

@app.route('/api/BuscarUsuario/<idUsuario>', methods=['GET'])
def get_usuario(idUsuario):
  task = Usuarios.query.get(idUsuario)
  return rolSchema.jsonify(task)

@app.route('/api/EditarUsuarioComprador/<idUsuario>', methods=['PUT'])
def put_usuario(idUsuario):
    usuario = Usuarios.query.get(idUsuario)
    nombreUsuario = request.json['nombreUsuario']
    apellidoPatUsuario = request.json['apellidoPatUsuario']
    apellidoMatUsuario = request.json['apellidoMatUsuario']
    idRol = 4
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
   app.run(debug=True)

