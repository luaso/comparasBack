from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioBodeguero.models.detalle_Subasta_model import Subastas, Productos, Subastas_Productos, Pujas
from app.UsuarioBodeguero.schemas.detalle_Subasta_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()

task_schema = TaskSchema()

class detallePujasSubasta(Resource):
    def get(self):
        try:
            idSubasta = request.json['idSubasta']

            filtro = Subastas.get_joins(idSubasta)

            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerMiOferta(Resource):
    def get(self):
        try:
            idSubastaGet = request.json['idSubasta']
            idUsuarioGet = request.json['idUsuario']

            filtro = Pujas.get_filter_or(idSubastaGet,idUsuarioGet)

            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
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
            return {"Estado de puja": "Completado"}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
