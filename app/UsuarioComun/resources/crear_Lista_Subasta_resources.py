from flask_restful import Api, Resource
from sqlalchemy import or_
from app.UsuarioComun.models.crear_Lista_Subasta_model import Subastas, Subastas_Productos, TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
db = SQLAlchemy()
taskSchema = TaskSchema()
class subastasEjecucion(Resource):
    def post(self):
        idUsuario = 1
        idEstado = 1
        tiempoInicial = datetime.now()
        nombreSubasta = 'Creación de lista'
        precioIdeal = 0.0
        fechaSubasta = 'Por definir'
        # ESTE DATO PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
        #=================================================================
        idDireccion = 24
        # =================================================================
        print('Selección de datos completado')
        crearSubasta = Subastas(idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, fechaSubasta,idDireccion)
        print('Agrupación de datos completado')
        db.session.add(crearSubasta)
        print('Sessión aperturada')
        idSubastaCreada = 0
        try:
            db.session.commit()
            print('Creación de SUBASTA completada')
            intCreacion = 1
            idSubastaCreada = crearSubasta.idSubasta
            print('ID :', idSubastaCreada)
        except:
            print('Error al Crear Subasta')

        data = request.get_json()
        print(data)
        for productos in data['productos']:
            print('idProducto:', productos['idProducto'])
            print('Cantidad:', productos['Cantidad'])
            if intCreacion == 1:
                idSubasta = idSubastaCreada
                idProducto = productos['idProducto']
                Cantidad = productos['Cantidad']
                new_task = Subastas_Productos(idSubasta, idProducto, Cantidad)
                db.session.add(new_task)
            try:
                db.session.commit()
                print('Productos Agregados a la subasta con exito')
            except:
                print('Error al agregar productos')
        return jsonify(idSubastaCreada)
