from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioBodeguero.models.aplicar_Subasta_model import Subastas, Productos, Subastas_Productos, Pujas
from app.usuarioBodeguero.schemas.aplicar_Subasta_schema import TaskSchema
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

class obtenerProductosSubasta(Resource):
    def get(self):
        try:
            chek_token = check_for_token(request.headers.get('token'))
            valid_token = chek_token['message']
            if valid_token != 'ok':
                return chek_token
            print('Intentado ingreso')
            idSubasta = request.json['idSubasta']
            filtro =  Subastas.get_joins(idSubasta)
            result = task_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"productos": result})
            return {"producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)
class guardarPuja(Resource):
     def post(self):
         chek_token = check_for_token(request.headers.get('token'))
         valid_token = chek_token['message']
         if valid_token != 'ok':
             return chek_token
         try:

            print('Ingresando a la puja')
            idSubasta = request.json['idSubasta']
            idUsuario = request.json['idUsuario']
            precioPuja = request.json['precioPuja']
            fechaPuja = request.json['fechaPuja']
            print(fechaPuja)
            puja = Pujas(idSubasta, idUsuario, precioPuja, fechaPuja)
            print('Intentado ingresar')
            puja.save()
            result="completado"
            #access_token = create_access_token(identity={"productos": result})
            return {"Estado de puja": result}, 200
         except Exception as ex:
            raise ObjectNotFound(ex)
