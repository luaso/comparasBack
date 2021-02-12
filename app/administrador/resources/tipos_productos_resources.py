from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.tipos_productos_model import Sub_Categorias, Categorias, Tipos_Productos
from app.administrador.schemas.tipos_productos_schema import TaskSchema
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

class obtenerTiposProductos(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro = Tipos_Productos.get_all()
            result = task_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"productos": result})
            return {"Tipos_Productos": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class tipoProductos(Resource):
    def get(self, idTipoProductos):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro = Tipos_Productos.find_by_id(idTipoProductos)
            result = task_schema.dump(filtro)
            #access_token = create_access_token(identity={"productos": result})
            return {"Tipos_Productos": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerSubCategorias(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro = Sub_Categorias.get_all()
            result = task_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"productos": result})
            return {"Sub_Categorias": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarTiposProductos(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()

        tipos_productos = res["tipos_productos"]

        try:
            nombreTipoProducto = tipos_productos['nombreTipoProducto']
            idSubCategorias = tipos_productos['idSubCategorias']

            try:
                tipos_Productos = Tipos_Productos(nombreTipoProducto, idSubCategorias)
                tipos_Productos.save_to_db()
                result="ok"
            except Exception as ex:
                raise ObjectNotFound(ex)
                #access_token = create_access_token(identity={"productos": result})
            return {'SubCategoria Guardada':result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class editarTiposProductos(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()
        tipos_productos = res['tipos_productos']
        try:
            idTipoProducto = tipos_productos['idTipoProducto']
            nombreProducto = tipos_productos['nombreTipoProducto']
            idSubCategorias = tipos_productos['idSubCategorias']


            tiposProductosEditar = Tipos_Productos.find_by_id(idTipoProducto)

            if tiposProductosEditar is None:
                raise ObjectNotFound('El id del Tipo de producto no existe')

            tiposProductosEditar.nombreProducto = nombreProducto
            tiposProductosEditar.idSubCategorias = idSubCategorias

            try:
                tiposProductosEditar.save_to_db()
                result="ok"
            except Exception as ex:
                raise ObjectNotFound(ex)
                #access_token = create_access_token(identity={"productos": result})
            return {'SubCategoria Editada':result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class eliminarTiposproductos(Resource):
    def delete(self, idTipoProducto):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            tipos_Productos = Tipos_Productos.find_by_id(idTipoProducto)
            tipos_Productos.delete_type()
            result="ok"
            #access_token = create_access_token(identity={"productos": result})
            return result
        except Exception as ex:
            raise ObjectNotFound(ex)
