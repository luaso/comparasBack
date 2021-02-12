from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.productos_supermercados_model import  Productos_Supermercados, Productos, Supermercados
from app.administrador.schemas.productos_supermercados_schema import TaskSchema, TaskSchema2
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from app.validateToken import check_for_token

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()
task_schema2 = TaskSchema2()
#Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)'''

class obtenerProductosSupermercado(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro =  Productos_Supermercados.get()
            result = task_schema.dump(filtro, many=True)

            #access_token = create_access_token(identity={"productos": result})

            return {"Productos_Supermercados": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class productoSupermercado(Resource):
    def get(self, idProductoSupermercado):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            filtro = Productos_Supermercados.get_query(idProductoSupermercado)
            print(filtro)
            result = task_schema2.dump(filtro)
            print(filtro)
            #access_token = create_access_token(identity={"productos": result})

            return {"Producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarSupermercado(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
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
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
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
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()
        productos_supermercados = res['productos_supermercados']
        try:
            idSupermercado = productos_supermercados['idSupermercado']
            idProducto = productos_supermercados['idProducto']
            fechaProducto = productos_supermercados['fechaProducto']
            precioRegular = productos_supermercados['precioRegular']
            precioOnline = productos_supermercados['precioOnline']
            precioTarjeta = productos_supermercados['precioTarjeta']
            nombreTarjeta = productos_supermercados['nombreTarjeta']

            try:
                productos = Productos_Supermercados(idSupermercado,idProducto,fechaProducto,precioRegular,precioOnline,precioTarjeta,nombreTarjeta)
                productos.save()
                result="ok"
            except Exception as ex:
                raise ObjectNotFound(ex)
                result = "no"
                #access_token = create_access_token(identity={"resultado": result})
            return {'producto_supermercado guardado':result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class editarProductosSupermercados(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()
        productos_supermercados = res['productos_supermercados']

        try:
            idProductoSupermercado = productos_supermercados['idProductoSupermercado']
            idSupermercado = productos_supermercados['idSupermercado']
            idProducto = productos_supermercados['idProducto']
            fechaProducto = productos_supermercados['fechaProducto']
            precioRegular = productos_supermercados['precioRegular']
            precioOnline = productos_supermercados['precioOnline']
            precioTarjeta = productos_supermercados['precioTarjeta']
            nombreTarjeta = productos_supermercados['nombreTarjeta']


            productosSupermercadosEditar = Productos_Supermercados.get_query(idProductoSupermercado)

            if productosSupermercadosEditar is None:
                raise ObjectNotFound('El id del producto_supermercado no existe')

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
            return {'productos_supermercados Editado': result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class eliminarProductosSupermercados(Resource):
    def delete(self, idProductoSupermercado):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            productos = Productos_Supermercados.find_by_id(idProductoSupermercado)
            if productos is None:
                raise ObjectNotFound('El id del producto_supermercado no existe')
            productos.delete_pro()
            result="eliminada"
            #access_token = create_access_token(identity={"resultado": result})
            return {'productos_supermercados eliminado': result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)