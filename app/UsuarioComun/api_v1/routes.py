from flask import Blueprint
from flask_restful import Api

from app.UsuarioComun.resources.productos_Buscar_Listar_resources import ProductoList, Producto, ProductosBuscados
from app.UsuarioComun.resources.crear_Lista_Subasta_resources import subastasEjecucion
from app.UsuarioComun.resources.crear_Lista_SubastaProductos_resources import buscarProductosSubastaEjecucion, compararProductosSupermercados
#from app.UsuarioComun.resources.registro_Usuario_resources import obtenerRol, guardarUsuario, buscarUsuario, editarUsuarioComprador,loginUsuario



UsuarioComun = Blueprint('UsuarioComun', __name__)




api = Api(UsuarioComun)
api.add_resource(ProductoList, '/api/producto/', endpoint='producto_list_resource')
api.add_resource(Producto, '/api/producto/<string:nombreProducto>', endpoint='producto_resource')
api.add_resource(ProductosBuscados, '/api/ProductosBuscados/<int:idSubasta>', endpoint='productoBuscados_resource')
api.add_resource(subastasEjecucion, '/api/Subasta', endpoint='crearSubasta_resource')
api.add_resource(buscarProductosSubastaEjecucion, '/api/SubastaProductos/<idSubasta>', endpoint='buscarProductosSubastaresource')
api.add_resource(compararProductosSupermercados, '/api/ComparacionSupermercados/<idSubasta>', endpoint='ComparacionSupermercados')
#api.add_resource(obtenerRol, '/api/ObtenerRol/', endpoint='ObtenerRol')
#api.add_resource(guardarUsuario, '/api/GuardarUsuario/', endpoint='GuardarUsuario')
#api.add_resource(buscarUsuario, '/api/BuscarUsuario/<int:idUsuario>', endpoint='buscarUsuario')
#api.add_resource(editarUsuarioComprador, '/api/EditarUsuarioComprador/', endpoint='editarUsuarioComprador')
#api.add_resource(loginUsuario, '/api/LoginUsuario/', endpoint='LoginUsuario')