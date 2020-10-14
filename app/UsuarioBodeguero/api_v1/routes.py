from flask import Blueprint
from flask_restful import Api

from app.UsuarioBodeguero.resources.subasta_ListarPorUsuario_resources import SubastaListarPorUsuario
from app.UsuarioBodeguero.resources.tiempoEstimado_Listar_resource import TiempoEstimadoSubasta

UsuarioBodeguero = Blueprint('UsuarioBodeguero', __name__)
api = Api(UsuarioBodeguero)

api.add_resource(SubastaListarPorUsuario, '/api/ListaSubastaPorUsuario/', endpoint='SubastaListarPorUsuario')
api.add_resource(TiempoEstimadoSubasta, '/api/ListarTiempoEstimado/', endpoint='TiempoEstimadoSubasta')