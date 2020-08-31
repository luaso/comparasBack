from flask import Blueprint
from flask_restful import Api

from app.administrador.resources.categorias_resource import Categoria, CategoriaList
from app.administrador.resources.supermercados_resources import Supermercado, SupermercadoList


Administrador = Blueprint('Administrador', __name__)




api = Api(Administrador)
api.add_resource(CategoriaList, '/api/categoria/', endpoint='categoria_list_resource')
api.add_resource(Categoria, '/api/categoria/<int:idCategoria>', endpoint='categoria_resource')
api.add_resource(SupermercadoList, '/api/supermercado/', endpoint='supermercado_list_resource')
api.add_resource(Supermercado, '/api/supermercado/<int:idSupermercado>', endpoint='supermercado_resource')
