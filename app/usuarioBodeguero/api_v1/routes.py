from flask import Blueprint
from flask_restful import Api

from app.usuarioBodeguero.resources.aplicar_Subasta_resources import obtenerProductosSubasta, guardarPuja
from app.usuarioBodeguero.resources.detalle_Subasta_resources import detallePujasSubasta, obtenerMiOferta, guardarNuevaPuja
from app.usuarioBodeguero.resources.ingresar_Subasta_resources import obtenerPosiblesSubastasBodeguero
from app.usuarioBodeguero.resources.mis_Subastas_Lista_resources import misSubastasBodeguero


usuarioBodeguero = Blueprint('usuarioBodeguero', __name__)
api = Api(usuarioBodeguero)

api.add_resource(obtenerProductosSubasta, '/api/obtenerProductosSubasta/', endpoint='obtenerProductosSubasta')
api.add_resource(guardarPuja, '/api/guardarPuja/', endpoint='guardarPuja')
api.add_resource(detallePujasSubasta, '/api/detallePujasSubasta/', endpoint='detallePujasSubasta')
api.add_resource(obtenerMiOferta, '/api/obtenerMiOferta/', endpoint='obtenerMiOferta')
api.add_resource(obtenerPosiblesSubastasBodeguero, '/api/obtenerPosiblesSubastasBodeguero/', endpoint='obtenerPosiblesSubastasBodeguero')
api.add_resource(misSubastasBodeguero, '/api/misSubastasBodeguero/<int:idUsuario>', endpoint='misSubastasBodeguero')
api.add_resource(guardarNuevaPuja, '/api/guardarNuevaPuja/', endpoint='guardarNuevaPuja')