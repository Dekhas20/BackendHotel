from enum import unique
from Config.Bd import db, ma

class Tipo_habitacion(db.Model):
    __tablename__ = 'Tipo_habitacion'
    id_tipo = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(70))
    Precio = db.Column(db.Float())
    Camas = db.Column(db.Integer())
    Descripcion = db.Column(db.Text())

    def __init__(self, Nombre, Precio, Camas, Descripcion):
        self.Nombre = Nombre
        self.Precio = Precio
        self.Camas = Camas
        self.Descripcion = Descripcion

db.create_all()

class Tipo_habitacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombre', 'Precio','Camas', 'Descripcion')
