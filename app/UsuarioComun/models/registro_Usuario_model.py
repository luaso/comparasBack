from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://desarrollador3:VzXY#FP$AqNI@64.227.98.56:5432/comparas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

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




class RolSchema(ma.Schema):
    class Meta:
        fields = ('idRol', 'nombreRol')

rolSchema = RolSchema()


#@app.route('/api/ObtenerRol/', methods=['GET'])
#def get():
    #print('22222')
    #filtro = db.session.query(Rol.nombreRol).all()
    #filtro = Rol.query.filter_by(idRol=1).first()

    #print(filtro)

    #resultado = rolSchema.dump(filtro, many=True)
    #print(resultado)
    #return {"productos": filtro}, 200



#if __name__ =="__main__":
   #app.run(debug=True)
