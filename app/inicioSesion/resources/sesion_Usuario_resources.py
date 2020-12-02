#pip install passlib
from passlib.hash import sha256_crypt
from flask_restful import Api, Resource
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app import ObjectNotFound
from app.inicioSesion.models.sesion_Usuario_model import Rol, Usuarios, Direcciones
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
db = SQLAlchemy()

#Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)'''


class loginUsuario(Resource):
    def post(self):
        try:
            email = request.json['email']
            password = request.json['password']
            psw = ''
            task = Usuarios.get_dato(email)
            for dato in task:
                psw = dato.password
                idUsuario = dato.idUsuario
                idRol = dato.idRol
            repuesta = '0'
            print('Validando pass text y pass cod')
            print(sha256_crypt.verify(password, psw))
            if sha256_crypt.verify(password, psw):
                return {"respuesta": "ok", "idUsuario": idUsuario, "idRol": idRol}
                #access_token = create_access_token(identity={"request": "ok"})
                #access_idUsuario = create_access_token(identity={"idusuario": idUsuario})
                #access_idRol = create_access_token(identity={"idRol": idRol})
                #return {"respuesta": access_token, "idUsuario": access_idUsuario, "idRol": access_idRol}

            else:
                return {"respuesta": "no", "idUsuario": 0, "idRol": 0}
                #access_token = create_access_token(identity={"request": "no"})
                #access_idUsuario = create_access_token(identity={"idusuario": 0})
                #access_idRol = create_access_token(identity={"idRol": 0})
                #return {"respuesta": access_token, "idUsuario": access_idUsuario, "idRol": access_idRol}
        except Exception as ex:
            raise ObjectNotFound(ex)
