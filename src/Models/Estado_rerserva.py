from Config.Bd import db, ma

class Estado_reserva(db.Model):
    __tablename__ = 'Estado_reserva'
    id_estado = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(70)
    )
    
    def __init__(self, Nombre):
        self.Nombre = Nombre

db.create_all()

class Estado_reservaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'Nombre')
