from flask import request
from flask_restful import Resource

from app.UsuarioComun.schemas.productos_Buscar_Listar_schema import ProductosBuscarListarSchema
from app.UsuarioComun.models.productos_Buscar_Listar_model import Productos
from app import ObjectNotFound

productos_Buscar_Listar_schema = ProductosBuscarListarSchema()
class ProductoList(Resource):
    def get(self):
        try:
            producto = Productos.get_all()
        except:
            raise ObjectNotFound('error al buscar')

        print(producto)
        result = productos_Buscar_Listar_schema.dump(producto, many=True)
        return {"productos": result}, 200



class Producto(Resource):
    def get(self, nombreProducto):


        producto = Productos.query.filter_by(nombreProducto=nombreProducto).first()


        #producto = Productos.query.order_by(Productos.nombreProducto).all()


        print(producto)

        if producto is None:
            raise ObjectNotFound('El producto no existe')
        result = productos_Buscar_Listar_schema.dump(producto)
        return {"producto": result}, 200
