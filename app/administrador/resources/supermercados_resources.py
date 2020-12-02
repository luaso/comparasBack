from flask import request
from flask_restful import Resource

from app.administrador.schemas.supermercado_schema import SupermercadosSchema
from app.administrador.models.supermercados_model import Supermercados, Parametros

from app import ObjectNotFound
import time, os
from os import remove
from werkzeug.utils import secure_filename
supermercado_schema = SupermercadosSchema()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

class SupermercadoList(Resource):
    def get(self):
        try:
            supermercado = Supermercados.get_all()

            filtroParam = Parametros.get(9)

            direccion = ''

            for datos in filtroParam:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')

        except:
            raise ObjectNotFound('error al buscar')

        print(supermercado)
        result = supermercado_schema.dump(supermercado, many=True)
        #access_token = create_access_token(identity={"supermercados": result})
        #access_direccion = create_access_token(identity={"url": direccion})
        return {"supermercados": result, "Parametro": [{ "url": direccion }]}, 200

    def post(self):

        imagen = request.files['pic']
        filtro = Parametros.get(9)

        for datos in filtro:
           direccion = datos.Valor

        try:
            filename = time.strftime("%H%M%S") + (time.strftime("%d%m%y")) + secure_filename(imagen.filename)
            mimetype = imagen.mimetype
            print(filename)
            print(mimetype)
            save_father_path = direccion
            os.chdir(save_father_path)
            img_path = os.path.join(save_father_path + filename)
            imagen.save(img_path)
            print('cogimos datos de la imagen')
            #return 'Carga de imagen dada'
        except Exception as ex:
            raise ObjectNotFound(ex)


        try:
            #data = request.json['prueba']
            #print(data)
            nombreSupermercado=request.form['nombreSupermercado']
            urlSupermercado=request.form['urlSupermercado']
            print('carga de datos de insomnia')
            print(nombreSupermercado)
            print(urlSupermercado)
            #nombreSupermercado=request.form["nombreSupermercado"]
            #urlSupermercado=request.form["urlSupermercado"]
        except Exception as ex:
            raise ObjectNotFound(ex)




        try:
            superPost = Supermercados(nombreSupermercado, filename, urlSupermercado)
            superPost.save()
            result="ok"
            #access_token = create_access_token(identity={"estado": result})
            return {"Datos Cargados":result}
        except Exception as ex:
            raise ObjectNotFound(ex)

        #result = supermercado_schema.dump(superPost)



class Supermercado(Resource):
    def get(self, idSupermercado):
        print("entro a get by id")
        supermercado = Supermercados.find_by_id(idSupermercado)
        print(supermercado)
        if supermercado is None:
            raise ObjectNotFound('El Supermercado no existe')
        result = supermercado_schema.dump(supermercado)
        #access_token = create_access_token(identity={"estado": result})
        return {"supermercado": result}, 200

    def delete(self, idSupermercado):
        supermercado = Supermercados.find_by_id(idSupermercado)
        if supermercado is None:
            print("dentro del if")
            raise ObjectNotFound('El supermercado no existe')
        try:
            supermercado.delete_from_db()
        except:
            raise ObjectNotFound('error al eliminar de la BD')
        result="Supermercado eliminado con exito"
        #access_token = create_access_token(identity={"estado": result})
        return {'msg': result}, 204

    def put(self, idSupermercado):
        print("put supermercado")
        nombreSupermercado = request.form['nombreSupermercado']
        urlSupermercado = request.form['urlSupermercado']



        supermercado = Supermercados.find_by_id(idSupermercado)
        supermercado.nombreSupermercado = nombreSupermercado
        supermercado.urlSupermercado = urlSupermercado

        cambioImagen = request.form['cambioImagen']
        imagen = ''

        if cambioImagen == 0 :
            filtro = Parametros.get(9)

            for datos in filtro:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')

            print(direccion + imagen)
            try:
                remove(direccion + imagen)
            except Exception as ex:
                print('No se encontró la imagen que desea editar.')
            try:
                imagen = request.files['pic']
                filename = time.strftime("%H%M%S") + (time.strftime("%d%m%y")) + secure_filename(imagen.filename)
                mimetype = imagen.mimetype
                print(filename)
                print(mimetype)
                save_father_path = direccion
                os.chdir(save_father_path)
                img_path = os.path.join(save_father_path + filename)
                imagen.save(img_path)
                imagen = filename
                supermercado.imagenSupermercado = imagen


                print('Se guardo la imagen correctamente')
            except Exception as ex:
                raise ObjectNotFound(ex)

        try:
            supermercado.save_to_db()
        except:
            raise ObjectNotFound('error al agregar a la BD')



        result = supermercado_schema.dump(supermercado)
        #access_token = create_access_token(identity={"estado": result})
        return {"supermercado": result}, 201

class SupermercadoBuscar(Resource):
    def get(self, nombreSupermercado):
        try:

            filtro = Supermercados.get_filter(nombreSupermercado)
            result = supermercado_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"estado": result})
            return {"Supermercado": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)