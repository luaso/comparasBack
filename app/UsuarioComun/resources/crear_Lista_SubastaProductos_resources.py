from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioComun.models.crear_Lista_SubastaProductos_model import Supermercados, Subastas,Productos,Productos_Supermercados,Subastas_Productos
from app.UsuarioComun.schemas.crear_Lista_SubastaProductos_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func
import json


db = SQLAlchemy()
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

task_schema = TaskSchema()

class buscarProductosSubastaEjecucion(Resource):
    def get(self, idSubasta):
        try:
            filtro = Subastas_Productos.get_joins_filter(idSubasta)

            for subastas_Productos, productos in filtro:
                print(productos.idProducto, productos.nombreProducto, subastas_Productos.idSubasta)
            resultado = task_schema.dump(filtro, many=True)
            #print(resultado)
        except Exception as ex:
            raise ObjectNotFound(ex)
        return {"productos": resultado}, 200

class compararProductosSupermercados(Resource):
    def get(self, idSubasta):
        try:
            filtro = Subastas_Productos.get_joins_filter_supermercados(idSubasta)
            #print(filtro)
        except Exception as ex:
            raise ObjectNotFound(ex)

        resultado = task_schema.dump(filtro, many=True)
        # print(resultado)
        return {"productos": resultado}, 200