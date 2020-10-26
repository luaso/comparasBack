from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioComun.models.crear_Lista_Subasta_model import Subastas, TaskSchema, Subastas_Productos
from app.UsuarioComun.schemas.crear_Lista_Subasta_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()

taskSchema = TaskSchema()

class subastasEjecucion(Resource):
    def post(self):
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
