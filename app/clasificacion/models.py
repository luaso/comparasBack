from app.db import db, BaseModelMixin

class Clasificacion(db.Model, BaseModelMixin):
    idClasificacion = db.Column(db.Integer, primary_key=True)
    nombreClasificacion = db.Column(db.String)


    def __init__(self, nombreClasificacion):
        self.nombreClasificacion = nombreClasificacion

    def __repr__(self):
        return f'Clasificacion({self.nombreClasificacion})'

    def __str__(self):
        return f'{self.nombreClasificacion}'