from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date

db = SQLAlchemy()

class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.DateTime)


    def __init__(self, nombreCategoria, fechaCreacion):
        self.nombreCategoria = nombreCategoria
        self.fechaCreacion = fechaCreacion

    def __repr__(self):
        return f'Categoria({self.nombreCategoria})'

    def __str__(self):
        return f'{self.nombreCategoria}'

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(nombreCategoria=name).first()

    @classmethod
    def find_by_id(cls, id):
        print("entro a find_by_id")
        return cls.query.get(id)