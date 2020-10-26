from flask import Blueprint
from flask_restful import Api

from app.UsuarioBodeguero.resources.aplicar_Subasta_resources import obtenerProductosSubasta, guardarPuja


UsuarioBodeguero = Blueprint('UsuarioBodeguero', __name__)
api = Api(UsuarioBodeguero)

api.add_resource(obtenerProductosSubasta, '/api/obtenerProductosSubasta/', endpoint='obtenerProductosSubasta')
api.add_resource(guardarPuja, '/api/guardarPuja/', endpoint='guardarPuja')
