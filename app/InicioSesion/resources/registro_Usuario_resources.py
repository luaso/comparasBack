from flask_restful import Api, Resource
from datetime import datetime
from app import ObjectNotFound
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from app import ObjectNotFound
from app.InicioSesion.models.registro_Usuario_model import Rol, Usuarios, RolSchema, Direcciones


db = SQLAlchemy()

rolSchema = RolSchema()

class obtenerRol(Resource):
    def get(self):
        #print('22222')
        filtro = Rol.query.filter(Rol.idRol.in_((3, 4)))

        #print(filtro)

        resultado = rolSchema.dump(filtro, many=True)
        #print(resultado)
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
            password = usuarios['password']
            imagen = usuarios['imagen']

            CrearUsuario = Usuarios(nombreUsuario, apellidoPatUsuario, apellidoMatUsuario, idRol, Ruc, razonSocial,
                                    nombreComercial, codigoPostalPais, telefono, celular, email, password, imagen)
            print(CrearUsuario)
            db.session.add(CrearUsuario)
            try:
                db.session.commit()
                idUsuarioFK = CrearUsuario.idUsuario
                print('Usuario agregado correctamente')
            except:
                print('Error al agregar usuario')

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
                db.session.add(CrearDireccion)
                db.session.commit()
                print('Direcciones agregadas correctamente')
            except:
                print('Error al agregar direccion')

        return ('Usuario registrado correctamente')

class buscarUsuario(Resource):
    def get(seft, idUsuario):
        print('prueba entrada get')
        task = Usuarios.query.get(idUsuario)
        filtro = db.session.query(Usuarios, Direcciones).outerjoin(Direcciones,
                 Usuarios.idUsuario == Direcciones.idUsuario).filter(
                 Usuarios.idUsuario == idUsuario).all()
        print(filtro)

        result = rolSchema.dump(filtro, many=True)
        print(result)
        print('=================================================')
        return {"producto": result}, 200

class editarUsuarioComprador(Resource):
    def put(seft):
        data = request.get_json()
        for usuario in data['Datos']:
            idUsuario = usuario['idUsuario']
            nombreUsuario = usuario['nombreUsuario']
            apellidoPatUsuario = usuario['apellidoPatUsuario']
            apellidoMatUsuario = usuario['apellidoMatUsuario']
            idRol = 3
            Ruc = usuario['Ruc']
            razonSocial = usuario['razonSocial']
            nombreComercial = usuario['nombreComercial']
            codigoPostalPais = usuario['codigoPostalPais']
            telefono = usuario['telefono']
            celular = usuario['celular']
            direccion = usuario['direccion']
            email = usuario['email']
            imagen = usuario['imagen']

        usuarioEditar = Usuarios.query.get(idUsuario)
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
        usuarioEditar.direccion = direccion
        usuarioEditar.email = email
        usuarioEditar.imagen = imagen
        db.session.commit()

        idUsuarioDireccion = idUsuario

        for direcciones in data['direcciones']:

            idUsuario = idUsuarioDireccion
            direccion = direcciones['direccion']
            latitud = direcciones['latitud']
            longitud = direcciones['longitud']

            print('entrando al try')
            try:
                CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
                print(CrearDireccion)
                db.session.add(CrearDireccion)
                db.session.commit()
                print('Direcciones agregadas correctamente')
            except:
                print('Error al agregar direccion')

        return ('Usuario editado correctamente')

class loginUsuario(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        try:
            task = db.session.query(Usuarios).filter_by(email=email).first()
            repuesta = '0'
            if task.password == password:
                repuesta = 'ok'
                idusuario = task.idUsuario
                idRol = task.idRol
            else:
                repuesta = 'nok'
                idusuario = 'Usuario no encontrado'
            return {"respuesta": repuesta, "idUsuario": idusuario, "idRol": idRol}
        except:
            return {"respuesta": "Correo no encontrado"}
