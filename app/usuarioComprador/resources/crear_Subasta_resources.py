from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.models.ver_Subastas_model import Subastas, Usuarios,  Productos
from app import ObjectNotFound

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
            filtro = Usuarios.get_joins_filter_obtener_direcciones(idUsuarioGet)
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

class crearSubasta(Resource):
    def put(self):
        idSubastaGet = request.json['idSubasta']
        CrearSubasta = Subastas.query.get(idSubastaGet)

        fechaSubasta = request.json['Fecha'] + ' ' + request.json['Hora']
        idDireccion = request.json['idDireccion']

        CrearSubasta.fechaSubasta = fechaSubasta
        CrearSubasta.idDireccion = idDireccion
        CrearSubasta.save_to_db()


        return {"Respuesta": 'Se creo la subasta correctamente'}
