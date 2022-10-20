from Config.Bd import db, ma

class Rol(db.Model):
    __tablename__ = 'Rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(70))

    def __init__(self, Nombre):
        self.Nombre = Nombre

db.create_all()

class RolSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombre')
