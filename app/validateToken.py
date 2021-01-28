from flask import jsonify, request
from functools import wraps
from app.inicioSesion.models.mantenimiento_Usuario_model import Rol, Usuarios
from app.inicioSesion.schemas.mantenimiento_Usuario_schema import RolSchemaToken
import jwt

rolSchemaToken = RolSchemaToken()


secret_Key = "DeveloperComparajrl"

def check_for_token(token_ur):


    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)
        rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status")}
    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}

    return   rept


def check_for_token_id(token_ur,id):
    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}
    if not id:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token no concuerda con el ID', 'status': '403'}
    try:
        data = jwt.decode(token_ur, secret_Key)
        print(data.get("user"))
        print(data.get("user"))
        userRol = Usuarios.get_rol(id)
        print("Rol")
        print(userRol)
        resultado = rolSchemaToken.dump(userRol, many=True)
        print("Resultado")
        if(data.get("user") == resultado[0]["Usuarios.email"]):
            rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"),'status': data.get("status"), 'rol': resultado[0]["Rol.idRol"]}
        else:
            rept = {'user': 'invalid', 'exp': '0', 'message': 'no concuerda el id con el usuario del token', 'status': '403'}

    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}
    return   rept