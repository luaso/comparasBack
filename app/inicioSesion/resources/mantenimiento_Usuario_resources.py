# pip install passlib
# pip install flask-jwt-extended
import json

from passlib.hash import sha256_crypt
from flask_restful import Api, Resource
from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import ObjectNotFound, validateToken
from app.inicioSesion.models.mantenimiento_Usuario_model import Rol, Usuarios, Direcciones, Parametros
from app.inicioSesion.schemas.mantenimiento_Usuario_schema import RolSchema
import os
import time
from werkzeug.utils import secure_filename
from os import remove
import bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from app.validateToken import check_for_token

db = SQLAlchemy()

# Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
jwt = JWTManager(app)'''

rolSchema = RolSchema()


class obtenerRol(Resource):
    def get(self):
        # print('22222')
        filtro = Rol.query.filter(Rol.idRol.in_((3, 4)))

        # print(filtro)

        resultado = rolSchema.dump(filtro, many=True)
        # print(resultado)
        return {"rol": resultado}, 200


class guardarUsuario(Resource):
    def post(self):
        print('ingresando a guardarusuario')
        data = request.get_json()

        for usuarios in data['usuarios']:
            print('ingresando a seccion usuarios')
            nombreUsuario = usuarios['nombreUsuario']
            apellidoPatUsuario = usuarios['apellidoPatUsuario']
            apellidoMatUsuario = usuarios['apellidoMatUsuario']
            idRol = usuarios['idRol']
            Ruc = usuarios['Ruc']
            razonSocial = usuarios['razonSocial']
            nombreComercial = usuarios['nombreComercial']
            codigoPostalPais = usuarios['codigoPostalPais']
            telefono = usuarios['telefono']
            celular = usuarios['celular']
            email = usuarios['email']
            # access_token = create_access_token(identity={"email": email})
            ###############################
            # Conversión de contraseña
            password = usuarios['password']

            # password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print('Contraseña creada', password)

            password = sha256_crypt.encrypt(password)
            print(password)
            print(sha256_crypt.verify("password", password))
            ###############################

            imagen = request.files['pic']

            if not imagen:
                return 'Imagen no seleccionada!', 400
            parametro_img = Parametros.get_query(10)
            for datos in parametro_img:
                print('impirmir valor')
                print(datos.Valor)
                direccion = datos.Valor
                print('aquí termina')

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
            except Exception as ex:
                raise ObjectNotFound(ex)

            imagen = filename

            CrearUsuario = Usuarios(nombreUsuario, apellidoPatUsuario, apellidoMatUsuario, idRol, Ruc, razonSocial,
                                    nombreComercial, codigoPostalPais, telefono, celular, email, password, imagen)
            print(CrearUsuario)
            try:

                CrearUsuario.save()
                idUsuarioFK = CrearUsuario.idUsuario
                print('Usuario agregado correctamente')
            except Exception as ex:
                raise ObjectNotFound(ex)

        for direcciones in data['direcciones']:
            idUsuario = idUsuarioFK
            print(idUsuario)
            direccion = direcciones['direccion']
            print(direccion)
            latitud = direcciones['latitud']
            print(latitud)
            longitud = direcciones['longitud']
            print(longitud)

            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
                print(CrearDireccion)

                CrearDireccion.save()
                print('Direcciones agregadas correctamente')
            except:
                print('Error al agregar direccion')

        # return {"access_token": access_token}, 200
        return ('Usuario registrado correctamente')



class buscarUsuario(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
         return chek_token
        task = Usuarios.query.get(idUsuario)
        filtro = Usuarios.get_buscar_usuario(idUsuario)
        # print(filtro)
        result = rolSchema.dump(filtro, many=True)
        print('=================================================')
        return {"producto": result}, 200


class editarUsuarioComprador(Resource):
    def put(seft):
        chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        data = request.get_json()
        idUsuarioDireccion = 0

        for usuario in data['Datos']:
            idUsuario = usuario['idUsuario']
            nombreUsuario = usuario['nombreUsuario']
            apellidoPatUsuario = usuario['apellidoPatUsuario']
            apellidoMatUsuario = usuario['apellidoMatUsuario']
            idRol = usuario['idRol']
            telefono = usuario['telefono']
            celular = usuario['celular']
            email = usuario['email']
            cambioImagen = usuario['cambioImagen']

            usuarioEditar = Usuarios.get_query(idUsuario)
            usuarioEditar.nombreUsuario = nombreUsuario
            usuarioEditar.apellidoPatUsuario = apellidoPatUsuario
            usuarioEditar.apellidoMatUsuario = apellidoMatUsuario
            usuarioEditar.idRol = idRol
            usuarioEditar.telefono = telefono
            usuarioEditar.celular = celular
            usuarioEditar.email = email

            if cambioImagen == 1:

                filtro = Parametros.get(2)

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
                    print('Se guardo la imagen correctamente')
                except Exception as ex:
                    raise ObjectNotFound(ex)

                usuarioEditar.Imagen = imagen

            print('Ingresando al save to db')
            try:
                usuarioEditar.save_to_db()
                print('realizado')
            except Exception as ex:
                print('error')
                raise ObjectNotFound(ex)
            # db.session.commit()

            idUsuarioDireccion = idUsuario

        filtro = Direcciones.get_query(idUsuarioDireccion)
        for direcciones in filtro:
            print(direcciones.idDireccion)
            direcciones = Direcciones.find_by_id(direcciones.idDireccion)
            direcciones.delete_from_db()

        for direcciones in data['direcciones']:

            idUsuario = idUsuarioDireccion
            direccion = direcciones['direccion']
            latitud = direcciones['latitud']
            longitud = direcciones['longitud']

            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
                print(CrearDireccion)
                CrearDireccion.save()

                print('Direcciones agregadas correctamente')
                Respuesta = "ok"
            except Exception as ex:
                raise ObjectNotFound(ex)
                Respuesta = "nok"
                print('Error al agregar direccion')

        # access_token = create_access_token(identity={"request": Respuesta})
        # return {"access_token": access_token}, 200
        return ('Usuario editado correctamente')


class editarUsuarioBodeguero(Resource):
    def put(seft):
        data = request.get_json()
        idUsuarioDireccion = 0

        for usuario in data['Datos']:
            idUsuario = usuario['idUsuario']
            nombreUsuario = usuario['nombreUsuario']
            apellidoPatUsuario = usuario['apellidoPatUsuario']
            apellidoMatUsuario = usuario['apellidoMatUsuario']
            idRol = usuario['idRol']
            Ruc = usuario['Ruc']
            razonSocial = usuario['razonSocial']
            nombreComercial = usuario['nombreComercial']
            codigoPostalPais = usuario['codigoPostalPais']
            telefono = usuario['telefono']
            celular = usuario['celular']
            email = usuario['email']
            imagen = usuario['imagen']

            usuarioEditar = Usuarios.get_query(idUsuario)
            usuarioEditar.nombreUsuario = nombreUsuario
            usuarioEditar.apellidoPatUsuario = apellidoPatUsuario
            usuarioEditar.apellidoMatUsuario = apellidoMatUsuario
            usuarioEditar.idRol = idRol
            usuarioEditar.Ruc = Ruc
            usuarioEditar.razonSocial = razonSocial
            usuarioEditar.nombreComercial = nombreComercial
            usuarioEditar.codigoPostalPais = codigoPostalPais
            usuarioEditar.telefono = telefono
            usuarioEditar.celular = celular
            usuarioEditar.email = email
            usuarioEditar.imagen = imagen
            print('Ingresando al save to db')
            try:
                usuarioEditar.save_to_db()
                print('realizado')
            except Exception as ex:
                print('error')
                raise ObjectNotFound(ex)
            # db.session.commit()

            idUsuarioDireccion = idUsuario

        filtro = Direcciones.get_query(idUsuarioDireccion)
        for direcciones in filtro:
            print(direcciones.idDireccion)
            direcciones = Direcciones.find_by_id(direcciones.idDireccion)
            direcciones.delete_from_db()

        for direcciones in data['direcciones']:

            idUsuario = idUsuarioDireccion
            direccion = direcciones['direccion']
            latitud = direcciones['latitud']
            longitud = direcciones['longitud']

            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
                print(CrearDireccion)
                CrearDireccion.save()

                print('Direcciones agregadas correctamente')

            except Exception as ex:
                raise ObjectNotFound(ex)

                print('Error al agregar direccion')

        # access_token = create_access_token(identity={"request": Respuesta})
        # return {"access_token": Respuesta}, 200
        return ('Usuario editado correctamente')
