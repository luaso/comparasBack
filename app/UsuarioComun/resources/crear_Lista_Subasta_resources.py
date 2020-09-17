from flask import request
from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioComun.schemas.crear_Lista_Subasta_schema import TaskSchema
from app.UsuarioComun.models.crear_Lista_Subasta_model import Subastas
from app import ObjectNotFound

taskSchema = TaskSchema()
class Subastas(Resource):
    def post():
        #data = request.get_json()
        #print(' data ================================')
        #print(data)

        #try:
        #    subasta_dict = taskSchema.load(data)
        #except Exception as ex:
        #    raise ObjectNotFound(ex)
        #print(' subasta_dict ================================')
        #print(subasta_dict)

        #idUsuario = request.json['idUsuario']
        #idEstado = request.json['idEstado']
        #tiempoInicial = request.json['tiempoInicial']
        #nombreSubasta = request.json['nombreSubasta']
        #precioIdeal = request.json['precioIdeal']
        #fechaSubasta = request.json['fechaSubasta']

        new_task = Subastas(idUsuario=1, idEstado=1, tiempoInicial='2020-02-10', nombreSubasta='dato de prueba 13:51', precioIdeal=0.0, fechaSubasta='dato de prueba 13:51')
        #print(new_task)
        db.session.add(new_task)
        db.session.commit()

        #try:
        #    subastas.save()
        #except:
        #    raise ObjectNotFound('error al agregar a la BD')
        #result = taskSchema.dump(subastas)
        #return {"supermercado": result}, 201