from app.db import db, BaseModelMixin
from sqlalchemy import Column, Integer, String


class Clasificacion(db.Model, BaseModelMixin):
    __tablename__= "clasificacion"
    idclasificacion = db.Column(db.Integer, primary_key=True)
    nombreclasificacion = db.Column(db.String)


    def __init__(self, nombreclasificacion):
        self.nombreclasificacion = nombreclasificacion

    def __repr__(self):
        return f'Clasificacion({self.nombreclasificacion})'

    def __str__(self):
        return f'{self.nombreclasificacion}'