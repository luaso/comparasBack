from flask import request
from flask_restful import Resource
from sqlalchemy import or_
from app.usuarioComun.schemas.productos_Buscar_Listar_schema import ProductosBuscarListarSchema
from app.usuarioComun.models.productos_Buscar_Listar_model import Productos, Categorias, Sub_Categorias, Tipos_Productos
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
            filtro = Productos.get_filter(nombreProducto)
            print('Selección de datos completado')
        except Exception as ex:
            raise ObjectNotFound(ex)

        if filtro is None:
            raise ObjectNotFound('El producto no existe')

        print('=================================================')

        result = productos_Buscar_Listar_schema.dump(filtro, many=True)
        print(result)
        print('=================================================')
        return {"producto": result}, 200






#class ProductosBuscados(Resource):
#    def get(self, idSubasta):
#        try:
#            #producto = Productos.get_all()
#            producto = Productos.query.filter(Productos.idSubasta.endswith('@example.com')).all()
#        except:
#            raise ObjectNotFound('error al buscar')

#        print(producto)
#        result = productos_Buscar_Listar_schema.dump(producto, many=True)
#        return {"productos": result}, 200