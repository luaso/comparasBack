from flask import Blueprint
from flask_restful import Api

from .resources.categorias_resource import CategoriaList, Categoria


categoria_v1 = Blueprint('categoria_v1', __name__)



api = Api(categoria_v1)
api.add_resource(CategoriaList, '/api/administrador/', endpoint='categoria_list_resource')
api.add_resource(Categoria, '/api/administrador/<string:nombreCategoria>', endpoint='categoria_resource')