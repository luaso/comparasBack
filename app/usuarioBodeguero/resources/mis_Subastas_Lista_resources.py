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
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()

class misSubastasBodeguero(Resource):
    def get(seft, idUsuario):
        try:
            #idUsuario = request.json['idUsuario']

            filtro = Subastas.get_join_filter(idUsuario)

            result = task_schema.dump(filtro, many=True)
            access_token = create_access_token(identity={"subastas": result})

            return {"Resultado": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)