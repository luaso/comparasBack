from flask import Blueprint
from flask_restful import Api

from app.usuarioComprador.resources.crear_Subasta_resources import listasUsuario, direccionSubasta, buscarProductos, crearSubasta
from app.usuarioComprador.resources.ver_Subastas_resources import listasSubastasCreadas, detalleSubasta, seleccionarGanador


usuarioComprador = Blueprint('usuarioComprador', __name__)

api = Api(UsuarioComun)
api.add_resource(ProductoList, '/api/producto/', endpoint='producto_list_resource')
api.add_resource(Producto, '/api/producto/<string:nombreProducto>', endpoint='producto_resource')
api.add_resource(subastasEjecucion, '/api/Subasta', endpoint='crearSubasta_resource')
api.add_resource(buscarProductosSubastaEjecucion, '/api/SubastaProductos/<idSubasta>', endpoint='buscarProductosSubastaresource')
api.add_resource(compararProductosSupermercados, '/api/ComparacionSupermercados/<idSubasta>', endpoint='ComparacionSupermercados')
