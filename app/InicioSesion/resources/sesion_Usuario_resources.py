from flask_restful import Api, Resource
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from app import ObjectNotFound
from app.InicioSesion.models.mantenimiento_Usuario_model import Rol, Usuarios, RolSchema, Direcciones

db = SQLAlchemy()

rolSchema = RolSchema()

class loginUsuario(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        try:
            task = db.session.query(Usuarios).filter_by(email=email).first()
            repuesta = '0'
            if task.password == password:
                repuesta = 'ok'
                idusuario = task.idUsuario
                idRol = task.idRol
            else:
                repuesta = 'nok'
                idusuario = 'Usuario no encontrado'
            return {"respuesta": repuesta, "idUsuario": idusuario, "idRol": idRol}
        except:
            return {"respuesta": "Correo no encontrado"}
