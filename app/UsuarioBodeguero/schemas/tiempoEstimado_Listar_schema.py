from marshmallow import fields
from app.ext import ma




class TiempoEstimadoSchema(ma.Schema):
    class Meta:
        fields = ('idTipoTiempo','Descripcion','Estado')

