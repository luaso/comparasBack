from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import or_
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    fechaCreacion = db.Column(db.Date)
    sub_categorias = db.relationship('Sub_Categorias', backref='Categorias', lazy=True)

    @classmethod
    def get(self):
        filtro = db.session.query(Categorias)
        return filtro


class Sub_Categorias(db.Model, BaseModelMixin):
    __tablename__= "SUB_CATEGORIAS"
    idSubCategorias = db.Column(db.Integer, primary_key=True)
    nombreSubCategoria = db.Column(db.String)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)
    categoria = db.relationship('Tipos_Productos', backref='Sub_Categorias', lazy=True)

    @classmethod
    def get_all(self):
        filtro = db.session.query(Sub_Categorias)
        return filtro

    @classmethod
    def get(self, idSubCategorias):
       filtro =  db.session.query(Sub_Categorias).filter(Sub_Categorias.idSubCategorias == idSubCategorias)
       return filtro

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_sub_cat(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_query(self, idSubCategorias):
        filtro = Sub_Categorias.query.get(idSubCategorias)
        return filtro

    def __init__(self, nombreSubCategoria,idCategoria):

        self.nombreSubCategoria = nombreSubCategoria
        self.idCategoria = idCategoria


class Tipos_Productos(db.Model, BaseModelMixin):
    __tablename__= "TIPOS_PRODUCTOS"
    idTipoProducto = db.Column(db.Integer, primary_key=True)
    nombreProducto = db.Column(db.String)
    idSubCategorias = db.Column(db.Integer, db.ForeignKey(Sub_Categorias.idSubCategorias), nullable=False)