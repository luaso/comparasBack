from flask import request
from flask_restful import Resource

from app.administrador.schemas.categoria_schema import CategoriasSchema
from app.administrador.models.categoria_model import Categorias
from app import ObjectNotFound

categoria_schema = CategoriasSchema()


class CategoriaList(Resource):
    def get(self):
        categoria = Categorias.get_all()
        print(categoria)
        result = categoria_schema.dump(categoria, many=True)
        return result

class Categoria(Resource):
    def get(self, nombreCategoria):
        print("entro a clase by id")
        categoria = Categorias.find_by_name(nombreCategoria)
        print(categoria)
        if categoria is None:
            raise ObjectNotFound('La administrador no existe')
        result = categoria_schema.dump(categoria)
        return result

    def delete(self, nombreCategoria):
        categoria = Categorias.find_by_name(nombreCategoria)
        print(categoria)
        if categoria:
            print("entro al if")
            categoria.delete_from_db()
            print("fin del if")
            return {'message': 'Categoria eliminada'}
        print("no entro al if")

    def post(self, nombreCategoria):
        data = request.get_json()
        print(data)
        categoria_dict = categoria_schema.load(data)
        print(categoria_dict)
        categoria = Categorias(nombreCategoria = categoria_dict['nombreCategoria'])
        print(categoria)
        categoria.save()
        result = categoria_schema.dump(categoria)
        return result, 201

    def put(self, nombreCategoria):
        data = request.get_json()
        print(data)
        #categoria_dict = categoria_schema.load(data)
        #print(categoria_dict)
        categoria = Categorias.find_by_name(nombreCategoria)
        print(categoria)
        if categoria is None:
            categoria = Categorias(data['nombreCategoria'])
        else:
            categoria.nombreCategoria = data['nombreCategoria']
        print(categoria)
        categoria.save_to_db()
        print("despues de guardar")
        result = categoria_schema.dump(categoria)
        return result, 201