from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.tipos_productos_model import  Sub_Categorias, Categorias, Tipos_Productos
from app.administrador.schemas.tipos_productos_schema import TaskSchema
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

task_schema = TaskSchema()

class obtenerTiposProductos(Resource):
    def get(self):
        try:
            filtro = Tipos_Productos.get_all()
            result = task_schema.dump(filtro, many=True)
            return {"Tipos_Productos": result}, 200
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

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Guardada', 200
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

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Editada', 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarTiposproductos(Resource):
    def delete(self):
        idTipoProducto = request.json['idTipoProducto']
        tipos_Productos = Tipos_Productos.get(idTipoProducto)
        tipos_Productos.delete_pro()