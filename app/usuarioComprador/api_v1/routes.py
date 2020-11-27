from flask import Blueprint
from flask_restful import Api

from app.usuarioComprador.resources.lista_resources import listas, lista
from app.usuarioComprador.resources.crear_Subasta_resources import listasUsuario, direccionSubasta, crearSubastaLista, buscarProductosCrearSubasta, crearListaComprador
from app.usuarioComprador.resources.ver_Subastas_resources import listasSubastasCreadas, detalleSubasta, seleccionarGanador, productosSubastaComprador
from app.usuarioComprador.resources.mis_Subastas_resources import misSubastasComprador



usuarioComprador = Blueprint('usuarioComprador', __name__)

api = Api(usuarioComprador)
api.add_resource(listas, '/api/listas/', endpoint='lists_resource')
api.add_resource(lista, '/api/lista/<int:idLista>', endpoint='product_list_resource')
api.add_resource(listasUsuario, '/api/listasUsuario/<int:idUsuario>', endpoint='listasUsuario')
api.add_resource(direccionSubasta, '/api/direccionSubasta/<string:idUsuario>', endpoint='direccionSubasta')
api.add_resource(crearSubastaLista, '/api/crearSubastaLista/', endpoint='crearSubastaLista')
api.add_resource(buscarProductosCrearSubasta, '/api/buscarProductosCrearSubasta/<string:nombreProducto>', endpoint='buscarProductosCrearSubasta')
api.add_resource(crearListaComprador, '/api/crearListaComprador/', endpoint='crearListaComprador')
api.add_resource(misSubastasComprador, '/api/misSubastasComprador/<int:idUsuario>', endpoint='misSubastasComprador')
api.add_resource(detalleSubasta, '/api/detalleSubasta/<int:idSubasta>', endpoint='detalleSubasta')
api.add_resource(seleccionarGanador, '/api/seleccionarGanador/', endpoint='seleccionarGanador')
api.add_resource(productosSubastaComprador, '/api/productosSubastaComprador/', endpoint='productosSubastaComprador')
