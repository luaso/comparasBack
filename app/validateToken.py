from flask import jsonify, request
from functools import wraps
from app.inicioSesion.models.mantenimiento_Usuario_model import Usuarios
from app.inicioSesion.schemas.mantenimiento_Usuario_schema import RolSchemaToken, UserSchemaToken
import jwt
from config.configuration import DevelopmentConfig
#from config.configuration import ProductionConfig          #Configuracion para produccion

rolSchemaToken = RolSchemaToken()
userSchemaToken = UserSchemaToken()

secret_Key = DevelopmentConfig.SECRET_KEY
#secret_Key = ProductionConfig.SECRET_KEY                   #Configuracion para produccion


def check_for_token(token_ur):

    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)
        rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status")}
    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}

    return rept


def check_for_token_id_rol(token_ur,id,rolUser):
    '''Funcion que valida si el token es correcto; si el id y el token pertenecen al mismo usuario; tambien si el rol puesto concuerda con los anteriores parametros '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    if not id:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda con el ID', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_rol(id)
        resultado = rolSchemaToken.dump(userRol, many=True)

        if (resultado[0]["Rol.idRol"] != rolUser):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'El usuario no puede realizar esta accion', 'status': '403'}
        elif (data.get("user") != resultado[0]["Usuarios.email"]):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'no concuerda el id con el usuario del token', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status"), 'rol': resultado[0]["Rol.idRol"], 'idUser':1}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept

def check_for_token_rol(token_ur):
    '''Funcion que valida si el token es correcto y devuelve el di y rol del usuario del token '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}

    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_email_token(data.get("user"))
        resultado = rolSchemaToken.dump(userRol)
        print(resultado)
        if (resultado["Rol.idRol"] != 3):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'El usuario no puede realizar esta accion', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status"), 'rol': resultado["Rol.idRol"]}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept


def check_for_token_id(token_ur,idUser):
    '''Funcion que valida si el token es correcto; tambien si el idUser pertenece al mismo usaurio que el del token '''
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    if not idUser:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda con el ID', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)

        userRol = Usuarios.get_query(idUser)

        emailUser = userRol.email

        if (data.get("user") != emailUser):
            rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda el id con el usuario del token', 'status': '403'}
        else:
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status")}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token Caducado ó invalido', 'status': '403'}
    return   rept