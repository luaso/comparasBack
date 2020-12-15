from flask import jsonify, request
from functools import wraps
import jwt


def check_for_token(token_ur):


    if not token_ur:
        rept = rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}
    try:
        data = jwt.decode(token_ur, 'DeveloperComparajrl')
        rept = {'user': data.get("user"), 'exp': data.get("exp"), 'message': data.get("message"), 'status': data.get("status")}
    except:
        rept = {'user': 'invalid', 'exp': '0', 'message': 'Token CadUcado ó invalido', 'status': '403'}

    return   rept

