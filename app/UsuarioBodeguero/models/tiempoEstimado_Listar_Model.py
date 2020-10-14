from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)




class Tiempo_Estimado_Subasta(db.Model):
    __tablename__= "TIPO_TIEMPO"
    idTipoTiempo = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.TEXT)
    Estado = db.Column(db.Integer)

    def __init__(self, idTipoTiempo, Descripcion, Estado):
        self.idTipoTiempo = idTipoTiempo
        self.Descripcion = Descripcion
        self.Estado = Estado
