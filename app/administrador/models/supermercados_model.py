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