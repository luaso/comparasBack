from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.schemas.lista_schema import ProductoSchema, SubastasSchema
from app.usuarioComprador.models.subastas_model import Subastas, Estado, Productos, Categorias, Sub_Categorias, Tipos_Productos, Rol, Usuarios, Subastas_Productos


from app import ObjectNotFound
from app.validateToken import check_for_token

taskSchema = TaskSchema()
productoSchema = ProductoSchema()
subastasSchema = SubastasSchema()

class listas(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idUsuario = 43
            lista = "Lista"
            print("test")
            filtro = Subastas.get_list_user(idUsuario, lista)
            print("test parte final")
            print(filtro)
            result = taskSchema.dump(filtro, many=True)
            print(result)

            return {"lista": result}, 201
        except Exception as ex:
            raise ObjectNotFound(ex)

    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idSubastaCreada = 0
            # ESTE DATO (DEFAULT) PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
            # =================================================================
            idUsuario = 1
            # =================================================================
            idEstado = 1
            tiempoInicial = datetime.now()
            nombreSubasta = 'Creación de lista'
            precioIdeal = 0.0
            fechaSubasta = datetime.now()
            # ESTE DATO (DEFAULT) PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
            # =================================================================
            idDireccion = 24
            # =================================================================
            print('Selección de datos completado')
            crearSubasta = Subastas(idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, idDireccion, fechaSubasta)
            print('Agrupación de datos completado')

            try:
                print('Creando Subasta...')
                crearSubasta.save()
                print('Creación de SUBASTA completada')
                intCreacion = 1
                idSubastaCreada = crearSubasta.idSubasta
                print('ID :', idSubastaCreada)
            except Exception as ex:
                raise ObjectNotFound(ex)

        except Exception as ex:
            raise ObjectNotFound(ex)

        data = request.get_json()
        print(data)
        for productos in data['productos']:
            print('idProducto:', productos['idProducto'])
            print('Cantidad:', productos['Cantidad'])
            try:
                if intCreacion == 1:
                    idSubasta = idSubastaCreada
                    idProducto = productos['idProducto']
                    Cantidad = productos['Cantidad']
                    subasta_productos = Subastas_Productos(idSubasta, idProducto, Cantidad)
                    subasta_productos.save()
                    print('Productos Agregados a la subasta con exito')
            except Exception as ex:
                raise ObjectNotFound(ex)

        return {"Subasta creada": idSubastaCreada}, 201

class lista(Resource):
    def get(self, idLista):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idUsuario = 1
            lista = idLista
            print("test unico")
            filtro = Subastas.get_list_for_id(idUsuario, lista)
            print("test parte final unico")
            print(filtro)
            result = productoSchema.dump(filtro, many=True)
            print(result)

            return {"lista": result}, 201
        except Exception as ex:
            raise ObjectNotFound(ex)



    def put(self, idLista):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        data = request.get_json()
        subasta = Subastas.find_by_id(idLista)
        print(subasta)
        if subasta is None:
            raise ObjectNotFound('No existe lista con ese id')
        else:

            Subastas_Productos.delete_rows_for_id(idLista)

            for productos in data['productos']:
                print('idProducto:', productos['idProducto'])
                print('Cantidad:', productos['Cantidad'])
                try:
                   idSubasta = idLista
                   idProducto = productos['idProducto']
                   Cantidad = productos['Cantidad']
                   subasta_productos = Subastas_Productos(idSubasta, idProducto, Cantidad)
                   subasta_productos.save()
                   print('Productos Agregados a la subasta con exito')
                except Exception as ex:
                    raise ObjectNotFound(ex)

        return {"Subasta actualizada": idLista}, 201

    def delete(self, idLista):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        subastas = Subastas.find_by_idd(idLista)
        print(subastas)
        if subastas is None:
            raise ObjectNotFound('No existe lista con ese id')
        else:
            print("1")
            elimiSubastas = Subastas(subastas.idSubasta,
                                     subastas.idUsuario,
                                     subastas.idEstado,
                                     subastas.tiempoInicial,
                                     subastas.nombreSubasta,
                                     subastas.precioIdeal,
                                     subastas.idDireccion,
                                     subastas.fechaSubasta)
            print("2")
            Subastas_Productos.delete_rows_for_id(idLista)
            print("3")
        return {"Lista eliminada": idLista}, 201











