from flask import Blueprint
from flask_restful import Api

from app.administrador.resources.categorias_resource import Categoria, CategoriaList

Administrador = Blueprint('Administrador', __name__)




api = Api(Administrador)
api.add_resource(CategoriaList, '/api/administrador/', endpoint='categoria_list_resource')
api.add_resource(Categoria, '/api/administrador/<string:nombreCategoria>', endpoint='categoria_resource')