from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.sub_categorias_model import  Sub_Categorias, Categorias
from app.administrador.schemas.sub_categorias_schema import TaskSchema
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()

class obtenerCategoria(Resource):
    def get(self):
        try:
            filtro = Categorias.get()
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"sub_categorias": result})

            return {"Sub_Categorias": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerSubCategoriaTotal(Resource):
    def get(self):
        try:

            filtro = Sub_Categorias.get_all()
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"sub_categorias": result})

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
                    result="ok"

                except Exception as ex:
                    raise ObjectNotFound(ex)
                #access_token = create_access_token(identity={"sub_categorias": result})
                return {'SubCategoria Guardada': result}, 200
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
                    result = "ok"
                except Exception as ex:
                    raise ObjectNotFound(ex)
                    result ="no"
                #access_token = create_access_token(identity={"sub_categorias": result})
                return {'SubCategoria Editada': result}, 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarSubCategorias(Resource):
    def delete(self, idSubCategorias):
        try:
            sub_categoria = Sub_Categorias.find_by_id(idSubCategorias)
            sub_categoria.delete_sub_cat()
            result="ok"
            #access_token = create_access_token(identity={"sub_categorias": result})
            return {"Eliminado": result}
        except Exception as ex:
            raise ObjectNotFound(ex)