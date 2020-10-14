
from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()
ma = Marshmallow()
class Rol(db.Model):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

    def __init__(self, idRol, nombreRol):
        self.idRol = idRol
        self.nombreRol = nombreRol



class Usuarios(db.Model):
    __tablename__ = "USUARIOS"
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String)
    apellidoPatUsuario = db.Column(db.String)
    apellidoMatUsuario = db.Column(db.String)
    idRol = db.Column(db.Integer,db.ForeignKey(Rol.idRol), nullable=False)
    Ruc = db.Column(db.String)
    razonSocial = db.Column(db.String)
    nombreComercial = db.Column(db.String)
    codigoPostalPais = db.Column(db.String)
    telefono = db.Column(db.String)
    celular = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    imagen = db.Column(db.String)
    direcciones = db.relationship('Direcciones', backref='Usuarios', lazy=True)

    def __init__(self, nombreUsuario,apellidoPatUsuario,apellidoMatUsuario,idRol,Ruc,razonSocial,nombreComercial,codigoPostalPais,telefono,celular,email,password,imagen):
        self.nombreUsuario = nombreUsuario
        self.apellidoPatUsuario = apellidoPatUsuario
        self.apellidoMatUsuario = apellidoMatUsuario
        self.idRol = idRol
        self.Ruc = Ruc
        self.razonSocial = razonSocial
        self.nombreComercial = nombreComercial
        self.codigoPostalPais = codigoPostalPais
        self.telefono = telefono
        self.celular = celular
        self.email = email
        self.password = password
        self.imagen = imagen

class Direcciones(db.Model):
    __tablename__="DIRECCIONES"
    idDireccion = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    direccion = db.Column(db.String)
    latitud = db.Column(db.String)
    longitud = db.Column(db.String)
    def __init__(self, idUsuario,direccion,latitud,longitud):
        #self.idDireccion=idDireccion
        self.idUsuario =idUsuario
        self.direccion= direccion
        self.latitud = latitud
        self.longitud = longitud


class RolSchema(ma.Schema):
    class Meta:
        fields = ('idRol', 'nombreRol','Usuarios.nombreUsuario','Usuarios.apellidoPatUsuario','Usuarios.apellidoMatUsuario','Usuarios.Ruc','Usuarios.razonSocial','Usuarios.nombreComercial','Usuarios.codigoPostalPais','Usuarios.telefono','Usuarios.celular','Usuarios.email','Usuarios.imagen','Usuarios.idUsuario','Direcciones.idDireccion','Direcciones.latitud','Direcciones.longitud', 'Direcciones.direccion')

rolSchema = RolSchema()


#db.create_all()
#rolsSchema = rolSchema(many=True)


"""@app.route('/api/ObtenerRol/', methods=['GET'])
def get1():
    print('22222')
    filtro=Rol.query.filter(Rol.idRol.in_((3,4)))


    print(filtro)

    resultado = rolSchema.dump(filtro, many=True)
    print(resultado)
    return {"rol": resultado}, 200

@app.route('/api/direcciones/', methods=['GET'])
def get():
    print('Estoy aqui')
    producto = Direcciones.query.filter(Direcciones.direccion.ilike('%1%'))
    print('Error al jalar')

    print(producto)
    result = rolSchema.dump(producto, many=True)
    return {"productos": result}, 200

@app.route('/api/agregarDireccion/', methods=['POST'])
def get2():
    #idDireccion=4
    idUsuario = 35
    direccion = '123123'
    latitud = '1231231232'
    longitud = '123123213'
    CrearDireccion = Direcciones(idUsuario, direccion, latitud, longitud)
    print(CrearDireccion)
    db.session.add(CrearDireccion)
    db.session.commit()
    return ('POR FIN UN RESULTADO BUENO CON ESA TABLA DE MIERDA')

@app.route('/api/GuardarUsuario/', methods=['POST'])
def post():
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
                                nombreComercial, codigoPostalPais, telefono, celular, email, password,imagen)
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

@app.route('/api/BuscarUsuario/<idUsuario>', methods=['GET'])
def get_usuario(idUsuario):
  task = Usuarios.query.get(idUsuario)
  return rolSchema.jsonify(task)

@app.route('/api/EditarUsuarioComprador/', methods=['PUT'])
def put_Comprador():
    data = request.get_json()
    for usuario in data['Datos']:

        idUsuario = usuario['idUsuario']
        nombreUsuario = usuario['nombreUsuario']
        apellidoPatUsuario = usuario['apellidoPatUsuario']
        apellidoMatUsuario = usuario['apellidoMatUsuario']
        idRol = 4
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

@app.route('/EliminarDireccion/<idDireccion>', methods=['DELETE'])
def delete_task(idDireccion):
  direcciones = Direcciones.query.get(idDireccion)
  db.session.delete(direcciones)
  db.session.commit()
  return ('Registro eliminado')


@app.route('/api/EditarUsuarioBodeguero/', methods=['PUT'])
def put_Bodeguero():
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


#LOGIN

@app.route('/api/LoginUsuario/', methods=['GET'])
def get_email():
    print('prueba entrada get')
    email = request.json['email']
    password = request.json['password']
    try:

        task = db.session.query(Usuarios).filter_by(email=email).first()
        print(task.idUsuario)
        print(task.password)
        repuesta = '0'

        if task.password == password:
           print('Correcto')
           repuesta = 'ok'
           print(task.idUsuario)
           idusuario = task.idUsuario
        else:
            print('incorrecto')
            repuesta = 'nok'
            idusuario = 'Usuario no encontrado'

        return {"respuesta": repuesta, "idUsuario": idusuario}
    except:
        return {"respuesta": "Correo no encontrado"}


if __name__ =="__main__":
   app.run(debug=True)"""

