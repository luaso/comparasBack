from flask import Blueprint
from flask_restful import Api

from app.usuarioComun.resources.productos_Buscar_Listar_resources import ProductoList, Producto
from app.usuarioComun.resources.crear_Lista_Subasta_resources import subastasEjecucion
from app.usuarioComun.resources.crear_Lista_SubastaProductos_resources import buscarProductosSubastaEjecucion, compararProductosSupermercados

usuarioComun = Blueprint('usuarioComun', __name__)

api = Api(usuarioComun)
api.add_resource(ProductoList, '/api/producto/', endpoint='producto_list_resource')
api.add_resource(Producto, '/api/producto/<string:nombreProducto>', endpoint='producto_resource')
api.add_resource(subastasEjecucion, '/api/Subasta', endpoint='crearSubasta_resource')
api.add_resource(buscarProductosSubastaEjecucion, '/api/SubastaProductos/<idSubasta>', endpoint='buscarProductosSubastaresource')
api.add_resource(compararProductosSupermercados, '/api/ComparacionSupermercados/<idSubasta>', endpoint='ComparacionSupermercados')
