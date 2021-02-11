from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.sub_categorias_model import Sub_Categorias, Categorias
from app.administrador.schemas.sub_categorias_schema import TaskSchema, TaskSchema2
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from app.validateToken import check_for_token

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()
task_schema2 = TaskSchema2()

class obtenerCategoria(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        print(chek_token)
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        try:
            filtro = Categorias.get()
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"sub_categorias": result})

            return {"Sub_Categorias": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class obtenerSubCategoriaTotal(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            filtro = Sub_Categorias.get_all()
            print(filtro)
            result = task_schema2.dump(filtro, many=True)

            #access_token = create_access_token(identity={"sub_categorias": result})

            return {"Sub_Categorias": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarSubCategoria(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        sub_categorias = request.get_json()
        datos = sub_categorias['subCategorias']

        try:
            nombreSubCategorias = datos['nombreSubCategorias']
            idCategoria = datos['idCategoria']
            print(idCategoria)
            subCategoria = Sub_Categorias(nombreSubCategorias=nombreSubCategorias, idCategoria=idCategoria)
            print(subCategoria)
            subCategoria.save_to_db()
            result="ok"
            print("3")

            #access_token = create_access_token(identity={"sub_categorias": result})
            return {'SubCategoria Guardada': result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class editarSubCategoria(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        sub_categorias = request.get_json()
        datos = sub_categorias['subCategorias']

        try:
            idSubCategorias = datos['idSubCategorias']
            nombreSubCategorias = datos['nombreSubCategorias']
            idCategoria = datos['idCategoria']

            subCategoriaEditar = Sub_Categorias.get_query(idSubCategorias)
            subCategoriaEditar.nombreSubCategorias = nombreSubCategorias
            subCategoriaEditar.idCategoria = idCategoria

            subCategoriaEditar.save_to_db()
            result = "ok"

                #access_token = create_access_token(identity={"sub_categorias": result})
            return {'SubCategoria Editada': result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class eliminarSubCategorias(Resource):
    def delete(self, idSubCategorias):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            sub_categoria = Sub_Categorias.find_by_id(idSubCategorias)
            sub_categoria.delete_sub_cat()
            result="ok"
            #access_token = create_access_token(identity={"sub_categorias": result})
            return {"Eliminado": result}
        except Exception as ex:
            raise ObjectNotFound(ex)