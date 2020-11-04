from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioBodeguero.models.mis_Subastas_Lista_model import Subastas, Usuarios, Estado, Pujas
from app.usuarioBodeguero.schemas.mis_Subastas_Lista_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()

task_schema = TaskSchema()

class misSubastasBodeguero(Resource):
    def get(seft):
        try:
            idUsuario = request.json['idUsuario']

            filtro = Subastas.get_join_filter(idUsuario)


            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)