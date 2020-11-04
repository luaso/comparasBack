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
    def get(self):
        try:
            idSubastaGet = request.json['idSubasta']
            filtro = Subastas.get_joins_filter_Detalle_Subasta(idSubastaGet)
            result = taskSchema.dump(filtro, many=True)
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
class seleccionarGanador(Resource):
    def put(self):
        try:
            idSubastaGet = request.json['idSubasta']
            CrearSubasta = Subastas.query.get(idSubastaGet)
            idUsuarioGanador = request.json['idUsuarioGanador']
            Subastas.idUsuarioGanador = idUsuarioGanador
            db.session.commit()
            return {"respuesta": 'Se guardo el ganador correctamente'}
        except Exception as ex:
            raise ObjectNotFound(ex)
