from flask_restful import Api, Resource
from sqlalchemy import or_
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func
import json

from app.UsuarioBodeguero.models.tiempoEstimado_Listar_Model import Tiempo_Estimado_Subasta
from app.UsuarioBodeguero.schemas.tiempoEstimado_Listar_schema import TiempoEstimadoSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
tiempoEstimado_schema=TiempoEstimadoSchema()

class TiempoEstimadoSubasta(Resource):
    def get(self):
        filtro = db.session.query(Tiempo_Estimado_Subasta). \
            filter().all()
        print(filtro)

        resultado = tiempoEstimado_schema.dump(filtro, many=True)
        return {"TiempoEstimado": resultado}, 200