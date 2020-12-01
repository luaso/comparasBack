from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.tipos_productos_model import Sub_Categorias, Categorias, Tipos_Productos
from app.administrador.schemas.tipos_productos_schema import TaskSchema
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

class obtenerTiposProductos(Resource):
    def get(self):
        try:
            filtro = Tipos_Productos.get_all()
            result = task_schema.dump(filtro, many=True)
            access_token = create_access_token(identity={"productos": result})
            return {"Tipos_Productos": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerSubCategorias(Resource):
    def get(self):
        try:
            filtro = Sub_Categorias.get_all()
            result = task_schema.dump(filtro, many=True)
            access_token = create_access_token(identity={"productos": result})
            return {"Sub_Categorias": access_token}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarTiposProductos(Resource):
    def post(self):
        tipos_productos = request.get_json()
        for datos in tipos_productos['tipos_productos']:

            try:
                nombreProducto = datos['nombreProducto']
                idSubCategorias = datos['idSubCategorias']

                try:
                    tipos_Productos = Tipos_Productos(nombreProducto,idSubCategorias)
                    tipos_Productos.save()
                    result="ok"
                except Exception as ex:
                    raise ObjectNotFound(ex)
                access_token = create_access_token(identity={"productos": result})
                return {'SubCategoria Guardada':access_token}, 200
            except Exception as ex:
                raise ObjectNotFound(ex)


class editarTiposProductos(Resource):
    def put(self):
        tipos_productos = request.get_json()
        for datos in tipos_productos['tipos_productos']:

            try:
                idTipoProducto = datos['idTipoProducto']
                nombreProducto = datos['nombreProducto']
                idSubCategorias = datos['idSubCategorias']


                tiposProductosEditar = Tipos_Productos.get_query(idTipoProducto)
                tiposProductosEditar.nombreProducto = nombreProducto
                tiposProductosEditar.idSubCategorias = idSubCategorias


                try:
                    tiposProductosEditar.save_to_db()
                    result="ok"
                except Exception as ex:
                    raise ObjectNotFound(ex)
                access_token = create_access_token(identity={"productos": result})
                return {'SubCategoria Editada':access_token}, 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarTiposproductos(Resource):
    def delete(self, idTipoProducto):

        try:
            tipos_Productos = Tipos_Productos.find_by_id(idTipoProducto)
            tipos_Productos.delete_type()
            result="ok"
            access_token = create_access_token(identity={"productos": result})
            return access_token
        except Exception as ex:
            raise ObjectNotFound(ex)
