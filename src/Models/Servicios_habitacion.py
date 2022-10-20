from enum import unique
from Config.Bd import db, ma

class Servicios_habitacion(db.Model):
    __tablename__ = 'Servicios_habitacion'
    id_servicio_habitacion = db.Column(db.Integer, primary_key=True)
    id_servicios = db.Column(db.Integer(), db.ForeignKey('Servicios.id_servicios'))
    id_habitacion = db.Column(db.Integer(), db.ForeignKey('Habitacion.id_habitacion'))

    def __init__(self, id_servicios, id_habitacion):
        self.id_servicios = id_servicios
        self.id_habitacion = id_habitacion

db.create_all()

class Servicios_habitacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'id_tipo', 'id_servicios')
