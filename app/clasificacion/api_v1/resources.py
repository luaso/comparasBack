from flask import request, Blueprint
from flask_restful import Api, Resource

from .schemas import ClasificacionSchema
from ..models import Clasificacion

clasificacion_v1 = Blueprint('clasificacion_v1', __name__)


class ClasificacionListResource(Resource):
    def get(self):
        clasificaciones = Clasificacion.get_all()
        print(clasificaciones)
        result = clasificacion_schema.dump(clasificaciones, many=True)
        return result


clasificacion_schema = ClasificacionSchema()

api = Api(clasificacion_v1)
api.add_resource(ClasificacionListResource, '/api/v1.0/clasificacion/', endpoint='clasificacion_list_resource')