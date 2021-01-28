from flask import Blueprint
from flask_restful import Api

from app.inicioSesion.resources.mantenimiento_Usuario_resources import obtenerRol,guardarUsuario,buscarUsuario,editarUsuarioComprador,editarUsuarioBodeguero
from app.inicioSesion.resources.sesion_Usuario_resources import loginUsuario


inicioSesion = Blueprint('inicioSesion', __name__)


api = Api(inicioSesion)

api.add_resource(obtenerRol, '/api/ObtenerRol/', endpoint='ObtenerRol')
api.add_resource(guardarUsuario, '/api/GuardarUsuario/', endpoint='GuardarUsuario')
api.add_resource(buscarUsuario, '/api/BuscarUsuario/<int:idUsuario>', endpoint='buscarUsuario')
api.add_resource(editarUsuarioComprador, '/api/EditarUsuarioComprador/', endpoint='editarUsuarioComprador')
api.add_resource(editarUsuarioBodeguero, '/api/EditarUsuarioBodeguero/', endpoint='editarUsuarioBodeguero')
api.add_resource(loginUsuario, '/api/LoginUsuario/', endpoint='LoginUsuario')