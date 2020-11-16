from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.sub_categorias_model import  Sub_Categorias, Categorias
from app.administrador.schemas.sub_categorias_schema import TaskSchema
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

task_schema = TaskSchema()

class obtenerCategoria(Resource):
    def get(self):
        try:
            filtro = Categorias.get()
            result = task_schema.dump(filtro, many=True)
            return {"Sub_Categorias": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerSubCategoria(Resource):
    def get(self):
        try:
            idSubCategorias = request.json['idSubCategorias']
            filtro =  Sub_Categorias.get(idSubCategorias)
            result = task_schema.dump(filtro, many=True)
            return {"Sub_Categorias": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarSubCategoria(Resource):
    def post(self):
        sub_categorias = request.get_json()
        for datos in sub_categorias['Sub_Categorias']:

            try:
                nombreSubCategorias = datos['nombreSubCategorias']
                idCategoria = datos['idCategoria']

                try:
                    subCategoria = Sub_Categorias(nombreSubCategorias,idCategoria)
                    subCategoria.save()

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Guardada', 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class editarSubCategoria(Resource):
    def put(self):
        sub_categorias = request.get_json()
        for datos in sub_categorias['Sub_Categorias']:

            try:
                idSubCategorias = datos['idSubCategorias']
                nombreSubCategorias = datos['nombreSubCategorias']
                idCategoria = datos['idCategoria']


                subCategoriaEditar = Sub_Categorias.get_query(idSubCategorias)
                subCategoriaEditar.nombreSubCategorias = nombreSubCategorias
                subCategoriaEditar.idCategoria = idCategoria


                try:
                    subCategoriaEditar.save_to_db()

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Editada', 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarSubCategorias(Resource):
    def delete(self):
        idSubCategorias = request.json['idSubCategorias']
        sub_categoria = Sub_Categorias.get(idSubCategorias)
        sub_categoria.delete_pro()