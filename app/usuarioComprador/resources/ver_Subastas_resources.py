from flask import request
from flask_restful import Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from app.usuarioComprador.schemas.ver_Subastas_schema import TaskSchema,Serializar
from app.usuarioComprador.models.ver_Subastas_model import Subastas, Usuarios, Estado
from app import ObjectNotFound

from config.configuration import AdditionalConfig

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from app.validateToken import check_for_token
db = SQLAlchemy()
taskSchema = TaskSchema()
class listasSubastasCreadas(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idUsuarioGet = request.json['idUsuario']
            filtro = Subastas.get_joins_filter_Subastas_Creadas(idUsuarioGet)
            result = taskSchema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"listasSubastasCreadas": result})
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class detalleSubasta(Resource):
    def get(self, idSubasta):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idSubastaGet = request.json['idSubasta']

            print("**********************************************************************")
            pujas = Subastas.find_by_id2(idSubasta)
            subastas = Subastas.find_by_id3(idSubasta)
            prueba2 = Serializar.serializarDetalleSubasta2(pujas, subastas)
            print("prueba2")
            print(prueba2)

            #print(jsonify(prueba))

            #result = taskSchema.dump(filtro, many=True)

            return prueba2
        except Exception as ex:
            print(ex)
            raise ObjectNotFound(ex)


class seleccionarGanador(Resource):
    def put(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            idSubastaGet = request.json['idSubasta']
            idUsuarioGanador = request.json['idUsuarioGanador']
            ganador = Subastas.query.get(idSubastaGet)

            print("ganador")
            print(type(idUsuarioGanador))
            estado = Estado.find_by_cod(AdditionalConfig.ESTADO4)
            print(estado)
            ganador.idEstado = estado.idEstado
            ganador.idUsuarioGanador = idUsuarioGanador
            print("usuarioganadro")
            print(type(ganador.idUsuarioGanador))

            ganador.save_to_db()
            print("ASIGNANDO")
            queryprods = (""" UPDATE public."SUBASTAS"
	            SET "direccionFinal"=(SELECT  "direccion" FROM "DIRECCIONES" WHERE "idDireccion"="SUBASTAS"."idDireccion")
	            WHERE "idSubasta"=""" + str(idSubastaGet) + """ """)

            db.session.execute(queryprods)
            db.session.commit()
            result="Se guardo el ganador correctamente"
            #access_token = create_access_token(identity={"seleccionarGanador": result})
            return {"respuesta": result}
        except Exception as ex:
            raise ObjectNotFound(ex)

class productosSubastaComprador(Resource):
    def get(self, idSubasta):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idSubastaGet = request.json['idSubasta']
            filtro = Subastas.get_productos_subasta(idSubasta)
            result = taskSchema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"productosSubastaComprador": result})
            return {"producto": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
