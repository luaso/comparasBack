from flask_restful import Api, Resource
from sqlalchemy import or_
from app.usuarioComprador.models.mis_Subastas_model import Subastas
from app.usuarioComprador.schemas.mis_Subastas_schema import TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

from app.validateToken import check_for_token

db = SQLAlchemy()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
task_schema = TaskSchema()

class misSubastasComprador(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            #idUsuario = request.json['idUsuario']

            filtro = Subastas.get_mis_subastas(idUsuario)


            result = task_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"Subastas": result})
            return {"Resultado": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class deleteMisSubastasComprador(Resource):
    def delete(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            idSubasta = request.json['idSubasta']
            # DELETE SUBASTA BY ID

            #print("Subastass por eliminar")
            subastas = Subastas.find_by_id(idSubasta)
            db.session.rollback()
            subastas.delete_from_db()
            result = "completado"
            return {"Result": result}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)

class validMisSubastasComprador(Resource):
    def post(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        try:


            idSubasta = request.json['idSubasta']
            # VALIDAR SUBASTA SI EXISTE CON PARTICIPANTES
            querysubas = ("""SELECT * FROM "PUJAS" WHERE "idSubasta"=""" + str(idSubasta) + """  limit 1;""")
            iduSbastanew = db.session.execute(querysubas)
            existe = "0"
            try:
                existe = str(iduSbastanew.fetchone()[0])
            except Exception as ex:
                existe = "0"

            return {"Result": existe}, 200
        except Exception as ex:
            raise ObjectNotFound(ex)
