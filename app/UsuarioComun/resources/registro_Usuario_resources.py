from flask_restful import Api, Resource
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from app import ObjectNotFound
from app.UsuarioComun.models.registro_Usuario_model import Rol, Usuarios, RolSchema
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

rolSchema = RolSchema()

class obtenerRol(Resource):
    def get(self):
        print('22222')
        filtro = db.session.query(Rol).all()

        for rol in filtro:
            print(rol.nombreRol)

        resultado = rolSchema.dump(filtro, many=True)
        print(resultado)
        return {"Roles por registro": resultado}, 200

class guardarUsuario(Resource):
    def post(self):
        print('ingresando a guardarusuario')
        data = request.get_json()

        for usuarios in data['usuarios']:
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
            direccion = usuarios['direccion']
            email = usuarios['email']
            password = usuarios['password']

            new_task = Usuarios(nombreUsuario,apellidoPatUsuario,apellidoMatUsuario, idRol, Ruc, razonSocial, nombreComercial, codigoPostalPais, telefono, celular, direccion, email, password)
            print(new_task)
            db.session.add(new_task)
            try:
                db.session.commit()
                print('Productos Agregados a la subasta con exito')
            except:
                print('Error al agregar productos')
        return ('Usuario registrado correctamente')

class buscarUsuario(Resource):
    def get(seft, idUsuario):
        print('prueba entrada get')
        task = Usuarios.query.get(idUsuario)
        print('prueba salida get')
        return rolSchema.jsonify(task)

class editarUsuarioComprador(Resource):
    def put(seft,idUsuario):
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
        password = request.json['password']

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
        usuario.password = password

        db.session.commit()

        return rolSchema.jsonify(usuario)

