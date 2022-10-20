from enum import unique
from Config.Bd import db, ma

class Servicios(db.Model):
    __tablename__ = 'Servicios'
    id_servicios = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(70))

    def __init__(self, Nombre):
        self.Nombre = Nombre

db.create_all()

class ServiciosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombre')
