from enum import unique
from Config.Bd import db, ma

class Habitacion(db.Model):
    __tablename__ = 'Habitacion'
    id_habitacion = db.Column(db.Integer, primary_key=True)
    Numero = db.Column(db.String(70), unique = True)
    Estado = db.Column(db.Integer(), db.ForeignKey('Estado_habitacion.id_estado_habitacion'))
    Tipo = db.Column(db.Integer(), db.ForeignKey('Tipo_habitacion.id_tipo'))

    def __init__(self, Numero, Estado, Tipo):
        self.Numero = Numero
        self.Estado = Estado
        self.Tipo = Tipo

db.create_all()

class HabitacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Numero', 'Estado','Tipo')
