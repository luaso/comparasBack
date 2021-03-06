from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.schemas.lista_schema import ProductoSchema, SubastasSchema, Subasta_ProductosTaskSchema
from app.usuarioComprador.models.subastas_model import Subastas, Subastas_Productos
from config.configuration import AdditionalConfig


from app import ObjectNotFound
from app.validateToken import check_for_token

subasta_ProductosSchema = Subasta_ProductosTaskSchema()
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
            idUsuario = chek_token["idUsuario"]
            codEstado = AdditionalConfig.ESTADO1
            print(idUsuario)
            print(codEstado)
            filtro = Subastas.get_list_user(idUsuario, codEstado)
            print("test parte final")
            print(filtro)
            result = taskSchema.dump(filtro, many=True)

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
            idUsuario = chek_token["idUsuario"]
            lista = idLista
            print("test unico")
            filtro = Subastas.get_list_for_id(idUsuario, lista)
            print("test parte final unico")
            print(filtro)
            result = productoSchema.dump(filtro, many=True)
            result1 = subasta_ProductosSchema.dump(filtro, many=True)

            print(result1)

            return {"lista": result1}, 201
        except Exception as ex:
            raise ObjectNotFound(ex)



    def put(self, idLista):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        data = request.get_json()
        subasta = Subastas.find_by_id(idLista)

        if subasta is None:
            raise ObjectNotFound('No existe lista con ese id')
        else:
            try:
                nombreLista = data["nombreLista"]

                if subasta.nombreSubasta != nombreLista:
                    subasta.nombreSubasta = nombreLista
                    subasta.save_to_db()

                Subastas_Productos.delete_rows_for_id(idLista)
                for productos in data['productos']:
                    print('idProducto:', productos['idProducto'])
                    print('Cantidad:', productos['Cantidad'])

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

            try:
                Subastas_Productos.delete_Subastas(idLista)
            except Exception as ex:
                raise ObjectNotFound(ex)
        return {"Lista eliminada": idLista}, 201











