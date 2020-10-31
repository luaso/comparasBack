from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.productos_model import  Productos, Tipos_Productos, Sub_Categorias, Categorias
from app.administrador.schemas.productos_schema import TaskSchema, TaskSchema2
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import cv2
db = SQLAlchemy()

task_schema = TaskSchema()
task_schema2= TaskSchema2()
class obtenerProductosTotal(Resource):
    def get(self):
        try:
            filtro =  Productos.get_joins()
            result = task_schema.dump(filtro, many=True)
            return {"producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerTipoProduto(Resource):
    def get(self):
        try:
            filtro =  Tipos_Productos.get_joins()
            result = task_schema2.dump(filtro, many=True)
            return {"Tipos de pruductos": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarproductoNuevo(Resource):
    def post(self):
        try:

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