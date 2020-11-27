from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.models.crear_Subasta_model import Subastas, Usuarios,  Productos, Direcciones, Subastas_Productos
from app import ObjectNotFound
import datetime
taskSchema = TaskSchema()

class listasUsuario(Resource):
    def get(self, idUsuario):
        try:
            #idUsuario = request.json['idUsuario']
            idEstado = 1
            filtro = Subastas.get_joins_filter_ubastas_usuarios(idUsuario, idEstado)
            result = taskSchema.dump(filtro, many=True)
            return {"Subastas": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class direccionSubasta(Resource):
    def get(self, idUsuario):
        try:
            #idUsuarioGet = request.json['idUsuario']
            filtro = Direcciones.get_direcciones(idUsuario)
            result = taskSchema.dump(filtro, many=True)
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarProductosCrearSubasta(Resource):
    def get(self, nombreProducto):
        try:
            filtro = Productos.get_filter_buscar_Productos(nombreProducto)
            result = taskSchema.dump(filtro, many=True)
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class crearSubastaLista(Resource):
    def put(self):
        try:
            idSubasta = request.json['idSubasta']
            CrearSubasta = Subastas.query.get(idSubasta)
            print(CrearSubasta)
            fechaSubasta = request.json['Fecha'] + ' ' + request.json['Hora']
            #fechaSubasta = datetime.datetime.now()
            print(fechaSubasta)
            idDireccion = request.json['idDireccion']

            CrearSubasta.fechaSubasta = fechaSubasta
            CrearSubasta.idDireccion = idDireccion
            CrearSubasta.save_to_db()
        except Exception as ex:
            raise ObjectNotFound(ex)

        return {"Respuesta": 'Se creo la subasta correctamente'}

class crearListaComprador(Resource):
    def post(self):
        try:

            # ESTE DATO (DEFAULT) PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
            # =================================================================
            idUsuario = request.json['idUsuario']
            # =================================================================
            idEstado = 1
            tiempoInicial = datetime.datetime.now()
            nombreSubasta = 'Creación de lista'
            precioIdeal = 0.0
            fechaSubasta = datetime.datetime.now()
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

        return "Subasta creada", 201