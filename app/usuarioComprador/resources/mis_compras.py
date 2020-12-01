from flask_restful import Api, Resource
from app import ObjectNotFound
from app.usuarioComprador.models.mis_compras import Subastas, Usuarios, Pujas
from app.usuarioComprador.schemas.mis_compras import TaskSchema, TaskSchema2, TaskSchema3
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
task_schema = TaskSchema()
task_schema2 = TaskSchema2()
task_schema3 = TaskSchema3()

class misComprasTotal(Resource):
    def get(seft, idUsuario):
        try:
            print('entrando')
            filtro = Subastas.get_compras(idUsuario)
            result = task_schema.dump(filtro, many=True)

            return {"Resultado": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)

class misComprasSeleccionada(Resource):
    def get(seft, idSubasta):
        try:
            print('entrando')
            filtro = Subastas.get_compraSeleccionada(idSubasta)
            result = task_schema.dump(filtro, many=True)

            filtroPro = Subastas.get_productosSubasta(idSubasta)
            result2 = task_schema2.dump(filtroPro, many=True)

            filtroganador = Subastas.get_bodegueroGanador(idSubasta)
            result3 = task_schema3.dump(filtroganador, many=True)

            return {"Pujas": result, "Productos": result2, "Ganador": result3}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)