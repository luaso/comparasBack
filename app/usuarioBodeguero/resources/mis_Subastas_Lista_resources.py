from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioBodeguero.models.mis_Subastas_Lista_model import Subastas, Usuarios, Estado, Pujas
from app.usuarioBodeguero.schemas.mis_Subastas_Lista_schema import TaskSchema
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

class misSubastasBodeguero(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:


            #filtro = Subastas.get_join_filter(idUsuario)
            filtro1 = Subastas.get_mis_subastas_disponibles(idUsuario)

            result = jsonify({"resultado": filtro1})
            #result = task_schema.dump(filtro, many=True)

            return result
        except Exception as ex:
            raise ObjectNotFound(ex)