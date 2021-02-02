from flask_restful import Api, Resource
from app.usuarioBodeguero.models.ingresar_Subasta_model import Subastas,  Direcciones, Usuarios, Estado
from app.usuarioBodeguero.schemas.ingresar_Subasta_schema import TaskSchema
from app import ObjectNotFound
from flask_sqlalchemy import SQLAlchemy
from flask import request

#Librerias de calculo de distancias entre dos puntos mediante lat y long
#pip install geopy
from geopy.geocoders import ArcGIS
from geopy.distance import geodesic
#=======================================================================
from app.validateToken import check_for_token

db = SQLAlchemy()

task_schema = TaskSchema()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
class obtenerPosiblesSubastasBodeguero(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idUsuario = request.json['idUsuario']
            filtro = Subastas.get_subastas()
            #print(filtro)
            result = task_schema.dump(filtro, many=True)

            coordenadas = Subastas.get_direccion_usuario_2km(idUsuario,result)
            print("antes del for")
            print(coordenadas)

            #access_token = create_access_token(identity={"posibles_subastas": result})
            return {"Resultado": coordenadas}, 200
            #return "dato"
        except Exception as ex:
            raise ObjectNotFound(ex)
