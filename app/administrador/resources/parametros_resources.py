from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.parametros_model import  Parametros
from app.administrador.schemas.parametros_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from datetime import date
from flask_sqlalchemy import SQLAlchemy

from app.validateToken import check_for_token

db = SQLAlchemy()

task_schema = TaskSchema()


class obtenerParametro(Resource):
    def get(self, idParametro):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            filtro =  Parametros.get(idParametro)
            result = task_schema.dump(filtro, many=True)
            return {"Parametro": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarParametro(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()
        parametros = res['Parametro']

        try:
            Descripcion = parametros['Descripcion']
            Estado = parametros['Estado']
            FecCrea = date.today()
            FecModifica = date.today()
            UsuCrea = parametros['UsuCrea']
            UsuModifica = parametros['UsuModifica']
            Valor = parametros['Valor']

            parametros = Parametros(Descripcion,Estado,FecCrea,FecModifica,UsuCrea,UsuModifica,Valor)
            parametros.save()


            return 'Parámetro guardaro', 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class editarParametro(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()
        parametros = res['Parametro']

        try:
            idParametros = parametros['idParametro']
            Descripcion = parametros['Descripcion']
            Estado = parametros['Estado']
            FecModifica = date.today()
            UsuModifica = parametros['UsuModifica']
            Valor = parametros['Valor']

            parametroEditar = Parametros.get_query(idParametros)

            if parametroEditar is None:
                raise ObjectNotFound('El id del parametro no existe')

            parametroEditar.Descripcion = Descripcion
            parametroEditar.Estado = Estado
            parametroEditar.FecModifica = FecModifica
            parametroEditar.UsuModifica = UsuModifica
            parametroEditar.Valor = Valor

            parametroEditar.save_to_db()

            return 'Parámetro editado correctamente', 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class eliminarParametro(Resource):
    def delete(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idParametros = request.json['idParametros']
            parametro = Parametros.get_query(idParametros)
            parametro.delete_parametro()
            return "Parámetro eliminado"
        except Exception as ex:
            raise ObjectNotFound(ex)


class mostrarParametrosTotal(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            filtro =  Parametros.get_all()
            result = task_schema.dump(filtro, many=True)
            return {"Parametro": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)