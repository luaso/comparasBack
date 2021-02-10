from flask import request, jsonify
from flask_restful import Api, Resource
from app import ObjectNotFound
from app.usuarioComprador.models.mis_compras import Subastas, Usuarios, Pujas
from app.usuarioComprador.schemas.mis_compras import TaskSchema, TaskSchema2, TaskSchema3
from flask_sqlalchemy import SQLAlchemy


from app.validateToken import check_for_token

db = SQLAlchemy()
task_schema = TaskSchema()
task_schema2 = TaskSchema2()
task_schema3 = TaskSchema3()

class misComprasTotal(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            print('entrando')
            filtro = Subastas.get_compras(idUsuario)
            #result = task_schema.dump(filtro, many=True)
            result = jsonify({"Resultado": filtro})
            return result

        except Exception as ex:
            raise ObjectNotFound(ex)

class misComprasSeleccionada(Resource):
    def get(seft, idSubasta):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:
            print('entrando')
            filtro = Subastas.get_direccion(idSubasta)
            print(filtro)
            result = task_schema.dump(filtro, many=True)
            print(result)

            filtroPro = Subastas.get_productosSubasta(idSubasta)
            result2 = task_schema2.dump(filtroPro, many=True)

            filtroganador = Subastas.get_bodegueroGanador(idSubasta)
            #AGREGAR EMAIL Y LOS OTROS DATOS
            result3 = task_schema3.dump(filtroganador, many=True)


            return {"Direccion": result, "Productos": result2, "Ganador": result3}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)