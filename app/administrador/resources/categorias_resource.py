from flask import request
from flask_restful import Resource

import sys

from app.administrador.schemas.categoria_schema import CategoriasSchema
from app.administrador.models.categoria_model import Categorias
from app import ObjectNotFound

categoria_schema = CategoriasSchema()


class CategoriaList(Resource):
    def get(self):
        try:
            categoria = Categorias.get_all()
        except:
            raise ObjectNotFound('error al buscar')

        print(categoria)
        result = categoria_schema.dump(categoria, many=True)
        return {"Categorias": result}, 200

class Categoria(Resource):
    def get(self, idCategoria):
        print("entro a get by id")
        categoria = Categorias.find_by_id(idCategoria)
        print(categoria)
        if categoria is None:
            raise ObjectNotFound('La categoria no existe')
        result = categoria_schema.dump(categoria)
        return {"categoria": result}, 200

    def delete(self, idCategoria):
        categoria = Categorias.find_by_id(idCategoria)
        if categoria is None:
            print("dentro del if")
            raise ObjectNotFound('La categoria no existe')
        try:
            categoria.delete_from_db()
        except:
            raise ObjectNotFound('error al eliminar de la BD')
        return {'msg': 'Categoria eliminada con exito'}, 204

    def post(self, nombreCategoria):
        data = request.get_json()
        try:
            categoria_dict = categoria_schema.load(data)
        except Exception as ex:
            raise ObjectNotFound(ex)
        print(categoria_dict)
        categoria = Categorias(nombreCategoria = categoria_dict['nombreCategoria'])
        print(categoria)
        try:
            categoria.save()
        except:
            raise ObjectNotFound('error al agregar a la BD')
        result = categoria_schema.dump(categoria)
        return {"categoria": result}, 201

    def put(self, idCategoria):
        data = request.get_json()
        print(data)
        try:
            categoria_dict = categoria_schema.load(data)
        except Exception as ex:
            raise ObjectNotFound(ex)
        print(categoria_dict)
        categoria = Categorias.find_by_id(idCategoria)
        print(categoria)
        if categoria is None:
            categoria = Categorias(data['nombreCategoria'])
        else:
            categoria.nombreCategoria = data['nombreCategoria']
        print(categoria)
        try:
            categoria.save_to_db()
        except:
            raise ObjectNotFound('error al agregar a la BD')
        result = categoria_schema.dump(categoria)
        return {"categoria": result}, 201