from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.productos_supermercados_model import  Productos_Supermercados, Productos, Supermercados
from app.administrador.schemas.productos_supermercados_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

task_schema = TaskSchema()


class obtenerProductosSupermercado(Resource):
    def get(self):
        try:
            filtro =  Productos_Supermercados.get()
            result = task_schema.dump(filtro, many=True)
            return {"Productos_Supermercados": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class productoSupermercado(Resource):
    def get(self):
        try:
            idProductoSupermercado = request.json['idProductoSupermercado']
            filtro = Productos_Supermercados.get_query(idProductoSupermercado)
            result = task_schema.dump(filtro, many=True)

            return {"Producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarSupermercado(Resource):
    def get(self):
        try:
            nombreSupermercado = request.json['nombreSupermercado']

            filtro = Supermercados.get_Supermercado(nombreSupermercado)

            result = task_schema.dump(filtro, many=True)

            return {"Producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)


class buscarProducto(Resource):
    def get(self):
        try:
            nombreProducto = request.json['nombreProducto']

            filtro = Productos.get_productos(nombreProducto)

            result = task_schema.dump(filtro, many=True)

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

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Guardada', 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class editarProductosSupermercados(Resource):
    def put(self):
        productos_supermercados = request.get_json()
        for datos in tipos_productos['productos']:

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

                except Exception as ex:
                    raise ObjectNotFound(ex)
                return 'SubCategoria Editada', 200
            except Exception as ex:
                raise ObjectNotFound(ex)

class eliminarProductosSupermercados(Resource):
    def delete(self):
        idProductoSupermercado = request.json['idProductoSupermercado']
        productos = Productos_Supermercados.get(idProductoSupermercado)
        productos.delete_pro()