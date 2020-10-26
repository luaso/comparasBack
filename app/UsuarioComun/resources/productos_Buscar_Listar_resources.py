from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.UsuarioComun.schemas.productos_Buscar_Listar_schema import ProductosBuscarListarSchema
from app.UsuarioComun.models.productos_Buscar_Listar_model import Productos, Categorias, Sub_Categorias, Tipos_Productos
from app import ObjectNotFound

productos_Buscar_Listar_schema = ProductosBuscarListarSchema()
class ProductoList(Resource):
    def get(self):
        try:
            print('Estoy aqui')
            producto = Productos.get_all()
            print('Error al jalar')
        except:
            raise ObjectNotFound('error al buscar')

        #print(producto)
        result = productos_Buscar_Listar_schema.dump(producto, many=True)
        return {"productos": result}, 200



class Producto(Resource):
    def get(self, nombreProducto):
        #producto = Productos.query.filter_by(nombreProducto=nombreProducto).first()
        print('entrando a get productos')
        try:
            producto = Productos.query.filter(or_(Productos.nombreProducto.ilike('%'+ nombreProducto +'%'), Productos.contenidoProducto.ilike('%'+ nombreProducto +'%')))
            print('Selección de datos completado')
        except Exception as ex:
            raise ObjectNotFound(ex)
            print('Error')
        print(producto)

        try:
            for resultado1 in producto:
                print(resultado1.nombreProducto)
        except Exception as ex:
            raise ObjectNotFound(ex)


        if producto is None:
            raise ObjectNotFound('El producto no existe')

        print('=================================================')
        result = productos_Buscar_Listar_schema.dump(producto, many=True)
        print(result)
        print('=================================================')
        return {"producto": result}, 200






class ProductosBuscados(Resource):
    def get(self, idSubasta):
        try:
            #producto = Productos.get_all()
            producto = Productos.query.filter(Productos.idSubasta.endswith('@example.com')).all()
        except:
            raise ObjectNotFound('error al buscar')

        print(producto)
        result = productos_Buscar_Listar_schema.dump(producto, many=True)
        return {"productos": result}, 200