from flask import request
from flask_restful import Resource

from app.administrador.schemas.supermercado_schema import SupermercadosSchema
from app.administrador.models.supermercados_model import Supermercados

from app import ObjectNotFound

supermercado_schema = SupermercadosSchema()


class SupermercadoList(Resource):
    def get(self):
        try:
            supermercado = Supermercados.get_all()
        except:
            raise ObjectNotFound('error al buscar')

        print(supermercado)
        result = supermercado_schema.dump(supermercado, many=True)
        return {"supermercados": result}, 200

    def post(self):
        data = request.get_json()
        try:
            supermercado_dict = supermercado_schema.load(data)
        except Exception as ex:
            raise ObjectNotFound(ex)
        print(supermercado_dict)
        supermercado = Supermercados(nombreSupermercado=supermercado_dict['nombreSupermercado'],
                                     imagenSupermercado=supermercado_dict['imagenSupermercado'],
                                     urlSupermercado=supermercado_dict['urlSupermercado'])
        print(supermercado)
        try:
            supermercado.save()
        except:
            raise ObjectNotFound('error al agregar a la BD')
        result = supermercado_schema.dump(supermercado)
        return {"supermercado": result}, 201


class Supermercado(Resource):
    def get(self, idSupermercado):
        print("entro a get by id")
        supermercado = Supermercados.find_by_id(idSupermercado)
        print(supermercado)
        if supermercado is None:
            raise ObjectNotFound('El Supermercado no existe')
        result = supermercado_schema.dump(supermercado)
        return {"supermercado": result}, 200

    def delete(self, idSupermercado):
        supermercado = Supermercados.find_by_id(idSupermercado)
        if supermercado is None:
            print("dentro del if")
            raise ObjectNotFound('El supermercado no existe')
        try:
            supermercado.delete_from_db()
        except:
            raise ObjectNotFound('error al eliminar de la BD')
        return {'msg': 'Supermercado eliminado con exito'}, 204

    def put(self, idSupermercado):
        data = request.get_json()
        print(data)
        print("put supermercado")
        try:
            supermercado_dict = supermercado_schema.load(data)
        except Exception as ex:
            raise ObjectNotFound(ex)
        print(idSupermercado)
        supermercado = Supermercados.find_by_id(idSupermercado)
        print(supermercado)
        if supermercado is None:
            supermercado = Supermercados(data['nombreSupermercado'])
        else:
            supermercado.nombreSupermercado = data['nombreSupermercado']
        print(supermercado)
        try:
            supermercado.save_to_db()
        except:
            raise ObjectNotFound('error al agregar a la BD')
        result = supermercado_schema.dump(supermercado)
        return {"supermercado": result}, 201

class SupermercadoBuscar(Resource):
    def get(self):
        try:
            nombreSupermercado = request.json['nombreSupermercado']
            filtro = Supermercados.get_filter(nombreSupermercado)
            result = supermercado_schema.dump(filtro, many=True)
            return {"Supermercado": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)