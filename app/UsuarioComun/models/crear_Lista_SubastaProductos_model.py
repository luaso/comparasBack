
from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()
ma = Marshmallow()
class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)

class Sub_Categorias(db.Model, BaseModelMixin):
    __tablename__= "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategoria = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)

class Tipos_Productos(db.Model, BaseModelMixin):
    __tablename__= "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)
    productos = db.relationship('Productos', backref='Tipos_Productos', lazy=True)


class Productos(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS"
    idProducto = db.Column(db.Integer, primary_key=True)
    idTipoProducto = db.Column(db.Integer, db.ForeignKey(Tipos_Productos.idTipoProducto), nullable=False)
    nombreProducto = db.Column(db.String)
    contenidoProducto = db.Column(db.String)
    Imagen = db.Column(db.String)
    codProducto = db.Column(db.String)
    marca = db.Column(db.String)
    presentacion = db.Column(db.String)
    unidadMedida = db.Column(db.String)
    cantidadPaquete = db.Column(db.Integer)
    subastas_productos = db.relationship('Subastas_Productos', backref='Productos', lazy=True)
    productos = db.relationship('Productos_Supermercados', backref='Productos', lazy=True)

class Estado(db.Model, BaseModelMixin):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)


class Rol(db.Model, BaseModelMixin):
    __tablename__ = "ROL"
    idRol = db.Column(db.Integer, primary_key=True)
    nombreRol = db.Column(db.String)
    usuarios = db.relationship('Usuarios', backref='Rol', lazy=True)

class Usuarios(db.Model, BaseModelMixin):
    __tablename__ = "USUARIOS"
    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String)
    idRol = db.Column(db.Integer,db.ForeignKey(Rol.idRol), nullable=False)
    Ruc = db.Column(db.String)
    razonSocial = db.Column(db.String)
    nombreComercial = db.Column(db.String)
    codigoPostalPais = db.Column(db.String)
    telefono = db.Column(db.String)
    celular = db.Column(db.String)
    direccion = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Usuarios', lazy=True)

class Subastas(db.Model, BaseModelMixin):
    __tablename__= "SUBASTAS"
    idSubasta = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey(Usuarios.idUsuario), nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey(Estado.idEstado), nullable=False)
    tiempoInicial = db.Column(db.Date)
    nombreSubasta = db.Column(db.String)
    precioIdeal = db.Column(db.Float)
    idDireccion = db.Column(db.Integer)
    fechaSubasta = db.Column(db.Date)
    subastas_productos = db.relationship('Subastas_Productos', backref='Subastas', lazy=True)

    def __init__(self, idUsuario, idEstado, tiempoInicial, nombreSubasta, precioIdeal, idDireccion, fechaSubasta):
        self.idUsuario = idUsuario
        self.idEstado = idEstado
        self.tiempoInicial = tiempoInicial
        self.nombreSubasta = nombreSubasta
        self.precioIdeal = precioIdeal
        self.idDireccion = idDireccion
        self.fechaSubasta = fechaSubasta

class Subastas_Productos(db.Model, BaseModelMixin):
    __tablename__= "SUBASTAS_PRODUCTOS"
    idSubastasProductos = db.Column(db.Integer, primary_key=True)
    idSubasta = db.Column(db.Integer,db.ForeignKey(Subastas.idSubasta), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    Cantidad = db.Column(db.Float)

    @classmethod
    def get_joins_filter(self, idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos). \
            outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            filter(Subastas_Productos.idSubasta == idSubasta).all()
        return filtro

    @classmethod
    def get_joins_filter_supermercados(self, idSubasta):
        filtro = db.session.query(Subastas_Productos, Productos_Supermercados, Productos, Supermercados). \
            outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto). \
            outerjoin(Productos_Supermercados, Productos.idProducto == Productos_Supermercados.idProducto). \
            outerjoin(Supermercados, Productos_Supermercados.idSupermercado == Supermercados.idSupermercado). \
            filter(Subastas_Productos.idSubasta == idSubasta).all()
        return filtro


    def __init__(self,idSubasta, idProducto, Cantidad):

        self.idSubasta = idSubasta
        self.idProducto = idProducto
        self.Cantidad = Cantidad

class Supermercados(db.Model, BaseModelMixin):
    __tablename__ = "SUPERMERCADOS"
    idSupermercado = db.Column(db.Integer, primary_key=True)
    nombreSupermercado = db.Column(db.String)
    imagenSupermercado = db.Column(db.String)
    urlSupermercado = db.Column(db.String)
    productos_supermercados = db.relationship('Productos_Supermercados', backref='Supermercados', lazy=True)

class Productos_Supermercados(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS_SUPERMERCADOS"
    idProductoSupermercado = db.Column(db.Integer, primary_key=True)
    idSupermercado = db.Column(db.Integer, db.ForeignKey(Supermercados.idSupermercado), nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey(Productos.idProducto), nullable=False)
    fechaProducto = db.Column(db.Date)
    precioRegular = db.Column(db.Float)
    precioOnline = db.Column(db.Float)
    precioTarjeta = db.Column(db.Float)
    nombreTarjeta = db.Column(db.String)










#@app.route('/api/SubastaProductos', methods=['POST'])
#def post_Subasta_Productos():
#    idSubasta = request.json['idSubasta']
#    idProducto = request.json['idProducto']
#    Cantidad = request.json['Cantidad']
#    new_task = Subastas_Productos(idSubasta, idProducto,Cantidad)
#    db.session.add(new_task)
#    db.session.commit()
#    return task_schema.jsonify(new_task)


#@app.route('/api/SubastaProductos', methods=['GET'])
#def get_Subasta_Productos():
#   task =  Subastas_Productos.query.all()
#   result = tasks_schema.dump(task)
#   return jsonify(result)


# FILTRAR LISTA DE PRODUCTOS DE SUBASTA_PRODUCTOS MEDIANTE LA ID DE SUBASTA
#@app.route('/api/SubastaProductos1/<idSubasta>', methods=['GET'])
#def get_Subasta_Productos_idSubasta(idSubasta):
#
#    filtro = db.session.query(Subastas_Productos, Productos).outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto).filter(Subastas_Productos.idSubasta==idSubasta).all()
#    for subastas_Productos, productos in filtro:
#        print(productos.idProducto, productos.nombreProducto)
#
#
#    resultado = task_schema.dump(filtro, many=True)
#    print(resultado)
#    return {"productos": resultado}, 200

# MOSTRAR DATOS DE COMPARACIÓN ENTRE LOS SUPERMERCADOS Y LOS PRODUCTOS QUE CONTIENEN
#@app.route('/api/ComparacionSupermercados/<idSubasta>', methods=['GET'])
#def get_Comparacion_Supermercados_Productos(idSubasta):
#    filtro = db.session.query(Subastas_Productos, Productos_Supermercados, Productos, Supermercados, Productos_Supermercados.idSupermercado * Productos_Supermercados.precio).\
#            outerjoin(Productos, Subastas_Productos.idProducto == Productos.idProducto).\
#            outerjoin(Productos_Supermercados, Productos.idProducto == Productos_Supermercados.idProducto). \
#            outerjoin(Supermercados, Productos_Supermercados.idSupermercado == Supermercados.idSupermercado). \
#            filter(Subastas_Productos.idSubasta==idSubasta).all()
#    print(filtro)
#
#    resultado = task_schema.dump(filtro, many=True)
#    #print(resultado)
#    return {"productos": resultado}, 200
#
#if __name__ =="__main__":
#    app.run(debug=True)
