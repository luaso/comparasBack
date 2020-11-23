from flask import Blueprint
from flask_restful import Api

from app.administrador.resources.categorias_resource import Categoria, CategoriaList
from app.administrador.resources.supermercados_resources import Supermercado, SupermercadoList, SupermercadoBuscar
from app.administrador.resources.productos_resources import obtenerProductosTotal, obtenerTipoProduto, guardarproductoNuevo,\
    mostrarProductoSeleccionado,mostrarParametros, editarProducto, eliminarProducto
from app.administrador.resources.parametros_resources import guardarParametro, obtenerParametro, mostrarParametrosTotal, editarParametro, eliminarParametro
from app.administrador.resources.productos_supermercados_resources import obtenerProductosSupermercado
from app.administrador.resources.tipos_productos_resources import obtenerTiposProductos, guardarTiposProductos, obtenerSubCategorias
administrador = Blueprint('administrador', __name__)




api = Api(administrador)
api.add_resource(CategoriaList, '/api/categoria/', endpoint='categoria_list_resource')
api.add_resource(Categoria, '/api/categoria/<int:idCategoria>', endpoint='categoria_resource')
api.add_resource(SupermercadoList, '/api/supermercado/', endpoint='supermercado_list_resource')
api.add_resource(Supermercado, '/api/supermercado/<int:idSupermercado>', endpoint='supermercado_resource')
api.add_resource(obtenerProductosTotal, '/api/obtenerProductosTotal/', endpoint='obtenerProductosTotal')
api.add_resource(obtenerTipoProduto, '/api/obtenerTipoProduto/', endpoint='obtenerTipoProduto')
api.add_resource(guardarproductoNuevo, '/api/guardarproductoNuevo/', endpoint='guardarproductoNuevo')
api.add_resource(mostrarProductoSeleccionado, '/api/mostrarProductoSeleccionado/', endpoint='mostrarProductoSeleccionado')
api.add_resource(mostrarParametros, '/api/mostrarParametros/', endpoint='mostrarParametros')
api.add_resource(editarProducto, '/api/editarProducto/', endpoint='editarProducto')
api.add_resource(eliminarProducto, '/api/eliminarProducto/', endpoint='eliminarProducto')
api.add_resource(obtenerParametro, '/api/obtenerParametro/', endpoint='obtenerParametro')
api.add_resource(guardarParametro, '/api/guardarParametro/', endpoint='guardarParametro')
api.add_resource(obtenerProductosSupermercado, '/api/obtenerProductosSupermercado/', endpoint='obtenerProductosSupermercado')
api.add_resource(mostrarParametrosTotal, '/api/mostrarParametrosTotal/', endpoint='mostrarParametrosTotal')
api.add_resource(SupermercadoBuscar, '/api/SupermercadoBuscar/<string:nombreSupermercado>', endpoint='SupermercadoBuscar')
api.add_resource(obtenerTiposProductos, '/api/obtenerTiposProductos/', endpoint='obtenerTiposProductos')
api.add_resource(guardarTiposProductos, '/api/guardarTiposProductos/', endpoint='guardarTiposProductos')
api.add_resource(obtenerSubCategorias, '/api/obtenerSubCategorias/', endpoint='obtenerSubCategorias')
api.add_resource(editarParametro, '/api/editarParametro/', endpoint='editarParametro')
api.add_resource(eliminarParametro, '/api/eliminarParametro/', endpoint='eliminarParametro')

