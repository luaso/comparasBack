from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.productos_supermercados_model import  Productos_Supermercados, Productos, Supermercados
from app.administrador.schemas.productos_supermercados_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()
#Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)'''

class obtenerProductosSupermercado(Resource):
    def get(self):
        try:
            filtro =  Productos_Supermercados.get()
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"productos": result})

            return {"Productos_Supermercados": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class productoSupermercado(Resource):
    def get(self):
        try:
            idProductoSupermercado = request.json['idProductoSupermercado']
            filtro = Productos_Supermercados.get_query(idProductoSupermercado)
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"productos": result})

            return {"Producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarSupermercado(Resource):
    def get(self):
        try:
            nombreSupermercado = request.json['nombreSupermercado']

            filtro = Supermercados.get_Supermercado(nombreSupermercado)

            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"productos": result})

            return {"Producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class buscarProducto(Resource):
    def get(self):
        try:
            nombreProducto = request.json['nombreProducto']

            filtro = Productos.get_productos(nombreProducto)

            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"productos": result})

            return {"Producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarProductosSupermercados(Resource):
    def post(self):
        productos_supermercados = request.get_json()
        for datos in productos_supermercados['productos']:

            try:
                idSupermercado = datos['idSupermercado']
                idProducto = datos['idProducto']
                fechaProducto = datos['fechaProducto']
                precioRegular = datos['precioRegular']
                precioOnline = datos['precioOnline']
                precioTarjeta = datos['precioTarjeta']
                nombreTarjeta = datos['nombreTarjeta']

                try:
                    productos = Productos_Supermercados(idSupermercado,idProducto,fechaProducto,precioRegular,precioOnline,precioTarjeta,nombreTarjeta)
                    productos.save()
                    result="ok"
                except Exception as ex:
                    raise ObjectNotFound(ex)
                    result = "no"
                #access_token = create_access_token(identity={"resultado": result})
                return {'SubCategoria Guardada':result}, 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class editarProductosSupermercados(Resource):
    def put(self):
        productos_supermercados = request.get_json()
        for datos in productos_supermercados['productos']:

            try:
                idProductoSupermercado = datos['idProductoSupermercado']
                idSupermercado = datos['idSupermercado']
                idProducto = datos['idProducto']
                fechaProducto = datos['fechaProducto']
                precioRegular = datos['precioRegular']
                precioOnline = datos['precioOnline']
                precioTarjeta = datos['precioTarjeta']
                nombreTarjeta = datos['nombreTarjeta']


                productosSupermercadosEditar = Productos_Supermercados.get_query(idProductoSupermercado)
                productosSupermercadosEditar.idSupermercado = idSupermercado
                productosSupermercadosEditar.idProducto = idProducto
                productosSupermercadosEditar.fechaProducto = fechaProducto
                productosSupermercadosEditar.precioRegular = precioRegular
                productosSupermercadosEditar.precioOnline = precioOnline
                productosSupermercadosEditar.precioTarjeta = precioTarjeta
                productosSupermercadosEditar.nombreTarjeta = nombreTarjeta


                try:
                    productosSupermercadosEditar.save_to_db()
                    result="ok"
                except Exception as ex:
                    raise ObjectNotFound(ex)
                    result = "no"
                #access_token = create_access_token(identity={"resultado": result})
                return {'SubCategoria Editada': result}, 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarProductosSupermercados(Resource):
    def delete(self, idProductoSupermercado):
        try:
            productos = Productos_Supermercados.get(idProductoSupermercado)
            productos.delete_pro()
            result="eliminada"
            #access_token = create_access_token(identity={"resultado": result})
            return {'SubCategoria': result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)