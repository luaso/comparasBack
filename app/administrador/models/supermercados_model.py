from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Supermercados(db.Model, BaseModelMixin):
    __tablename__= "SUPERMERCADOS"
    idSupermercado = db.Column(db.Integer, primary_key=True)
    nombreSupermercado = db.Column(db.String)
    imagenSupermercado = db.Column(db.String)
    urlSupermercado = db.Column(db.String)


    def __init__(self, nombreSupermercado, imagenSupermercado, urlSupermercado):
        self.nombreSupermercado = nombreSupermercado
        self.imagenSupermercado = imagenSupermercado
        self.urlSupermercado = urlSupermercado

    def __repr__(self):
        return f'Categoria({self.nombreSupermercado}, {self.imagenSupermercado}, {self.urlSupermercado})'

    def __str__(self):
        return f'{self.nombreSupermercado}'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(nombreSupermercado=name).first()

    @classmethod
    def find_by_id(cls, id):
        print("entro a find_by_id")
        return cls.query.get(id)

    @classmethod
    def get_filter(self, nombreSupermercado):
        filtro = Supermercados.query.filter(Supermercados.nombreSupermercado.ilike('%' + nombreSupermercado + '%'))
        return filtro

class Parametros(db.Model, BaseModelMixin):
    __tablename__="PARAMETROS"
    idParametros = db.Column(db.Integer, primary_key=True)
    Descripcion = db.Column(db.String)
    Estado = db.Column(db.Integer)
    FecCrea = db.Column(db.Date)
    FecModifica = db.Column(db.Date)
    UsuCrea = db.Column(db.Integer)
    UsuModifica = db.Column(db.Integer)
    Valor = db.Column(db.String)

    @classmethod
    def get(self, idParametros):

       filtro =  db.session.query(Parametros).filter(Parametros.idParametros == idParametros)

       return filtro