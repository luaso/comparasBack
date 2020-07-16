from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import ClasificacionSchema
from ..models import Clasificacion
from app import ObjectNotFound


clasificacion_v1 = Blueprint('clasificacion_v1', __name__)
clasificacion_schema = ClasificacionSchema()

class ClasificacionListResource(Resource):
    def get(self):
        clasificaciones = Clasificacion.get_all()
        print(clasificaciones)
        result = clasificacion_schema.dump(clasificaciones, many=True)
        return result

    def post(self):
        data = request.get_json()
        print(data)
        clasificacion_dict = clasificacion_schema.load(data)
        print(clasificacion_dict)
        clasificacion = Clasificacion(nombreclasificacion = clasificacion_dict['nombreclasificacion'])
        print(clasificacion)
        clasificacion.save()
        result = clasificacion_schema.dump(clasificacion)
        return result, 201


class ClasificacionById(Resource):
    def get(self, clasificacion_id):
        print("entro a clase by id")
        clasificacion = Clasificacion.get_by_id(clasificacion_id)
        print(clasificacion)
        if clasificacion is None:
            raise ObjectNotFound('La clasificacion no existe')
        result = clasificacion_schema.dump(clasificacion)
        return result
    #def put(self):
    #def delete(self):



clasificacion_schema = ClasificacionSchema()

api = Api(clasificacion_v1)
api.add_resource(ClasificacionListResource, '/api/v1.0/clasificacion/', endpoint='clasificacion_list_resource')
api.add_resource(ClasificacionById, '/api/v1.0/clasificacion/<int:clasificacion_id>', endpoint='clasificacion_resource')