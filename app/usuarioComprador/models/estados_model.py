from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Estado(db.Model):
    __tablename__ = "ESTADO"
    idEstado = db.Column(db.Integer, primary_key=True)
    nombreEstado = db.Column(db.String)
    subastas = db.relationship('Subastas', backref='Estado', lazy=True)

    def __init__(self, idEstado, nombreEstado, subastas):
        self.idEstado = idEstado
        self.nombreEstado = nombreEstado
        self.subastas = subastas

    def __repr__(self):
        return f'Estado({self.idEstado}, {self.nombreEstado}, {self.subastas})'

    def __str__(self):
        return f'{self.nombreEstado}'

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