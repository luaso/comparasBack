from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.models.crear_Subasta_model import Subastas, Usuarios,  Productos, Direcciones
from app import ObjectNotFound
import datetime
taskSchema = TaskSchema()

class listasUsuario(Resource):
    def get(self):
        try:
            idUsuario = request.json['idUsuario']
            idEstado = 1

            filtro = Subastas.get_joins_filter_ubastas_usuarios(idUsuario, idEstado)
            result = taskSchema.dump(filtro, many=True)
            return {"Subastas": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class direccionSubasta(Resource):
    def get(self):
        try:
            idUsuarioGet = request.json['idUsuario']
            filtro = Direcciones.get_direcciones(idUsuarioGet)
            result = taskSchema.dump(filtro, many=True)
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarProductos(Resource):
    def get(self, nombreProducto):
        try:
            filtro = Productos.get_filter_buscar_Productos(nombreProducto)
            result = taskSchema.dump(filtro, many=True)
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class crearSubastaLista(Resource):
    def put(self):
        try:
            idSubasta = request.json['idSubasta']
            CrearSubasta = Subastas.query.get(idSubasta)
            print(CrearSubasta)
            fechaSubasta = request.json['Fecha'] + ' ' + request.json['Hora']
            #fechaSubasta = datetime.datetime.now()
            print(fechaSubasta)
            idDireccion = request.json['idDireccion']

            CrearSubasta.fechaSubasta = fechaSubasta
            CrearSubasta.idDireccion = idDireccion
            CrearSubasta.save_to_db()
        except Exception as ex:
            raise ObjectNotFound(ex)

        return {"Respuesta": 'Se creo la subasta correctamente'}
