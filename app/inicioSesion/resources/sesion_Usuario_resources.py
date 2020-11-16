#pip install passlib
from passlib.hash import sha256_crypt
from flask_restful import Api, Resource
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from app import ObjectNotFound
from app.inicioSesion.models.sesion_Usuario_model import Rol, Usuarios, Direcciones
import bcrypt
db = SQLAlchemy()



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
            else:
                return {"respuesta": "no", "idUsuario": 0, "idRol": 0}
        except Exception as ex:
            raise ObjectNotFound(ex)
