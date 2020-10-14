from flask import Blueprint
from flask_restful import Api

from app.InicioSesion.resources.registro_Usuario_resources import obtenerRol,guardarUsuario,buscarUsuario,editarUsuarioComprador,loginUsuario

InicioSesion = Blueprint('InicioSesion', __name__)


api = Api(InicioSesion)

api.add_resource(obtenerRol, '/api/ObtenerRol/', endpoint='ObtenerRol')
api.add_resource(guardarUsuario, '/api/GuardarUsuario/', endpoint='GuardarUsuario')
api.add_resource(buscarUsuario, '/api/BuscarUsuario/<int:idUsuario>', endpoint='buscarUsuario')
api.add_resource(editarUsuarioComprador, '/api/EditarUsuarioComprador/', endpoint='editarUsuarioComprador')
api.add_resource(loginUsuario, '/api/LoginUsuario/', endpoint='LoginUsuario')