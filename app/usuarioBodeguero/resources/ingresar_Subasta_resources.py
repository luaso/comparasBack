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

db = SQLAlchemy()

task_schema = TaskSchema()

class obtenerPosiblesSubastasBodeguero(Resource):
    def get(self):
        try:
            idUsuario = request.json['idUsuario']
            try:
                filtro = Direcciones.get(idUsuario)

                for data in filtro:

                    usuarioBodegueroCoor = ((data.latitud, data.longitud))

            except Exception as ex:
                raise ObjectNotFound(ex)

            try:

                for data in filtro:

                    usuarioCompradorCoor = ((data.latitud, data.longitud))



            except Exception as ex:
                raise ObjectNotFound(ex)

            distancia = str(geodesic(usuarioBodegueroCoor, usuarioCompradorCoor).km)

            print("Distancia entre ny y tokyo:" + distancia + " km")



            filtro = Subastas.get_join_filter()
            #print(filtro)
            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
