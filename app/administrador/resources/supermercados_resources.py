from flask import request
from flask_restful import Resource

from app.administrador.schemas.supermercado_schema import SupermercadosSchema
from app.administrador.models.supermercados_model import Supermercados, Parametros
from app import ObjectNotFound
from config.configuration import AdditionalConfig
import time, os
from os import remove
from werkzeug.utils import secure_filename
from app.validateToken import check_for_token

import base64

supermercado_schema = SupermercadosSchema()
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

class SupermercadoList(Resource):
    def get(self):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
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
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        res = request.get_json()

        supermercado = res["supermercado"]
        nombreSupermercado = supermercado["nombreSupermercado"]
        urlSupermercado = supermercado["urlSupermercado"]
        imagenSupermercadoR = supermercado["imagenSupermercado"]

        rutaimg = AdditionalConfig.RUTAIMAGENESSUPERMERCADOS

        try:
            imgdata = base64.b64decode(imagenSupermercadoR)
            filename = 'app/imagenes/supermercados/' + nombreSupermercado + '.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)
            imagenSupermercado = rutaimg + nombreSupermercado + '.jpg'

            superPost = Supermercados(nombreSupermercado, imagenSupermercado, urlSupermercado)
            superPost.save()
            result = "ok"
            #access_token = create_access_token(identity={"estado": result})
            return {"Datos Cargados":result}
        except Exception as ex:
            raise ObjectNotFound(ex)

        #result = supermercado_schema.dump(superPost)



class Supermercado(Resource):
    def get(self, idSupermercado):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        print("entro a get by id")
        supermercado = Supermercados.find_by_id(idSupermercado)
        print(supermercado)
        if supermercado is None:
            raise ObjectNotFound('El Supermercado no existe')
        result = supermercado_schema.dump(supermercado)
        #access_token = create_access_token(identity={"estado": result})
        return {"supermercado": result}, 200

    def delete(self, idSupermercado):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
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
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token

        res = request.get_json()
        supermercadoRes = res["supermercado"]
        nombreSupermercado = supermercadoRes["nombreSupermercado"]
        urlSupermercado = supermercadoRes["urlSupermercado"]
        cambioImagen = supermercadoRes["cambioImagen"]
        imagenSupermercadoR = supermercadoRes["imagenSupermercado"]

        rutaimg = AdditionalConfig.RUTAIMAGENESSUPERMERCADOS

        supermercado = Supermercados.find_by_id(idSupermercado)

        if supermercado is None:
            raise ObjectNotFound('El id del supermercado no existe')
        else:

            supermercado.nombreSupermercado = nombreSupermercado
            supermercado.urlSupermercado = urlSupermercado

            try:
                if cambioImagen == 1:
                    imgdata = base64.b64decode(imagenSupermercadoR)
                    filename = 'app/imagenes/supermercados/' + nombreSupermercado + '.jpg'

                    with open(filename, 'wb') as f:
                        f.write(imgdata)

                    imagenSupermercado = rutaimg + nombreSupermercado + '.jpg'
                    supermercado.imagenSupermercado = imagenSupermercado

                supermercado.save_to_db()

                result = "ok"
                return {"Datos Cargados": result}
            except Exception as ex:
                raise ObjectNotFound(ex)


class SupermercadoBuscar(Resource):
    def get(self, nombreSupermercado):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        try:

            filtro = Supermercados.get_filter(nombreSupermercado)
            result = supermercado_schema.dump(filtro, many=True)
            #access_token = create_access_token(identity={"estado": result})
            return {"Supermercado": result}, 200

        except Exception as ex:
            raise ObjectNotFound(ex)