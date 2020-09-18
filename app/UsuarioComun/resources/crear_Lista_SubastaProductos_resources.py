from flask_restful import Api, Resource
from sqlalchemy import or_
#from app.UsuarioComun.schemas.crear_Lista_Subasta_schema import TaskSchema
from app.UsuarioComun.models.crear_Lista_SubastaProductos_model import Supermercados, Estado, Rol,Usuarios,Subastas,Categorias,Productos,Productos_Supermercados,Subastas_Productos,TaskSchema
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, func
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

class buscarProductosSubastaEjecucion(Resource):
    def get(self, idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos).outerjoin(Productos,Subastas_Productos.idProducto == Productos.idProducto).filter(Subastas_Productos.idSubasta == idSubasta).all()
        for subastas_Productos, productos in filtro:
            print(productos.idProducto, productos.nombreProducto)
        resultado = task_schema.dump(filtro, many=True)
        print(resultado)
        return {"productos": resultado}, 200

class compararProductosSupermercados(Resource):
    def get(self, idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos_Supermercados, Productos, Supermercados, Productos_Supermercados.idSupermercado * Productos_Supermercados.precio). \
            outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            outerjoin(Productos_Supermercados, Productos.idProducto == Productos_Supermercados.idProducto). \
            outerjoin(Supermercados, Productos_Supermercados.idSupermercado == Supermercados.idSupermercado). \
            filter(Subastas_Productos.idSubasta == idSubasta).all()
        print(filtro)

        resultado = task_schema.dump(filtro, many=True)
        # print(resultado)
        return {"productos": resultado}, 200