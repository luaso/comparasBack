from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.parametros_model import  Parametros
from app.administrador.schemas.parametros_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

task_schema = TaskSchema()


class obtenerParametro(Resource):
    def get(self):
        try:
            idParametros = request.json['idParametros']
            filtro =  Parametros.get(idParametros)
            result = task_schema.dump(filtro, many=True)
            return {"Parametro": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarParametro(Resource):
    def post(self):
        parametros = request.get_json()
        for datos in parametros['Parametro']:

            try:
                Descripcion = datos['Descripcion']
                Estado = datos['Estado']
                FecCrea = date.today()
                FecModifica = date.today()
                UsuCrea = datos['UsuCrea']
                UsuModifica = datos['UsuModifica']
                Valor = datos['Valor']
                try:
                    parametros = Parametros(Descripcion,Estado,FecCrea,FecModifica,UsuCrea,UsuModifica,Valor)
                    parametros.save()

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'Parámetro guardaro', 200
            except Exception as ex:
                raise ObjectNotFound(ex)
class editarParametro(Resource):
    def put(self):
        parametros = request.get_json()
        for datos in parametros['Parametro']:

            try:
                idParametros = datos['idParametros']
                Descripcion = datos['Descripcion']
                Estado = datos['Estado']

                FecModifica = date.today()
                UsuCrea = datos['UsuCrea']
                UsuModifica = datos['UsuModifica']
                Valor = datos['Valor']

                parametroEditar = Parametros.get_query(idParametros)
                parametroEditar.Descripcion = Descripcion
                parametroEditar.Estado = Estado

                parametroEditar.FecModifica = FecModifica
                parametroEditar.UsuCrea = UsuCrea
                parametroEditar.UsuModifica = UsuModifica
                parametroEditar.Valor = Valor

                try:
                    parametroEditar.save_to_db()

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'Parámetro guardaro', 200
            except Exception as ex:
                raise ObjectNotFound(ex)


class eliminarParametro(Resource):
    def delete(self):
        try:
            idParametros = request.json['idParametros']
            parametro = Parametros.get_query(idParametros)
            parametro.delete_parametro()
            return "Parámetro eliminado"
        except Exception as ex:
            raise ObjectNotFound(ex)


class mostrarParametrosTotal(Resource):
    def get(self):
        try:

            filtro =  Parametros.get_all()
            result = task_schema.dump(filtro, many=True)
            return {"Parametro": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)