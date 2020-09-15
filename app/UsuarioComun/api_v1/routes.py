from flask import Blueprint
from flask_restful import Api

from app.UsuarioComun.resources.productos_Buscar_Listar_resources import ProductoList, Producto, ProductosBuscados



UsuarioComun = Blueprint('UsuarioComun', __name__)




api = Api(UsuarioComun)
api.add_resource(ProductoList, '/api/producto/', endpoint='producto_list_resource')
api.add_resource(Producto, '/api/producto/<string:nombreProducto>', endpoint='producto_resource')
api.add_resource(ProductosBuscados, '/api/ProductosBuscados/<int:idSubasta>', endpoint='productoBuscados_resource')
