from flask import Blueprint
from flask_restful import Api

from app.usuarioComprador.resources.lista_resources import listas, lista
from app.usuarioComprador.resources.ver_Subastas_resources import listasSubastasCreadas, detalleSubasta, seleccionarGanador


usuarioComprador = Blueprint('usuarioComprador', __name__)

api = Api(usuarioComprador)
api.add_resource(listas, '/api/listas/', endpoint='lists_resource')
api.add_resource(lista, '/api/lista/<int:idLista>', endpoint='product_list_resource')
#api.add_resource(subastasEjecucion, '/api/Subasta', endpoint='crearSubasta_resource')
#api.add_resource(buscarProductosSubastaEjecucion, '/api/SubastaProductos/<idSubasta>', endpoint='buscarProductosSubastaresource')
#api.add_resource(compararProductosSupermercados, '/api/ComparacionSupermercados/<idSubasta>', endpoint='ComparacionSupermercados')
