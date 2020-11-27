from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.ver_Subastas_schema import TaskSchema
from app.usuarioComprador.models.ver_Subastas_model import Subastas, Usuarios, Estado
from app import ObjectNotFound


taskSchema = TaskSchema()
class listasSubastasCreadas(Resource):
    def get(self):
        try:
            idUsuarioGet = request.json['idUsuario']
            filtro = Subastas.get_joins_filter_Subastas_Creadas(idUsuarioGet)
            result = taskSchema.dump(filtro, many=True)
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class detalleSubasta(Resource):
    def get(self, idSubasta):
        try:
            #idSubastaGet = request.json['idSubasta']
            filtro = Subastas.get_joins_filter_Detalle_Subasta(idSubasta)
            result = taskSchema.dump(filtro, many=True)
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
class seleccionarGanador(Resource):
    def put(self):
        try:
            idSubastaGet = request.json['idSubasta']
            idUsuarioGanador = request.json['idUsuarioGanador']
            ganador = Subastas.query.get(idSubastaGet)
            ganador.idUsuarioGanador = idUsuarioGanador
            ganador.save_to_db()
            return {"respuesta": 'Se guardo el ganador correctamente'}
        except Exception as ex:
            raise ObjectNotFound(ex)
class productosSubastaComprador(Resource):
    def get(self, idSubasta):
        try:
            #idSubastaGet = request.json['idSubasta']
            filtro = Subastas.get_productos_subasta(idSubasta)
            result = taskSchema.dump(filtro, many=True)
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
