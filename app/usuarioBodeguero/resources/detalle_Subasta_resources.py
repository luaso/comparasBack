from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioBodeguero.models.detalle_Subasta_model import Subastas, Productos, Subastas_Productos, Pujas
from app.usuarioBodeguero.schemas.detalle_Subasta_schema import TaskSchema
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

class detallePujasSubasta(Resource):
    def get(self):
        try:
            idSubasta = request.json['idSubasta']

            filtro = Subastas.get_joins(idSubasta)

            result = task_schema.dump(filtro, many=True)
            access_token = create_access_token(identity={"productos": result})

            return {"Resultado": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerMiOferta(Resource):
    def get(self):
        try:
            idSubastaGet = request.json['idSubasta']
            idUsuarioGet = request.json['idUsuario']

            filtro = Pujas.get_filter_or(idSubastaGet,idUsuarioGet)

            result = task_schema.dump(filtro, many=True)
            access_token = create_access_token(identity={"productos": result})

            return {"Resultado": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class guardarNuevaPuja(Resource):
    def post(self):
        try:
            print('Ingresando a la puja')
            idSubasta = request.json['idSubasta']
            idUsuario = request.json['idUsuario']
            precioPuja = request.json['precioPuja']
            fechaPuja = request.json['fechaPuja']
            puja = Pujas(idSubasta, idUsuario, precioPuja, fechaPuja)
            print('Intentado ingresar')
            puja.save()
            result="Completado"
            access_token = create_access_token(identity={"productos": result})
            return {"Estado de puja": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
