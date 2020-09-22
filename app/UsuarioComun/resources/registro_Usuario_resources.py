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