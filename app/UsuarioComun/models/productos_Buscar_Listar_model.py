from app.db import db, BaseModelMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String


db = SQLAlchemy()

class Categorias(db.Model, BaseModelMixin):
    __tablename__= "CATEGORIAS"
    idCategoria = db.Column(db.Integer, primary_key=True)
    nombreCategoria = db.Column(db.String)
    productos = db.relationship('Productos', backref='Categorias', lazy=True)


class Productos(db.Model, BaseModelMixin):
    __tablename__ = "PRODUCTOS"
    idProducto = db.Column(db.Integer, primary_key=True)
    idCategoria = db.Column(db.Integer, db.ForeignKey(Categorias.idCategoria), nullable=False)

    nombreProducto = db.Column(db.String)
    contenidoProducto = db.Column(db.String)
    Imagen = db.Column(db.String)





