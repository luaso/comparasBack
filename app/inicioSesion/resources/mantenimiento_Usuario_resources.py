import datetime
import traceback

from config.configuration import AdditionalConfig
from passlib.hash import sha256_crypt
from flask_restful import Api, Resource
from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import ObjectNotFound, validateToken
from app.inicioSesion.models.mantenimiento_Usuario_model import Rol, Usuarios, Direcciones, Parametros
from app.inicioSesion.schemas.mantenimiento_Usuario_schema import RolSchema

import base64

from app.validateToken import check_for_token, check_for_token_id_rol, check_for_token_rol, check_for_token_id

db = SQLAlchemy()

# Pruebas
'''app = Flask(__name__)
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'secret'  # Change this!
jwt = JWTManager(app)'''

rolSchema = RolSchema()


class obtenerRol(Resource):
    def get(self):
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
            print('ingresando a seccion usuarios 2')
            # Verificar si el email existe

            usuarioExist = Usuarios.get_email(email)
            print(usuarioExist)
            if usuarioExist is not None:
                return {"respuesta": "Existe"}, 200

            # access_token = create_access_token(identity={"email": email})
            ###############################
            # Conversión de contraseña
            password = usuarios['password']

            # password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            # print('Contraseña creada', password)

            password = sha256_crypt.encrypt(password)
            print(password)
            print(sha256_crypt.verify("password", password))
            #####################EditarUsuarioComprador##########

            # imagen = request.files['pic']

            CrearUsuario = Usuarios(nombreUsuario, apellidoPatUsuario, apellidoMatUsuario, idRol, Ruc, razonSocial,
                                    nombreComercial, codigoPostalPais, telefono, celular, email, password)
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
            referencia = direcciones['referencia']
            print(referencia)
            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud, referencia)
                print(CrearDireccion)

                CrearDireccion.save()
                print('Direcciones agregadas correctamente')
            except:
                print('Error al agregar direccion')

        # return {"access_token": access_token}, 200
        return {"respuesta": "Usuario registrado correctamente"}


class buscarUsuario(Resource):
    def get(seft, idUsuario):
        chek_token = check_for_token_id(request.headers.get('token'), idUsuario)
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        task = Usuarios.query.get(idUsuario)
        filtro = Usuarios.get_buscar_usuario(idUsuario)
        # print(filtro)
        result = rolSchema.dump(filtro, many=True)
        resultd = check_for_token_rol(request.headers.get('token'))
        print(result)
        print('================================================')
        return {"producto": result}, 200

def getbyid(idUsuario):
    try:
        usuarioExist = Usuarios.get_query(idUsuario)
        pasActual = str(usuarioExist.password)
        print(pasActual)
        return pasActual
    except Exception as ex:
        return "No_Existe"

