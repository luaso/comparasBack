from flask_restful import Api, Resource
from sqlalchemy import or_
#from app.UsuarioComun.schemas.crear_Lista_Subasta_schema import TaskSchema
from app.UsuarioComun.models.registro_Usuario_model import Rol, Usuarios, RolSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from app import ObjectNotFound
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


rolSchema = RolSchema()

class ObtenerRol(Resource):
    print('1111111111111111111111')
    def get(self):
        print('2222222222222222222222222')
        try:
            #rol = Rol.query.filter(or_(Rol.idRol==1, Rol.idRol==2))
            #rol = Rol.query.filter_by(Rol.idRol==1).first()
            rol = Rol.get_all()
        except:
            print('Error al buscar')
            #raise ObjectNotFound('error al buscar')
        print(rol)
        result = rolSchema.dump(rol, many=True)
        return {"productos": result}, 200
