from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioComprador.models.mis_Subastas_model import Subastas
from app.usuarioComprador.schemas.mis_Subastas_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from app.validateToken import check_for_token

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()

class misSubastasComprador(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idUsuario = request.json['idUsuario']

            filtro = Subastas.get_mis_subastas(idUsuario)


            result = task_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"Subastas": result})
            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)