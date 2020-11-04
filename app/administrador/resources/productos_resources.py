from flask_restful import Api, Resource
from sqlalchemy import or_
from app.administrador.models.productos_model import  Productos, Tipos_Productos, Sub_Categorias, Categorias, Parametros
from app.administrador.schemas.productos_schema import TaskSchema, TaskSchema2
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import cv2
import os
import time
from werkzeug.utils import secure_filename
db = SQLAlchemy()

task_schema = TaskSchema()
task_schema2= TaskSchema2()
class obtenerProductosTotal(Resource):
    def get(self):
        try:
            filtro =  Productos.get_joins()
            result = task_schema.dump(filtro, many=True)
            return {"producto": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerTipoProduto(Resource):
    def get(self):
        try:
            filtro =  Tipos_Productos.get_joins()
            result = task_schema2.dump(filtro, many=True)
            return {"Tipos de pruductos": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarproductoNuevo(Resource):
    def post(self):
        idProductoMax = 0
        imagen = request.files['pic']
        if not imagen:
            return 'Imagen no seleccionada!', 400
        try:
            filtro = Parametros.get(2)
            filtroMax = Productos.get_Max()
            direccion = ''

            for datos in filtro:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')

            for datos in filtroMax:
                print(datos.idProducto)
                idProductoMax = datos.idProducto
                idProductoMax = idProductoMax + 1
        except Exception as ex:
            raise ObjectNotFound(ex)
        try:
            filename = time.strftime("%H%M%S") + (time.strftime("%d%m%y")) + secure_filename(imagen.filename)
            mimetype = imagen.mimetype
            print(filename)
            print(mimetype)
            save_father_path = direccion
            os.chdir(save_father_path)
            img_path = os.path.join(save_father_path + filename)
            imagen.save(img_path)
            print('cogimos datos de la imagen')
        except Exception as ex:
            raise ObjectNotFound(ex)
        idTipoProducto = 2
        nombreProducto = 'test imagen'
        contenidoProducto = 'test imagen contenido'
        Imagen = filename
        codProducto = 'COD' + str(idProductoMax)
        marca = 'plaza vea'
        presentacion = 'en bolsa'
        unidadMedida = 'g'
        cantidadPaquete = 300
        try:
            productos = Productos(idTipoProducto,nombreProducto,contenidoProducto,Imagen,codProducto,marca,presentacion,unidadMedida,cantidadPaquete)
            productos.save()
            print(Imagen)
        except Exception as ex:
            raise ObjectNotFound(ex)
        return 'Imagen cargada', 200

class mostrarProductoSeleccionado(Resource):
    def get(self):
        idProducto = request.json['idProducto']
        filtro = Productos.get(idProducto)

        for datos in filtro:
            print('impirmir valor')
            print(datos.Valor)
            direccion = datos.Valor
            print('aquí termina')

        result = task_schema.dump(filtro, many=True)

        return {"Producto": result}, 200

class mostrarParametros(Resource):
    def get(self):
        filtroParametro = Parametros.get(2)
        result = task_schema.dump(filtroParametro, many=True)

        return {"Direccion": result}, 200

class editarProducto(Resource):
    def put(self):
        data = request.get_json()
        for producto in data['Producto']:
            print('Guardando datos de producto')

            idProducto = producto['idProducto']
            idTipoProducto = producto['idTipoProducto']
            nombreProducto = producto['nombreProducto']
            contenidoProducto = producto['contenidoProducto']
            marca = producto['marca']
            presentacion = producto['presentacion']
            unidadMedida = producto['unidadMedida']
            cantidadPaquete = producto['cantidadPaquete']

            productoEditar = Productos.get_query(idUsuario)
            productoEditar.nombreUsuario = nombreUsuario


        try:
            producto = Productos(idTipoProducto, nombreProducto, contenidoProducto, marca, presentacion,unidadMedida, cantidadPaquete)
            producto.save()
        except Exception as ex:
            raise ObjectNotFound(ex)
