from flask_restful import Resource
from app.administrador.models.productos_model import  Productos, Tipos_Productos, Parametros
from app.administrador.schemas.productos_schema import TaskSchema, TaskSchema2
from app import ObjectNotFound
from flask import request
from flask_sqlalchemy import SQLAlchemy

import os
import time
from os import remove

from werkzeug.utils import secure_filename
db = SQLAlchemy()

task_schema = TaskSchema()
task_schema2= TaskSchema2()
class obtenerProductosTotal(Resource):
    def get(self):
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

            return {"producto": result, "Parametro": [{ "url": direccion }]}, 200

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

        idTipoProducto = request.json['idTipoProducto']
        nombreProducto = request.json['nombreProducto']
        contenidoProducto = request.json['contenidoProducto']
        Imagen = filename
        codProducto = 'COD' + str(idProductoMax)
        marca = request.json['marca']
        presentacion = request.json['presentacion']
        unidadMedida = request.json['unidadMedida']
        cantidadPaquete = request.json['cantidadPaquete']
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
        imagen=''
        for producto in data['Producto']:
            print('Guardando datos de producto')

            idProducto = producto['idProducto']

            filtroImagen = Productos.get(idProducto)

            for datos in filtroImagen:
                print('impirmir valor')
                print(datos.Imagen)
                imagen = datos.Imagen
                print('aquí termina')

            idTipoProducto = producto['idTipoProducto']
            nombreProducto = producto['nombreProducto']
            contenidoProducto = producto['contenidoProducto']
            marca = producto['marca']
            presentacion = producto['presentacion']
            unidadMedida = producto['unidadMedida']
            cantidadPaquete = producto['cantidadPaquete']
            cambioImagen = producto['cambioImagen']

            productoEditar = Productos.get_query(idProducto)
            productoEditar.idTipoProducto = idTipoProducto
            productoEditar.nombreProducto = nombreProducto
            productoEditar.contenidoProducto = contenidoProducto
            productoEditar.marca = marca
            productoEditar.presentacion = presentacion
            productoEditar.unidadMedida = unidadMedida
            productoEditar.cantidadPaquete = cantidadPaquete

            slash = r'\''
            direccion = ''
            imagen = ''
            try:
                if cambioImagen == 1 :

                    filtro = Parametros.get(2)

                    for datos in filtro:
                        print('impirmir valor')
                        print(datos.Valor)
                        direccion = datos.Valor
                        print('aquí termina')

                    print(direccion + imagen)
                    try:
                        remove(direccion + imagen)
                    except Exception as ex:
                        print('No se encontró la imagen que desea editar.')
                    try:
                        imagen = request.files['pic']
                        filename = time.strftime("%H%M%S") + (time.strftime("%d%m%y")) + secure_filename(imagen.filename)
                        mimetype = imagen.mimetype
                        print(filename)
                        print(mimetype)
                        save_father_path = direccion
                        os.chdir(save_father_path)
                        img_path = os.path.join(save_father_path + filename)
                        imagen.save(img_path)
                        imagen = filename
                        print('Se guardo la imagen correctamente')
                    except Exception as ex:
                        raise ObjectNotFound(ex)


                productoEditar.Imagen = imagen
            except Exception as ex:
                raise ObjectNotFound(ex)
        try:
            productoEditar.save_to_db()
            return 'ok'
        except Exception as ex:
            raise ObjectNotFound(ex)

class eliminarProducto(Resource):
    def delete(self):
        idProducto = request.json['idProducto']
        direccion = ''
        imagen = ''
        flagRemove=0
        producto = Productos.get_query(idProducto)
        try:


            filtro = Parametros.get(2)

            for datos in filtro:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')

            filtroImagen = Productos.get(idProducto)

            for datos in filtroImagen:
                print('impirmir valor')
                print(datos.Imagen)
                imagen = datos.Imagen
                print('aquí termina')

            if direccion != '' and imagen != '':

                try:
                    producto.delete_pro()
                    flagRemove = 1

                except Exception as ex:
                    return 'No se pudo eliminar correctamente '

                if flagRemove == 1:
                    try:
                        remove(direccion + imagen)
                        direccion = ''
                        imagen = ''
                        flagRemove = 0
                        return 'successful'
                    except Exception as ex:
                        return 'No se encontró imagen o dirección'





        except Exception as ex:
            raise ObjectNotFound(ex)
            return 'Producto no encontrado'
        return 'Eliminado Correctamente'