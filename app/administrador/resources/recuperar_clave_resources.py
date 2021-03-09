# pip install passlib
import datetime

from passlib.hash import sha256_crypt
from flask_restful import Api, Resource
from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import ObjectNotFound, validateToken
from app.inicioSesion.models.mantenimiento_Usuario_model import Rol, Usuarios
from app.inicioSesion.models.sesion_Usuario_model import rolSchema
from app.validateToken import sendEmailrecoverPassword

db = SQLAlchemy()


# Pruebas
class recuperarClave(Resource):
    def post(self):
        try:
            email = request.json['email']
            psw = ''
            idUsuario= getbyid(email)
            if(idUsuario=="No_Existe"):
                return {"respuesta": "Correo no existe"}

            x = datetime.datetime.now()
            hourseconds = (str(x.minute) + "_" + str(x.second))
            paswordview=hourseconds+str(idUsuario)
            password = sha256_crypt.encrypt(paswordview)
            print(password)
            print(paswordview)
            print(sha256_crypt.verify("password", password))
            usuarioEditar = Usuarios.get_query(idUsuario)
            usuarioEditar.password = password
            try:
                usuarioEditar.save_to_db()
                sendEmailrecoverPassword(email,paswordview)
                print('realizado')
            except Exception as ex:
                print('error')
                raise ObjectNotFound(ex)
            return {"respuesta": "Enviado"}
        except Exception as ex:
            raise ObjectNotFound(ex)

def getbyid(email):
    try:
        usuarioExist = Usuarios.get_email(email)
        iduser=str(usuarioExist.idUsuario)
        print(iduser)
        return iduser
    except Exception as ex:
        return "No_Existe"
