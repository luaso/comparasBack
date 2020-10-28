from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioBodeguero.models.ingresar_Subasta_model import Subastas,  Direcciones, Usuarios, Estado
from app.UsuarioBodeguero.schemas.ingresar_Subasta_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()

task_schema = TaskSchema()

class obtenerPosiblesSubastasBodeguero(Resource):
    def get(self):
        try:

            filtro = Subastas.get_join_filter()

            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)