class editarUsuarioComprador(Resource):
    #@property
    def put(seft):
        '''Metodo para editar un usuario con el Rol1'''
        data = request.get_json()
        rolUser = AdditionalConfig.ROL1
        chek_token = check_for_token_id_rol(request.headers.get('token'), data["Datos"][0]["idUsuario"], rolUser)
        # chek_token = check_for_token(request.headers.get('token'))
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        iduser=data["Datos"][0]["idUsuario"]
        cambio=data["Datos"][0]["cambioClave"]
        clavAct=data["Datos"][0]["claveActual"]
        idUsuarioDireccion = 0
        claveActualUser = getbyid(iduser)
        validClave = (sha256_crypt.verify(clavAct, claveActualUser))
        validPwd=0
        if str(validClave) == "False":
            validPwd=1
        if cambio == 1 and validPwd == 1:
            return str('Clave Incorrecto')
        for usuario in data['Datos']:
            idUsuario = usuario['idUsuario']
            nombreUsuario = usuario['nombreUsuario']
            apellidoPatUsuario = usuario['apellidoPatUsuario']
            apellidoMatUsuario = usuario['apellidoMatUsuario']
            telefono = usuario['telefono']
            celular = usuario['celular']
            # email = usuario['email']
            cambioImagen = usuario['cambioImagen']
            imgstring = usuario['imagen']

            cambioClave = usuario['cambioClave']
            nuevaClave = usuario['nuevaClave']

            usuarioEditar = Usuarios.get_query(idUsuario)
            usuarioEditar.codigoPostalPais = usuario['codigoPostalPais']
            usuarioEditar.nombreUsuario = nombreUsuario
            usuarioEditar.apellidoPatUsuario = apellidoPatUsuario
            usuarioEditar.apellidoMatUsuario = apellidoMatUsuario
            # usuarioEditar.idRol = idRol
            usuarioEditar.telefono = telefono
            usuarioEditar.celular = celular
            # usuarioEditar.email = email

            print("SEND CAMBIO: " + str(cambioClave))
            if cambioClave == 1:
                usuarioEditar.password = sha256_crypt.encrypt(nuevaClave)

            try:
                if cambioImagen == 1:
                    rutaimg = AdditionalConfig.RUTAIMAGENESUSUARIOS
                    imgdata = base64.b64decode(imgstring)
                    x = datetime.datetime.now()
                    hourseconds = (str(x.minute) + "_" + str(x.second))
                    filename = 'app/imagenes/usuarios/' + str(usuario['idUsuario']) + hourseconds + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    usuarioEditar.imagen = rutaimg + str(usuario['idUsuario']) + hourseconds + '.jpg'
            except Exception as ex:
                raise ObjectNotFound(ex)

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
            print("idDireccion")
            print(direcciones.idDireccion)
            direccion = Direcciones.find_by_id(direcciones.idDireccion)
            print("Direccion")
            print(direccion.idUsuario)
            direccion.delete_from_db()
            print(data['direcciones'])
        for direcciones in data['direcciones']:

            idUsuario = idUsuarioDireccion
            direccion = direcciones['direccion']
            latitud = direcciones['latitud']
            longitud = direcciones['longitud']
            referencia = direcciones['referencia']
            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud, referencia)
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
        '''Metodo para editar un usuario con el Rol2'''
        data = request.get_json()
        rolUser = AdditionalConfig.ROL2
        chek_token = check_for_token_id_rol(request.headers.get('token'), data["Datos"][0]["idUsuario"], rolUser)
        valid_token = chek_token['message']
        if valid_token != 'ok':
            return chek_token
        iduser = data["Datos"][0]["idUsuario"]
        cambio = data["Datos"][0]["cambioClave"]
        clavAct = data["Datos"][0]["claveActual"]
        claveActualUser = getbyid(iduser)
        validClave = (sha256_crypt.verify(clavAct, claveActualUser))
        validPwd = 0
        if str(validClave) == "False":
            validPwd = 1
        if cambio == 1 and validPwd == 1:
            return str('Clave Incorrecto')
        idUsuarioDireccion = 0

        for usuario in data['Datos']:
            idUsuario = usuario['idUsuario']
            nombreUsuario = usuario['nombreUsuario']
            apellidoPatUsuario = usuario['apellidoPatUsuario']
            apellidoMatUsuario = usuario['apellidoMatUsuario']
            # idRol = usuario['idRol']
            Ruc = usuario['Ruc']
            razonSocial = usuario['razonSocial']
            nombreComercial = usuario['nombreComercial']
            codigoPostalPais = usuario['codigoPostalPais']
            telefono = usuario['telefono']
            celular = usuario['celular']
            # email = usuario['email']
            cambioImagen = usuario['cambioImagen']
            cambioClave = usuario['cambioClave']
            nuevaClave = usuario['nuevaClave']

            imgstring = usuario['imagen']

            usuarioEditar = Usuarios.get_query(idUsuario)
            usuarioEditar.nombreUsuario = nombreUsuario
            usuarioEditar.apellidoPatUsuario = apellidoPatUsuario
            usuarioEditar.apellidoMatUsuario = apellidoMatUsuario
            # usuarioEditar.idRol = idRol
            usuarioEditar.Ruc = Ruc
            usuarioEditar.razonSocial = razonSocial
            usuarioEditar.nombreComercial = nombreComercial
            usuarioEditar.codigoPostalPais = codigoPostalPais
            usuarioEditar.telefono = telefono
            usuarioEditar.celular = celular
            if cambioClave == 1:
                usuarioEditar.password = sha256_crypt.encrypt(nuevaClave)

            try:
                if cambioImagen == 1:
                    rutaimg = AdditionalConfig.RUTAIMAGENESUSUARIOS
                    imgdata = base64.b64decode(imgstring)
                    x = datetime.datetime.now()
                    hourseconds = (str(x.minute) + "_" + str(x.second))
                    filename = 'app/imagenes/usuarios/' + str(usuario['idUsuario']) + hourseconds + '.jpg'
                    with open(filename, 'wb') as f:
                        f.write(imgdata)
                    usuarioEditar.imagen = rutaimg + str(usuario['idUsuario']) + hourseconds + '.jpg'
            except Exception as ex:
                raise ObjectNotFound(ex)

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
            print(direcciones)
            direcciones.delete_from_db()
            print('salio del primer for')
        for direcciones in data['direcciones']:

            idUsuario = idUsuarioDireccion
            direccion = direcciones['direccion']
            latitud = direcciones['latitud']
            longitud = direcciones['longitud']
            referencia ="-"
            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud,referencia)
                print(CrearDireccion)
                CrearDireccion.save()

                print('Direcciones agregadas correctamente')
                Respuesta = "ok"
            except Exception as ex:
                raise ObjectNotFound(ex)
                Respuesta = "nok"
                print('Error al agregar direccion')

        return ('Usuario editado correctamente')
