from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioComprador.models.mis_Subastas_model import Subastas
from app.usuarioComprador.schemas.mis_Subastas_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()

task_schema = TaskSchema()

class misSubastasComprador(Resource):
    def get(seft, idUsuario):
        try:
            #idUsuario = request.json['idUsuario']

            filtro = Subastas.get_mis_subastas(idUsuario)


            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)