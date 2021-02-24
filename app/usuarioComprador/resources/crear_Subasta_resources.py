from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComprador.schemas.crear_Subasta_schema import TaskSchema
from app.usuarioComprador.models.crear_Subasta_model import Subastas, Usuarios,  Productos, Direcciones, Subastas_Productos
from app.usuarioComprador.models.ver_Subastas_model import Estado
from app import ObjectNotFound, db
from datetime import datetime
from config.configuration import AdditionalConfig
from app.validateToken import check_for_token

taskSchema = TaskSchema()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
class listasUsuario(Resource):
    def get(self, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idUsuario = request.json['idUsuario']
            idEstado = 1
            filtro = Subastas.get_joins_filter_ubastas_usuarios(idUsuario, idEstado)
            result = taskSchema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"listas": result})
            return {"Subastas": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class cammbiarListaUsuario(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            data = request.get_json()
            idSubasta = data["idSubasta"]
            idUsuario = data["idUsuario"]

            user = Usuarios.get_by_id(idUsuario)

            apellidoPatUsuario = user.apellidoPatUsuario
            fechaACtual = datetime.now().strftime("%d-%m-%Y, %H:%M:%S")
            print(apellidoPatUsuario)
            print(fechaACtual)
            nombreLista = "Lista-Subasta-" + apellidoPatUsuario + " " + fechaACtual
            subasta = Subastas.find_by_id(idSubasta)
            print(subasta.idUsuario)
            if subasta is None:
                raise ObjectNotFound('No existe lista con ese id')
            else:
                if subasta.idUsuario == 1:
                    if subasta.idEstado == 1:
                        print("el usaurio es 1")
                        subasta.idUsuario = idUsuario
                        subasta.nombreSubasta = nombreLista
                        subasta.save_to_db()
                    else:
                        raise ObjectNotFound('La accion no es correcta')
                else:
                    raise ObjectNotFound('La lista ya tiene dueño')
            result = "Lista editada"
            return {"Lista": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class direccionSubasta(Resource):
    def get(self, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idUsuarioGet = request.json['idUsuario']
            filtro = Direcciones.get_direcciones(idUsuario)
            result = taskSchema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"direcciones": result})
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class buscarProductosCrearSubasta(Resource):
    def get(self, nombreProducto):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            filtro = Productos.get_filter_buscar_Productos(nombreProducto)
            result = taskSchema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"productos": result})
            return {"Direcciones": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class crearSubastaLista(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        try:

            # resultsque = db.session.execute('SELECT * FROM my_table WHERE my_column = :val', {'val': 5})

            idSubasta = request.json['idSubasta']

            CrearSubasta = Subastas.query.get(idSubasta)
            print(CrearSubasta)
            fechaSubasta = request.json['Fecha'] + ' ' + request.json['Hora']
            #fechaSubasta = datetime.datetime.now()
            print(fechaSubasta)
            idDireccion = request.json['idDireccion']
            CrearSubasta.fechaSubasta = fechaSubasta
            CrearSubasta.idDireccion = idDireccion
            CrearSubasta.idEstado = 2
            CrearSubasta.save_to_db()
            queryisnert = ("""INSERT INTO "SUBASTAS"("idUsuario","idEstado","tiempoInicial","nombreSubasta","precioIdeal","idDireccion","fechaSubasta")
                        SELECT "idUsuario",1,'"""+request.json['Fecha']+"""',"nombreSubasta","precioIdeal", "idDireccion", "fechaSubasta"
                        FROM "SUBASTAS" WHERE "idSubasta"=""" + str(idSubasta) + """  RETURNING "idSubasta";""")
            print(queryisnert)
            iduSbastanew = db.session.execute(queryisnert)

            idnuevo = iduSbastanew.fetchone()[0]
            print("Isertado: " + str(idnuevo) + " idusbasta:" + str(idSubasta))
            queryprods = """INSERT INTO "SUBASTAS_PRODUCTOS"("idSubasta", "idProducto", "Cantidad")
                        select """ + str(
                idnuevo) + """, "idProducto", "Cantidad" from "SUBASTAS_PRODUCTOS" where "idSubasta"=""" + str(
                idSubasta)
            print(queryprods)
            db.session.commit()
            db.session.execute(queryprods)
            db.session.commit()
            print('EJECUTADO:')
            result="Se creo la subasta correctamente"
        except Exception as ex:
            raise ObjectNotFound(ex)
        #access_token = create_access_token(identity={"crearLista": result})
        return {"Respuesta": result}

class crearListaComprador(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            # ESTE DATO (DEFAULT) PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
            # =================================================================
            idUsuario = request.json['idUsuario']
            nombreLista = request.json['nombreLista']
            # =================================================================

            estado = Estado.find_by_cod(AdditionalConfig.ESTADO1)

            idEstado = estado.idEstado

            tiempoInicial = datetime.now()
            print(tiempoInicial)
            nombreSubasta = nombreLista
            precioIdeal = 0.0
            fechaSubasta = datetime.now()
            # ESTE DATO (DEFAULT) PUEDE VARIAR SEGUN EL REGISTRO DE LA TABLA DIRECCIONES
            # =================================================================
            idDireccion = AdditionalConfig.DIRECCIONNODEFINIDA
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
                    result = "Subasta creada"
            except Exception as ex:
                raise ObjectNotFound(ex)
        #access_token = create_access_token(identity={"crearListaComprador": result})
        return {"Subasta creada":result}, 201