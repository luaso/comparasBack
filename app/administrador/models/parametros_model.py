from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
db = SQLAlchemy()


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
    def get_all(self):
        filtro = db.session.query(Parametros)
        return filtro

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_sub_cat(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_query(self, idParametros):
        filtro = Parametros.query.get(idParametros)
        return filtro

    @classmethod
    def get(cls, idParametros):
        filtro = db.session.query(Parametros).filter(Parametros.idParametros == idParametros).all()
        return filtro

    def delete_parametro(self):
        db.session.delete(self)
        db.session.commit()

    def __init__(self, Descripcion, Estado,FecCrea,FecModifica,UsuCrea,UsuModifica,Valor):
        # self.idProducto = idProducto
        self.Descripcion = Descripcion
        self.Estado = Estado
        self.FecCrea = FecCrea
        self.FecModifica = FecModifica
        self.UsuCrea = UsuCrea
        self.UsuModifica = UsuModifica
        self.Valor = Valor
