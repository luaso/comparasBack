from flask import Blueprint
from flask_restful import Api

from app.usuarioComprador.resources.lista_resources import listas, lista
from app.usuarioComprador.resources.crear_Subasta_resources import listasUsuario, direccionSubasta, crearSubastaLista
from app.usuarioComprador.resources.ver_Subastas_resources import listasSubastasCreadas, detalleSubasta, seleccionarGanador


usuarioComprador = Blueprint('usuarioComprador', __name__)

api = Api(usuarioComprador)
api.add_resource(listas, '/api/listas/', endpoint='lists_resource')
api.add_resource(lista, '/api/lista/<int:idLista>', endpoint='product_list_resource')
api.add_resource(listasUsuario, '/api/listasUsuario/', endpoint='listasUsuario')
api.add_resource(direccionSubasta, '/api/direccionSubasta/', endpoint='direccionSubasta')
api.add_resource(crearSubastaLista, '/api/crearSubastaLista/', endpoint='crearSubastaLista')
