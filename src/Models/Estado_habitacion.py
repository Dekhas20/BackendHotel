from enum import unique
from Config.Bd import db, ma

class Estado_habitacion(db.Model):
    __tablename__ = 'Estado_habitacion'
    id_estado_habitacion = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(70))

    def __init__(self, Nombre):
        self.Nombre = Nombre

db.create_all()

class Estado_habitacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombre')
