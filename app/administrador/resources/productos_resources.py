from flask_restful import Resource
from app.administrador.models.productos_model import  Productos, Tipos_Productos, Parametros
from app.administrador.schemas.productos_schema import TaskSchema, TaskSchema2
from app import ObjectNotFound
from flask import request, Flask
from flask_sqlalchemy import SQLAlchemy
from config.configuration import AdditionalConfig

import base64
import os
import time
from os import remove

from werkzeug.utils import secure_filename

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from app.validateToken import check_for_token

db = SQLAlchemy()

#Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)'''

task_schema = TaskSchema()
task_schema2= TaskSchema2()
class obtenerProductosTotal(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro =  Productos.get_joins()

            filtroParam = Parametros.get(2)

            direccion = ''

            for datos in filtroParam:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')


            result = task_schema.dump(filtro, many=True)
            #access_producto = create_access_token(identity={"productos": result})
            #access_direccion = create_access_token(identity={"direccion": direccion})

            return {"producto": result, "Parametro": [{ "url": direccion }]}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class obtenerTipoProduto(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro =  Tipos_Productos.get_joins()
            result = task_schema2.dump(filtro, many=True)

            #access_tipos_productos = create_access_token(identity={"tipos_productos": result})

            return {"Tipos de pruductos": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class guardarproductoNuevo(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        res = request.get_json()
        productoRes = res["producto"]

        idTipoProducto = productoRes['idTipoProducto']
        codProducto = productoRes['codProducto']
        nombreProducto = productoRes['nombreProducto']
        contenidoProducto = productoRes['contenidoProducto']

        marca = productoRes['marca']
        presentacion = productoRes['presentacion']
        unidadMedida = productoRes['unidadMedida']
        cantidadPaquete = productoRes['cantidadPaquete']
        imagen = productoRes['imagen']

        rutaimg = AdditionalConfig.RUTAIMAGENESPRODUCTOS


        if imagen is None:
            return {"respuesta":'Imagen no seleccionada!'}, 400

        try:
            filtro = Productos.get_por_cod(codProducto)
            print("filtro")
            print(filtro == [])

            imgdata = base64.b64decode(imagen)
            filename = 'app/imagenes/productos/' + codProducto + '.jpg'

            if filtro == []:

                with open(filename, 'wb') as f:
                    f.write(imgdata)

                imagenProductoURL = rutaimg + codProducto + '.jpg'

                productos = Productos(idTipoProducto, nombreProducto, contenidoProducto, imagenProductoURL, codProducto, marca,
                                          presentacion, unidadMedida, cantidadPaquete)
                print(productos)
                productos.save_to_db()
                result = "ok"

            else:
                return {"respuesta":'Ya existe un producto con este codigo'}, 400

        except Exception as ex:
            raise ObjectNotFound(ex)


        #access_token = create_access_token(identity={"tipos_productos": result})
        return {'respuesta': result}, 200

class mostrarProductoSeleccionado(Resource):
    def get(self, idProducto):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        print("asdasd")
        filtro = Productos.get(idProducto)
        print("asdasd")
        result = task_schema.dump(filtro, many=True)
        #access_token = create_access_token(identity={"producto": result})
        return {"Producto": result}, 200

class mostrarParametros(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        filtroParametro = Parametros.get(2)
        result = task_schema.dump(filtroParametro, many=True)
        #access_token = create_access_token(identity={"parametro": result})
        return {"Direccion": result}, 200

class editarProducto(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        #--------

        res = request.get_json()
        productoRes = res["producto"]

        idProducto = productoRes['idProducto']
        idTipoProducto = productoRes['idTipoProducto']
        codProducto = productoRes['codProducto']
        nombreProducto = productoRes['nombreProducto']
        contenidoProducto = productoRes['contenidoProducto']

        marca = productoRes['marca']
        presentacion = productoRes['presentacion']
        unidadMedida = productoRes['unidadMedida']
        cantidadPaquete = productoRes['cantidadPaquete']
        imagen = productoRes['imagen']
        cambioImagen = productoRes['cambioImagen']

        rutaimg = AdditionalConfig.RUTAIMAGENESPRODUCTOS

        try:
            productos = Productos.find_by_id(idProducto)
            print("filtro")
            print(productos)

            imgdata = base64.b64decode(imagen)
            filename = 'app/imagenes/productos/' + codProducto + '.jpg'

            if productos is None:
                raise ObjectNotFound('El id del producto no existe')

            productos.idTipoProducto = idTipoProducto
            productos.codProducto = codProducto
            productos.nombreProducto = nombreProducto
            productos.contenidoProducto = contenidoProducto
            productos.marca = marca
            productos.presentacion = presentacion
            productos.unidadMedida = unidadMedida
            productos.cantidadPaquete = cantidadPaquete

            if cambioImagen == 1:
                imgdata = base64.b64decode(imagen)
                filename = 'app/imagenes/productos/' + codProducto + '.jpg'

                with open(filename, 'wb') as f:
                    f.write(imgdata)

                imagenProductoURL = rutaimg + codProducto + '.jpg'
                productos.Imagen = imagenProductoURL

            productos.save_to_db()
            result = "ok"
            return {"Producto editado": result}

        except Exception as ex:
            raise ObjectNotFound(ex)

        #--------


class eliminarProducto(Resource):
    def delete(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        res = request.get_json()
        idProducto = res['idProducto']
        print(res)
        try:
            producto = Productos.get_query(idProducto)
            if producto is None:
                raise ObjectNotFound('El id del producto no existe')
            producto.delete_pro()
        except Exception as ex:
            raise ObjectNotFound(ex)
        result = 'ok'

        #access_token = create_access_token(identity={"parametro": result})
        return {"respuesta":result}
